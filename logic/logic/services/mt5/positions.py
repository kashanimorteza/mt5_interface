"""The Positions Function Group: one method for every Function MT5 Service lists under Positions."""

from typing import Any

from logic.services.mt5 import terminal as terminal_processes


class Positions:
    """One method for every Function of the Positions Function Group, each run in the Terminal Process of its Terminal."""

    @staticmethod
    def positions_total(terminal: str) -> Any:
        """Get the number of open positions."""
        return terminal_processes.call(terminal, "positions_total", (), {}, (None,))

    @staticmethod
    def positions_get(
        terminal: str,
        *,
        symbol: str | None = None,
        group: str | None = None,
        ticket: int | None = None,
    ) -> Any:
        """Get open positions with the ability to filter by symbol or ticket."""
        return terminal_processes.call(
            terminal,
            "positions_get",
            (),
            terminal_processes.named(symbol=symbol, group=group, ticket=ticket),
            (None,),
        )
