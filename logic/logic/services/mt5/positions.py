"""Positions Function Group of MT5 Service."""

from logic.services.mt5.terminal import JSON, call


class Positions:
    """Count and read open positions."""

    def __init__(self, terminal: str) -> None:
        """Bind this Function Group to the Terminal of its MT5 instance."""
        self._terminal = terminal

    def positions_total(self) -> JSON:
        """Return the number of open positions."""
        return call(self._terminal, "positions_total")

    def positions_get(
        self,
        symbol: str | None = None,
        group: str | None = None,
        ticket: int | None = None,
    ) -> JSON:
        """Return open positions, optionally filtered by symbol, group, or ticket."""
        return call(
            self._terminal,
            "positions_get",
            named={"symbol": symbol, "group": group, "ticket": ticket},
        )
