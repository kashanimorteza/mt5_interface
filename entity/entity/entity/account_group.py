"""The Account Group Entity."""

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
    name="Account Group",
    description="Defines an independent group for organizing trading accounts owned by one user.",
    fields=(
        FieldDeclaration(
            name="id",
            type=FieldType.INTEGER,
            nullable=False,
            immutable=True,
            value_generation=ValueGeneration.AUTO_INCREMENT,
        ),
        FieldDeclaration(
            name="user_id",
            type=FieldType.INTEGER,
            nullable=False,
            description="Identifies the user who owns the account group.",
        ),
        FieldDeclaration(
            name="name",
            type=FieldType.STRING,
            nullable=False,
            description="The account group's display name.",
        ),
        FieldDeclaration(
            name="is_active",
            type=FieldType.BOOLEAN,
            nullable=False,
            description="Indicates whether the account group is active.",
            default=True,
        ),
        FieldDeclaration(
            name="description",
            type=FieldType.STRING,
            nullable=True,
            description="Describes the account group.",
        ),
    ),
    relations=(
        Relation(local_field="user_id", target_entity="User", target_field="id"),
    ),
    unique_constraints=(UniquenessConstraint(("user_id", "name")),),
)


class AccountGroup(Foundation, table=True):
    """Defines an independent group for organizing trading accounts owned by one user."""

    declaration: ClassVar[Declaration] = DECLARATION

    __tablename__ = "account_group"
    __table_args__ = _storage.table_args(DECLARATION)

    id: int | None = _storage.column(DECLARATION, "id")
    user_id: int = _storage.column(DECLARATION, "user_id")
    name: str = _storage.column(DECLARATION, "name")
    is_active: bool = _storage.column(DECLARATION, "is_active")
    description: str | None = _storage.column(DECLARATION, "description")
