import pytest
from src.data_generator import generate_mock_datasets
from src.validator import DataValidator

def test_deduplication_detection():
    src, mart = generate_mock_datasets()
    validator = DataValidator(src, mart)
    assert validator.validate_deduplication() > 0, "No duplicate records detected"

def test_id_transformation():
    src, _ = generate_mock_datasets()
    transformed = src["fund_id_raw"].str.replace("EXT_", "", regex=False)
    assert not transformed.str.startswith("EXT_").any(), "ID transformation failed"