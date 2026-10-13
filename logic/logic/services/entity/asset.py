"""The Asset Child Service."""

from entity import interface as entity

from logic.services.entity.base import BaseEntity


class Asset(BaseEntity):
    """Every Base Action, bound to the Asset Entity."""

    _entity = entity.Asset
