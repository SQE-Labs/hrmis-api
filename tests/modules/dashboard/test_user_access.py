import os
import pytest
from src.clients.dashboard_client import DashboardClient
from utils.logger import logger  # ✅ your custom logger instance


@pytest.mark.module_dashboard
@pytest.mark.regression
@pytest.mark.smoke
@pytest.mark.role("hr")
@pytest.mark.role("superadmin")
def test_dashboard(ctx):
    """Verify Dashboard API's Users Menu with detailed logging."""
    logger.info("🚀 Starting test: Dashboard → Users Menu API")

    # Initialize client
    
    logger.info("🧩 Initializing DashboardClient...")
    client = DashboardClient(ctx)

    # Send request
    logger.info("📤 Sending GET request to Users Menu endpoint...")
    response = client.get_users_menu()

    # Validate HTTP response
    logger.info(f"📥 Received response | Status: {response.status}")
    logger.debug(f"Response body:\n{response.text()}")

    assert response.ok, f"❌ Request failed | Status: {response.status} | Body: {response.text()}"
    logger.info("✅ Request successful — Status OK")

    # Validate response format
    json_body = response.json()
    logger.info(f"🧾 Response JSON type: {type(json_body).__name__}")
    assert isinstance(json_body, (list, dict)), f"Unexpected JSON type: {type(json_body)}"

    logger.info("🎯 Test completed successfully for Dashboard Users Menu ✅")
