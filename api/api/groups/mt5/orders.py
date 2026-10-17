"""Orders Adapter of MT5 Group: one Endpoint for every Function of the Orders group."""

from typing import Annotated

from fastapi import APIRouter, Body
from logic.interface import MT5
from pydantic import JsonValue

from api.endpoints import PlainRoute

router = APIRouter(prefix="/orders", tags=["MT5 · Orders"], route_class=PlainRoute)


@router.post(
    "/orders_total",
    openapi_extra={
        "externalDocs": {
            "description": "orders_total in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5orderstotal_py",
        }
    },
)
def orders_total(
    terminal: Annotated[
        str,
        Body(
            embed=True,
            description="Name of a Terminal in MT5 Service's config.yaml, such as demo.",
            examples=["demo"],
        ),
    ],
) -> JsonValue:
    """Return the number of active orders."""
    return MT5(terminal).Orders.orders_total()


@router.post(
    "/orders_get",
    openapi_extra={
        "externalDocs": {
            "description": "orders_get in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5ordersget_py",
        }
    },
)
def orders_get(
    terminal: Annotated[
        str,
        Body(
            embed=True,
            description="Name of a Terminal in MT5 Service's config.yaml, such as demo.",
            examples=["demo"],
        ),
    ],
    symbol: Annotated[
        str | None,
        Body(
            embed=True,
            description="Financial instrument name, such as EURUSD.",
            examples=["EURUSD"],
        ),
    ] = None,
    group: Annotated[
        str | None,
        Body(
            embed=True,
            description="Filter on symbol names, such as *USD*; several patterns are separated by commas and ! excludes.",
            examples=["*USD*"],
        ),
    ] = None,
    ticket: Annotated[
        int | None,
        Body(
            embed=True,
            description="Ticket of one order, position, or deal.",
            examples=[530218319],
        ),
    ] = None,
) -> JsonValue:
    """Return active orders, optionally filtered by symbol, group, or ticket."""
    return MT5(terminal).Orders.orders_get(symbol=symbol, group=group, ticket=ticket)


@router.post(
    "/order_calc_margin",
    openapi_extra={
        "externalDocs": {
            "description": "order_calc_margin in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5ordercalcmargin_py",
        }
    },
)
def order_calc_margin(
    terminal: Annotated[
        str,
        Body(
            embed=True,
            description="Name of a Terminal in MT5 Service's config.yaml, such as demo.",
            examples=["demo"],
        ),
    ],
    action: Annotated[
        int,
        Body(
            embed=True,
            description="Order type as an ORDER_TYPE_* value from the Constants Endpoint, such as 0 for ORDER_TYPE_BUY.",
            examples=[0],
        ),
    ],
    symbol: Annotated[
        str,
        Body(
            embed=True,
            description="Financial instrument name, such as EURUSD.",
            examples=["EURUSD"],
        ),
    ],
    volume: Annotated[
        float, Body(embed=True, description="Volume in lots.", examples=[0.1])
    ],
    price: Annotated[
        float, Body(embed=True, description="Open price.", examples=[1.085])
    ],
) -> JsonValue:
    """Return the margin in account currency for a trading operation."""
    return MT5(terminal).Orders.order_calc_margin(
        action=action, symbol=symbol, volume=volume, price=price
    )


@router.post(
    "/order_calc_profit",
    openapi_extra={
        "externalDocs": {
            "description": "order_calc_profit in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5ordercalcprofit_py",
        }
    },
)
def order_calc_profit(
    terminal: Annotated[
        str,
        Body(
            embed=True,
            description="Name of a Terminal in MT5 Service's config.yaml, such as demo.",
            examples=["demo"],
        ),
    ],
    action: Annotated[
        int,
        Body(
            embed=True,
            description="Order type as an ORDER_TYPE_* value from the Constants Endpoint, such as 0 for ORDER_TYPE_BUY.",
            examples=[0],
        ),
    ],
    symbol: Annotated[
        str,
        Body(
            embed=True,
            description="Financial instrument name, such as EURUSD.",
            examples=["EURUSD"],
        ),
    ],
    volume: Annotated[
        float, Body(embed=True, description="Volume in lots.", examples=[0.1])
    ],
    price_open: Annotated[
        float, Body(embed=True, description="Open price.", examples=[1.085])
    ],
    price_close: Annotated[
        float, Body(embed=True, description="Close price.", examples=[1.09])
    ],
) -> JsonValue:
    """Return the profit in account currency for a trading operation."""
    return MT5(terminal).Orders.order_calc_profit(
        action=action,
        symbol=symbol,
        volume=volume,
        price_open=price_open,
        price_close=price_close,
    )


@router.post(
    "/order_check",
    openapi_extra={
        "externalDocs": {
            "description": "order_check in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5ordercheck_py",
        }
    },
)
def order_check(
    terminal: Annotated[
        str,
        Body(
            embed=True,
            description="Name of a Terminal in MT5 Service's config.yaml, such as demo.",
            examples=["demo"],
        ),
    ],
    request: Annotated[
        dict[str, JsonValue],
        Body(
            embed=True,
            description="Trade request object with the fields of the MqlTradeRequest structure; enumerated values come from the Constants Endpoint.",
            examples=[
                {
                    "action": 1,
                    "symbol": "EURUSD",
                    "volume": 0.1,
                    "type": 0,
                    "price": 1.085,
                }
            ],
        ),
    ],
) -> JsonValue:
    """Check funds sufficiency for a trade request."""
    return MT5(terminal).Orders.order_check(request=request)


@router.post(
    "/order_send",
    openapi_extra={
        "externalDocs": {
            "description": "order_send in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5ordersend_py",
        }
    },
)
def order_send(
    terminal: Annotated[
        str,
        Body(
            embed=True,
            description="Name of a Terminal in MT5 Service's config.yaml, such as demo.",
            examples=["demo"],
        ),
    ],
    request: Annotated[
        dict[str, JsonValue],
        Body(
            embed=True,
            description="Trade request object with the fields of the MqlTradeRequest structure; enumerated values come from the Constants Endpoint.",
            examples=[
                {
                    "action": 1,
                    "symbol": "EURUSD",
                    "volume": 0.1,
                    "type": 0,
                    "price": 1.085,
                }
            ],
        ),
    ],
) -> JsonValue:
    """Send a trade request to the trade server."""
    return MT5(terminal).Orders.order_send(request=request)
