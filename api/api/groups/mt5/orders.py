"""Orders Adapter of MT5 Group: one Endpoint for every Function of the Orders group."""

from typing import Annotated

from fastapi import APIRouter, Body
from logic.interface import MT5
from pydantic import JsonValue

from api.endpoints import PlainRoute

router = APIRouter(prefix="/orders", tags=["MT5 · Orders"], route_class=PlainRoute)


@router.post("/orders_total")
def orders_total(terminal: Annotated[str, Body(embed=True)]) -> JsonValue:
    """Return the number of active orders."""
    return MT5(terminal).Orders.orders_total()


@router.post("/orders_get")
def orders_get(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str | None, Body(embed=True)] = None,
    group: Annotated[str | None, Body(embed=True)] = None,
    ticket: Annotated[int | None, Body(embed=True)] = None,
) -> JsonValue:
    """Return active orders, optionally filtered by symbol, group, or ticket."""
    return MT5(terminal).Orders.orders_get(symbol=symbol, group=group, ticket=ticket)


@router.post("/order_calc_margin")
def order_calc_margin(
    terminal: Annotated[str, Body(embed=True)],
    action: Annotated[int, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
    volume: Annotated[float, Body(embed=True)],
    price: Annotated[float, Body(embed=True)],
) -> JsonValue:
    """Return the margin in account currency for a trading operation."""
    return MT5(terminal).Orders.order_calc_margin(
        action=action, symbol=symbol, volume=volume, price=price
    )


@router.post("/order_calc_profit")
def order_calc_profit(
    terminal: Annotated[str, Body(embed=True)],
    action: Annotated[int, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
    volume: Annotated[float, Body(embed=True)],
    price_open: Annotated[float, Body(embed=True)],
    price_close: Annotated[float, Body(embed=True)],
) -> JsonValue:
    """Return the profit in account currency for a trading operation."""
    return MT5(terminal).Orders.order_calc_profit(
        action=action,
        symbol=symbol,
        volume=volume,
        price_open=price_open,
        price_close=price_close,
    )


@router.post("/order_check")
def order_check(
    terminal: Annotated[str, Body(embed=True)],
    request: Annotated[dict[str, JsonValue], Body(embed=True)],
) -> JsonValue:
    """Check funds sufficiency for a trade request."""
    return MT5(terminal).Orders.order_check(request=request)


@router.post("/order_send")
def order_send(
    terminal: Annotated[str, Body(embed=True)],
    request: Annotated[dict[str, JsonValue], Body(embed=True)],
) -> JsonValue:
    """Send a trade request to the trade server."""
    return MT5(terminal).Orders.order_send(request=request)
