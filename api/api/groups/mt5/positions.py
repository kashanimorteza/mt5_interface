"""Positions Adapter of MT5 Group: one Endpoint for every Function of the Positions group."""

from typing import Annotated

from fastapi import APIRouter, Body
from logic.interface import MT5
from pydantic import JsonValue

from api.endpoints import PlainRoute

router = APIRouter(
    prefix="/positions", tags=["MT5 · Positions"], route_class=PlainRoute
)


@router.post("/positions_total")
def positions_total(terminal: Annotated[str, Body(embed=True)]) -> JsonValue:
    """Return the number of open positions."""
    return MT5(terminal).Positions.positions_total()


@router.post("/positions_get")
def positions_get(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str | None, Body(embed=True)] = None,
    group: Annotated[str | None, Body(embed=True)] = None,
    ticket: Annotated[int | None, Body(embed=True)] = None,
) -> JsonValue:
    """Return open positions, optionally filtered by symbol, group, or ticket."""
    return MT5(terminal).Positions.positions_get(
        symbol=symbol, group=group, ticket=ticket
    )
