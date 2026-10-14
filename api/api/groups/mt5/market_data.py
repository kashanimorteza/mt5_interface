"""The market_data Adapter: one Endpoint for every Function of the MarketData Function Group."""

from typing import Annotated, Any

from fastapi import APIRouter, Body
from logic.interface import MT5

from api import endpoints

router = APIRouter(
    prefix="/market_data",
    tags=["MT5 · market_data"],
    route_class=endpoints.ResultRoute,
)


@router.post("/copy_rates_from", response_model=None)
def copy_rates_from(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
    timeframe: Annotated[int, Body(embed=True)],
    date_from: Annotated[int, Body(embed=True)],
    count: Annotated[int, Body(embed=True)],
) -> Any:
    """Get bars from the MetaTrader 5 terminal starting from the specified date."""
    return MT5.MarketData.copy_rates_from(terminal, symbol, timeframe, date_from, count)


@router.post("/copy_rates_from_pos", response_model=None)
def copy_rates_from_pos(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
    timeframe: Annotated[int, Body(embed=True)],
    start_pos: Annotated[int, Body(embed=True)],
    count: Annotated[int, Body(embed=True)],
) -> Any:
    """Get bars from the MetaTrader 5 terminal starting from the specified index."""
    return MT5.MarketData.copy_rates_from_pos(
        terminal, symbol, timeframe, start_pos, count
    )


@router.post("/copy_rates_range", response_model=None)
def copy_rates_range(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
    timeframe: Annotated[int, Body(embed=True)],
    date_from: Annotated[int, Body(embed=True)],
    date_to: Annotated[int, Body(embed=True)],
) -> Any:
    """Get bars in the specified date range from the MetaTrader 5 terminal."""
    return MT5.MarketData.copy_rates_range(
        terminal, symbol, timeframe, date_from, date_to
    )


@router.post("/copy_ticks_from", response_model=None)
def copy_ticks_from(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
    date_from: Annotated[int, Body(embed=True)],
    count: Annotated[int, Body(embed=True)],
    flags: Annotated[int, Body(embed=True)],
) -> Any:
    """Get ticks from the MetaTrader 5 terminal starting from the specified date."""
    return MT5.MarketData.copy_ticks_from(terminal, symbol, date_from, count, flags)


@router.post("/copy_ticks_range", response_model=None)
def copy_ticks_range(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
    date_from: Annotated[int, Body(embed=True)],
    date_to: Annotated[int, Body(embed=True)],
    flags: Annotated[int, Body(embed=True)],
) -> Any:
    """Get ticks for the specified date range from the MetaTrader 5 terminal."""
    return MT5.MarketData.copy_ticks_range(terminal, symbol, date_from, date_to, flags)
