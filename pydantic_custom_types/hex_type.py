from pydantic import GetJsonSchemaHandler
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue
from .custom_type import CustomType
from re import compile

HEX_REGEX = r"^(-)?0x[0-9a-fA-F]+$"
INVALID_HEX_FORMAT_MSG = "invalid hexadecimal string format '%s'"


class HexType(CustomType):
    """custom type to parse hexa-decimal and integer type and convert former to integer"""

    @classmethod
    def validate(cls, value):
        """
        validate the value is a valid hexa-decimal string and convert it to integer
        """
        value = value.strip().lower() if isinstance(value, str) else value

        if not compile(HEX_REGEX).match(value):
            raise ValueError(INVALID_HEX_FORMAT_MSG % value)
        try:
            return int(value, 16)
        except ValueError as err:
            raise ValueError(INVALID_HEX_FORMAT_MSG % value) from err

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = handler(schema)
        json_schema.update(pattern=HEX_REGEX, type="string")
        return json_schema

    @classmethod
    def __repr__(cls):
        return "Union[str, int]"
