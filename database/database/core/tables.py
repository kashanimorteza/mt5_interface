"""create_tables: the Tables of the Entity Collection, built only from the Entities."""

from typing import Any

from entity.interface import entities
from sqlalchemy import Connection, Inspector, Table, UniqueConstraint, inspect

from database.core import data
from database.core.errors import DeclarationMismatchError
from database.core.values import SetupResult, database_instance


def _table(entity: Any) -> Table:
    return entity.__table__


def _declared(table: Table, link: Connection) -> dict[str, Any]:
    uniques = {
        tuple(column.name for column in constraint.columns)
        for constraint in table.constraints
        if isinstance(constraint, UniqueConstraint)
    }
    uniques |= {(column.name,) for column in table.columns if column.unique}
    return {
        "columns": [
            (column.name, str(column.type.compile(link.dialect)), column.nullable)
            for column in table.columns
        ],
        "primary key": sorted(column.name for column in table.primary_key.columns),
        "foreign keys": sorted(
            (key.parent.name, key.column.table.name, key.column.name)
            for key in table.foreign_keys
        ),
        "uniqueness constraints": sorted(uniques),
        "indexes": sorted(
            (tuple(column.name for column in index.columns), bool(index.unique))
            for index in table.indexes
        ),
    }


def _stored(inspector: Inspector, name: str, link: Connection) -> dict[str, Any]:
    foreign_keys = []
    for key in inspector.get_foreign_keys(name):
        foreign_keys += [
            (local, key["referred_table"], remote)
            for local, remote in zip(
                key["constrained_columns"], key["referred_columns"]
            )
        ]
    return {
        "columns": [
            (
                column["name"],
                str(column["type"].compile(link.dialect)),
                column["nullable"],
            )
            for column in inspector.get_columns(name)
        ],
        "primary key": sorted(inspector.get_pk_constraint(name)["constrained_columns"]),
        "foreign keys": sorted(foreign_keys),
        "uniqueness constraints": sorted(
            tuple(item["column_names"])
            for item in inspector.get_unique_constraints(name)
        ),
        "indexes": sorted(
            (
                tuple(str(column) for column in item["column_names"]),
                bool(item["unique"]),
            )
            for item in inspector.get_indexes(name)
        ),
    }


def differences(link: Connection) -> list[str]:
    """Describe how every existing Entity Table differs from its Entity's Declaration."""
    inspector = inspect(link)
    existing = set(inspector.get_table_names())
    found: list[str] = []
    for item in entities:
        table = _table(item)
        if table.name not in existing:
            continue
        declared, stored = _declared(table, link), _stored(inspector, table.name, link)
        found += [
            f"Table {table.name} differs from {item.declaration.name} in its {aspect}"
            for aspect in declared
            if declared[aspect] != stored[aspect]
        ]
    return found


def create(link: Connection) -> int:
    """Create the missing Entity Tables after checking existing ones; return the Table count."""
    found = differences(link)
    if found:
        raise DeclarationMismatchError(
            "create_tables stopped without changing anything: " + "; ".join(found)
        )
    tables = [_table(item) for item in entities]
    entities[0].metadata.create_all(link, tables=tables)
    return len(tables)


def create_tables(instance: database_instance | None) -> SetupResult:
    """Create every Table of the Entity Collection on the selected Instance."""
    count, used = data.run(instance, lambda _unit, link: create(link))
    return SetupResult(
        command="create_tables",
        instance=used,
        success=True,
        affected=count,
        message=f"All {count} Entity Tables are present and match their Entities.",
    )
