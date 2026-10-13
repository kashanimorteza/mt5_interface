"""The User Child Service."""

from entity import interface as entity

from logic.services.entity.base import BaseEntity


class User(BaseEntity):
    """Every Base Action, bound to the User Entity."""

    _entity = entity.User
