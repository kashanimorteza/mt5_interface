"""The Account Group Child Service."""

from entity import interface as entity

from logic.services.entity.base import BaseEntity


class AccountGroup(BaseEntity):
    """Every Base Action, bound to the Account Group Entity."""

    _entity = entity.AccountGroup
