"""Coordinating the Setup Operations, including prepare."""

from collections.abc import Callable

from database.core import initial_data, tables
from database.core.errors import DatabaseError, SetupError
from database.core.values import SetupResult, database_instance


def _named(
    command: str,
    instance: database_instance | None,
    operation: Callable[[database_instance | None], SetupResult],
) -> SetupResult:
    try:
        return operation(instance)
    except DatabaseError as error:
        where = (
            f"Instance {instance.value}"
            if isinstance(instance, database_instance)
            else "the default Instance"
        )
        failure = type(error)(f"{command} on {where} failed: {error}")
    # Raised outside the handler so no original error is attached.
    raise failure


def create_tables(instance: database_instance | None) -> SetupResult:
    """Create every Entity Table on the selected Instance."""
    return _named("create_tables", instance, tables.create_tables)


def insert_initial_data(instance: database_instance | None) -> SetupResult:
    """Insert the configured Initial Data on the selected Instance."""
    return _named("insert_initial_data", instance, initial_data.insert_initial_data)


def prepare(instance: database_instance | None) -> SetupResult:
    """Run create_tables and then insert_initial_data, stopping when create_tables fails."""
    created = _named("prepare", instance, tables.create_tables)
    try:
        inserted = initial_data.insert_initial_data(created.instance)
    except DatabaseError as error:
        failure = SetupError(
            f"prepare on Instance {created.instance.value} is incomplete: the Tables are "
            f"ready but insert_initial_data failed: {error}"
        )
    else:
        return SetupResult(
            command="prepare",
            instance=created.instance,
            success=True,
            affected=None,
            message=f"{created.message} {inserted.message}",
        )
    raise failure
