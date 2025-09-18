import pytest, os

@pytest.mark.smoke
@pytest.mark.module("assets")
@pytest.mark.role_l1
def test_asset_request_list_as_l1(api_l1):
    prefix = os.getenv("API_PREFIX", "HRMBackendTest").strip("/")
    r = api_l1.get(f"/{prefix}/assest/assestRequestList?pageSize=10&page=1")
    assert r.ok, r.text()
    assert isinstance(r.json(), (list, dict))
