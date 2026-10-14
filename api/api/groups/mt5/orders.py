"""The orders Adapter: one Endpoint for every Function of the Orders Function Group."""

from typing import Annotated, Any

from fastapi import APIRouter, Body
from logic.interface import MT5

from api import endpoints

router = APIRouter(
    prefix="/orders",
    tags=["MT5 · orders"],
    route_class=endpoints.ResultRoute,
)


@router.post("/orders_total", response_model=None)
def orders_total(
    terminal: Annotated[str, Body(embed=True)],
) -> Any:
    """Get the number of active orders."""
    return MT5.Orders.orders_total(terminal)


@router.post("/orders_get", response_model=None)
def orders_get(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str | None, Body(embed=True)] = None,
    group: Annotated[str | None, Body(embed=True)] = None,
    ticket: Annotated[int | None, Body(embed=True)] = None,
) -> Any:
    """Get active orders with the ability to filter by symbol or ticket."""
    return MT5.Orders.orders_get(terminal, symbol=symbol, group=group, ticket=ticket)


@router.post("/order_calc_margin", response_model=None)
def order_calc_margin(
    terminal: Annotated[str, Body(embed=True)],
    action: Annotated[int, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
    volume: Annotated[float, Body(embed=True)],
    price: Annotated[float, Body(embed=True)],
) -> Any:
    """Return margin in the account currency to perform a specified trading operation."""
    return MT5.Orders.order_calc_margin(terminal, action, symbol, volume, price)


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
    return MT5.Orders.order_calc_profit(
        terminal, action, symbol, volume, price_open, price_close
    )


@router.post("/order_check", response_model=None)
def order_check(
    terminal: Annotated[str, Body(embed=True)],
    request: Annotated[dict[str, Any], Body(embed=True)],
) -> Any:
    """Check funds sufficiency for performing a required trading operation. Check result are returned as the MqlTradeCheckResult structure."""
    return MT5.Orders.order_check(terminal, request)


@router.post("/order_send", response_model=None)
def order_send(
    terminal: Annotated[str, Body(embed=True)],
    request: Annotated[dict[str, Any], Body(embed=True)],
) -> Any:
    """Send a request to perform a trading operation from the terminal to the trade server. The function is similar to OrderSend."""
    return MT5.Orders.order_send(terminal, request)
