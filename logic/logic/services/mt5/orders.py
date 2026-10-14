"""The Orders Function Group: one method for every Function MT5 Service lists under Orders."""

from typing import Any

from logic.services.mt5 import terminal as terminal_processes


class Orders:
    """One method for every Function of the Orders Function Group, each run in the Terminal Process of its Terminal."""

    @staticmethod
    def orders_total(terminal: str) -> Any:
        """Get the number of active orders."""
        return terminal_processes.call(terminal, "orders_total", (), {}, (None,))

    @staticmethod
    def orders_get(
        terminal: str,
        *,
        symbol: str | None = None,
        group: str | None = None,
        ticket: int | None = None,
    ) -> Any:
        """Get active orders with the ability to filter by symbol or ticket."""
        return terminal_processes.call(
            terminal,
            "orders_get",
            (),
            terminal_processes.named(symbol=symbol, group=group, ticket=ticket),
            (None,),
        )

    @staticmethod
    def order_calc_margin(
        terminal: str, action: int, symbol: str, volume: float, price: float
    ) -> Any:
        """Return margin in the account currency to perform a specified trading operation."""
        return terminal_processes.call(
            terminal,
            "order_calc_margin",
            terminal_processes.given(
                action=action, symbol=symbol, volume=volume, price=price
            ),
            {},
            (None,),
        )

    @staticmethod
    def order_calc_profit(
        terminal: str,
        action: int,
        symbol: str,
        volume: float,
        price_open: float,
        price_close: float,
    ) -> Any:
        """Return profit in the account currency for a specified trading operation."""
        return terminal_processes.call(
            terminal,
            "order_calc_profit",
            terminal_processes.given(
                action=action,
                symbol=symbol,
                volume=volume,
                price_open=price_open,
                price_close=price_close,
            ),
            {},
            (None,),
        )

    @staticmethod
    def order_check(terminal: str, request: dict[str, Any]) -> Any:
        """Check funds sufficiency for performing a required trading operation. Check result are returned as the MqlTradeCheckResult structure."""
        return terminal_processes.call(
            terminal,
            "order_check",
            terminal_processes.given(request=request),
            {},
            (None,),
        )

    @staticmethod
    def order_send(terminal: str, request: dict[str, Any]) -> Any:
        """Send a request to perform a trading operation from the terminal to the trade server. The function is similar to OrderSend."""
        return terminal_processes.call(
            terminal,
            "order_send",
            terminal_processes.given(request=request),
            {},
            (None,),
        )
