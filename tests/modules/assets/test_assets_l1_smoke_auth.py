# tests/modules/test_assets_l1_smoke_auth.py
import pytest
from src.clients.assets_client import AssetsClient

@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.module_assets
def test_asset_request_list(ctx):
    client = AssetsClient(ctx)
    r = client.list_requests(page_size=10, page=1)
    assert r.ok, r.text()
    assert isinstance(r.json(), (list, dict))
