import pytest
from src.clients.payroll_client import SalaryUploadClient
import os

@pytest.mark.smoke
@pytest.mark.role("hr")
def test_salary_upload(ctx):

    #    print("SUPERADMIN_USER:", os.getenv("SUPERADMIN_USER"))
    #    print("BASEURL:", os.getenv("BASE_URL"))
    #    print("API_PREFIX:", os.getenv("API_PREFIX"))
    #    print("CTX TYPE:", type(ctx))
       file_path = "C:/Users/Caelius Consulting/Downloads/demo_salary_sheet.xlsx"
    #    print("Uploading file:", file_path)

       client = SalaryUploadClient(ctx)
       response = client.upload_salary(employee_type='CONTRACT', month='may', excelFile=(file_path))
       assert response.ok, response.text()

      

   