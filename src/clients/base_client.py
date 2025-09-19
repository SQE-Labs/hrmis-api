# src/clients/base_client.py
"""Thin HTTP wrapper around Playwright's APIRequestContext with
consistent status checks and API_PREFIX path joining handled by callers.
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
        assert r.status in expected, f"{r.status} :: {r.text()}"
        return r

    def get(self, path: str, expected: Iterable[int] | None = None, **kwargs: Dict[str, Any]) -> APIResponse:
        """GET base+path with passthrough kwargs; assert expected status."""
        r = self.ctx.get(self.base + path, **kwargs)
        return self._assert_status(r, expected)

    def post(self, path: str, expected: Iterable[int] | None = (200, 201), **kwargs: Dict[str, Any]) -> APIResponse:
        """POST base+path with passthrough kwargs; default expected to 200/201."""
        r = self.ctx.post(self.base + path, **kwargs)
        return self._assert_status(r, expected)

    def put(self, path: str, expected: Iterable[int] | None = None, **kwargs: Dict[str, Any]) -> APIResponse:
        """PUT base+path with passthrough kwargs; assert expected status."""
        r = self.ctx.put(self.base + path, **kwargs)
        return self._assert_status(r, expected)

    def delete(self, path: str, expected: Iterable[int] | None = None, **kwargs: Dict[str, Any]) -> APIResponse:
        """DELETE base+path with passthrough kwargs; assert expected status."""
        r = self.ctx.delete(self.base + path, **kwargs)
        return self._assert_status(r, expected)
