"""The Broker Entity."""

from typing import ClassVar

from entity.core import _storage
from entity.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniquenessConstraint,
    ValueGeneration,
)
from entity.core.foundation import Foundation

DECLARATION = Declaration(
    name="Broker",
    description=(
        "Defines a broker supported by the system and identifies the user who owns its "
        "configuration."
    ),
    fields=(
        FieldDeclaration(
            name="id",
            type=FieldType.INTEGER,
            nullable=False,
            immutable=True,
            value_generation=ValueGeneration.AUTO_INCREMENT,
        ),
        FieldDeclaration(
            name="name",
            type=FieldType.STRING,
            nullable=False,
            description="The broker's display name.",
        ),
        FieldDeclaration(
            name="user_id",
            type=FieldType.INTEGER,
            nullable=False,
            description="Identifies the user who owns the broker configuration.",
        ),
        FieldDeclaration(
            name="is_active",
            type=FieldType.BOOLEAN,
            nullable=False,
            description="Indicates whether the broker is active.",
            default=True,
        ),
        FieldDeclaration(
            name="description",
            type=FieldType.STRING,
            nullable=True,
            description="Describes the broker.",
        ),
    ),
    relations=(
        Relation(local_field="user_id", target_entity="User", target_field="id"),
    ),
    unique_constraints=(UniquenessConstraint(("user_id", "name")),),
)


class Broker(Foundation, table=True):
    """Defines a broker supported by the system."""

    declaration: ClassVar[Declaration] = DECLARATION

    __tablename__ = "broker"
    __table_args__ = _storage.table_args(DECLARATION)

    id: int | None = _storage.column(DECLARATION, "id")
    name: str = _storage.column(DECLARATION, "name")
    user_id: int = _storage.column(DECLARATION, "user_id")
    is_active: bool = _storage.column(DECLARATION, "is_active")
    description: str | None = _storage.column(DECLARATION, "description")
