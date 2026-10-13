"""The Account Child Service."""

from entity import interface as entity

from logic.services.entity.base import BaseEntity


class Account(BaseEntity):
    """Every Base Action, bound to the Account Entity."""

    _entity = entity.Account
