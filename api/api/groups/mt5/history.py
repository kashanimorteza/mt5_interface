"""The history Adapter: one Endpoint for every Function of the History Function Group."""

from typing import Annotated, Any

from fastapi import APIRouter, Body
from logic.interface import MT5

from api import endpoints

router = APIRouter(
    prefix="/history",
    tags=["MT5 · history"],
    route_class=endpoints.ResultRoute,
)


@router.post("/history_orders_total", response_model=None)
def history_orders_total(
    terminal: Annotated[str, Body(embed=True)],
    date_from: Annotated[int, Body(embed=True)],
    date_to: Annotated[int, Body(embed=True)],
) -> Any:
    """Get the number of orders in trading history within the specified interval."""
    return MT5.History.history_orders_total(terminal, date_from, date_to)


@router.post("/history_orders_get", response_model=None)
def history_orders_get(
    terminal: Annotated[str, Body(embed=True)],
    date_from: Annotated[int | None, Body(embed=True)] = None,
    date_to: Annotated[int | None, Body(embed=True)] = None,
    group: Annotated[str | None, Body(embed=True)] = None,
    ticket: Annotated[int | None, Body(embed=True)] = None,
    position: Annotated[int | None, Body(embed=True)] = None,
) -> Any:
    """Get orders from trading history with the ability to filter by ticket or position."""
    return MT5.History.history_orders_get(
        terminal, date_from, date_to, group=group, ticket=ticket, position=position
    )


@router.post("/history_deals_total", response_model=None)
def history_deals_total(
    terminal: Annotated[str, Body(embed=True)],
    date_from: Annotated[int, Body(embed=True)],
    date_to: Annotated[int, Body(embed=True)],
) -> Any:
    """Get the number of deals in trading history within the specified interval."""
    return MT5.History.history_deals_total(terminal, date_from, date_to)


@router.post("/history_deals_get", response_model=None)
def history_deals_get(
    terminal: Annotated[str, Body(embed=True)],
    date_from: Annotated[int | None, Body(embed=True)] = None,
    date_to: Annotated[int | None, Body(embed=True)] = None,
    group: Annotated[str | None, Body(embed=True)] = None,
    ticket: Annotated[int | None, Body(embed=True)] = None,
    position: Annotated[int | None, Body(embed=True)] = None,
) -> Any:
    """Get deals from trading history within the specified interval with the ability to filter by ticket or position."""
    return MT5.History.history_deals_get(
        terminal, date_from, date_to, group=group, ticket=ticket, position=position
    )
