"""The shared routing of every public request: validate, resolve, forward, and materialize."""

import decimal
import functools
import json
from collections.abc import Callable, Mapping, Sequence
from typing import Any

from entity.interface import entities
from pydantic import ValidationError
from sqlalchemy import Connection, Engine

from database.core import query
from database.core.configuration import Configuration, load
from database.core.errors import (
    ConfigurationError,
    DeclarationMismatchError,
    InactiveInstanceError,
    InvalidInputError,
)
from database.core.values import (
    CheckedOrder,
    CommandResult,
    FilterCombination,
    database_instance,
)
from database.engine import sqlite

_UNITS = {"sqlite": sqlite}
"""The Engine unit of every Engine used by an active Instance."""

_ZERO = {"integer": 0, "float": 0.0, "decimal": decimal.Decimal(0)}

_engines: dict[str, Engine] = {}


@functools.cache
def configuration() -> Configuration:
    """Return the validated Database Configuration, loaded once."""
    return load(_UNITS.keys())


def run[T](
    instance: database_instance | None, work: Callable[[Any, Connection], T]
) -> tuple[T, database_instance]:
    """Run work with the selected Instance's Engine unit in one transaction on that Instance."""
    settings = configuration()
    if instance is None:
        instance = settings.default_instance
    elif not isinstance(instance, database_instance):
        raise ConfigurationError("instance must be a DatabaseInstance member")
    connection = settings.instances[instance.value]
    if not connection.active:
        raise InactiveInstanceError(f"Instance {instance.value} is inactive")
    unit = _UNITS[connection.engine]
    engine = _engines.get(connection.key)
    if engine is None:
        engine = _engines[connection.key] = unit.create(connection)
    return unit.run(engine, connection.key, lambda link: work(unit, link)), instance


def entity_class(entity: Any) -> Any:
    """Return the given Entity class when it belongs to the Entity Collection."""
    if not any(entity is item for item in entities):
        raise InvalidInputError("Expected an Entity class of the Entity Collection")
    return entity


def _entity_of(entity: Any) -> Any:
    if not any(type(entity) is item for item in entities):
        raise InvalidInputError("Expected an Entity instance of the Entity Collection")
    return type(entity)


def _generated(field: Any) -> bool:
    return field.value_generation == "auto_increment"


def _json_value(type_name: str, value: Any) -> Any:
    if value is None or type_name in {"string", "integer", "float", "boolean"}:
        return value
    if type_name in {"decimal", "uuid"}:
        return str(value)
    return value.isoformat()


def materialize(entity: Any, row: Mapping[str, Any]) -> Any:
    """Build the Entity from a stored row through its own construction."""
    fields = entity.declaration.fields
    text = json.dumps(
        {
            field.name: _json_value(str(field.type), row.get(field.name))
            for field in fields
        }
    )
    try:
        return entity.from_json(text)
    except ValidationError as error:
        names = sorted({str(item["loc"][0]) for item in error.errors() if item["loc"]})
        failure = DeclarationMismatchError(
            f"A stored {entity.declaration.name} record (id {row.get('id')}) does not "
            f"satisfy its Entity contract in: {', '.join(names) or 'the record'}"
        )
    # Raised outside the handler so no stored value is attached.
    raise failure


def _identity(entity: Any, key: Any) -> Any:
    field = next(item for item in entity.declaration.fields if item.name == "id")
    return query.normalized(entity, "id", str(field.type), key)


def _combination(combination: Any) -> FilterCombination:
    if combination is None:
        return configuration().query.combination
    if not isinstance(combination, FilterCombination):
        raise InvalidInputError("combination must be a FilterCombination member")
    return combination


def _orders(entity: Any, orders: Any) -> tuple[CheckedOrder, ...]:
    if orders is not None:
        return query.check_orders(entity, orders)
    defaults = configuration().query
    field = next(
        item for item in entity.declaration.fields if item.name == defaults.order_field
    )
    return (
        CheckedOrder(
            defaults.order_field,
            str(field.type),
            defaults.order_direction.name == "DESCENDING",
        ),
    )


def _limit(limit: Any) -> int:
    if limit is None:
        return configuration().query.limit
    if type(limit) is not int:
        raise InvalidInputError("limit must be an integer")
    return limit if limit > 0 else -1


def add(entity: Any, instance: database_instance | None) -> Any:
    """Store one complete new Entity and return it as stored."""
    kind = _entity_of(entity)
    values: dict[str, Any] = {}
    for field in kind.declaration.fields:
        value = getattr(entity, field.name)
        if _generated(field):
            if value is not None:
                raise InvalidInputError(
                    f"{field.name} of a new Entity is assigned by storage"
                )
            continue
        values[field.name] = value
    stored, _ = run(
        instance,
        lambda unit, link: materialize(
            kind, unit.insert_row(link, kind.__table__, values)
        ),
    )
    return stored


