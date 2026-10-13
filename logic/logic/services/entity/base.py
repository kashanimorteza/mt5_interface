"""Base: every Entity Operation of Database, as one Action each, for the Entity a Child binds."""

import builtins
from collections.abc import Sequence
from typing import Any, ClassVar

from database.interface import (
    database_error,
    database_instance,
    database_interface,
    database_value,
)


class BaseEntity:
    """The shared Actions every Child Service inherits, working through one Database object."""

    _entity: ClassVar[Any]

    def __init__(self) -> None:
        self._database = database_interface()

    def _own(self, entity: Any) -> Any:
        if type(entity) is not self._entity:
            raise database_error.InvalidInputError(
                f"Expected an instance of {self._entity.__name__}"
            )
        return entity

    def add(self, entity: Any, instance: database_instance | None = None) -> Any:
        """Store one complete new Entity and return it as stored, with generated values."""
        return self._database.add(self._own(entity), instance)

    def update(
        self, entity: Any, instance: database_instance | None = None
    ) -> Any | None:
        """Replace every mutable Field of the record the Entity's id locates, or return None."""
        return self._database.update(self._own(entity), instance)

    def list(
        self,
        filters: Sequence[database_value.Filter] | None = None,
        combination: database_value.FilterCombination | None = None,
        orders: Sequence[database_value.Order] | None = None,
        limit: int | None = None,
        instance: database_instance | None = None,
    ) -> builtins.list[Any]:
        """Return the matching Entities, ordered and bounded by a positive limit."""
        return self._database.list(
            self._entity, filters, combination, orders, limit, instance
        )

    def get_by_id(
        self, id: int, instance: database_instance | None = None
    ) -> Any | None:
        """Return the Entity with this id, or None."""
        return self._database.get_by_id(self._entity, id, instance)

    def delete(self, id: int, instance: database_instance | None = None) -> Any | None:
        """Delete the Entity with this id and return it as it was, or None."""
        return self._database.delete(self._entity, id, instance)

    def enable(self, id: int, instance: database_instance | None = None) -> Any | None:
        """Set only is_active to true and return the final Entity, or None."""
        return self._database.enable(self._entity, id, instance)

    def disable(self, id: int, instance: database_instance | None = None) -> Any | None:
        """Set only is_active to false and return the final Entity, or None."""
        return self._database.disable(self._entity, id, instance)

    def count(
        self,
        filters: Sequence[database_value.Filter] | None = None,
        combination: database_value.FilterCombination | None = None,
        instance: database_instance | None = None,
    ) -> int:
        """Return the number of matching records."""
        return self._database.count(self._entity, filters, combination, instance)

    def sum(
        self,
        field: Any,
        filters: Sequence[database_value.Filter] | None = None,
        combination: database_value.FilterCombination | None = None,
        instance: database_instance | None = None,
    ) -> Any:
        """Return the total of one numeric Field over matching records, or zero."""
        return self._database.sum(self._entity, field, filters, combination, instance)

    def min(
        self,
        field: Any,
        filters: Sequence[database_value.Filter] | None = None,
        combination: database_value.FilterCombination | None = None,
        instance: database_instance | None = None,
    ) -> Any:
        """Return the smallest value of one Field over matching records, or None."""
        return self._database.min(self._entity, field, filters, combination, instance)

    def max(
        self,
        field: Any,
        filters: Sequence[database_value.Filter] | None = None,
        combination: database_value.FilterCombination | None = None,
        instance: database_instance | None = None,
    ) -> Any:
        """Return the largest value of one Field over matching records, or None."""
        return self._database.max(self._entity, field, filters, combination, instance)

    def truncate(self, instance: database_instance | None = None) -> int:
        """Delete every record of the Entity, keeping its Table, and return the count."""
        return self._database.truncate(self._entity, instance)
