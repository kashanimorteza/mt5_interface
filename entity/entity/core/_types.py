"""Field Type realization: the in-language value and JSON Object form of each Field Type."""

import datetime as dt
import decimal
import math
import uuid
from collections.abc import Callable
from typing import Annotated, Any

from pydantic import AwareDatetime, BeforeValidator
from pydantic_core import PydanticKnownError


def _exact_float(value: Any) -> Any:
    if type(value) is not float:
        raise PydanticKnownError("float_type")
    if not math.isfinite(value):
        raise PydanticKnownError("finite_number")
    return value


Float = Annotated[float, BeforeValidator(_exact_float)]

PYTHON_TYPES: dict[str, Any] = {
    "string": str,
    "integer": int,
    "float": Float,
    "decimal": decimal.Decimal,
    "boolean": bool,
    "datetime": AwareDatetime,
    "date": dt.date,
    "time": dt.time,
    "uuid": uuid.UUID,
}

_TEXT_DECODERS: dict[str, Callable[[str], Any]] = {
    "decimal": decimal.Decimal,
    "datetime": dt.datetime.fromisoformat,
    "date": dt.date.fromisoformat,
    "time": dt.time.fromisoformat,
    "uuid": uuid.UUID,
}


def is_known(type_name: str) -> bool:
    """Return whether a Type belongs to the closed Field Type set."""
    return type_name in PYTHON_TYPES


def python_type(type_name: str, *, optional: bool) -> Any:
    """Return the in-language annotation that realizes a Field Type."""
    realized = PYTHON_TYPES[type_name]
    return realized | None if optional else realized


def matches(type_name: str, value: Any) -> bool:
    """Return whether a non-null value belongs to the value category of a Field Type."""
    match type_name:
        case "string":
            return type(value) is str
        case "integer":
            return type(value) is int
        case "float":
            return type(value) is float and math.isfinite(value)
        case "decimal":
            return type(value) is decimal.Decimal and value.is_finite()
        case "boolean":
            return type(value) is bool
        case "datetime":
            return type(value) is dt.datetime and value.utcoffset() is not None
        case "date":
            return type(value) is dt.date
        case "time":
            return type(value) is dt.time
        case "uuid":
            return type(value) is uuid.UUID
    return False


def to_json_value(type_name: str, value: Any) -> Any:
    """Return the JSON Object form of a Field value."""
    if value is None or type_name in {"string", "integer", "float", "boolean"}:
        return value
    if type_name == "decimal":
        return str(value)
    if type_name == "uuid":
        return str(value)
    return value.isoformat()


def from_json_value(type_name: str, value: Any) -> Any:
    """Decode the text form of a Field value; undecodable text is left for Validation to refuse."""
    decoder = _TEXT_DECODERS.get(type_name)
    if decoder is None or type(value) is not str:
        return value
    try:
        return decoder(value)
    except ValueError, decimal.InvalidOperation:
        return value
