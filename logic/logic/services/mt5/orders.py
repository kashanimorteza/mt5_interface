"""Orders Function Group of MT5 Service."""

from logic.services.mt5.terminal import JSON, call


class Orders:
    """Read active orders and calculate, check, and send trade requests."""

    @staticmethod
    def orders_total(terminal: str) -> JSON:
        """Return the number of active orders."""
        return call(terminal, "orders_total")

    @staticmethod
    def orders_get(
        terminal: str,
        symbol: str | None = None,
        group: str | None = None,
        ticket: int | None = None,
    ) -> JSON:
        """Return active orders, optionally filtered by symbol, group, or ticket."""
        return call(
            terminal,
            "orders_get",
            named={"symbol": symbol, "group": group, "ticket": ticket},
        )

    @staticmethod
    def order_calc_margin(
        terminal: str, action: int, symbol: str, volume: float, price: float
    ) -> JSON:
        """Return the margin in account currency for a trading operation."""
        return call(
            terminal,
            "order_calc_margin",
            {"action": action, "symbol": symbol, "volume": volume, "price": price},
        )

    @staticmethod
    def order_calc_profit(
        terminal: str,
        action: int,
        symbol: str,
        volume: float,
        price_open: float,
        price_close: float,
    ) -> JSON:
        """Return the profit in account currency for a trading operation."""
        return call(
            terminal,
            "order_calc_profit",
            {
                "action": action,
                "symbol": symbol,
                "volume": volume,
                "price_open": price_open,
                "price_close": price_close,
            },
        )

    @staticmethod
    def order_check(terminal: str, request: dict[str, JSON]) -> JSON:
        """Check funds sufficiency for a trade request."""
        return call(terminal, "order_check", {"request": request})

    @staticmethod
    def order_send(terminal: str, request: dict[str, JSON]) -> JSON:
        """Send a trade request to the trade server."""
        return call(terminal, "order_send", {"request": request})
