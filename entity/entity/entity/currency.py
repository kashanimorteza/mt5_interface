"""The Currency Entity."""

from typing import ClassVar

from entity.core import _storage
from entity.core.declaration import (
    Declaration,
    FieldConstraints,
    FieldDeclaration,
    FieldType,
    Relation,
    UniquenessConstraint,
    ValueGeneration,
)
from entity.core.foundation import Foundation

DECLARATION = Declaration(
    name="Currency",
    description=(
        "Defines a currency that can be used by the trading system and identifies its "
        "standard code, display symbol, associated country or region, and monetary "
        "decimal precision."
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
            description="Identifies the user who owns this currency.",
        ),
        FieldDeclaration(
            name="code",
            type=FieldType.STRING,
            nullable=False,
            description="The currency's standard three-letter code, such as `USD` or `EUR`.",
            constraints=FieldConstraints(size=3),
        ),
        FieldDeclaration(
            name="symbol",
            type=FieldType.STRING,
            nullable=True,
            description="The currency's display symbol, such as `$`, `€`, or `£`.",
        ),
        FieldDeclaration(
            name="country",
            type=FieldType.STRING,
            nullable=True,
            description="Identifies the country or region associated with the currency.",
        ),
        FieldDeclaration(
            name="decimal_digits",
            type=FieldType.INTEGER,
            nullable=False,
            description=(
                "Defines the number of decimal digits normally used for monetary values "
                "in the currency."
            ),
            default=2,
        ),
        FieldDeclaration(
            name="is_active",
            type=FieldType.BOOLEAN,
            nullable=False,
            description="Indicates whether the currency is active.",
            default=True,
        ),
        FieldDeclaration(
            name="description",
            type=FieldType.STRING,
            nullable=True,
            description="Describes the currency.",
        ),
    ),
    relations=(
        Relation(local_field="user_id", target_entity="User", target_field="id"),
    ),
    unique_constraints=(UniquenessConstraint(("user_id", "code")),),
)


class Currency(Foundation, table=True):
    """Defines a currency that can be used by the trading system."""

    declaration: ClassVar[Declaration] = DECLARATION

    __tablename__ = "currency"
    __table_args__ = _storage.table_args(DECLARATION)

    id: int | None = _storage.column(DECLARATION, "id")
    user_id: int = _storage.column(DECLARATION, "user_id")
    code: str = _storage.column(DECLARATION, "code")
    symbol: str | None = _storage.column(DECLARATION, "symbol")
    country: str | None = _storage.column(DECLARATION, "country")
    decimal_digits: int = _storage.column(DECLARATION, "decimal_digits")
    is_active: bool = _storage.column(DECLARATION, "is_active")
    description: str | None = _storage.column(DECLARATION, "description")
