"""Storage Mapping: the table-ready form every Entity derives from its Declaration."""

import decimal
import keyword
import re
import uuid
from typing import Any

from sqlalchemy import Dialect, Identity, MetaData, String, TypeDecorator
from sqlalchemy import Index as TableIndex
from sqlalchemy.orm import registry as Registry
from sqlmodel import Field, UniqueConstraint, UTCDateTime

from entity.core.declaration import (
    NO_DEFAULT,
    Declaration,
    FieldDeclaration,
    FieldType,
    ValueGeneration,
)

NAMING_CONVENTION = {
    "pk": "pk_%(table_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ix": "ix_%(table_name)s_%(column_0_N_name)s",
}

registry = Registry(metadata=MetaData(naming_convention=NAMING_CONVENTION))
"""The shared table registry; its metadata holds exactly the Entities' tables."""


class ExactDecimal(TypeDecorator[decimal.Decimal]):
    """Stores a decimal as its exact text and reads it back as a decimal on every Engine."""

    impl = String
    cache_ok = True

    def process_bind_param(
        self, value: decimal.Decimal | None, dialect: Dialect
    ) -> str | None:
        return None if value is None else str(value)

    def process_result_value(
        self, value: Any, dialect: Dialect
    ) -> decimal.Decimal | None:
        return None if value is None else decimal.Decimal(value)


def _words(logical_name: str) -> list[str]:
    words = re.findall(r"[A-Za-z0-9]+", logical_name)
    if not words or words[0][0].isdigit():
        raise ValueError(f"Cannot resolve a physical name for {logical_name!r}")
    return words


def _checked(physical_name: str, logical_name: str) -> str:
    if not physical_name.isidentifier() or keyword.iskeyword(physical_name):
        raise ValueError(
            f"Physical name {physical_name!r} of {logical_name!r} is reserved"
        )
    return physical_name


def type_name(logical_name: str) -> str:
    """Return the physical type name of an Entity."""
    words = _words(logical_name)
    return _checked("".join(word[0].upper() + word[1:] for word in words), logical_name)


def table_name(logical_name: str) -> str:
    """Return the physical table name of an Entity."""
    return _checked(
        "_".join(word.lower() for word in _words(logical_name)), logical_name
    )


def _generated_identifier(field: FieldDeclaration) -> Any:
    if field.type is FieldType.UUID:
        return uuid.uuid4
    return lambda: str(uuid.uuid4())


def column(declaration: Declaration, name: str) -> Any:
    """Return the realized Field for one Field Declaration and its Entity's Metadata."""
    field = next(item for item in declaration.fields if item.name == name)
    options: dict[str, Any] = {
        "description": field.description,
        "nullable": field.nullable,
        "primary_key": name == declaration.primary_key,
        "unique": _single(declaration.unique_constraints, name),
        "index": _single(declaration.indexes, name),
    }
    relation = next(
        (item for item in declaration.relations if item.local_field == name), None
    )
    if relation is not None:
        options["foreign_key"] = (
            f"{table_name(relation.target_entity)}.{relation.target_field}"
        )
    if field.constraints.size is not None:
        options["max_length"] = field.constraints.size
    if field.type is FieldType.DECIMAL:
        options["sa_type"] = ExactDecimal
    elif field.type is FieldType.DATETIME:
        options["sa_type"] = UTCDateTime
    if field.value_generation is ValueGeneration.AUTO_INCREMENT:
        options["default"] = None
        options["sa_column_args"] = [Identity()]
    elif field.value_generation is ValueGeneration.GENERATED_IDENTIFIER:
        options["default_factory"] = _generated_identifier(field)
    elif field.default is not NO_DEFAULT:
        options["default"] = field.default
    elif field.nullable:
        options["default"] = None
    return Field(**options)


def _single(entries: tuple[Any, ...], name: str) -> bool:
    return any(entry.fields == (name,) for entry in entries)


def table_args(declaration: Declaration) -> tuple[Any, ...]:
    """Return the table-level constraints, indexes, and options of an Entity's table."""
    table = table_name(declaration.name)
    args: list[Any] = [
        UniqueConstraint(*entry.fields)
        for entry in declaration.unique_constraints
        if len(entry.fields) > 1
    ]
    args += [
        TableIndex(f"ix_{table}_{'_'.join(entry.fields)}", *entry.fields)
        for entry in declaration.indexes
        if len(entry.fields) > 1
    ]
    auto_increment = any(
        item.value_generation is ValueGeneration.AUTO_INCREMENT
        for item in declaration.fields
    )
    return (*args, {"sqlite_autoincrement": True}) if auto_increment else tuple(args)
