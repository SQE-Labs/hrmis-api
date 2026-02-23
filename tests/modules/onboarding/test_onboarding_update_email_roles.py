# tests/modules/onboarding/test_onboarding_update_email_roles.py
import os
import time
import pytest
from conftest import _p
from src.endpoints.onboarding import ONBOARDING_UPDATE_EMAIL
from src.clients.onboarding_client import OnboardingClient

RUN_MUTATING = os.getenv("RUN_MUTATING_ONBOARDING", "false").lower() == "true"
ENV_NAME = os.getenv("ENV_NAME", "").lower()
ALLOW_MUTATE_ENVS = set(os.getenv("ALLOW_MUTATE_ENVS", "dev,qa,sit,staging,test").lower().split(","))

EMP_ID = int(os.getenv("TEST_ONBOARDING_EMP_ID", "117"))
DOMAIN = os.getenv("TEST_ONBOARDING_DOMAIN", "caeliusconsulting.com").strip() or "caeliusconsulting.com"

def _email(tag: str):
    return f"approved.{tag}@{DOMAIN}"

def _skip_if_env_blocked():
    if ENV_NAME and ENV_NAME not in ALLOW_MUTATE_ENVS:
        pytest.skip(f"Mutating blocked for ENV_NAME={ENV_NAME}")

@pytest.mark.module_onboarding
@pytest.mark.regression
@pytest.mark.role("superadmin")
@pytest.mark.skipif(not RUN_MUTATING, reason="Mutating onboarding disabled")
def test_update_email_superadmin(ctx):
    _skip_if_env_blocked()
    client = OnboardingClient(ctx)
    r = client.update_email(employee_id=EMP_ID, email=_email(str(int(time.time()))))
    assert r.ok, r.text()

@pytest.mark.module_onboarding
@pytest.mark.regression
@pytest.mark.role("l3")
@pytest.mark.skipif(not RUN_MUTATING, reason="Mutating onboarding disabled")
def test_update_email_l3(ctx):
    _skip_if_env_blocked()
    client = OnboardingClient(ctx)
    r = client.update_email(employee_id=EMP_ID, email=_email(f"l3.{int(time.time())}"))
    assert r.ok, r.text()

@pytest.mark.module_onboarding
@pytest.mark.negative
@pytest.mark.role("employee")
@pytest.mark.skipif(not RUN_MUTATING, reason="Mutating onboarding disabled")
def test_update_email_employee_forbidden(ctx):
    _skip_if_env_blocked()
    r = ctx.put(_p(f"{ONBOARDING_UPDATE_EMAIL}?employeeId={EMP_ID}&email={_email(f'emp.{int(time.time())}')}"))
    assert r.status == 403, f"Expected 403, got {r.status}: {r.text()}"
