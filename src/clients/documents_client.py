# src/clients/documents_client.py
"""Client for Documents endpoints; groups list/upload helpers."""

import os
from playwright.sync_api import APIRequestContext
from .base_client import BaseClient
from src.endpoints.documents import DOC_STATUS_LIST, DOC_UPLOAD_V2

def _p(path: str) -> str:
    """Prefix path with API_PREFIX application base."""
    prefix = os.getenv("API_PREFIX", "HRMBackendTest").strip("/")
    return f"/{prefix}/{path.lstrip('/')}"

class DocumentsClient(BaseClient):
    """Thin wrapper over APIRequestContext for Documents module."""

    def __init__(self, ctx: APIRequestContext):
        """Store the authenticated request context."""
        super().__init__(ctx)

    def list_status(self):
        """Return documents status list envelope: {'data': [...], 'message': ...}."""
        return self.get(_p(DOC_STATUS_LIST))

    def upload_v2(self, file_tuple, employee_id: str, doc_type: str):
        """Upload a document using multipart form fields: file, employeeId, docType."""
        return self.post(
            _p(DOC_UPLOAD_V2),
            multipart={
                "docFile": file_tuple,
                "employeeId": employee_id,
                "docType": doc_type,
            },
        )
