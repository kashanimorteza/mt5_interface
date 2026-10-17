"""History Adapter of MT5 Group: one Endpoint for every Function of the History group."""

from typing import Annotated

from fastapi import APIRouter, Body
from logic.interface import MT5
from pydantic import JsonValue

from api.endpoints import PlainRoute

router = APIRouter(prefix="/history", tags=["MT5 · History"], route_class=PlainRoute)


@router.post("/history_orders_total")
def history_orders_total(
    terminal: Annotated[str, Body(embed=True)],
    date_from: Annotated[int, Body(embed=True)],
    date_to: Annotated[int, Body(embed=True)],
) -> JsonValue:
    """Return the number of history orders within an interval."""
    return MT5(terminal).History.history_orders_total(
        date_from=date_from, date_to=date_to
    )


@router.post("/history_orders_get")
def history_orders_get(
    terminal: Annotated[str, Body(embed=True)],
    date_from: Annotated[int | None, Body(embed=True)] = None,
    date_to: Annotated[int | None, Body(embed=True)] = None,
    group: Annotated[str | None, Body(embed=True)] = None,
    ticket: Annotated[int | None, Body(embed=True)] = None,
    position: Annotated[int | None, Body(embed=True)] = None,
) -> JsonValue:
    """Return history orders within an interval, or by order or position ticket."""
    return MT5(terminal).History.history_orders_get(
        date_from=date_from,
        date_to=date_to,
        group=group,
        ticket=ticket,
        position=position,
    )


@router.post("/history_deals_total")
def history_deals_total(
    terminal: Annotated[str, Body(embed=True)],
    date_from: Annotated[int, Body(embed=True)],
    date_to: Annotated[int, Body(embed=True)],
) -> JsonValue:
    """Return the number of history deals within an interval."""
    return MT5(terminal).History.history_deals_total(
        date_from=date_from, date_to=date_to
    )


@router.post("/history_deals_get")
def history_deals_get(
    terminal: Annotated[str, Body(embed=True)],
    date_from: Annotated[int | None, Body(embed=True)] = None,
    date_to: Annotated[int | None, Body(embed=True)] = None,
    group: Annotated[str | None, Body(embed=True)] = None,
    ticket: Annotated[int | None, Body(embed=True)] = None,
    position: Annotated[int | None, Body(embed=True)] = None,
) -> JsonValue:
    """Return history deals within an interval, or by order or position ticket."""
    return MT5(terminal).History.history_deals_get(
        date_from=date_from,
        date_to=date_to,
        group=group,
        ticket=ticket,
        position=position,
    )
