from typing import Any, Dict, Type
from marshmallow.validate import Validator
from marshmallow import ValidationError, fields
from marshmallow_dataclass import NewType
from beam.types import TypeSerializer


class IsInstanceOf(Validator):
    def __init__(self, instanceType: Type):
        self.instanceType = instanceType

    def __call__(self, value: Any) -> Any:
        if isinstance(value, self.instanceType):
            return value

        raise ValidationError([f"needs to be type {self.instanceType}"])


class IsFileMethod(Validator):
    def __init__(self) -> None:
        super().__init__()

    def _raise_validation_error(self):
        raise ValidationError("must be a string in form {pathToFile}:{method}")

    def _validate(self, text):
        if not isinstance(text, str):
            self._raise_validation_error()

        parsed_handler = text.split(":")

        if len(parsed_handler) != 2:
            self._raise_validation_error()

    def __call__(self, value: str) -> str:
        self._validate(value)
        return value


TypeSerializerDict = NewType(
    "TypeSerializerDict",
    Dict[str, TypeSerializer],
    field=fields.Dict,
    keys=fields.String(),
    values=fields.Field(validate=IsInstanceOf(TypeSerializer)),
    required=True,
)
