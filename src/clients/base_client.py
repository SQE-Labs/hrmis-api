# src/clients/base_client.py
from typing import Optional, Dict, Any
from playwright.sync_api import APIRequestContext, APIResponse

class BaseClient:
    def __init__(self, ctx: APIRequestContext, base: str = ""):
        self.ctx = ctx
        self.base = base.rstrip("/")

    def get(self, path: str, **kwargs: Dict[str, Any]) -> APIResponse:
        r = self.ctx.get(self.base + path, **kwargs)
        assert r.ok, f"{r.status} :: {r.text()}"
        return r

    def post(self, path: str, **kwargs: Dict[str, Any]) -> APIResponse:
        r = self.ctx.post(self.base + path, **kwargs)
        assert r.status in (200, 201), f"{r.status} :: {r.text()}"
        return r

    def put(self, path: str, **kwargs: Dict[str, Any]) -> APIResponse:
        r = self.ctx.put(self.base + path, **kwargs)
        assert r.ok, f"{r.status} :: {r.text()}"
        return r

    def delete(self, path: str, **kwargs: Dict[str, Any]) -> APIResponse:
        r = self.ctx.delete(self.base + path, **kwargs)
        assert r.ok, f"{r.status} :: {r.text()}"
        return r
