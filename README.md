# HRMIS API Tests

Playwright + Pytest setup for API testing with smoke and role-based auth.

## Setup
python -m venv .venv && .venv\Scripts\activate   # or source .venv/bin/activate
pip install -r requirements.txt

## Run
# Unauth smoke (reachability)
pytest -m smoke --html=report.html --self-contained-html

# HR-auth smoke
pytest -m "role_hr and smoke" --html=report_hr.html --self-contained-html

# L1-auth smoke
pytest -m "role_l1 and smoke" --html=report_l1.html --self-contained-html

## Notes
- BASE_URL is host; API_PREFIX is the app path. All requests use "/{API_PREFIX}/...".
- If signin rejects JSON, switch login payload between data= and form= in conftest.py.