def update(entity: Any, instance: database_instance | None) -> Any:
    """Replace every mutable Field of the record the Entity's id locates."""
    kind = _entity_of(entity)
    if entity.id is None:
        raise InvalidInputError(
            "update needs a stored Entity whose id locates the record"
        )
    values = {
        field.name: getattr(entity, field.name)
        for field in kind.declaration.fields
        if not field.immutable and not _generated(field)
    }
    return _changed(kind, entity.id, values, instance)


def _changed(
    kind: Any, key: Any, values: Mapping[str, Any], instance: database_instance | None
) -> Any:
    def work(unit: Any, link: Connection) -> Any:
        row = unit.update_row(link, kind.__table__, key, values)
        return None if row is None else materialize(kind, row)

    stored, _ = run(instance, work)
    return stored


def _found(
    kind: Any, key: Any, instance: database_instance | None, operation: str
) -> Any:
    def work(unit: Any, link: Connection) -> Any:
        row = getattr(unit, operation)(link, kind.__table__, key)
        return None if row is None else materialize(kind, row)

    stored, _ = run(instance, work)
    return stored


def get_by_id(entity: Any, key: Any, instance: database_instance | None) -> Any:
    """Return the Entity with this id, or None."""
    kind = entity_class(entity)
    return _found(kind, _identity(kind, key), instance, "get_row")


def delete(entity: Any, key: Any, instance: database_instance | None) -> Any:
    """Delete the Entity with this id and return it as it was, or None."""
    kind = entity_class(entity)
    return _found(kind, _identity(kind, key), instance, "delete_row")


def set_active(
    entity: Any, key: Any, active: bool, instance: database_instance | None
) -> Any:
    """Set only is_active of the Entity with this id and return it, or None."""
    kind = entity_class(entity)
    return _changed(kind, _identity(kind, key), {"is_active": active}, instance)


def list_entities(
    entity: Any,
    filters: Any,
    combination: Any,
    orders: Any,
    limit: Any,
    instance: database_instance | None,
) -> list[Any]:
    """Return the matching Entities in order, bounded by a positive limit."""
    kind = entity_class(entity)
    checked = query.check_filters(kind, filters)
    joined = _combination(combination)
    ordered = _orders(kind, orders)
    bound = _limit(limit)
    found, _ = run(
        instance,
        lambda unit, link: [
            materialize(kind, row)
            for row in unit.select_rows(
                link, kind.__table__, checked, joined, ordered, bound
            )
        ],
    )
    return found


def count(
    entity: Any, filters: Any, combination: Any, instance: database_instance | None
) -> int:
    """Return the number of matching records."""
    kind = entity_class(entity)
    checked = query.check_filters(kind, filters)
    joined = _combination(combination)
    total, _ = run(
        instance, lambda unit, link: unit.count(link, kind.__table__, checked, joined)
    )
    return total


def aggregate(
    function: str,
    entity: Any,
    field: Any,
    filters: Any,
    combination: Any,
    instance: database_instance | None,
) -> Any:
    """Return the sum, minimum, or maximum of one Field over matching records."""
    kind = entity_class(entity)
    name, type_name = query.field_of(kind, field)
    accepted = query.NUMERIC if function == "sum" else query.COMPARABLE
    if type_name not in accepted:
        raise InvalidInputError(
            f"{function} cannot use {kind.__name__}.{name} of Type {type_name}"
        )
    checked = query.check_filters(kind, filters)
    joined = _combination(combination)
    value, _ = run(
        instance,
        lambda unit, link: unit.aggregate(
            link, kind.__table__, function, name, type_name, checked, joined
        ),
    )
    if value is None and function == "sum":
        return _ZERO[type_name]
    return value


def truncate(entity: Any, instance: database_instance | None) -> int:
    """Delete every record of the Entity, keeping its Table, and return the deleted count."""
    kind = entity_class(entity)
    deleted, _ = run(instance, lambda unit, link: unit.truncate(link, kind.__table__))
    return deleted


def execute_command(
    command: Any, parameters: Any, instance: database_instance | None
) -> CommandResult:
    """Run one native command with bound parameters on the selected Instance."""
    if type(command) is not str or not command.strip():
        raise InvalidInputError("command must be a non-empty native command")
    if parameters is None:
        bound: Mapping[str, Any] | tuple[Any, ...] = ()
    elif isinstance(parameters, Mapping) and all(
        type(key) is str for key in parameters
    ):
        bound = dict(parameters)
    elif isinstance(parameters, Sequence) and not isinstance(parameters, (str, bytes)):
        bound = tuple(parameters)
    else:
        raise InvalidInputError("parameters must be a mapping or a sequence of values")
    (rows, affected, columns), used = run(
        instance, lambda unit, link: unit.execute(link, command, bound)
    )
    return CommandResult(
        rows=rows,
        affected=affected,
        columns=columns,
        success=True,
        message="Command executed.",
        instance=used,
    )
