"""Endpoints: the common HTTP rules API applies to every Group's Endpoints around their Handlers."""

import datetime as dt
import decimal
import functools
import json
import uuid
from collections.abc import Callable
from typing import Annotated, Any

from fastapi import Body, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from logic.interface import Entity as source
from pydantic import BaseModel, ValidationError

PROBLEM_MEDIA_TYPE = "application/problem+json"

ERROR_STATUS = {
    "InvalidInputError": 422,
    "RequestValidationError": 422,
    "InactiveInstanceError": 503,
    "ConnectionFailureError": 503,
    "ExecutionError": 500,
    "DeclarationMismatchError": 500,
    "ConfigurationError": 500,
}
"""The status of every error the error table names; any other error is answered with 500."""


# --- Errors -----------------------------------------------------------------------------


def problem(request: Request, error: Exception) -> JSONResponse:
    """Answer an error as RFC 9457 Problem Details whose type is the error's class name."""
    kind = type(error).__name__
    status = ERROR_STATUS.get(kind, 500)
    detail = (
        "; ".join(
            f"{'.'.join(str(part) for part in item['loc'])}: {item['msg']}"
            for item in error.errors()
        )
        if isinstance(error, RequestValidationError)
        else str(error)
        if isinstance(error, source.database_error.DatabaseError)
        else "The request could not be completed."
    )
    return JSONResponse(
        {"type": kind, "title": kind, "status": status, "detail": detail},
        status_code=status,
        media_type=PROBLEM_MEDIA_TYPE,
    )


# --- Results ----------------------------------------------------------------------------


def _encoded(value: Any) -> Any:
    if isinstance(value, list):
        return [_encoded(item) for item in value]
    if hasattr(value, "to_json"):
        return json.loads(value.to_json())
    if isinstance(value, (decimal.Decimal, uuid.UUID)):
        return str(value)
    if isinstance(value, (dt.datetime, dt.date, dt.time)):
        return value.isoformat()
    return value


class ResultResponse(JSONResponse):
    """Sends an Action's result unchanged, with every Entity in its own JSON form."""

    def render(self, content: Any) -> bytes:
        return json.dumps(
            _encoded(content), ensure_ascii=False, allow_nan=False
        ).encode()


class ResultRoute(APIRoute):
    """Serves every Handler's result through ResultResponse, never through the generic encoder."""

    def __init__(self, path: str, endpoint: Callable[..., Any], **kwargs: Any) -> None:
        @functools.wraps(endpoint)
        def serving(*args: Any, **values: Any) -> ResultResponse:
            return ResultResponse(endpoint(*args, **values))

        super().__init__(path, serving, **kwargs)


# --- Non-simple Parameters --------------------------------------------------------------

_TEXT_DECODERS: dict[str, Callable[[str], Any]] = {
    "decimal": decimal.Decimal,
    "datetime": dt.datetime.fromisoformat,
    "date": dt.date.fromisoformat,
    "time": dt.time.fromisoformat,
    "uuid": uuid.UUID,
}


class FilterForm(BaseModel):
    """A Filter as it travels: its Field's name, its operator, and its value."""

    field: str
    operator: source.database_value.FilterOperator
    value: Any = None


class OrderForm(BaseModel):
    """An Order as it travels: its Field's name and its direction."""

    field: str
    direction: source.database_value.OrderDirection = (
        source.database_value.OrderDirection.ASCENDING
    )


def _declared(entity: Any) -> dict[str, str]:
    return {field.name: str(field.type) for field in entity.declaration.fields}


def _reference(entity: Any, name: str) -> Any:
    if name not in _declared(entity):
        raise source.database_error.InvalidInputError(
            f"{entity.__name__} has no Field named {name!r}"
        )
    return getattr(entity, name)


def _value(type_name: str, value: Any) -> Any:
    decoder = _TEXT_DECODERS.get(type_name)
    if decoder is None:
        return value
    if type_name == "decimal" and type(value) in (int, float):
        value = str(value)
    if type(value) is not str:
        return value
    try:
        return decoder(value)
    except ValueError, decimal.InvalidOperation:
        # Left as text, so the source refuses it as an incompatible value.
        return value


def entity_in(bound: Any) -> Callable[..., Any]:
    """The Entity Parameter: a JSON object of the Entity's fields, built by the Entity itself."""

    def entity_parameter(
        entity: Annotated[dict[str, Any], Body(embed=True, title=bound.__name__)],
    ) -> Any:
        try:
            return bound.from_json(json.dumps(entity))
        except ValidationError as error:
            names = sorted(
                {str(item["loc"][0]) for item in error.errors() if item["loc"]}
            )
            failure = source.database_error.InvalidInputError(
                f"The {bound.__name__} object is invalid in: {', '.join(names) or 'its fields'}"
            )
        # Raised outside the handler so no supplied value is attached.
        raise failure

    return entity_parameter


def filters_in(bound: Any) -> Callable[..., Any]:
    """The filters Parameter: Filter objects whose fields name Fields of the bound Entity."""

    def filters_parameter(
        filters: Annotated[list[FilterForm] | None, Body(embed=True)] = None,
    ) -> Any:
        if filters is None:
            return None
        declared = _declared(bound)
        converted = []
        for item in filters:
            reference = _reference(bound, item.field)
            value = item.value
            if isinstance(value, list):
                value = [_value(declared[item.field], member) for member in value]
            elif value is not None:
                value = _value(declared[item.field], value)
            converted.append(
                source.database_value.Filter(reference, item.operator, value)
            )
        return converted

    return filters_parameter


def orders_in(bound: Any) -> Callable[..., Any]:
    """The orders Parameter: Order objects whose fields name Fields of the bound Entity."""

    def orders_parameter(
        orders: Annotated[list[OrderForm] | None, Body(embed=True)] = None,
    ) -> Any:
        if orders is None:
            return None
        return [
            source.database_value.Order(_reference(bound, item.field), item.direction)
            for item in orders
        ]

    return orders_parameter


def field_in(bound: Any) -> Callable[..., Any]:
    """The field Parameter: the name of a Field of the bound Entity."""

    def field_parameter(field: Annotated[str, Body(embed=True)]) -> Any:
        return _reference(bound, field)

    return field_parameter


def _instance(name: str | None) -> Any:
    if name is None:
        return None
    members = source.database_instance.__members__
    if name not in members:
        raise source.database_error.ConfigurationError(
            f"instance must name a DatabaseInstance member: {', '.join(members)}"
        )
    return members[name]


def instance_in_query(instance: Annotated[str | None, Query()] = None) -> Any:
    """The instance Parameter in Query: the name of a DatabaseInstance member."""
    return _instance(instance)


def instance_in_body(instance: Annotated[str | None, Body(embed=True)] = None) -> Any:
    """The instance Parameter in Body: the name of a DatabaseInstance member."""
    return _instance(instance)


def combination_in_query(
    combination: Annotated[
        source.database_value.FilterCombination | None, Query()
    ] = None,
) -> Any:
    """The combination Parameter in Query: a FilterCombination member name."""
    return combination


def combination_in_body(
    combination: Annotated[
        source.database_value.FilterCombination | None, Body(embed=True)
    ] = None,
) -> Any:
    """The combination Parameter in Body: a FilterCombination member name."""
    return combination


def limit_in_query(limit: Annotated[int | None, Query()] = None) -> Any:
    """The limit Parameter in Query."""
    return limit


def limit_in_body(limit: Annotated[int | None, Body(embed=True)] = None) -> Any:
    """The limit Parameter in Body."""
    return limit
