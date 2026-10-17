"""Positions Adapter of MT5 Group: one Endpoint for every Function of the Positions group."""

from typing import Annotated

from fastapi import APIRouter, Body
from logic.interface import MT5
from pydantic import JsonValue

from api.endpoints import PlainRoute

router = APIRouter(
    prefix="/positions", tags=["MT5 · Positions"], route_class=PlainRoute
)


@router.post(
    "/positions_total",
    openapi_extra={
        "externalDocs": {
            "description": "positions_total in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5positionstotal_py",
        }
    },
)
def positions_total(
    terminal: Annotated[
        str,
        Body(
            embed=True,
            description="Name of a Terminal in MT5 Service's config.yaml, such as demo.",
            examples=["demo"],
        ),
    ],
) -> JsonValue:
    """Return the number of open positions."""
    return MT5(terminal).Positions.positions_total()


@router.post(
    "/positions_get",
    openapi_extra={
        "externalDocs": {
            "description": "positions_get in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5positionsget_py",
        }
    },
)
def positions_get(
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
    """Return open positions, optionally filtered by symbol, group, or ticket."""
    return MT5(terminal).Positions.positions_get(
        symbol=symbol, group=group, ticket=ticket
    )
