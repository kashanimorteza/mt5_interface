"""The Account Entity."""

import decimal
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
    name="Account",
    description=(
        "Defines a funded trading account through which the system executes trades and "
        "launches positions. Each Account identifies the trading account and its account-level "
        "login credentials, while its selected Instance owns the separate technical connection "
        "to MetaTrader 5."
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
            description="The account's display name.",
        ),
        FieldDeclaration(
            name="group_id",
            type=FieldType.INTEGER,
            nullable=False,
            description="Identifies the account group that contains the account.",
        ),
        FieldDeclaration(
            name="broker_id",
            type=FieldType.INTEGER,
            nullable=False,
            description="Identifies the broker that owns the account.",
        ),
        FieldDeclaration(
            name="instance_id",
            type=FieldType.INTEGER,
            nullable=False,
            description="Identifies the trading-platform instance used to connect this account.",
        ),
        FieldDeclaration(
            name="base_currency_id",
            type=FieldType.INTEGER,
            nullable=False,
            description="Identifies the base currency used by the account.",
        ),
        FieldDeclaration(
            name="username",
            type=FieldType.STRING,
            nullable=False,
            description="The username identifier used to access the trading account.",
        ),
        FieldDeclaration(
            name="password",
            type=FieldType.STRING,
            nullable=False,
            description="The credential used to access the trading account.",
            sensitivity=Sensitivity.PASSWORD,
        ),
        FieldDeclaration(
            name="leverage",
            type=FieldType.INTEGER,
            nullable=False,
            description="Defines the account's leverage multiplier.",
        ),
        FieldDeclaration(
            name="balance",
            type=FieldType.DECIMAL,
            nullable=False,
            description="Stores the account's current balance.",
            default=decimal.Decimal(0),
        ),
        FieldDeclaration(
            name="account_type",
            type=FieldType.STRING,
            nullable=False,
            description="Identifies the account model, such as `cfd` or `spread_betting`.",
        ),
        FieldDeclaration(
            name="is_active",
            type=FieldType.BOOLEAN,
            nullable=False,
            description="Indicates whether the account is active.",
            default=True,
        ),
        FieldDeclaration(
            name="description",
            type=FieldType.STRING,
            nullable=True,
            description="Describes the account.",
        ),
    ),
    relations=(
        Relation(
            local_field="group_id", target_entity="Account Group", target_field="id"
        ),
        Relation(local_field="broker_id", target_entity="Broker", target_field="id"),
        Relation(
            local_field="instance_id", target_entity="Instance", target_field="id"
        ),
        Relation(
            local_field="base_currency_id", target_entity="Currency", target_field="id"
        ),
    ),
    unique_constraints=(
        UniquenessConstraint(("name",)),
        UniquenessConstraint(("group_id", "broker_id", "instance_id")),
    ),
)


class Account(Foundation, table=True):
    """Defines a funded trading account through which the system executes trades."""

    declaration: ClassVar[Declaration] = DECLARATION

    __tablename__ = "account"
    __table_args__ = _storage.table_args(DECLARATION)

    id: int | None = _storage.column(DECLARATION, "id")
    name: str = _storage.column(DECLARATION, "name")
    group_id: int = _storage.column(DECLARATION, "group_id")
    broker_id: int = _storage.column(DECLARATION, "broker_id")
    instance_id: int = _storage.column(DECLARATION, "instance_id")
    base_currency_id: int = _storage.column(DECLARATION, "base_currency_id")
    username: str = _storage.column(DECLARATION, "username")
    password: str = _storage.column(DECLARATION, "password")
    leverage: int = _storage.column(DECLARATION, "leverage")
    balance: decimal.Decimal = _storage.column(DECLARATION, "balance")
    account_type: str = _storage.column(DECLARATION, "account_type")
    is_active: bool = _storage.column(DECLARATION, "is_active")
    description: str | None = _storage.column(DECLARATION, "description")
