# src/endpoints/onboarding.py
"""Centralized endpoints for the Employee Onboarding module."""

# Core
ONBOARDING_INVITE = "onboarding"  # POST multipart: emailId, employeeName, offerLetter (file)
ONBOARDING_USERS = "user"  # GET all users
ONBOARDING_DEPARTMENTS = "onboarding/departmentlist"  # GET all departments

# Views
ONBOARDING_INVITATIONS = "onboarding/invitations"  # + ?status=pending&pageSize=10&page=1
ONBOARDING_PAGED = "onboarding/paged"              # + ?status=PENDING&pageSize=10&page=1

# Actions
ONBOARDING_UPDATE_EMAIL = "onboarding/v2/updateEmail"  # PUT + ?email=...&employeeId=...
def ONBOARDING_HR_APPROVE(employee_id: int) -> str:
    return f"onboarding/v2/{employee_id}/approve"  # PUT + HR query params
