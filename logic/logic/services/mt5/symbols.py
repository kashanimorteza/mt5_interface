"""The Symbols Function Group: one method for every Function MT5 Service lists under Symbols."""

from typing import Any

from logic.services.mt5 import terminal as terminal_processes


class Symbols:
    """One method for every Function of the Symbols Function Group, each run in the Terminal Process of its Terminal."""

    @staticmethod
    def symbols_total(terminal: str) -> Any:
        """Get the number of all financial instruments in the MetaTrader 5 terminal."""
        return terminal_processes.call(terminal, "symbols_total", (), {}, (None,))

    @staticmethod
    def symbols_get(terminal: str, group: str | None = None) -> Any:
        """Get all financial instruments from the MetaTrader 5 terminal."""
        return terminal_processes.call(
            terminal, "symbols_get", (), terminal_processes.named(group=group), (None,)
        )

    @staticmethod
    def symbol_info(terminal: str, symbol: str) -> Any:
        """Get data on the specified financial instrument."""
        return terminal_processes.call(
            terminal,
            "symbol_info",
            terminal_processes.given(symbol=symbol),
            {},
            (None,),
        )

    @staticmethod
    def symbol_info_tick(terminal: str, symbol: str) -> Any:
        """Get the last tick for the specified financial instrument."""
        return terminal_processes.call(
            terminal,
            "symbol_info_tick",
            terminal_processes.given(symbol=symbol),
            {},
            (None,),
        )

    @staticmethod
    def symbol_select(terminal: str, symbol: str, enable: bool | None = None) -> Any:
        """Select a symbol in the MarketWatch window or remove a symbol from the window."""
        return terminal_processes.call(
            terminal,
            "symbol_select",
            terminal_processes.given(symbol=symbol, enable=enable),
            {},
            (False,),
        )
