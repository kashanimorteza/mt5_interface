"""The Broker Child Service."""

from entity import interface as entity

from logic.services.entity.base import BaseEntity


class Broker(BaseEntity):
    """Every Base Action, bound to the Broker Entity."""

    _entity = entity.Broker
