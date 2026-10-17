"""MarketData Adapter of MT5 Group: one Endpoint for every Function of the MarketData group."""

from typing import Annotated

from fastapi import APIRouter, Body
from logic.interface import MT5
from pydantic import JsonValue

from api.endpoints import PlainRoute

router = APIRouter(
    prefix="/market_data", tags=["MT5 · MarketData"], route_class=PlainRoute
)


@router.post("/copy_rates_from")
def copy_rates_from(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
    timeframe: Annotated[int, Body(embed=True)],
    date_from: Annotated[int, Body(embed=True)],
    count: Annotated[int, Body(embed=True)],
) -> JsonValue:
    """Return bars starting from a date."""
    return MT5(terminal).MarketData.copy_rates_from(
        symbol=symbol, timeframe=timeframe, date_from=date_from, count=count
    )


@router.post("/copy_rates_from_pos")
def copy_rates_from_pos(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
    timeframe: Annotated[int, Body(embed=True)],
    start_pos: Annotated[int, Body(embed=True)],
    count: Annotated[int, Body(embed=True)],
) -> JsonValue:
    """Return bars starting from a bar index."""
    return MT5(terminal).MarketData.copy_rates_from_pos(
        symbol=symbol, timeframe=timeframe, start_pos=start_pos, count=count
    )


@router.post("/copy_rates_range")
def copy_rates_range(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
    timeframe: Annotated[int, Body(embed=True)],
    date_from: Annotated[int, Body(embed=True)],
    date_to: Annotated[int, Body(embed=True)],
) -> JsonValue:
    """Return bars within a date range."""
    return MT5(terminal).MarketData.copy_rates_range(
        symbol=symbol, timeframe=timeframe, date_from=date_from, date_to=date_to
    )


@router.post("/copy_ticks_from")
def copy_ticks_from(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
    date_from: Annotated[int, Body(embed=True)],
    count: Annotated[int, Body(embed=True)],
    flags: Annotated[int, Body(embed=True)],
) -> JsonValue:
    """Return ticks starting from a date."""
    return MT5(terminal).MarketData.copy_ticks_from(
        symbol=symbol, date_from=date_from, count=count, flags=flags
    )


@router.post("/copy_ticks_range")
def copy_ticks_range(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
    date_from: Annotated[int, Body(embed=True)],
    date_to: Annotated[int, Body(embed=True)],
    flags: Annotated[int, Body(embed=True)],
) -> JsonValue:
    """Return ticks within a date range."""
    return MT5(terminal).MarketData.copy_ticks_range(
        symbol=symbol, date_from=date_from, date_to=date_to, flags=flags
    )
