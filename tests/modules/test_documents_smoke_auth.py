import pytest
import os

@pytest.mark.smoke
@pytest.mark.module("documents")
@pytest.mark.role_hr
def test_document_status_list_as_hr(api_hr):
    prefix = os.getenv("API_PREFIX", "HRMBackendTest").strip("/")
    r = api_hr.get(f"/{prefix}/document/v1/list/status")
    assert r.ok, r.text()
    assert isinstance(r.json(), (list, dict))
