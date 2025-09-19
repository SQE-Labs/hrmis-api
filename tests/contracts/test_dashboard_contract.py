# tests/contracts/test_dashboard_contract.py
import json, os, pytest, jsonschema

def _p(path: str) -> str:
    prefix = os.getenv("API_PREFIX", "HRMBackendTest").strip("/")
    return f"/{prefix}/{path.lstrip('/')}"

@pytest.mark.contract
@pytest.mark.regression
@pytest.mark.module_dashboard
def test_users_menu_contract(ctx):
    schema_path = os.path.join("src", "schemas", "dashboard", "users_list.schema.json")
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    r = ctx.get(_p("menu/v1/users"))
    assert r.ok, r.text()
    jsonschema.validate(instance=r.json(), schema=schema)
