"""The symbols Adapter: one Endpoint for every Function of the Symbols Function Group."""

from typing import Annotated, Any

from fastapi import APIRouter, Body
from logic.interface import MT5

from api import endpoints

router = APIRouter(
    prefix="/symbols",
    tags=["MT5 · symbols"],
    route_class=endpoints.ResultRoute,
)


@router.post("/symbols_total", response_model=None)
def symbols_total(
    terminal: Annotated[str, Body(embed=True)],
) -> Any:
    """Get the number of all financial instruments in the MetaTrader 5 terminal."""
    return MT5.Symbols.symbols_total(terminal)


@router.post("/symbols_get", response_model=None)
def symbols_get(
    terminal: Annotated[str, Body(embed=True)],
    group: Annotated[str | None, Body(embed=True)] = None,
) -> Any:
    """Get all financial instruments from the MetaTrader 5 terminal."""
    return MT5.Symbols.symbols_get(terminal, group)


@router.post("/symbol_info", response_model=None)
def symbol_info(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
) -> Any:
    """Get data on the specified financial instrument."""
    return MT5.Symbols.symbol_info(terminal, symbol)


@router.post("/symbol_info_tick", response_model=None)
def symbol_info_tick(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
) -> Any:
    """Get the last tick for the specified financial instrument."""
    return MT5.Symbols.symbol_info_tick(terminal, symbol)


@router.post("/symbol_select", response_model=None)
def symbol_select(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
    enable: Annotated[bool | None, Body(embed=True)] = None,
) -> Any:
    """Select a symbol in the MarketWatch window or remove a symbol from the window."""
    return MT5.Symbols.symbol_select(terminal, symbol, enable)
