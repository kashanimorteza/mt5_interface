"""Connection Adapter of MT5 Group: one Endpoint for every Function of the Connection group."""

from typing import Annotated

from fastapi import APIRouter, Body
from logic.interface import MT5
from pydantic import JsonValue

router = APIRouter(prefix="/connection", tags=["MT5 · Connection"])


@router.post("/initialize")
def initialize(
    terminal: Annotated[str, Body(embed=True)],
    path: Annotated[str | None, Body(embed=True)] = None,
    login: Annotated[int | None, Body(embed=True)] = None,
    password: Annotated[str | None, Body(embed=True)] = None,
    server: Annotated[str | None, Body(embed=True)] = None,
    timeout: Annotated[int | None, Body(embed=True)] = None,
    portable: Annotated[bool, Body(embed=True)] = False,
) -> JsonValue:
    """Establish a connection with the Terminal, starting its Terminal Process."""
    return MT5.MT5(terminal).Connection.initialize(
        path=path,
        login=login,
        password=password,
        server=server,
        timeout=timeout,
        portable=portable,
    )


@router.post("/login")
def login(
    terminal: Annotated[str, Body(embed=True)],
    login: Annotated[int, Body(embed=True)],
    password: Annotated[str | None, Body(embed=True)] = None,
    server: Annotated[str | None, Body(embed=True)] = None,
    timeout: Annotated[int | None, Body(embed=True)] = None,
) -> JsonValue:
    """Connect to a trading account."""
    return MT5.MT5(terminal).Connection.login(
        login=login, password=password, server=server, timeout=timeout
    )


@router.post("/shutdown")
def shutdown(terminal: Annotated[str, Body(embed=True)]) -> JsonValue:
    """Close the connection to the Terminal and end its Terminal Process."""
    return MT5.MT5(terminal).Connection.shutdown()


@router.post("/version")
def version(terminal: Annotated[str, Body(embed=True)]) -> JsonValue:
    """Return the Terminal version, build, and release date as a Timestamp."""
    return MT5.MT5(terminal).Connection.version()


@router.post("/last_error")
def last_error(terminal: Annotated[str, Body(embed=True)]) -> JsonValue:
    """Return the last error code and description."""
    return MT5.MT5(terminal).Connection.last_error()


@router.post("/account_info")
def account_info(terminal: Annotated[str, Body(embed=True)]) -> JsonValue:
    """Return info on the current trading account."""
    return MT5.MT5(terminal).Connection.account_info()


@router.post("/terminal_info")
def terminal_info(terminal: Annotated[str, Body(embed=True)]) -> JsonValue:
    """Return the Terminal status and settings."""
    return MT5.MT5(terminal).Connection.terminal_info()
