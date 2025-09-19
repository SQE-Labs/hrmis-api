# src/clients/documents_client.py
"""Client for Documents endpoints; groups list/upload helpers."""

import os
from typing import Any, Dict
from playwright.sync_api import APIRequestContext

def _p(path: str) -> str:
    """Prefix path with API_PREFIX application base."""
    prefix = os.getenv("API_PREFIX", "HRMBackendTest").strip("/")
    return f"/{prefix}/{path.lstrip('/')}"

class DocumentsClient:
    """Thin wrapper over APIRequestContext for Documents module."""

    def __init__(self, ctx: APIRequestContext):
        """Store the authenticated request context."""
        self.ctx = ctx

    def list_status(self):
        """Return documents status list envelope: {'data': [...], 'message': ...}."""
        return self.ctx.get(_p("document/v1/list/status"))

    def upload_v2(self, file_tuple, employee_id: str, doc_type: str):
        """Upload a document using multipart form fields: file, employeeId, docType."""
        return self.ctx.post(
            _p("document/v2/upload"),
            multipart={
                "docFile": file_tuple,
                "employeeId": employee_id,
                "docType": doc_type,
            },
        )
