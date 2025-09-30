# tests/contracts/test_onboarding_contracts.py
import os, json, pytest, jsonschema
from src.clients.onboarding_client import OnboardingClient

def _load_schema(rel_path: str):
    with open(rel_path, "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.mark.contract
@pytest.mark.regression
@pytest.mark.module_onboarding
def test_users_list_contract(ctx):
    schema = _load_schema(os.path.join("src", "schemas", "onboarding", "users_list.schema.json"))
    c = OnboardingClient(ctx)
    r = c.users()
    assert r.ok, r.text()
    jsonschema.validate(instance=r.json(), schema=schema)

@pytest.mark.contract
@pytest.mark.regression
@pytest.mark.module_onboarding
def test_departments_list_contract(ctx):
    schema = _load_schema(os.path.join("src", "schemas", "onboarding", "departments_list.schema.json"))
    c = OnboardingClient(ctx)
    r = c.departments()
    assert r.ok, r.text()
    jsonschema.validate(instance=r.json(), schema=schema)

@pytest.mark.contract
@pytest.mark.regression
@pytest.mark.module_onboarding
def test_invitations_pending_contract(ctx):
    schema = _load_schema(os.path.join("src", "schemas", "onboarding", "invitations_list.schema.json"))
    c = OnboardingClient(ctx)
    r = c.invitations(status="pending", page_size=10, page=1)
    assert r.ok, r.text()
    jsonschema.validate(instance=r.json(), schema=schema)

@pytest.mark.contract
@pytest.mark.regression
@pytest.mark.module_onboarding
def test_paged_pending_contract(ctx):
    schema = _load_schema(os.path.join("src", "schemas", "onboarding", "paged_list.schema.json"))
    c = OnboardingClient(ctx)
    r = c.paged(status="PENDING", page_size=10, page=1)
    assert r.ok, r.text()
    jsonschema.validate(instance=r.json(), schema=schema)

