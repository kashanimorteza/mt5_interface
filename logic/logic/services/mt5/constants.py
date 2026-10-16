"""Constants of MT5 Service: every named constant of the Package with its value."""

import multiprocessing
import threading
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures.process import BrokenProcessPool
from typing import ClassVar

from logic.services.mt5.terminal import GENERIC_FAIL, MT5Error

type Constant = int | float | str


def _read() -> dict[str, Constant]:
    """Read every Constant from the Package, run in a separate process."""
    import MetaTrader5 as mt5  # ty: ignore[unresolved-import]

    return {
        name: value
        for name, value in vars(mt5).items()
        if name.isupper()
        and isinstance(value, int | float | str)
        and not isinstance(value, bool)
    }


def _load() -> dict[str, Constant]:
    context = multiprocessing.get_context("spawn")
    try:
        with ProcessPoolExecutor(max_workers=1, mp_context=context) as executor:
            return executor.submit(_read).result()
    except ImportError as error:
        raise MT5Error(
            GENERIC_FAIL, f"The MetaTrader5 package is unavailable: {error}"
        ) from None
    except (BrokenProcessPool, OSError) as error:
        raise MT5Error(
            GENERIC_FAIL,
            f"The Constants cannot be read: {type(error).__name__}: {error}",
        ) from None


class _ConstantsType(type):
    def __getattr__(cls, name: str) -> Constant:
        if name.startswith("_"):
            raise AttributeError(name)
        try:
            return Constants.all()[name]
        except KeyError:
            raise AttributeError(name) from None


class Constants(metaclass=_ConstantsType):
    """Every Constant of the Package by its own name, such as Constants.TIMEFRAME_H1."""

    _values: ClassVar[dict[str, Constant] | None] = None
    _lock: ClassVar[threading.Lock] = threading.Lock()

    @classmethod
    def all(cls) -> dict[str, Constant]:
        """Return every Constant as Plain Data, a dictionary from name to value."""
        with cls._lock:
            if cls._values is None:
                cls._values = _load()
            return dict(cls._values)
