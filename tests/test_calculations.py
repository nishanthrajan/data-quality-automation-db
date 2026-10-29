import pytest
from src.data_generator import generate_mock_datasets
from src.validator import DataValidator

def setup_module():
    global validator
    src, mart = generate_mock_datasets()
    validator = DataValidator(src, mart)

def test_aum_calculation_accuracy():
    is_valid, discrepancies = validator.validate_aum_calculations()
    assert is_valid, f"AUM calculation mismatch in {len(discrepancies)} records"

def test_zero_handling_edge_case():
    _, mart = generate_mock_datasets()
    assert mart["calculated_aum"].notnull().all(), "AUM contains nulls from computation error"