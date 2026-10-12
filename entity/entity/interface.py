"""The Entity Interface: every Entity by its own name and together in the Entity Collection."""

from entity.entity.account import Account
from entity.entity.account_group import AccountGroup
from entity.entity.asset import Asset
from entity.entity.broker import Broker
from entity.entity.currency import Currency
from entity.entity.instance import Instance
from entity.entity.user import User

__all__ = [
    "Account",
    "AccountGroup",
    "Asset",
    "Broker",
    "Currency",
    "Instance",
    "User",
    "entities",
]

entities = (User, Instance, Currency, Broker, Asset, AccountGroup, Account)
