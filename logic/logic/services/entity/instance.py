"""The Instance Child Service."""

from entity import interface as entity

from logic.services.entity.base import BaseEntity


class Instance(BaseEntity):
    """Every Base Action, bound to the Instance Entity."""

    _entity = entity.Instance
