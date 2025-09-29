# HRMIS API Tests

Playwright + Pytest setup for fast, structured API testing with superadmin-first coverage, module-based selection, contracts, smokes, and targeted negatives.

---

## Table of Contents

- [Overview](#overview)
- [Project Layout](#project-layout)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Environment Configuration](#environment-configuration)
- [Markers and Selection](#markers-and-selection)
- [Core Commands](#core-commands)
  - [Quick Starts](#quick-starts)
  - [Module Runs](#module-runs)
  - [Positive vs Negative vs Contracts](#positive-vs-negative-vs-contracts)
  - [Role Overrides](#role-overrides)
  - [Reports and Logging](#reports-and-logging)
  - [Speed and Failure Control](#speed-and-failure-control)
  - [Targeted Runs](#targeted-runs)
- [Superadmin-First Workflow](#superadminfirst-workflow)
- [Clients and Schemas](#clients-and-schemas)
- [Troubleshooting](#troubleshooting)
- [Conventions](#conventions)

---

## Overview

This repository uses **Playwright's APIRequestContext** with **Pytest fixtures** to run fast, browserless API tests.  
Tests are organized by business modules, with separate suites for smokes, contracts, and negatives to keep feedback **quick and focused**.

---

## Project Layout

```
tests/
  modules/       # Positive and smoke tests per module
  contracts/     # JSON Schema contract checks
  negative/      # RBAC and invalid-input checks

src/
  clients/       # Thin wrappers for module endpoints
  schemas/       # JSON Schemas for contract tests

Config
  pytest.ini     # Markers and defaults
  conftest.py    # Role fixtures, generic ctx, URL helper
```

---

## Prerequisites

- Python **3.10+** and a virtual environment
- Playwright Python and test dependencies installed from `requirements.txt`

---

## Setup

```bash
# Create and activate virtual environment

# Windows
python -m venv .venv && .venv\Scripts\activate

# macOS/Linux
python -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file in the repo root.

### **Required:**
- `BASE_URL=https://topuptalent.com`
- `API_PREFIX=HRMBackendTest`

### **Role Credentials:**
- `SUPERADMIN_USER`, `SUPERADMIN_PASS`
- `HR_USER`, `HR_PASS`
- `EMPLOYEE_USER`, `EMPLOYEE_PASS`
- `ASSET_L1_USER`, `ASSET_L1_PASS`
- `ASSET_L2_USER`, `ASSET_L2_PASS`
- `ASSET_STORE_USER`, `ASSET_STORE_PASS`

### **Optional:**
- `DEFAULT_ROLE=superadmin`

### **Notes:**
- `BASE_URL` is the host and `API_PREFIX` is the application path.  
  All API calls use `/{API_PREFIX}/...`.
- If signin rejects JSON, toggle the login payload between `data=` and `form=` in the auth helper inside `conftest.py`.

---

## Markers and Selection

### **Module Markers:**
- `module_documents`
- `module_assets`
- `module_announcements`
- `module_dashboard`

### **Scenarios:**
- `smoke`
- `contract`
- `negative`

### **Role Override:**
- `role(name)` → Switch role per test while keeping a global default role for the run.

> **Tip:**  
> Static module markers enable clean `-m` selection across folders so negatives and contracts still run with their module.

---

## Core Commands

### Quick Starts
```bash
# Full suite (default role: superadmin)
pytest

# Fast CI gate (smokes + contracts)
pytest -m "smoke or contract" -q
```

---

### Module Runs
```bash
# Documents
pytest -m module_documents

# Assets
pytest -m module_assets

# Announcements
pytest -m module_announcements

# Dashboard
pytest -m module_dashboard
```

---

### Positive vs Negative vs Contracts
```bash
# Documents positives only
pytest -m "module_documents and not negative and not contract"

# Documents contracts only
pytest -m "module_documents and contract"

# Documents smoke only
pytest -m "module_documents and smoke"

# Assets negatives only
pytest -m "module_assets and negative"

# Only negatives folder
pytest tests/negative -q
```

---

### Role Overrides
```bash
# Global role switch to HR
pytest --role hr -m module_documents

# Assets smoke as L1
pytest --role l1 -m "module_assets and smoke"

# Entire run as EMPLOYEE
pytest --role employee

# CI default role via env
DEFAULT_ROLE=hr pytest -m module_documents
```

**Per-test override:**  
Add `@pytest.mark.role("employee")` on the test to override the global role for that one test.

---

### Reports and Logging
```bash
# HTML report (contracts)
pytest -m contract --html=report_contract.html --self-contained-html

# JUnit XML for CI
pytest -m "smoke or contract" --junitxml=reports/junit.xml

# Verbose output
pytest -vv

# Show slow tests
pytest --durations=10 --durations-min=1.0
```

---

### Speed and Failure Control
```bash
# Parallel (requires pytest-xdist)
pytest -m module_documents -n auto

# Stop on first failure
pytest -m module_documents -x

# Failures first on re-run
pytest --ff

# Only last failed
pytest --last-failed
```

---

### Targeted Runs
```bash
# Single file
pytest tests/contracts/test_documents_contract.py

# Single test
pytest tests/contracts/test_documents_contract.py::test_documents_status_list_contract -q

# Keyword filter
pytest -m module_documents -k "status_list"

# Collect only (no execution)
pytest -m module_assets --collect-only

# List available markers
pytest --markers
```

---

## Superadmin-First Workflow

- **Phase 1:**  
  Complete smoke, positives, and contracts per module under superadmin using the `ctx` fixture as the default context for broad coverage.

- **Phase 2:**  
  Add `role(name)` markers and use global `--role` runs to validate HR, Employee, L1/L2, and Store access with the same tests.

---

## Clients and Schemas

**Clients:**
- Thin wrappers around Playwright's APIRequestContext centralize paths and success code checks so tests focus on assertions.
- Examples:
  - `AssetsClient.list_requests`
  - `DocumentsClient.list_status`
  - `DocumentsClient.upload_v2`

**Schemas:**
- Contract tests validate response envelopes and stable fields to catch breaking changes early.


---

## Troubleshooting

- **Auth failures:**  
  Verify credentials in `.env` and that signin uses `data=` or `form=` as required by the backend.

- **HTML report missing:**  
  Ensure `pytest-html` is installed and include both `--html` and `--self-contained-html` flags.

- **JSON Schema warnings in editor:**  
  The editor may not fully support 2020-12; use `draft-07` in `$schema` if you prefer a clean editor experience.

- **Mixed envelopes (array vs object):**  
  Keep permissive schemas early and tighten once endpoints stabilize to reduce false failures.

---

## Conventions

- Keep **positives** in `tests/modules`, **negatives** in `tests/negative`, **contracts** in `tests/contracts`.
- Always **tag tests with the correct module marker** so a single `-m module_<name>` collects from all folders.
- Prefer the `ctx` fixture in tests; use per-test `role(name)` only for explicit RBAC verification.
