# conftest.py
import os
import re
import pytest
from collections.abc import Generator
from typing import Dict, Optional, Union
from _pytest.fixtures import FixtureLookupError
from playwright.sync_api import Playwright, APIRequestContext, sync_playwright

# ---------- CLI and role selection ----------

def pytest_addoption(parser):
    parser.addoption(
        "--role",
        action="store",
        default=os.getenv("DEFAULT_ROLE", "superadmin"),
        help="Default role to run tests under (superadmin, hr, employee, l1, l2, l3, store)",
    )

@pytest.fixture(scope="session")
def default_role(request) -> str:
    return request.config.getoption("--role")

@pytest.fixture
def ctx(request, default_role):
    """
    Generic request context:
    - Uses @pytest.mark.role("<name>") on the test if present.
    - Else uses --role or DEFAULT_ROLE=superadmin.
    """
    role_marker = request.node.get_closest_marker("role")
    role = role_marker.args[0] if role_marker and role_marker.args else default_role
    fixture_name = f"api_{role}"
    try:
        return request.getfixturevalue(fixture_name)
    except FixtureLookupError:
        pytest.fail(f"Unknown role '{role}': missing fixture '{fixture_name}'")

# ---------- URL helper ----------

def _p(path: str) -> str:
    """Join API_PREFIX with a relative path."""
    prefix = os.getenv("API_PREFIX", "HRMBackendTest").strip("/")
    return f"/{prefix}/{path.lstrip('/')}"

# ---------- Playwright bootstrap (no plugin required) ----------

@pytest.fixture(scope="session")
def playwright() -> Generator[Playwright, None, None]:
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("BASE_URL", "https://topuptalent.com")

@pytest.fixture(scope="session")
def unauth_ctx(playwright: Playwright, base_url: str) -> Generator[APIRequestContext, None, None]:
    # Global default API timeout (ms)
    timeout_ms = int(os.getenv("API_TIMEOUT_MS", "30000"))
    ctx = playwright.request.new_context(base_url=base_url, timeout=timeout_ms)
    yield ctx
    ctx.dispose()

# ---------- Auth helpers (JSON by default + configurable) ----------

def _signin(ctx: APIRequestContext, login_path: str, email: Optional[str], password: Optional[str]) -> str:
    """
    Sign in and return bearer token.

    SIGNIN_MODE:
      - 'data' (default): JSON body via data={} (Content-Type: application/json)
      - 'form'          : application/x-www-form-urlencoded via form={}
    Timeouts:
      - SIGNIN_TIMEOUT_MS (overrides API_TIMEOUT_MS for signin only)
    """
    assert email and password, "Environment variables for user and password are not set"
    mode = os.getenv("SIGNIN_MODE", "data").lower()
    timeout_ms = int(os.getenv("SIGNIN_TIMEOUT_MS", os.getenv("API_TIMEOUT_MS", "30000")))

    if mode == "form":
        resp = ctx.post(login_path, form={"email": email, "password": password}, timeout=timeout_ms)
    else:
        # Default to JSON body to match collections
        resp = ctx.post(
            login_path,
            data={"email": email, "password": password},
            timeout=timeout_ms,
        )

    assert resp.ok, f"Auth failed for {email}: {resp.status} :: {resp.text()}"
    body = resp.json()
    token = body.get("accessToken") or body.get("token") or body.get("access_token")
    assert token, f"No token in response: {body}"
    return token

def _auth_ctx(playwright: Playwright, base_url: str, email_env: str, pass_env: str) -> APIRequestContext:
    timeout_ms = int(os.getenv("API_TIMEOUT_MS", "30000"))
    bootstrap = playwright.request.new_context(base_url=base_url, timeout=timeout_ms)
    login_path = _p("api/auth/signin")
    token = _signin(bootstrap, login_path, os.getenv(email_env), os.getenv(pass_env))
    bootstrap.dispose()
    return playwright.request.new_context(
        base_url=base_url,
        timeout=timeout_ms,
        extra_http_headers={"Authorization": f"Bearer {token}"}
    )

