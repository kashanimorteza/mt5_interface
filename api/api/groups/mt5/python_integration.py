"""The python_integration Adapter: one Endpoint for every Function of the PythonIntegration Function Group."""

import datetime as dt
from typing import Annotated, Any

from fastapi import APIRouter, Body
from logic.interface import MT5

from api import endpoints

router = APIRouter(
    prefix="/python_integration",
    tags=["MT5 · python_integration"],
    route_class=endpoints.ResultRoute,
)


@router.post("/initialize", response_model=None)
def initialize(
    terminal: Annotated[str, Body(embed=True)],
    path: Annotated[str | None, Body(embed=True)] = None,
    login: Annotated[int | None, Body(embed=True)] = None,
    password: Annotated[str | None, Body(embed=True)] = None,
    server: Annotated[str | None, Body(embed=True)] = None,
    timeout: Annotated[int | None, Body(embed=True)] = None,
    portable: Annotated[bool, Body(embed=True)] = False,
) -> Any:
    """Establish a connection with the MetaTrader 5 terminal."""
    return MT5.PythonIntegration.initialize(
        terminal,
        path,
        login=login,
        password=password,
        server=server,
        timeout=timeout,
        portable=portable,
    )


@router.post("/login", response_model=None)
def login(
    terminal: Annotated[str, Body(embed=True)],
    login: Annotated[int, Body(embed=True)],
    password: Annotated[str | None, Body(embed=True)] = None,
    server: Annotated[str | None, Body(embed=True)] = None,
    timeout: Annotated[int | None, Body(embed=True)] = None,
) -> Any:
    """Connect to a trading account using specified parameters."""
    return MT5.PythonIntegration.login(
        terminal, login, password=password, server=server, timeout=timeout
    )


@router.post("/shutdown", response_model=None)
def shutdown(
    terminal: Annotated[str, Body(embed=True)],
) -> Any:
    """Close the previously established connection to the MetaTrader 5 terminal."""
    return MT5.PythonIntegration.shutdown(terminal)


@router.post("/version", response_model=None)
def version(
    terminal: Annotated[str, Body(embed=True)],
) -> Any:
    """Return the MetaTrader 5 terminal version."""
    return MT5.PythonIntegration.version(terminal)


@router.post("/last_error", response_model=None)
def last_error(
    terminal: Annotated[str, Body(embed=True)],
) -> Any:
    """Return data on the last error."""
    return MT5.PythonIntegration.last_error(terminal)


@router.post("/account_info", response_model=None)
def account_info(
    terminal: Annotated[str, Body(embed=True)],
) -> Any:
    """Get info on the current trading account."""
    return MT5.PythonIntegration.account_info(terminal)


@router.post("/terminal_info", response_model=None)
def terminal_info(
    terminal: Annotated[str, Body(embed=True)],
) -> Any:
    """Get the connected MetaTrader 5 client terminal status and settings."""
    return MT5.PythonIntegration.terminal_info(terminal)


@router.post("/symbols_total", response_model=None)
def symbols_total(
    terminal: Annotated[str, Body(embed=True)],
) -> Any:
    """Get the number of all financial instruments in the MetaTrader 5 terminal."""
    return MT5.PythonIntegration.symbols_total(terminal)


@router.post("/symbols_get", response_model=None)
def symbols_get(
    terminal: Annotated[str, Body(embed=True)],
    group: Annotated[str | None, Body(embed=True)] = None,
) -> Any:
    """Get all financial instruments from the MetaTrader 5 terminal."""
    return MT5.PythonIntegration.symbols_get(terminal, group)


@router.post("/symbol_info", response_model=None)
def symbol_info(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
) -> Any:
    """Get data on the specified financial instrument."""
    return MT5.PythonIntegration.symbol_info(terminal, symbol)


@router.post("/symbol_info_tick", response_model=None)
def symbol_info_tick(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
) -> Any:
    """Get the last tick for the specified financial instrument."""
    return MT5.PythonIntegration.symbol_info_tick(terminal, symbol)


@router.post("/symbol_select", response_model=None)
def symbol_select(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
    enable: Annotated[bool | None, Body(embed=True)] = None,
) -> Any:
    """Select a symbol in the MarketWatch window or remove a symbol from the window."""
    return MT5.PythonIntegration.symbol_select(terminal, symbol, enable)


