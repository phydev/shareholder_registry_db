import pytest
from src.shareholder_registry.ingestion.parsers import parse_address


def test_parse_address_standard_norwegian():
    # Arrange
    address = "0484 OSLO"
    expected_dict = {"postal_code": "0484", "location": "OSLO"}

    # Evaluate
    result, needs_review = parse_address(address)

    # Assert
    assert result == expected_dict
    assert needs_review is False


def test_parse_address_international_with_comma():
    # Arrange
    address = "THANI 84290, THAILAND"
    expected_dict = {"postal_code": "84290", "location": "THANI, THAILAND"}

    # Evaluate
    result, needs_review = parse_address(address)

    # Assert
    assert result == expected_dict
    assert needs_review is False


def test_parse_address_country_only_no_digits():
    # Arrange
    address = "SWEDEN"
    expected_dict = {"postal_code": None, "location": "SWEDEN"}

    # Evaluate
    result, needs_review = parse_address(address)

    # Assert
    assert result == expected_dict
    assert needs_review is False


def test_parse_address_chaotic_duplicated_user_input():
    # Arrange
    address = (
        "1925 BLAKER 1925 BLAKER 1925 BLAKER 1925 BLAKER 1925 BLAKER "
        "1925 BLAKER 1925 BLAKER 1927 RÅNÅSFOSS 1927 RÅNÅSFOSS 1927 RÅNÅSFOSS"
    )
    expected_dict = {"postal_code": "1925", "location": "BLAKER RÅNÅSFOSS"}

    # Evaluate
    result, needs_review = parse_address(address)

    # Assert
    assert result == expected_dict
    assert needs_review is True


def test_parse_address_empty_string():
    # Arrange
    address = "   "
    expected_dict = {"postal_code": None, "location": None}

    # Evaluate
    result, needs_review = parse_address(address)

    # Assert
    assert result == expected_dict
    assert needs_review is False
