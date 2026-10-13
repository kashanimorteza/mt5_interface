"""The Currency Child Service."""

from entity import interface as entity

from logic.services.entity.base import BaseEntity


class Currency(BaseEntity):
    """Every Base Action, bound to the Currency Entity."""

    _entity = entity.Currency
