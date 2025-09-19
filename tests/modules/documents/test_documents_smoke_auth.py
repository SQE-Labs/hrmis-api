# tests/modules/test_documents_smoke_auth.py
import os
import pytest
from src.endpoints.documents import DOC_STATUS_LIST

@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.module_documents
def test_document_status_list(ctx):
    prefix = os.getenv("API_PREFIX", "HRMBackendTest").strip("/")
    r = ctx.get(f"/{prefix}/{DOC_STATUS_LIST}")
    assert r.ok, r.text()
    assert isinstance(r.json(), (list, dict))