@router.post("/market_book_add", response_model=None)
def market_book_add(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
) -> Any:
    """Subscribes the MetaTrader 5 terminal to the Market Depth change events for a specified symbol."""
    return MT5.PythonIntegration.market_book_add(terminal, symbol)


@router.post("/market_book_get", response_model=None)
def market_book_get(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
) -> Any:
    """Returns a tuple from BookInfo featuring Market Depth entries for the specified symbol."""
    return MT5.PythonIntegration.market_book_get(terminal, symbol)


@router.post("/market_book_release", response_model=None)
def market_book_release(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
) -> Any:
    """Cancels subscription of the MetaTrader 5 terminal to the Market Depth change events for a specified symbol."""
    return MT5.PythonIntegration.market_book_release(terminal, symbol)


@router.post("/copy_rates_from", response_model=None)
def copy_rates_from(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
    timeframe: Annotated[int, Body(embed=True)],
    date_from: Annotated[dt.datetime | int, Body(embed=True)],
    count: Annotated[int, Body(embed=True)],
) -> Any:
    """Get bars from the MetaTrader 5 terminal starting from the specified date."""
    return MT5.PythonIntegration.copy_rates_from(
        terminal, symbol, timeframe, date_from, count
    )


@router.post("/copy_rates_from_pos", response_model=None)
def copy_rates_from_pos(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
    timeframe: Annotated[int, Body(embed=True)],
    start_pos: Annotated[int, Body(embed=True)],
    count: Annotated[int, Body(embed=True)],
) -> Any:
    """Get bars from the MetaTrader 5 terminal starting from the specified index."""
    return MT5.PythonIntegration.copy_rates_from_pos(
        terminal, symbol, timeframe, start_pos, count
    )


@router.post("/copy_rates_range", response_model=None)
def copy_rates_range(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
    timeframe: Annotated[int, Body(embed=True)],
    date_from: Annotated[dt.datetime | int, Body(embed=True)],
    date_to: Annotated[dt.datetime | int, Body(embed=True)],
) -> Any:
    """Get bars in the specified date range from the MetaTrader 5 terminal."""
    return MT5.PythonIntegration.copy_rates_range(
        terminal, symbol, timeframe, date_from, date_to
    )


@router.post("/copy_ticks_from", response_model=None)
def copy_ticks_from(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
    date_from: Annotated[dt.datetime | int, Body(embed=True)],
    count: Annotated[int, Body(embed=True)],
    flags: Annotated[int, Body(embed=True)],
) -> Any:
    """Get ticks from the MetaTrader 5 terminal starting from the specified date."""
    return MT5.PythonIntegration.copy_ticks_from(
        terminal, symbol, date_from, count, flags
    )


@router.post("/copy_ticks_range", response_model=None)
def copy_ticks_range(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
    date_from: Annotated[dt.datetime | int, Body(embed=True)],
    date_to: Annotated[dt.datetime | int, Body(embed=True)],
    flags: Annotated[int, Body(embed=True)],
) -> Any:
    """Get ticks for the specified date range from the MetaTrader 5 terminal."""
    return MT5.PythonIntegration.copy_ticks_range(
        terminal, symbol, date_from, date_to, flags
    )


@router.post("/orders_total", response_model=None)
def orders_total(
    terminal: Annotated[str, Body(embed=True)],
) -> Any:
    """Get the number of active orders."""
    return MT5.PythonIntegration.orders_total(terminal)


@router.post("/orders_get", response_model=None)
def orders_get(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str | None, Body(embed=True)] = None,
    group: Annotated[str | None, Body(embed=True)] = None,
    ticket: Annotated[int | None, Body(embed=True)] = None,
) -> Any:
    """Get active orders with the ability to filter by symbol or ticket."""
    return MT5.PythonIntegration.orders_get(
        terminal, symbol=symbol, group=group, ticket=ticket
    )


