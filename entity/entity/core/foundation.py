"""Foundation: the public shared contract converting every Entity to and from its JSON Object."""

import json
from typing import Any, LiteralString, Self, cast

from pydantic import ValidationError
from pydantic_core import PydanticCustomError

from entity.core import _types
from entity.core._base import REPLACEMENT, Base


class _NotJson(ValueError):
    pass


def _unique_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise _NotJson(f"repeated key {key!r}")
        result[key] = value
    return result


def _standard_constant(name: str) -> Any:
    raise _NotJson(f"non-standard constant {name}")


class Foundation(Base):
    """Every Entity's lossless round trip through JSON text."""

    def to_json(self) -> str:
        """Return JSON text with one root object whose keys are the Fields in Declaration order."""
        return json.dumps(
            {
                field.name: _types.to_json_value(field.type, getattr(self, field.name))
                for field in type(self).declaration.fields
            },
            ensure_ascii=False,
            allow_nan=False,
        )

    @classmethod
    def from_json(cls, text: str) -> Self:
        """Build the Entity from JSON text with the same rules as direct construction."""
        try:
            if type(text) is not str:
                raise _NotJson("input is not text")
            value = json.loads(
                text, object_pairs_hook=_unique_keys, parse_constant=_standard_constant
            )
        except (_NotJson, json.JSONDecodeError) as error:
            raise cls._not_json(f"Invalid JSON: {error}", text) from None
        if type(value) is not dict:
            raise cls._not_json("Input should be one JSON object", text)
        for field in cls.declaration.fields:
            if field.name in value:
                value[field.name] = _types.from_json_value(
                    field.type, value[field.name]
                )
        return cls._from_stored(value)

    @classmethod
    def _not_json(cls, message: str, text: Any) -> ValidationError:
        shown = REPLACEMENT if cls._sensitive() else text
        return ValidationError.from_exception_data(
            cls.__name__,
            [
                {
                    "type": PydanticCustomError(
                        "json_invalid", cast(LiteralString, message)
                    ),
                    "loc": (),
                    "input": shown,
                }
            ],
        )
