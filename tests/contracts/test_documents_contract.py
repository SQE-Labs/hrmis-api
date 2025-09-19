# tests/contracts/test_documents_contract.py
import json, os, pytest, jsonschema
from src.clients.documents_client import DocumentsClient

@pytest.mark.contract
@pytest.mark.regression
@pytest.mark.module_documents
def test_documents_status_list_contract(ctx):
    schema_path = os.path.join("src", "schemas", "documents", "status_list.schema.json")
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    client = DocumentsClient(ctx)
    r = client.list_status()
    assert r.ok, r.text()
    body = r.json()
    jsonschema.validate(instance=body, schema=schema)