@router.post("/order_calc_margin", response_model=None)
def order_calc_margin(
    terminal: Annotated[str, Body(embed=True)],
    action: Annotated[int, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
    volume: Annotated[float, Body(embed=True)],
    price: Annotated[float, Body(embed=True)],
) -> Any:
    """Return margin in the account currency to perform a specified trading operation."""
    return MT5.PythonIntegration.order_calc_margin(
        terminal, action, symbol, volume, price
    )


@router.post("/order_calc_profit", response_model=None)
def order_calc_profit(
    terminal: Annotated[str, Body(embed=True)],
    action: Annotated[int, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
    volume: Annotated[float, Body(embed=True)],
    price_open: Annotated[float, Body(embed=True)],
    price_close: Annotated[float, Body(embed=True)],
) -> Any:
    """Return profit in the account currency for a specified trading operation."""
    return MT5.PythonIntegration.order_calc_profit(
        terminal, action, symbol, volume, price_open, price_close
    )


@router.post("/order_check", response_model=None)
def order_check(
    terminal: Annotated[str, Body(embed=True)],
    request: Annotated[dict[str, Any], Body(embed=True)],
) -> Any:
    """Check funds sufficiency for performing a required trading operation. Check result are returned as the MqlTradeCheckResult structure."""
    return MT5.PythonIntegration.order_check(terminal, request)


@router.post("/order_send", response_model=None)
def order_send(
    terminal: Annotated[str, Body(embed=True)],
    request: Annotated[dict[str, Any], Body(embed=True)],
) -> Any:
    """Send a request to perform a trading operation from the terminal to the trade server. The function is similar to OrderSend."""
    return MT5.PythonIntegration.order_send(terminal, request)


@router.post("/positions_total", response_model=None)
def positions_total(
    terminal: Annotated[str, Body(embed=True)],
) -> Any:
    """Get the number of open positions."""
    return MT5.PythonIntegration.positions_total(terminal)


@router.post("/positions_get", response_model=None)
def positions_get(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str | None, Body(embed=True)] = None,
    group: Annotated[str | None, Body(embed=True)] = None,
    ticket: Annotated[int | None, Body(embed=True)] = None,
) -> Any:
    """Get open positions with the ability to filter by symbol or ticket."""
    return MT5.PythonIntegration.positions_get(
        terminal, symbol=symbol, group=group, ticket=ticket
    )


@router.post("/history_orders_total", response_model=None)
def history_orders_total(
    terminal: Annotated[str, Body(embed=True)],
    date_from: Annotated[dt.datetime | int, Body(embed=True)],
    date_to: Annotated[dt.datetime | int, Body(embed=True)],
) -> Any:
    """Get the number of orders in trading history within the specified interval."""
    return MT5.PythonIntegration.history_orders_total(terminal, date_from, date_to)


@router.post("/history_orders_get", response_model=None)
def history_orders_get(
    terminal: Annotated[str, Body(embed=True)],
    date_from: Annotated[dt.datetime | int | None, Body(embed=True)] = None,
    date_to: Annotated[dt.datetime | int | None, Body(embed=True)] = None,
    group: Annotated[str | None, Body(embed=True)] = None,
    ticket: Annotated[int | None, Body(embed=True)] = None,
    position: Annotated[int | None, Body(embed=True)] = None,
) -> Any:
    """Get orders from trading history with the ability to filter by ticket or position."""
    return MT5.PythonIntegration.history_orders_get(
        terminal, date_from, date_to, group=group, ticket=ticket, position=position
    )


@router.post("/history_deals_total", response_model=None)
def history_deals_total(
    terminal: Annotated[str, Body(embed=True)],
    date_from: Annotated[dt.datetime | int, Body(embed=True)],
    date_to: Annotated[dt.datetime | int, Body(embed=True)],
) -> Any:
    """Get the number of deals in trading history within the specified interval."""
    return MT5.PythonIntegration.history_deals_total(terminal, date_from, date_to)


@router.post("/history_deals_get", response_model=None)
def history_deals_get(
    terminal: Annotated[str, Body(embed=True)],
    date_from: Annotated[dt.datetime | int | None, Body(embed=True)] = None,
    date_to: Annotated[dt.datetime | int | None, Body(embed=True)] = None,
    group: Annotated[str | None, Body(embed=True)] = None,
    ticket: Annotated[int | None, Body(embed=True)] = None,
    position: Annotated[int | None, Body(embed=True)] = None,
) -> Any:
    """Get deals from trading history within the specified interval with the ability to filter by ticket or position."""
    return MT5.PythonIntegration.history_deals_get(
        terminal, date_from, date_to, group=group, ticket=ticket, position=position
    )
