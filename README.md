# Automated Data Quality & Testing Framework for Fund Valuation Pipelines

## 1. Overview
Production-grade testing framework designed to validate fund valuation data pipelines for Deutsche Bank. It covers calculation accuracy, layer-to-layer record completeness, deduplication, and ID transformation rules.

## 2. Framework Architecture
- `src/data_generator.py`: Generates mock batch data with edge cases (zero division, missing records, duplicates).
- `src/validator.py`: Reconciliation and data quality assertion functions.
- `tests/`: Modular Pytest suite covering calculations, completeness, and DQ rules.
- `.github/workflows/`: Automated CI/CD pipeline using GitHub Actions.

## 3. How to Run & Validate
1. Install dependencies:
   ```bash
   pip install -r requirements.txt