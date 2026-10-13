"""Checking Conditions and Sorts against the given Entity."""

import datetime as dt
import decimal
import math
import uuid
from collections.abc import Sequence
from typing import Any

from sqlalchemy.orm import InstrumentedAttribute

from database.core.errors import InvalidInputError
from database.core.values import (
    CheckedFilter,
    CheckedOrder,
    Filter,
    FilterOperator,
    Order,
    OrderDirection,
)

NUMERIC = frozenset({"integer", "float", "decimal"})
"""The declared Types a sum accepts."""

COMPARABLE = frozenset(
    {"integer", "float", "decimal", "string", "datetime", "date", "time"}
)
"""The declared Types an ordering comparison, minimum, or maximum accepts."""

_TEXTUAL = frozenset({"string"})
_COMPARISONS = frozenset(
    {
        FilterOperator.GREATER_THAN,
        FilterOperator.GREATER_OR_EQUAL,
        FilterOperator.LESS_THAN,
        FilterOperator.LESS_OR_EQUAL,
    }
)
_TEXT_MATCHES = frozenset(
    {FilterOperator.CONTAINS, FilterOperator.STARTS_WITH, FilterOperator.ENDS_WITH}
)
_NULL_CHECKS = frozenset({FilterOperator.IS_NULL, FilterOperator.IS_NOT_NULL})


def field_of(entity: Any, reference: Any) -> tuple[str, str]:
    """Return the name and declared Type of a Field reference the given Entity exposes."""
    names = {field.name: field for field in entity.declaration.fields}
    if (
        not isinstance(reference, InstrumentedAttribute)
        or reference.class_ is not entity
        or reference.key not in names
    ):
        raise InvalidInputError(
            f"Expected a Field reference of {entity.__name__}, such as {entity.__name__}.id"
        )
    return reference.key, str(names[reference.key].type)


def normalized(entity: Any, name: str, type_name: str, value: Any) -> Any:
    match type_name:
        case "string" if type(value) is str:
            return value
        case "integer" if type(value) is int:
            return value
        case "float" if type(value) is float and math.isfinite(value):
            return value
        case "float" if type(value) is int:
            return float(value)
        case "decimal" if type(value) is decimal.Decimal and value.is_finite():
            return value
        case "decimal" if type(value) is int:
            return decimal.Decimal(value)
        case "boolean" if type(value) is bool:
            return value
        case "datetime" if type(value) is dt.datetime and value.utcoffset() is not None:
            return value
        case "date" if type(value) is dt.date:
            return value
        case "time" if type(value) is dt.time:
            return value
        case "uuid" if type(value) is uuid.UUID:
            return value
    raise InvalidInputError(
        f"The value for {entity.__name__}.{name} is not compatible with its Type {type_name}"
    )


def _sequence(values: Any, kind: type, what: str) -> tuple[Any, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise InvalidInputError(f"{what} must be a sequence of {kind.__name__} values")
    if not all(isinstance(item, kind) for item in values):
        raise InvalidInputError(f"{what} must hold only {kind.__name__} values")
    return tuple(values)


def check_filter(entity: Any, item: Filter) -> CheckedFilter:
    """Check one Filter against the given Entity."""
    name, type_name = field_of(entity, item.field)
    operator = item.operator
    if not isinstance(operator, FilterOperator):
        raise InvalidInputError("A Filter operator must be a FilterOperator member")
    where = f"{entity.__name__}.{name}"
    if operator in _NULL_CHECKS:
        if item.value is not None:
            raise InvalidInputError(f"{operator.name} on {where} takes no value")
        return CheckedFilter(name, type_name, operator, None)
    if item.value is None:
        raise InvalidInputError(f"{operator.name} on {where} needs a value")
    if operator in _TEXT_MATCHES and type_name not in _TEXTUAL:
        raise InvalidInputError(
            f"{operator.name} needs a textual Field; {where} is {type_name}"
        )
    if operator in _COMPARISONS and type_name not in COMPARABLE:
        raise InvalidInputError(
            f"{operator.name} cannot compare {where} of Type {type_name}"
        )
    if operator is FilterOperator.IN:
        value = item.value
        if isinstance(value, (str, bytes, dict)) or not isinstance(
            value, (list, tuple, set, frozenset)
        ):
            raise InvalidInputError(f"IN on {where} needs a collection of values")
        members = [normalized(entity, name, type_name, member) for member in value]
        return CheckedFilter(name, type_name, operator, tuple(members))
    return CheckedFilter(
        name, type_name, operator, normalized(entity, name, type_name, item.value)
    )


def check_filters(entity: Any, filters: Any) -> tuple[CheckedFilter, ...]:
    """Check every supplied Filter against the given Entity."""
    if filters is None:
        return ()
    return tuple(
        check_filter(entity, item) for item in _sequence(filters, Filter, "filters")
    )


def check_order(entity: Any, item: Order) -> CheckedOrder:
    """Check one Order against the given Entity."""
    name, type_name = field_of(entity, item.field)
    if not isinstance(item.direction, OrderDirection):
        raise InvalidInputError("An Order direction must be an OrderDirection member")
    return CheckedOrder(name, type_name, item.direction is OrderDirection.DESCENDING)


def check_orders(entity: Any, orders: Any) -> tuple[CheckedOrder, ...]:
    """Check every supplied Order against the given Entity, keeping their sequence."""
    return tuple(
        check_order(entity, item) for item in _sequence(orders, Order, "orders")
    )
