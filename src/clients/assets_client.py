# src/clients/assets_client.py
"""Client for Assets endpoints; centralizes common paths and options."""

import os
from playwright.sync_api import APIRequestContext

def _p(path: str) -> str:
    """Prefix path with API_PREFIX application base."""
    prefix = os.getenv("API_PREFIX", "HRMBackendTest").strip("/")
    return f"/{prefix}/{path.lstrip('/')}"

class AssetsClient:
    """Thin wrapper over APIRequestContext for Assets module."""

    def __init__(self, ctx: APIRequestContext):
        """Store the authenticated request context."""
        self.ctx = ctx

    def list_types(self):
        """Return list of asset types (shape may be array or object wrapper)."""
        return self.ctx.get(_p("assest/list"))

    def list_requests(self, page_size: int = 10, page: int = 1):
        """Return paginated asset requests visible to the caller."""
        return self.ctx.get(_p(f"assest/assestRequestList?pageSize={page_size}&page={page}"))
