# src/clients/base_client.py
"""Thin HTTP wrapper around Playwright's APIRequestContext with
consistent status checks and explicit payload encoding methods.
"""

from typing import Dict, Any, Iterable
from playwright.sync_api import APIRequestContext, APIResponse


class BaseClient:
    """Base client that centralizes request calls and status assertions."""

    def __init__(self, ctx: APIRequestContext, base: str = ""):
        """Store shared request context and optional static base prefix."""
        self.ctx = ctx
        self.base = base.rstrip("/")

    def _assert_status(self, r: APIResponse, expected: Iterable[int] | None = None) -> APIResponse:
        """Assert response status is in expected codes (defaults to 2xx) and return response."""
        if expected is None:
            expected = range(200, 300)
        assert r.status in expected, f"Assertion Failed: Expected status in {list(expected)}, but got {r.status}. Response: {r.text()}"
        return r

    # --- Generic Methods ---
    
    def get(self, path: str, expected: Iterable[int] | None = None, **kwargs: Any) -> APIResponse:
        """GET base+path with passthrough kwargs; assert expected status."""
        r = self.ctx.get(self.base + path, **kwargs)
        return self._assert_status(r, expected)

    def post(self, path: str, expected: Iterable[int] | None = (200, 201), **kwargs: Any) -> APIResponse:
        """POST base+path with passthrough kwargs; default expected to 200/201."""
        r = self.ctx.post(self.base + path, **kwargs)
        return self._assert_status(r, expected)

    def put(self, path: str, expected: Iterable[int] | None = None, **kwargs: Any) -> APIResponse:
        """PUT base+path with passthrough kwargs; assert expected status."""
        r = self.ctx.put(self.base + path, **kwargs)
        return self._assert_status(r, expected)

    def delete(self, path: str, expected: Iterable[int] | None = None, **kwargs: Any) -> APIResponse:
        """DELETE base+path with passthrough kwargs; assert expected status."""
        r = self.ctx.delete(self.base + path, **kwargs)
        return self._assert_status(r, expected)

    # --- Specific Payload Helpers ---

    def post_form(self, path: str, data: Dict[str, Any], expected: Iterable[int] | None = (200, 201)) -> APIResponse:
        """POST with application/x-www-form-urlencoded data."""
        return self.post(path, expected=expected, form=data)

    def post_json(self, path: str, data: Dict[str, Any], expected: Iterable[int] | None = (200, 201)) -> APIResponse:
        """POST with application/json data."""
        return self.post(path, expected=expected, data=data)

    def put_form(self, path: str, data: Dict[str, Any], expected: Iterable[int] | None = None) -> APIResponse:
        """PUT with application/x-www-form-urlencoded data."""
        return self.put(path, expected=expected, form=data)

    def put_multipart(self, path: str, data: Dict[str, Any], expected: Iterable[int] | None = None) -> APIResponse:
        """PUT with multipart/form-data."""
        return self.put(path, expected=expected, multipart=data)