# ---------- Role-scoped APIRequestContext fixtures ----------

@pytest.fixture(scope="session")
def api_hr(playwright: Playwright, base_url: str) -> Generator[APIRequestContext, None, None]:
    ctx = _auth_ctx(playwright, base_url, "HR_USER", "HR_PASS")
    yield ctx
    ctx.dispose()

@pytest.fixture(scope="session")
def api_employee(playwright: Playwright, base_url: str) -> Generator[APIRequestContext, None, None]:
    ctx = _auth_ctx(playwright, base_url, "EMPLOYEE_USER", "EMPLOYEE_PASS")
    yield ctx
    ctx.dispose()

@pytest.fixture(scope="session")
def api_superadmin(playwright: Playwright, base_url: str) -> Generator[APIRequestContext, None, None]:
    ctx = _auth_ctx(playwright, base_url, "SUPERADMIN_USER", "SUPERADMIN_PASS")
    yield ctx
    ctx.dispose()

@pytest.fixture(scope="session")
def api_l1(playwright: Playwright, base_url: str) -> Generator[APIRequestContext, None, None]:
    ctx = _auth_ctx(playwright, base_url, "ASSET_L1_USER", "ASSET_L1_PASS")
    yield ctx
    ctx.dispose()

@pytest.fixture(scope="session")
def api_l2(playwright: Playwright, base_url: str) -> Generator[APIRequestContext, None, None]:
    ctx = _auth_ctx(playwright, base_url, "ASSET_L2_USER", "ASSET_L2_PASS")
    yield ctx
    ctx.dispose()

@pytest.fixture(scope="session")
def api_l3(playwright: Playwright, base_url: str) -> Generator[APIRequestContext, None, None]:
    ctx = _auth_ctx(playwright, base_url, "ASSET_L3_USER", "ASSET_L3_PASS")
    yield ctx
    ctx.dispose()

@pytest.fixture(scope="session")
def api_store(playwright: Playwright, base_url: str) -> Generator[APIRequestContext, None, None]:
    ctx = _auth_ctx(playwright, base_url, "ASSET_STORE_USER", "ASSET_STORE_PASS")
    yield ctx
    ctx.dispose()

@pytest.fixture(scope="session")
def request_ctx(unauth_ctx: APIRequestContext) -> APIRequestContext:
    return unauth_ctx

# ---------- Identity resolver for EMPLOYEE (optional) ----------

def _clean_code(val: Optional[str]) -> Optional[str]:
    """Treat empty or placeholder values like '<...>' as unset."""
    if not val:
        return None
    s = val.strip()
    if not s or re.match(r"^<.*>$", s):
        return None
    return s

def _clean_id(val: Optional[str]) -> Optional[int]:
    """Return int if numeric; otherwise unset."""
    if not val:
        return None
    s = val.strip()
    return int(s) if s.isdigit() else None

@pytest.fixture(scope="session")
def identity_employee(api_employee: APIRequestContext) -> Dict[str, Union[str, int, None]]:
    """
    Resolve logged-in employee identity:
    - Prefer EMPLOYEE_CODE / EMPLOYEE_ID if set to real values (not '<...>').
    - Else infer from the employee's own asset list (first page).
    """
    code = _clean_code(os.getenv("EMPLOYEE_CODE"))
    emp_id = _clean_id(os.getenv("EMPLOYEE_ID"))

    if code or emp_id is not None:
        return {"employeeCode": code, "employeeId": emp_id, "source": "env"}

    r = api_employee.get(_p("assest/assestRequestList?pageSize=5&page=1"))
    if r.ok:
        body = r.json()
        items = body["data"] if isinstance(body, dict) and "data" in body else (body if isinstance(body, list) else [])
        if items:
            first = items[0]
            emp_id = first.get("employeeId")
            name = first.get("employeeName")
            code = first.get("employeeCode") or first.get("empCode")
            return {"employeeCode": code, "employeeId": emp_id, "employeeName": name, "source": "inferred"}

    return {"employeeCode": None, "employeeId": None, "source": "unknown"}
