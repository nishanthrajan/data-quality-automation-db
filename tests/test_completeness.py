import pytest
from src.data_generator import generate_mock_datasets
from src.validator import DataValidator

def test_record_completeness():
    src, mart = generate_mock_datasets()
    validator = DataValidator(src, mart)
    missing = validator.check_completeness()
    assert "FUND_D" in missing, "Completeness engine failed to identify missing fund"