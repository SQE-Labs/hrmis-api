import pytest
from src.clients.login_client import LoginClient
from src.endpoints.login import LOGIN
from utils.logger import get_logger  # assuming you have this utility

logger = get_logger(__name__)
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.module_login
@pytest.mark.role("employee")
def test_login(ctx):
    client = LoginClient(ctx)
    email = "vishal.thakur1@caeliusconsulting.com"
    password = "Test@1234"
    
    logger.info("Starting login test for user: %s", email)
    r = client.login(email, password)

    # Log request & response for traceability
    logger.debug("Request Endpoint: %s", LOGIN)
    logger.debug("Response Status Code: %s", r.status_code)
    logger.debug("Response Body: %s", r.text)

    assert r.ok, f"Login API failed: {r.text}"
    assert isinstance(r.json(), (list, dict)), "Response is not valid JSON"

    logger.info("✅ Login test passed successfully for %s", email)
