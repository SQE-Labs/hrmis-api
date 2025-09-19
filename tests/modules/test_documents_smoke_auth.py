# tests/modules/test_documents_smoke_auth.py
import os
import pytest

@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.module_documents
def test_document_status_list(ctx):
    prefix = os.getenv("API_PREFIX", "HRMBackendTest").strip("/")
    r = ctx.get(f"/{prefix}/document/v1/list/status")
    assert r.ok, r.text()
    assert isinstance(r.json(), (list, dict))
