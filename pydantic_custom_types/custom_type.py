from typing import Any, Callable
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema


class CustomType:
    _schema_method: Callable = core_schema.any_schema

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        raise NotImplementedError("Child class must implement")

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate,
            cls._schema_method(),
        )
