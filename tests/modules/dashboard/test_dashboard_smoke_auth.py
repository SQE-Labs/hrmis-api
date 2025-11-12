# tests/modules/test_assets_l1_smoke_auth.py
import pytest
from src.clients.dashboard_client import DashboardClient

@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.module_dashboard
def test_dashboard(ctx):
    client = DashboardClient(ctx)
    r = client.get_users_menu()
    assert r.ok, r.text()
    assert isinstance(r.json(), (list, dict))


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.module_login
@pytest.mark.role("employee")
def test_dashboard_punch_data(ctx):
    client = DashboardClient(ctx)
    r = client.get_punch_data_menu()
    assert r.ok, r.text()
    assert isinstance(r.json(), (list, dict))



    

    
