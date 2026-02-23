# src/clients/assets_client.py
"""Client for Assets endpoints; centralizes common paths and options."""

import os
from playwright.sync_api import APIRequestContext
from .base_client import BaseClient
from src.endpoints.assets import ASSET_LIST_TYPES, ASSET_REQUESTS

def _p(path: str) -> str:
    """Prefix path with API_PREFIX application base."""
    prefix = os.getenv("API_PREFIX", "HRMBackendTest").strip("/")
    return f"/{prefix}/{path.lstrip('/')}"

class AssetsClient(BaseClient):
    """Thin wrapper over APIRequestContext for Assets module."""

    def __init__(self, ctx: APIRequestContext):
        """Store the authenticated request context."""
        super().__init__(ctx)

    def list_types(self):
        """Return list of asset types (shape may be array or object wrapper)."""
        return self.get(_p(ASSET_LIST_TYPES))

    def list_requests(self, page_size: int = 10, page: int = 1):
        """Return paginated asset requests visible to the caller."""
        return self.get(_p(f"{ASSET_REQUESTS}?pageSize={page_size}&page={page}"))
