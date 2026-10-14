"""The MarketBook Function Group: one method for every Function MT5 Service lists under MarketBook."""

from typing import Any

from logic.services.mt5 import terminal as terminal_processes


class MarketBook:
    """One method for every Function of the MarketBook Function Group, each run in the Terminal Process of its Terminal."""

    @staticmethod
    def market_book_add(terminal: str, symbol: str) -> Any:
        """Subscribes the MetaTrader 5 terminal to the Market Depth change events for a specified symbol."""
        return terminal_processes.call(
            terminal,
            "market_book_add",
            terminal_processes.given(symbol=symbol),
            {},
            (False,),
        )

    @staticmethod
    def market_book_get(terminal: str, symbol: str) -> Any:
        """Returns a tuple from BookInfo featuring Market Depth entries for the specified symbol."""
        return terminal_processes.call(
            terminal,
            "market_book_get",
            terminal_processes.given(symbol=symbol),
            {},
            (None,),
        )

    @staticmethod
    def market_book_release(terminal: str, symbol: str) -> Any:
        """Cancels subscription of the MetaTrader 5 terminal to the Market Depth change events for a specified symbol."""
        return terminal_processes.call(
            terminal,
            "market_book_release",
            terminal_processes.given(symbol=symbol),
            {},
            (False,),
        )
