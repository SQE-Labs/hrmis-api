import os
from playwright.sync_api import APIRequestContext
from .base_client import BaseClient
from src.endpoints.login import LOGIN


def _p(path: str) -> str:
    """Prefix path with API_PREFIX (e.g., HRMBackendTest)."""
    prefix = os.getenv("API_PREFIX", "HRMBackendTest").strip("/")
    return f"/{prefix}/{path.lstrip('/')}"


class LoginClient(BaseClient):
    """Thin wrapper over APIRequestContext for Login module."""

    def __init__(self, ctx: APIRequestContext):
        """Initialize with Playwright API request context."""
        super().__init__(ctx)

    def login(self, email: str, password: str):
        """Perform login request and return response."""
        response = self.post(
            _p(LOGIN),
            data={  
                "username": email,  
                "password": password,
            },
            headers={"Accept": "application/json"},  
        )

      
        if not response.ok:
            raise AssertionError(f"Login failed: {response.status} - {response.text()}")

        return response
