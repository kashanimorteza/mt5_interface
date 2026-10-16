"""Orders Function Group of MT5 Service."""

from logic.services.mt5.terminal import JSON, call


class Orders:
    """Read active orders and calculate, check, and send trade requests."""

    def __init__(self, terminal: str) -> None:
        """Bind this Function Group to the Terminal of its MT5 instance."""
        self._terminal = terminal

    def orders_total(self) -> JSON:
        """Return the number of active orders."""
        return call(self._terminal, "orders_total")

    def orders_get(
        self,
        symbol: str | None = None,
        group: str | None = None,
        ticket: int | None = None,
    ) -> JSON:
        """Return active orders, optionally filtered by symbol, group, or ticket."""
        return call(
            self._terminal,
            "orders_get",
            named={"symbol": symbol, "group": group, "ticket": ticket},
        )

    def order_calc_margin(
        self, action: int, symbol: str, volume: float, price: float
    ) -> JSON:
        """Return the margin in account currency for a trading operation."""
        return call(
            self._terminal,
            "order_calc_margin",
            {"action": action, "symbol": symbol, "volume": volume, "price": price},
        )

    def order_calc_profit(
        self,
        action: int,
        symbol: str,
        volume: float,
        price_open: float,
        price_close: float,
    ) -> JSON:
        """Return the profit in account currency for a trading operation."""
        return call(
            self._terminal,
            "order_calc_profit",
            {
                "action": action,
                "symbol": symbol,
                "volume": volume,
                "price_open": price_open,
                "price_close": price_close,
            },
        )

    def order_check(self, request: dict[str, JSON]) -> JSON:
        """Check funds sufficiency for a trade request."""
        return call(self._terminal, "order_check", {"request": request})

    def order_send(self, request: dict[str, JSON]) -> JSON:
        """Send a trade request to the trade server."""
        return call(self._terminal, "order_send", {"request": request})
