import os
from playwright.sync_api import APIRequestContext, APIResponse
from .base_client import BaseClient
from src.endpoints.dashboard import USERS_MENU,PUNCH_MENU
from utils.logger import log_request, log_response , logger


def _p(path: str) -> str:
    """Prefix path with API_PREFIX application base."""
    prefix = os.getenv("API_PREFIX", "HRMBackendTest").strip("/")
    return f"/{prefix}/{path.lstrip('/')}"


class DashboardClient(BaseClient):
    """Thin wrapper over APIRequestContext for Dashboard module."""

    def __init__(self, ctx: APIRequestContext):
        """Store the authenticated request context."""
        if ctx is None:
            logger.error("❌ APIRequestContext is None — DashboardClient cannot initialize.")
            raise ValueError("APIRequestContext cannot be None.")
        super().__init__(ctx)
        self.ctx = ctx
        logger.info("✅ DashboardClient initialized successfully.")

    def get_users_menu(self) -> APIResponse:
        """Return users menu data."""
        endpoint = _p(USERS_MENU)
        log_request("GET", endpoint)
        response = self.get(endpoint)
        if response is None:
            logger.error(f"No response returned from GET {endpoint}")
        else:
            log_response(response)
        return response

    def get_punch_data_menu(self) -> APIResponse:
        """Return punch data menu."""
        endpoint = _p(PUNCH_MENU)
        log_request("GET", endpoint)
        response = self.get(endpoint)
        if response is None:
            logger.error(f" No response returned from GET {endpoint}")
        else:
            log_response(response)
        return response
