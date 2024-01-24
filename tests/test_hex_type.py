import pytest

from pydantic import BaseModel
from pydantic_custom_types.hex_type import HexType


class Variable(BaseModel):
    value: HexType


class TestHexType:
    @pytest.mark.parametrize(
        "value, expected",
        [
            ("0x123", 0x123),
            ("0x1234567890abcdef", 0x1234567890ABCDEF),
            ("0x0", 0x0),
            ("0x00", 0x00),
            ("0xFE", 0xFE),
        ],
    )
    def test_valid_hex(self, value, expected):
        """
        Requirement: If the value is a valid hexa-decimal string, return hexa-decimal integer
        """
        assert Variable(name="test", value=value).value == expected

    @pytest.mark.parametrize(
        "value",
        [
            "0x",
            "0x1234567890abcdefg",
            "0xf.",
            "0x.",
            "0.0",
            "str",
        ],
    )
    def test_invalid_hex(self, value):
        """
        Requirement: If the value is not a valid hexa-decimal string, raise a ValueError
        """
        with pytest.raises(ValueError, match="invalid hexadecimal string format"):
            Variable(name="test", value=value)
