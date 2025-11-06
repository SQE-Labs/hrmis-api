import os
from playwright.sync_api import APIRequestContext, APIResponse
from .base_client import BaseClient
from src.endpoints.payroll import SALARY_UPLOAD

def _p(path: str) -> str:
    prefix = os.getenv("API_PREFIX", "HRMBackendTest").strip("/")
    return f"/{prefix}/{path.lstrip('/')}"

class SalaryUploadClient(BaseClient):
    def __init__(self, ctx: APIRequestContext):
        super().__init__(ctx)

    def upload_salary(self, employee_type: str, month: str, excelFile):
        return self.post(_p (f"{SALARY_UPLOAD}?employeeType={employee_type}&month={month}"))