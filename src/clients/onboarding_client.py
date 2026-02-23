"""Client for Employee Onboarding endpoints; groups list and action helpers."""

import os
from typing import Any, Dict, Tuple, Optional
from playwright.sync_api import APIRequestContext, APIResponse
from .base_client import BaseClient
from src.endpoints.onboarding import (
    ONBOARDING_INVITE,
    ONBOARDING_USERS,
    ONBOARDING_DEPARTMENTS,
    ONBOARDING_INVITATIONS,
    ONBOARDING_PAGED,
    ONBOARDING_UPDATE_EMAIL,
    ONBOARDING_HR_APPROVE,
)

def _p(path: str) -> str:
    """Prefix path with API_PREFIX application base."""
    prefix = os.getenv("API_PREFIX", "HRMBackendTest").strip("/")
    return f"/{prefix}/{path.lstrip('/')}"

class OnboardingClient(BaseClient):
    """Thin wrapper over APIRequestContext for Employee Onboarding."""

    def __init__(self, ctx: APIRequestContext):
        """Store the authenticated request context."""
        super().__init__(ctx)

    # -------- Helpers --------

    def _items_and_meta(self, body: Any) -> Tuple[Any, Optional[Dict[str, Any]]]:
        """
        Normalize list responses across shapes:
        - list
        - {"data": [...]}
        - {"data": {"data": [...], "totalPages": n, "totalElements": m}}
        Returns (items, meta) where meta is the dict that may contain pagination keys.
        """
        if isinstance(body, dict) and "data" in body:
            inner = body["data"]
            if isinstance(inner, dict) and "data" in inner:
                return inner.get("data"), inner
            return inner, body
        return body, None

    # -------- Lists --------

    def users(self) -> APIResponse:
        """Get all users (directory/IT approval)."""
        return self.get(_p(ONBOARDING_USERS))

    def departments(self) -> APIResponse:
        """Get all departments used during onboarding."""
        return self.get(_p(ONBOARDING_DEPARTMENTS))

    def invitations(self, status: str = "pending", page_size: int = 10, page: int = 1) -> APIResponse:
        """Get invitation list filtered by status (pending by default)."""
        return self.get(_p(f"{ONBOARDING_INVITATIONS}?status={status}&pageSize={page_size}&page={page}"))

    def paged(self, status: str = "PENDING", page_size: int = 10, page: int = 1) -> APIResponse:
        """Get paged onboarding requests for a given status."""
        return self.get(_p(f"{ONBOARDING_PAGED}?status={status}&pageSize={page_size}&page={page}"))

    # -------- Actions (asserting) --------

    def invite_employee(self, email_id: str, employee_name: str, file_tuple) -> APIResponse:
        """
        Invite an employee via multipart form data; guarded test usage recommended.
        file_tuple is (filename, filebytes/fileobj, mime).
        """
        return self.post(
            _p(ONBOARDING_INVITE),
            multipart={"emailId": email_id, "employeeName": employee_name, "offerLetter": file_tuple},
            expected=(200, 201, 204),
        )

    def update_email(self, employee_id: int, email: str) -> APIResponse:
        """Approve/set a Caelius email for a given employee."""
        return self.put(_p(f"{ONBOARDING_UPDATE_EMAIL}?email={email}&employeeId={employee_id}"))

    def hr_approve(
        self,
        employee_id: int,
        employee_type: str,
        manager_id: int,
        designation_id: int,
        leave_manager_id: int,
        employee_subtype: str,
    ) -> APIResponse:
        """HR approval step for onboarding with required assignment metadata."""
        qs = (
            f"employeeType={employee_type}"
            f"&managerId={manager_id}"
            f"&designationId={designation_id}"
            f"&leaveManagerId={leave_manager_id}"
            f"&employeeSubType={employee_subtype}"
        )
        return self.put(_p(f"{ONBOARDING_HR_APPROVE(employee_id)}?{qs}"))

    # -------- Actions (raw, non-asserting) --------

    def hr_approve_raw(
        self,
        employee_id: int,
        employee_type: str,
        manager_id: int,
        designation_id: int,
        leave_manager_id: int,
        employee_subtype: str,
    ) -> APIResponse:
        """
        Same as hr_approve but returns the raw APIResponse without asserting status,
        allowing tests to inspect non-2xx payloads and xfail on known validation errors.
        """
        qs = (
            f"employeeType={employee_type}"
            f"&managerId={manager_id}"
            f"&designationId={designation_id}"
            f"&leaveManagerId={leave_manager_id}"
            f"&employeeSubType={employee_subtype}"
        )
        # Use the underlying context to bypass BaseClient status assertion
        return self.ctx.put(_p(f"{ONBOARDING_HR_APPROVE(employee_id)}?{qs}"))
    
    def it_approve(self, employee_id: int) -> APIResponse:
        """
        IT approval step for onboarding.
        Uses the onboarding/v2 approve endpoint under the hood.
        """
        # Confirmed endpoint path for IT approval
        return self.put(
            _p(f"onboarding/v2/{employee_id}/approve"),
            expected=(200, 204),
        )
    
    def paged_approval_pending(self, page_size: int = 20, page: int = 1) -> APIResponse:
        """
        Get paged onboarding requests with status 'APPROVAL_PENDING'.
        """
        return self.get(_p(f"{ONBOARDING_PAGED}?status=APPROVAL_PENDING&pageSize={page_size}&page={page}"))

