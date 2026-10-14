"""The connection Adapter: one Endpoint for every Function of the Connection Function Group."""

from typing import Annotated, Any

from fastapi import APIRouter, Body
from logic.interface import MT5

from api import endpoints

router = APIRouter(
    prefix="/connection",
    tags=["MT5 · connection"],
    route_class=endpoints.ResultRoute,
)


@router.post("/initialize", response_model=None)
def initialize(
    terminal: Annotated[str, Body(embed=True)],
    path: Annotated[str | None, Body(embed=True)] = None,
    login: Annotated[int | None, Body(embed=True)] = None,
    password: Annotated[str | None, Body(embed=True)] = None,
    server: Annotated[str | None, Body(embed=True)] = None,
    timeout: Annotated[int | None, Body(embed=True)] = None,
    portable: Annotated[bool, Body(embed=True)] = False,
) -> Any:
    """Establish a connection with the MetaTrader 5 terminal."""
    return MT5.Connection.initialize(
        terminal,
        path,
        login=login,
        password=password,
        server=server,
        timeout=timeout,
        portable=portable,
    )


@router.post("/login", response_model=None)
def login(
    terminal: Annotated[str, Body(embed=True)],
    login: Annotated[int, Body(embed=True)],
    password: Annotated[str | None, Body(embed=True)] = None,
    server: Annotated[str | None, Body(embed=True)] = None,
    timeout: Annotated[int | None, Body(embed=True)] = None,
) -> Any:
    """Connect to a trading account using specified parameters."""
    return MT5.Connection.login(
        terminal, login, password=password, server=server, timeout=timeout
    )


@router.post("/shutdown", response_model=None)
def shutdown(
    terminal: Annotated[str, Body(embed=True)],
) -> Any:
    """Close the previously established connection to the MetaTrader 5 terminal."""
    return MT5.Connection.shutdown(terminal)


@router.post("/version", response_model=None)
def version(
    terminal: Annotated[str, Body(embed=True)],
) -> Any:
    """Return the MetaTrader 5 terminal version."""
    return MT5.Connection.version(terminal)


@router.post("/last_error", response_model=None)
def last_error(
    terminal: Annotated[str, Body(embed=True)],
) -> Any:
    """Return data on the last error."""
    return MT5.Connection.last_error(terminal)


@router.post("/account_info", response_model=None)
def account_info(
    terminal: Annotated[str, Body(embed=True)],
) -> Any:
    """Get info on the current trading account."""
    return MT5.Connection.account_info(terminal)


@router.post("/terminal_info", response_model=None)
def terminal_info(
    terminal: Annotated[str, Body(embed=True)],
) -> Any:
    """Get the connected MetaTrader 5 client terminal status and settings."""
    return MT5.Connection.terminal_info(terminal)
