"""The Python Integration Function Group: every Function of the Package Documentation's Python Integration section."""

import datetime as dt
from typing import Any

from logic.services.mt5 import terminal as terminal_processes


def _given(*values: Any) -> tuple:
    """The unnamed parameters a caller supplied, in order, up to the first one left out."""
    given = []
    for value in values:
        if value is None:
            break
        given.append(value)
    return tuple(given)


def _named(**values: Any) -> dict[str, Any]:
    """The named parameters a caller supplied."""
    return {name: value for name, value in values.items() if value is not None}


class PythonIntegration:
    """One method for every Function of the Package, each run in the Terminal Process of its Terminal."""

    @staticmethod
    def initialize(
        terminal: str,
        path: str | None = None,
        *,
        login: int | None = None,
        password: str | None = None,
        server: str | None = None,
        timeout: int | None = None,
        portable: bool = False,
    ) -> Any:
        """Establish a connection with the MetaTrader 5 terminal."""
        return terminal_processes.open(
            terminal,
            _given(path),
            _named(
                login=login,
                password=password,
                server=server,
                timeout=timeout,
                portable=portable,
            ),
            (False,),
        )

    @staticmethod
    def login(
        terminal: str,
        login: int,
        *,
        password: str | None = None,
        server: str | None = None,
        timeout: int | None = None,
    ) -> Any:
        """Connect to a trading account using specified parameters."""
        return terminal_processes.call(
            terminal,
            "login",
            _given(login),
            _named(password=password, server=server, timeout=timeout),
            (False,),
        )

    @staticmethod
    def shutdown(terminal: str) -> Any:
        """Close the previously established connection to the MetaTrader 5 terminal."""
        return terminal_processes.call(terminal, "shutdown", (), {}, ())

    @staticmethod
    def version(terminal: str) -> Any:
        """Return the MetaTrader 5 terminal version."""
        return terminal_processes.call(terminal, "version", (), {}, (None,))

    @staticmethod
    def last_error(terminal: str) -> Any:
        """Return data on the last error."""
        return terminal_processes.call(terminal, "last_error", (), {}, ())

    @staticmethod
    def account_info(terminal: str) -> Any:
        """Get info on the current trading account."""
        return terminal_processes.call(terminal, "account_info", (), {}, (None,))

    @staticmethod
    def terminal_info(terminal: str) -> Any:
        """Get the connected MetaTrader 5 client terminal status and settings."""
        return terminal_processes.call(terminal, "terminal_info", (), {}, (None,))

    @staticmethod
    def symbols_total(terminal: str) -> Any:
        """Get the number of all financial instruments in the MetaTrader 5 terminal."""
        return terminal_processes.call(terminal, "symbols_total", (), {}, (None,))

    @staticmethod
    def symbols_get(terminal: str, group: str | None = None) -> Any:
        """Get all financial instruments from the MetaTrader 5 terminal."""
        return terminal_processes.call(
            terminal, "symbols_get", (), _named(group=group), (None,)
        )

    @staticmethod
    def symbol_info(terminal: str, symbol: str) -> Any:
        """Get data on the specified financial instrument."""
        return terminal_processes.call(
            terminal, "symbol_info", _given(symbol), {}, (None,)
        )

    @staticmethod
    def symbol_info_tick(terminal: str, symbol: str) -> Any:
        """Get the last tick for the specified financial instrument."""
        return terminal_processes.call(
            terminal, "symbol_info_tick", _given(symbol), {}, (None,)
        )

    @staticmethod
    def symbol_select(terminal: str, symbol: str, enable: bool | None = None) -> Any:
        """Select a symbol in the MarketWatch window or remove a symbol from the window."""
        return terminal_processes.call(
            terminal, "symbol_select", _given(symbol, enable), {}, (False,)
        )

    @staticmethod
    def market_book_add(terminal: str, symbol: str) -> Any:
        """Subscribes the MetaTrader 5 terminal to the Market Depth change events for a specified symbol."""
        return terminal_processes.call(
            terminal, "market_book_add", _given(symbol), {}, (False,)
        )

    @staticmethod
    def market_book_get(terminal: str, symbol: str) -> Any:
        """Returns a tuple from BookInfo featuring Market Depth entries for the specified symbol."""
        return terminal_processes.call(
            terminal, "market_book_get", _given(symbol), {}, (None,)
        )

    @staticmethod
    def market_book_release(terminal: str, symbol: str) -> Any:
        """Cancels subscription of the MetaTrader 5 terminal to the Market Depth change events for a specified symbol."""
        return terminal_processes.call(
            terminal, "market_book_release", _given(symbol), {}, (False,)
        )

    @staticmethod
    def copy_rates_from(
        terminal: str,
        symbol: str,
        timeframe: int,
        date_from: dt.datetime | int,
        count: int,
    ) -> Any:
        """Get bars from the MetaTrader 5 terminal starting from the specified date."""
        return terminal_processes.call(
            terminal,
            "copy_rates_from",
            _given(symbol, timeframe, date_from, count),
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
            _given(symbol, timeframe, start_pos, count),
            {},
            (None,),
        )

    @staticmethod
    def copy_rates_range(
        terminal: str,
        symbol: str,
        timeframe: int,
        date_from: dt.datetime | int,
        date_to: dt.datetime | int,
    ) -> Any:
        """Get bars in the specified date range from the MetaTrader 5 terminal."""
        return terminal_processes.call(
            terminal,
            "copy_rates_range",
            _given(symbol, timeframe, date_from, date_to),
            {},
            (None,),
        )

    @staticmethod
    def copy_ticks_from(
        terminal: str, symbol: str, date_from: dt.datetime | int, count: int, flags: int
    ) -> Any:
        """Get ticks from the MetaTrader 5 terminal starting from the specified date."""
        return terminal_processes.call(
            terminal,
            "copy_ticks_from",
            _given(symbol, date_from, count, flags),
            {},
            (None,),
        )

    @staticmethod
    def copy_ticks_range(
        terminal: str,
        symbol: str,
        date_from: dt.datetime | int,
        date_to: dt.datetime | int,
        flags: int,
    ) -> Any:
        """Get ticks for the specified date range from the MetaTrader 5 terminal."""
        return terminal_processes.call(
            terminal,
            "copy_ticks_range",
            _given(symbol, date_from, date_to, flags),
            {},
            (None,),
        )

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
            _named(symbol=symbol, group=group, ticket=ticket),
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
            _given(action, symbol, volume, price),
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
            _given(action, symbol, volume, price_open, price_close),
            {},
            (None,),
        )

    @staticmethod
    def order_check(terminal: str, request: dict[str, Any]) -> Any:
        """Check funds sufficiency for performing a required trading operation. Check result are returned as the MqlTradeCheckResult structure."""
        return terminal_processes.call(
            terminal, "order_check", _given(request), {}, (None,)
        )

    @staticmethod
    def order_send(terminal: str, request: dict[str, Any]) -> Any:
        """Send a request to perform a trading operation from the terminal to the trade server. The function is similar to OrderSend."""
        return terminal_processes.call(
            terminal, "order_send", _given(request), {}, (None,)
        )

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
            _named(symbol=symbol, group=group, ticket=ticket),
            (None,),
        )

    @staticmethod
    def history_orders_total(
        terminal: str, date_from: dt.datetime | int, date_to: dt.datetime | int
    ) -> Any:
        """Get the number of orders in trading history within the specified interval."""
        return terminal_processes.call(
            terminal, "history_orders_total", _given(date_from, date_to), {}, (None,)
        )

    @staticmethod
    def history_orders_get(
        terminal: str,
        date_from: dt.datetime | int | None = None,
        date_to: dt.datetime | int | None = None,
        *,
        group: str | None = None,
        ticket: int | None = None,
        position: int | None = None,
    ) -> Any:
        """Get orders from trading history with the ability to filter by ticket or position."""
        return terminal_processes.call(
            terminal,
            "history_orders_get",
            _given(date_from, date_to),
            _named(group=group, ticket=ticket, position=position),
            (None,),
        )

    @staticmethod
    def history_deals_total(
        terminal: str, date_from: dt.datetime | int, date_to: dt.datetime | int
    ) -> Any:
        """Get the number of deals in trading history within the specified interval."""
        return terminal_processes.call(
            terminal, "history_deals_total", _given(date_from, date_to), {}, (None,)
        )

    @staticmethod
    def history_deals_get(
        terminal: str,
        date_from: dt.datetime | int | None = None,
        date_to: dt.datetime | int | None = None,
        *,
        group: str | None = None,
        ticket: int | None = None,
        position: int | None = None,
    ) -> Any:
        """Get deals from trading history within the specified interval with the ability to filter by ticket or position."""
        return terminal_processes.call(
            terminal,
            "history_deals_get",
            _given(date_from, date_to),
            _named(group=group, ticket=ticket, position=position),
            (None,),
        )
