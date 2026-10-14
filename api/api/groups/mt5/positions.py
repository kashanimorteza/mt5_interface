"""The positions Adapter: one Endpoint for every Function of the Positions Function Group."""

from typing import Annotated, Any

from fastapi import APIRouter, Body
from logic.interface import MT5

from api import endpoints

router = APIRouter(
    prefix="/positions",
    tags=["MT5 · positions"],
    route_class=endpoints.ResultRoute,
)


@router.post("/positions_total", response_model=None)
def positions_total(
    terminal: Annotated[str, Body(embed=True)],
) -> Any:
    """Get the number of open positions."""
    return MT5.Positions.positions_total(terminal)


@router.post("/positions_get", response_model=None)
def positions_get(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str | None, Body(embed=True)] = None,
    group: Annotated[str | None, Body(embed=True)] = None,
    ticket: Annotated[int | None, Body(embed=True)] = None,
) -> Any:
    """Get open positions with the ability to filter by symbol or ticket."""
    return MT5.Positions.positions_get(
        terminal, symbol=symbol, group=group, ticket=ticket
    )
