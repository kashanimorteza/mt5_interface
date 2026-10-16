"""Symbols Adapter of MT5 Group: one Endpoint for every Function of the Symbols group."""

from typing import Annotated

from fastapi import APIRouter, Body
from logic.interface import MT5
from pydantic import JsonValue

router = APIRouter(prefix="/symbols", tags=["MT5 · Symbols"])


@router.post("/symbols_total")
def symbols_total(terminal: Annotated[str, Body(embed=True)]) -> JsonValue:
    """Return the number of all financial instruments."""
    return MT5.MT5(terminal).Symbols.symbols_total()


@router.post("/symbols_get")
def symbols_get(
    terminal: Annotated[str, Body(embed=True)],
    group: Annotated[str | None, Body(embed=True)] = None,
) -> JsonValue:
    """Return all financial instruments, optionally filtered by group."""
    return MT5.MT5(terminal).Symbols.symbols_get(group=group)


@router.post("/symbol_info")
def symbol_info(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
) -> JsonValue:
    """Return data on a financial instrument."""
    return MT5.MT5(terminal).Symbols.symbol_info(symbol=symbol)


@router.post("/symbol_info_tick")
def symbol_info_tick(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
) -> JsonValue:
    """Return the last tick of a financial instrument."""
    return MT5.MT5(terminal).Symbols.symbol_info_tick(symbol=symbol)


@router.post("/symbol_select")
def symbol_select(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
    enable: Annotated[bool | None, Body(embed=True)] = None,
) -> JsonValue:
    """Select a symbol in MarketWatch, or remove it when enable is False."""
    return MT5.MT5(terminal).Symbols.symbol_select(symbol=symbol, enable=enable)
