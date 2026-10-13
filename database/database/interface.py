"""The Database Interface: the only public entry point, published as six prefixed groups."""

import builtins
from collections.abc import Mapping, Sequence
from typing import Any

from database.core import data, errors, setup
from database.core.values import (
    CommandResult,
    Filter,
    FilterCombination,
    FilterOperator,
    Order,
    OrderDirection,
    SetupResult,
    database_instance,
)

__all__ = [
    "database_error",
    "database_instance",
    "database_interface",
    "database_result",
    "database_setup",
    "database_value",
]


class database_value:
    """What a consumer passes to an Operation: the values of Condition and Sort."""

    Filter = Filter
    FilterOperator = FilterOperator
    FilterCombination = FilterCombination
    Order = Order
    OrderDirection = OrderDirection


class database_result:
    """What a consumer reads back from the Command and Setup Operations."""

    CommandResult = CommandResult
    SetupResult = SetupResult


class database_error:
    """Every Database error, so a consumer can catch it."""

    DatabaseError = errors.DatabaseError
    ConfigurationError = errors.ConfigurationError
    InactiveInstanceError = errors.InactiveInstanceError
    InvalidInputError = errors.InvalidInputError
    DeclarationMismatchError = errors.DeclarationMismatchError
    ConnectionFailureError = errors.ConnectionFailureError
    ExecutionError = errors.ExecutionError
    SetupError = errors.SetupError


class database_interface:
    """Every Entity Operation and the Command Operation; create it once and call it."""

    def add[E](self, entity: E, instance: database_instance | None = None) -> E:
        """Store one complete new Entity and return it as stored, with generated values."""
        return data.add(entity, instance)

    def update[E](
        self, entity: E, instance: database_instance | None = None
    ) -> E | None:
        """Replace every mutable Field of the record the Entity's id locates, or return None."""
        return data.update(entity, instance)

    def list[E](
        self,
        entity: type[E],
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        orders: Sequence[Order] | None = None,
        limit: int | None = None,
        instance: database_instance | None = None,
    ) -> builtins.list[E]:
        """Return the matching Entities, ordered and bounded by a positive limit."""
        return data.list_entities(entity, filters, combination, orders, limit, instance)

    def get_by_id[E](
        self, entity: type[E], id: int, instance: database_instance | None = None
    ) -> E | None:
        """Return the Entity with this id, or None."""
        return data.get_by_id(entity, id, instance)

    def delete[E](
        self, entity: type[E], id: int, instance: database_instance | None = None
    ) -> E | None:
        """Delete the Entity with this id and return it as it was, or None."""
        return data.delete(entity, id, instance)

    def enable[E](
        self, entity: type[E], id: int, instance: database_instance | None = None
    ) -> E | None:
        """Set only is_active to true and return the final Entity, or None."""
        return data.set_active(entity, id, True, instance)

    def disable[E](
        self, entity: type[E], id: int, instance: database_instance | None = None
    ) -> E | None:
        """Set only is_active to false and return the final Entity, or None."""
        return data.set_active(entity, id, False, instance)

    def count(
        self,
        entity: type,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: database_instance | None = None,
    ) -> int:
        """Return the number of matching records."""
        return data.count(entity, filters, combination, instance)

    def sum(
        self,
        entity: type,
        field: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: database_instance | None = None,
    ) -> Any:
        """Return the total of one numeric Field over matching records, or zero."""
        return data.aggregate("sum", entity, field, filters, combination, instance)

    def min(
        self,
        entity: type,
        field: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: database_instance | None = None,
    ) -> Any:
        """Return the smallest value of one Field over matching records, or None."""
        return data.aggregate("min", entity, field, filters, combination, instance)

    def max(
        self,
        entity: type,
        field: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: database_instance | None = None,
    ) -> Any:
        """Return the largest value of one Field over matching records, or None."""
        return data.aggregate("max", entity, field, filters, combination, instance)

    def truncate(self, entity: type, instance: database_instance | None = None) -> int:
        """Delete every record of the Entity, keeping its Table, and return the count."""
        return data.truncate(entity, instance)

    def execute_command(
        self,
        command: str,
        parameters: Mapping[str, Any] | Sequence[Any] | None = None,
        instance: database_instance | None = None,
    ) -> CommandResult:
        """Run one native command with bound parameters on the selected Instance."""
        return data.execute_command(command, parameters, instance)


class database_setup:
    """Every Setup Operation; create it and call it."""

    def create_tables(self, instance: database_instance | None = None) -> SetupResult:
        """Create every Table of the Entity Collection; stop on a differing Table."""
        return setup.create_tables(instance)

    def insert_initial_data(
        self, instance: database_instance | None = None
    ) -> SetupResult:
        """Insert every missing configured Initial Data record; skip identical ones."""
        return setup.insert_initial_data(instance)

    def prepare(self, instance: database_instance | None = None) -> SetupResult:
        """Run create_tables and then insert_initial_data."""
        return setup.prepare(instance)
