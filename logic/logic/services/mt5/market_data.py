"""The MarketData Function Group: one method for every Function MT5 Service lists under MarketData."""

from typing import Any

from logic.services.mt5 import terminal as terminal_processes


class MarketData:
    """One method for every Function of the MarketData Function Group, each run in the Terminal Process of its Terminal."""

    @staticmethod
    def copy_rates_from(
        terminal: str, symbol: str, timeframe: int, date_from: int, count: int
    ) -> Any:
        """Get bars from the MetaTrader 5 terminal starting from the specified date."""
        return terminal_processes.call(
            terminal,
            "copy_rates_from",
            terminal_processes.given(
                symbol=symbol, timeframe=timeframe, date_from=date_from, count=count
            ),
            {},
            (None,),
        )

    @staticmethod
    def copy_rates_from_pos(
        terminal: str, symbol: str, timeframe: int, start_pos: int, count: int
    ) -> Any:
        """Get bars from the MetaTrader 5 terminal starting from the specified index."""
        return terminal_processes.call(
            terminal,
            "copy_rates_from_pos",
            terminal_processes.given(
                symbol=symbol, timeframe=timeframe, start_pos=start_pos, count=count
            ),
            {},
            (None,),
        )

    @staticmethod
    def copy_rates_range(
        terminal: str, symbol: str, timeframe: int, date_from: int, date_to: int
    ) -> Any:
        """Get bars in the specified date range from the MetaTrader 5 terminal."""
        return terminal_processes.call(
            terminal,
            "copy_rates_range",
            terminal_processes.given(
                symbol=symbol, timeframe=timeframe, date_from=date_from, date_to=date_to
            ),
            {},
            (None,),
        )

    @staticmethod
    def copy_ticks_from(
        terminal: str, symbol: str, date_from: int, count: int, flags: int
    ) -> Any:
        """Get ticks from the MetaTrader 5 terminal starting from the specified date."""
        return terminal_processes.call(
            terminal,
            "copy_ticks_from",
            terminal_processes.given(
                symbol=symbol, date_from=date_from, count=count, flags=flags
            ),
            {},
            (None,),
        )

    @staticmethod
    def copy_ticks_range(
        terminal: str, symbol: str, date_from: int, date_to: int, flags: int
    ) -> Any:
        """Get ticks for the specified date range from the MetaTrader 5 terminal."""
        return terminal_processes.call(
            terminal,
            "copy_ticks_range",
            terminal_processes.given(
                symbol=symbol, date_from=date_from, date_to=date_to, flags=flags
            ),
            {},
            (None,),
        )
