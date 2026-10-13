"""The Entity Service Interface: every Child Service, the Entity each binds, and three Database groups."""

from database.interface import database_error, database_instance, database_value

from logic.services.entity import (
    account,
    account_group,
    asset,
    broker,
    currency,
    instance,
    user,
)

__all__ = ["Entity", "Service", "database_error", "database_instance", "database_value"]


class Service:
    """One Child Service for every Entity of the Entity Collection."""

    User = user.User
    Instance = instance.Instance
    Currency = currency.Currency
    Broker = broker.Broker
    Asset = asset.Asset
    AccountGroup = account_group.AccountGroup
    Account = account.Account


class Entity:
    """The Entity every Child Service binds, under the Child Service's name."""

    User = user.User._entity
    Instance = instance.Instance._entity
    Currency = currency.Currency._entity
    Broker = broker.Broker._entity
    Asset = asset.Asset._entity
    AccountGroup = account_group.AccountGroup._entity
    Account = account.Account._entity
