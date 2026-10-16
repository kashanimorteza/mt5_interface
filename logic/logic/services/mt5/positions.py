"""Positions Function Group of MT5 Service."""

from logic.services.mt5.terminal import JSON, call


class Positions:
    """Count and read open positions."""

    @staticmethod
    def positions_total(terminal: str) -> JSON:
        """Return the number of open positions."""
        return call(terminal, "positions_total")

    @staticmethod
    def positions_get(
        terminal: str,
        symbol: str | None = None,
        group: str | None = None,
        ticket: int | None = None,
    ) -> JSON:
        """Return open positions, optionally filtered by symbol, group, or ticket."""
        return call(
            terminal,
            "positions_get",
            named={"symbol": symbol, "group": group, "ticket": ticket},
        )
