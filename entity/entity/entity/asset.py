"""The Asset Entity."""

from typing import ClassVar

from entity.core import _storage
from entity.core._types import Float
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
    name="Asset",
    description=(
        "Defines an asset that can be selected for trading. It provides the system with the "
        "complete set of available tradable assets and identifies the category of each asset "
        "so the system knows exactly what is being traded."
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
            name="broker_id",
            type=FieldType.INTEGER,
            nullable=False,
            description="Identifies the broker that provides this asset.",
        ),
        FieldDeclaration(
            name="symbol",
            type=FieldType.STRING,
            nullable=False,
            description="Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`.",
        ),
        FieldDeclaration(
            name="category",
            type=FieldType.STRING,
            nullable=False,
            description=(
                "Identifies the asset category, such as `Currency`, `Commodity`, or "
                "`Cryptocurrency`."
            ),
        ),
        FieldDeclaration(
            name="point_size",
            type=FieldType.FLOAT,
            nullable=False,
            description="Stores the size of one point for the asset.",
            default=0.0,
        ),
        FieldDeclaration(
            name="digits",
            type=FieldType.INTEGER,
            nullable=False,
            description="Stores the number of decimal digits used for the asset's price.",
            default=0,
        ),
        FieldDeclaration(
            name="is_active",
            type=FieldType.BOOLEAN,
            nullable=False,
            description="Indicates whether the asset is active.",
            default=True,
        ),
        FieldDeclaration(
            name="description",
            type=FieldType.STRING,
            nullable=True,
            description="Describes the asset.",
        ),
    ),
    relations=(
        Relation(local_field="broker_id", target_entity="Broker", target_field="id"),
    ),
    unique_constraints=(UniquenessConstraint(("broker_id", "symbol")),),
)


class Asset(Foundation, table=True):
    """Defines an asset that can be selected for trading."""

    declaration: ClassVar[Declaration] = DECLARATION

    __tablename__ = "asset"
    __table_args__ = _storage.table_args(DECLARATION)

    id: int | None = _storage.column(DECLARATION, "id")
    broker_id: int = _storage.column(DECLARATION, "broker_id")
    symbol: str = _storage.column(DECLARATION, "symbol")
    category: str = _storage.column(DECLARATION, "category")
    point_size: Float = _storage.column(DECLARATION, "point_size")
    digits: int = _storage.column(DECLARATION, "digits")
    is_active: bool = _storage.column(DECLARATION, "is_active")
    description: str | None = _storage.column(DECLARATION, "description")
