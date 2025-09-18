# conftest.py
import os
import pytest
from collections.abc import Generator
from playwright.sync_api import Playwright, APIRequestContext, sync_playwright

# If pytest-playwright plugin is not installed, provide a playwright fixture
@pytest.fixture(scope="session")
def playwright() -> Generator[Playwright, None, None]:
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("BASE_URL", "https://topuptalent.com")

@pytest.fixture(scope="session")
def api_prefix() -> str:
    # Path segment for this backend
    return os.getenv("API_PREFIX", "HRMBackendTest").strip("/")

def _join(api_prefix: str, path: str) -> str:
    # Always build prefix + relative path without leading slash
    return f"/{api_prefix}/{path.lstrip('/')}"

@pytest.fixture(scope="session")
def unauth_ctx(playwright: Playwright, base_url: str) -> Generator[APIRequestContext, None, None]:
    ctx = playwright.request.new_context(base_url=base_url)
    yield ctx
    ctx.dispose()

def _signin(ctx: APIRequestContext, login_path: str, email: str | None, password: str | None) -> str:
    assert email and password, "Environment variables for user and password are not set"
    resp = ctx.post(login_path, data={"email": email, "password": password})
    assert resp.ok, f"Auth failed for {email}: {resp.status} :: {resp.text()}"
    body = resp.json()
    token = body.get("accessToken") or body.get("token") or body.get("access_token")
    assert token, f"No token in response: {body}"
    return token

def _auth_ctx(playwright: Playwright, base_url: str, api_prefix: str, email_env: str, pass_env: str) -> APIRequestContext:
    bootstrap = playwright.request.new_context(base_url=base_url)
    login_path = _join(api_prefix, "api/auth/signin")
    token = _signin(bootstrap, login_path, os.getenv(email_env), os.getenv(pass_env))
    bootstrap.dispose()
    return playwright.request.new_context(
        base_url=base_url,
        extra_http_headers={"Authorization": f"Bearer {token}"}
    )

# Role-scoped contexts
@pytest.fixture(scope="session")
def api_hr(playwright: Playwright, base_url: str, api_prefix: str) -> Generator[APIRequestContext, None, None]:
    ctx = _auth_ctx(playwright, base_url, api_prefix, "HR_USER", "HR_PASS")
    yield ctx
    ctx.dispose()

@pytest.fixture(scope="session")
def api_employee(playwright: Playwright, base_url: str, api_prefix: str) -> Generator[APIRequestContext, None, None]:
    ctx = _auth_ctx(playwright, base_url, api_prefix, "EMPLOYEE_USER", "EMPLOYEE_PASS")
    yield ctx
    ctx.dispose()

@pytest.fixture(scope="session")
def api_superadmin(playwright: Playwright, base_url: str, api_prefix: str) -> Generator[APIRequestContext, None, None]:
    ctx = _auth_ctx(playwright, base_url, api_prefix, "SUPERADMIN_USER", "SUPERADMIN_PASS")
    yield ctx
    ctx.dispose()

@pytest.fixture(scope="session")
def api_l1(playwright: Playwright, base_url: str, api_prefix: str) -> Generator[APIRequestContext, None, None]:
    ctx = _auth_ctx(playwright, base_url, api_prefix, "ASSET_L1_USER", "ASSET_L1_PASS")
    yield ctx
    ctx.dispose()

@pytest.fixture(scope="session")
def api_l2(playwright: Playwright, base_url: str, api_prefix: str) -> Generator[APIRequestContext, None, None]:
    ctx = _auth_ctx(playwright, base_url, api_prefix, "ASSET_L2_USER", "ASSET_L2_PASS")
    yield ctx
    ctx.dispose()

@pytest.fixture(scope="session")
def api_store(playwright: Playwright, base_url: str, api_prefix: str) -> Generator[APIRequestContext, None, None]:
    ctx = _auth_ctx(playwright, base_url, api_prefix, "ASSET_STORE_USER", "ASSET_STORE_PASS")
    yield ctx
    ctx.dispose()

@pytest.fixture(scope="session")
def request_ctx(unauth_ctx: APIRequestContext) -> APIRequestContext:
    return unauth_ctx
