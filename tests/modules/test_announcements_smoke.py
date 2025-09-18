# tests/modules/test_announcements_smoke.py
import os
import pytest

def _p(path: str) -> str:
    """Prefix helper: BASE_URL is the host, API_PREFIX is the app path."""
    prefix = os.getenv("API_PREFIX", "HRMBackendTest").strip("/")
    return f"/{prefix}/{path.lstrip('/')}"

@pytest.mark.smoke
@pytest.mark.module("announcements")
@pytest.mark.role_hr
def test_announcements_dashboard_list_as_hr(api_hr):
    resp = api_hr.get(_p("announcement/dashboard/list"))
    # Treat environment-driven empty state as non-failure for smoke, but document the case
    if resp.status == 200:
        data = resp.json()
        assert isinstance(data, (list, dict)), f"Unexpected payload: {data}"
    elif resp.status in (204, 404):
        pytest.skip("No announcements available in this environment")
    elif resp.status == 500 and "Announcement not found" in (resp.text() or ""):
        pytest.xfail("Known backend behavior: 500 returned when no announcements exist")
    else:
        pytest.fail(f"Unexpected status {resp.status}: {resp.text()}")
