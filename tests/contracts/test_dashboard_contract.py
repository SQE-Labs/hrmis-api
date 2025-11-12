import os, json, pytest, jsonschema
from src.endpoints.dashboard import USERS_MENU, PUNCH_MENU

def _load_schema(rel_path: str):
    with open(rel_path, "r", encoding="utf-8") as f:
        return json.load(f)

def _p(path: str) -> str:
    prefix = os.getenv("API_PREFIX", "HRMBackendTest").strip("/")
    return f"/{prefix}/{path.lstrip('/')}"

@pytest.mark.contract
@pytest.mark.regression
@pytest.mark.module_dashboard
def test_users_menu_contract(ctx):
    schema = _load_schema(os.path.join("src", "schemas", "dashboard", "users_list.schema.json"))
    r = ctx.get(_p(USERS_MENU))
    assert r.ok, r.text()
    jsonschema.validate(instance=r.json(), schema=schema)


@pytest.mark.contract
@pytest.mark.regression
@pytest.mark.module_dashboard
def test_users_menu_contract(ctx):
    schema = _load_schema(os.path.join("src", "schemas", "dashboard", "punchin_details.schema.json"))
    r = ctx.get(_p(PUNCH_MENU))
    assert r.ok, r.text()
    jsonschema.validate(instance=r.json(), schema=schema)