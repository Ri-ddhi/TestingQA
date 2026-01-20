import pytest

from main import normalize_phone

# Valid Inputs
def test_normalized():
    assert normalize_phone("+9779856712340") == "+9779856712340"

def test_starting_with_zero():
    assert normalize_phone("09856712340") == "+9779856712340"

def test_ten_digit_number():
    assert normalize_phone("9723123701") == "+9779723123701"

def test_number_with_spaces_and_dashes():
    assert normalize_phone("9 756-712370") == "+9779756712370"

# Invalid Inputs
def test_short_number():
    with pytest.raises(ValueError, match="Invalid phone number"):
        normalize_phone("345221")

def test_alphanumeric_value():
    with pytest.raises(ValueError, match="Invalid phone number"):
        normalize_phone("345@112210")

def test_invalid_ten_digits():
    with pytest.raises(ValueError, match="Invalid phone number"):
        normalize_phone("9345112211")

def test_invalid_country_code():
    with pytest.raises(ValueError, match="Invalid phone number"):
        normalize_phone("+019345112211")

#Edge Cases
def test_with_uncommon_prefix():
    assert normalize_phone("01457891100") == "+9771457891100"

def test_with_all_zeros():
    assert normalize_phone("+9770000000000") == "+9770000000000"

def test_with_letter():
    assert normalize_phone("+97798riddh123") == "+97798riddh123"
