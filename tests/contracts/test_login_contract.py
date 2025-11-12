import json
import os
import pytest
import jsonschema
from src.clients.login_client import LoginClient
from utils.logger import logger, log_request, log_response  


@pytest.mark.contract
@pytest.mark.regression
@pytest.mark.module_login
@pytest.mark.role("superadmin")
def test_login_contract(ctx):
    logger.info("=== 🧩 Starting Login Contract Test ===")

    # Load JSON schema
    schema_path = os.path.join("src", "schemas", "login", "login.schema.json")
    logger.info(f"Loading login schema from: {schema_path}")

    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
        logger.debug(f"Schema Loaded Successfully: {schema}")
    except Exception as e:
        logger.exception(f"❌ Failed to load schema: {e}")
        pytest.fail(f"Schema file loading failed: {e}")

    # Initialize client
    logger.info("Initializing LoginClient...")
    client = LoginClient(ctx)

    # Log request details before sending
    logger.info("Sending login request...")
    try:
        log_request("POST", client.url, headers=client.headers, body=client.payload)
    except AttributeError:
        logger.warning("⚠️ LoginClient does not expose url/headers/payload attributes — skipping request log.")

    # Send request
    r = client.login(email="vishal.thakur1@caeliusconsulting.com", password="Test@1234")

    # Log response details
    log_response(r)

    # Validate response status
    logger.info("Validating response status...")
    assert r.ok, f"❌ Login API failed with status {r.status_code} and body: {r.text}"

    # Validate schema
    logger.info("Validating response schema...")
    body = r.json()

    try:
        jsonschema.validate(instance=body, schema=schema)
        logger.info("✅ Response schema validation successful.")
    except jsonschema.exceptions.ValidationError as e:
        logger.error(f"❌ Schema validation failed: {e.message}")
        pytest.fail(f"Schema validation error: {e.message}")

    logger.info("=== ✅ Login Contract Test Completed Successfully ===\n")
