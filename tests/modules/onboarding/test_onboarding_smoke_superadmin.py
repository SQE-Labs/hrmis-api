# tests/modules/onboarding/test_onboarding_smoke_superadmin.py
import json
import pytest
from src.clients.onboarding_client import OnboardingClient

def _extract_items_and_meta(body):
    """
    Normalize shapes:
    - list
    - {"data":[...]}
    - {"data":{"data":[...], ...}}
    Return (items, meta_dict_or_None).
    """
    if isinstance(body, list):
        return body, None
    if isinstance(body, dict) and "data" in body:
        inner = body["data"]
        if isinstance(inner, dict) and "data" in inner:
            return inner["data"], inner
        return inner, body
    return body, None

def _debug_dump(label, body):
    try:
        print(f"[SMOKE:{label}]", json.dumps(body, indent=2, ensure_ascii=False)[:4000])
    except Exception:
        print(f"[SMOKE:{label}] <non-serializable>")

@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.module_onboarding
def test_onboarding_users_list(ctx):
    c = OnboardingClient(ctx)
    r = c.users()
    assert r.ok, r.text()
    body = r.json()
    _debug_dump("USERS", body)
    assert isinstance(body, (list, dict)), f"Unexpected payload type: {type(body)}"

@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.module_onboarding
def test_onboarding_departments_list(ctx):
    c = OnboardingClient(ctx)
    r = c.departments()
    assert r.ok, r.text()
    body = r.json()
    _debug_dump("DEPARTMENTS", body)
    assert isinstance(body, (list, dict)), f"Unexpected payload type: {type(body)}"

@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.module_onboarding
def test_onboarding_invitations_pending(ctx):
    c = OnboardingClient(ctx)
    r = c.invitations(status="pending", page_size=10, page=1)
    assert r.ok, r.text()
    body = r.json()
    items, meta = _extract_items_and_meta(body)
    _debug_dump("INVITATIONS_PENDING", body)
    assert isinstance(items, list), f"Unexpected payload: {type(body)}"
    if isinstance(meta, dict):
        assert "totalPages" in meta and "totalElements" in meta, f"No pagination metadata keys in: {list(meta.keys())}"

@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.module_onboarding
def test_onboarding_paged_pending(ctx):
    c = OnboardingClient(ctx)
    r = c.paged(status="PENDING", page_size=10, page=1)
    assert r.ok, r.text()
    body = r.json()
    items, meta = _extract_items_and_meta(body)
    _debug_dump("PAGED_PENDING", body)
    assert isinstance(items, list), f"Unexpected payload: {type(body)}"
    if isinstance(meta, dict):
        assert "totalPages" in meta and "totalElements" in meta, f"No pagination metadata keys in: {list(meta.keys())}"
