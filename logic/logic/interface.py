"""The Logic Interface: every Logic Service's own Interface, under the Service's name."""

from logic.services.entity import interface as Entity
from logic.services.mt5 import interface as MT5

__all__ = ["MT5", "Entity"]
