"""The User Entity."""

from typing import ClassVar

from entity.core import _storage
from entity.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Sensitivity,
    UniquenessConstraint,
    ValueGeneration,
)
from entity.core.foundation import Foundation

DECLARATION = Declaration(
    name="User",
    description=(
        "Defines an independent user of the system and enables multi-user operation. "
        "Each user can have a separate set of settings, allowing new users to be added "
        "with configurations that remain distinct from those of existing users."
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
            description="The user's display name.",
        ),
        FieldDeclaration(
            name="username",
            type=FieldType.STRING,
            nullable=False,
            description="The username used to identify the user.",
        ),
        FieldDeclaration(
            name="password",
            type=FieldType.STRING,
            nullable=False,
            description="The password credential used by the user.",
            sensitivity=Sensitivity.PASSWORD,
        ),
        FieldDeclaration(
            name="api_key",
            type=FieldType.STRING,
            nullable=False,
            description="The API key assigned to the user.",
            sensitivity=Sensitivity.SENSITIVE,
        ),
        FieldDeclaration(
            name="is_active",
            type=FieldType.BOOLEAN,
            nullable=False,
            description="Indicates whether the user is active.",
            default=True,
        ),
        FieldDeclaration(
            name="description",
            type=FieldType.STRING,
            nullable=True,
            description="Describes the user.",
        ),
    ),
    unique_constraints=(
        UniquenessConstraint(("name",)),
        UniquenessConstraint(("username",)),
    ),
)


class User(Foundation, table=True):
    """Defines an independent user of the system and enables multi-user operation."""

    declaration: ClassVar[Declaration] = DECLARATION

    __tablename__ = "user"
    __table_args__ = _storage.table_args(DECLARATION)

    id: int | None = _storage.column(DECLARATION, "id")
    name: str = _storage.column(DECLARATION, "name")
    username: str = _storage.column(DECLARATION, "username")
    password: str = _storage.column(DECLARATION, "password")
    api_key: str = _storage.column(DECLARATION, "api_key")
    is_active: bool = _storage.column(DECLARATION, "is_active")
    description: str | None = _storage.column(DECLARATION, "description")
