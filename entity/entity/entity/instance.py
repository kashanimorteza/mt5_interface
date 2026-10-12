"""The Instance Entity."""

from typing import ClassVar

from entity.core import _storage
from entity.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    Sensitivity,
    UniquenessConstraint,
    ValueGeneration,
)
from entity.core.foundation import Foundation

DECLARATION = Declaration(
    name="Instance",
    description=(
        "Defines a user-owned connection instance through which the system accesses MetaTrader 5."
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
            name="user_id",
            type=FieldType.INTEGER,
            nullable=False,
            description="Identifies the user who owns this instance.",
        ),
        FieldDeclaration(
            name="name",
            type=FieldType.STRING,
            nullable=False,
            description="The instance's display name.",
        ),
        FieldDeclaration(
            name="ip",
            type=FieldType.STRING,
            nullable=True,
            description=(
                "Identifies the technical network address used to reach MetaTrader 5 "
                "when required."
            ),
        ),
        FieldDeclaration(
            name="username",
            type=FieldType.STRING,
            nullable=True,
            description=(
                "Defines the technical username used to establish the Instance connection "
                "when required."
            ),
        ),
        FieldDeclaration(
            name="password",
            type=FieldType.STRING,
            nullable=True,
            description=(
                "Defines the technical password used to establish the Instance connection "
                "when required."
            ),
            sensitivity=Sensitivity.PASSWORD,
        ),
        FieldDeclaration(
            name="api_key",
            type=FieldType.STRING,
            nullable=True,
            description=(
                "Defines the technical API credential used to establish the Instance "
                "connection when required."
            ),
            sensitivity=Sensitivity.SENSITIVE,
        ),
        FieldDeclaration(
            name="is_active",
            type=FieldType.BOOLEAN,
            nullable=False,
            description="Indicates whether the instance is active.",
            default=True,
        ),
        FieldDeclaration(
            name="description",
            type=FieldType.STRING,
            nullable=True,
            description="Describes the instance.",
        ),
    ),
    relations=(
        Relation(local_field="user_id", target_entity="User", target_field="id"),
    ),
    unique_constraints=(UniquenessConstraint(("user_id", "name")),),
)


class Instance(Foundation, table=True):
    """Defines a user-owned connection instance through which the system accesses MetaTrader 5."""

    declaration: ClassVar[Declaration] = DECLARATION

    __tablename__ = "instance"
    __table_args__ = _storage.table_args(DECLARATION)

    id: int | None = _storage.column(DECLARATION, "id")
    user_id: int = _storage.column(DECLARATION, "user_id")
    name: str = _storage.column(DECLARATION, "name")
    ip: str | None = _storage.column(DECLARATION, "ip")
    username: str | None = _storage.column(DECLARATION, "username")
    password: str | None = _storage.column(DECLARATION, "password")
    api_key: str | None = _storage.column(DECLARATION, "api_key")
    is_active: bool = _storage.column(DECLARATION, "is_active")
    description: str | None = _storage.column(DECLARATION, "description")
