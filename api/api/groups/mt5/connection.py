"""Connection Adapter of MT5 Group: one Endpoint for every Function of the Connection group."""

from typing import Annotated

from fastapi import APIRouter, Body
from logic.interface import MT5
from pydantic import JsonValue

from api.endpoints import PlainRoute

router = APIRouter(
    prefix="/connection", tags=["MT5 · Connection"], route_class=PlainRoute
)


@router.post(
    "/initialize",
    openapi_extra={
        "externalDocs": {
            "description": "initialize in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5initialize_py",
        }
    },
)
def initialize(
    terminal: Annotated[
        str,
        Body(
            embed=True,
            description="Name of a Terminal in MT5 Service's config.yaml, such as demo.",
            examples=["demo"],
        ),
    ],
    path: Annotated[
        str | None,
        Body(
            embed=True,
            description="Path of the terminal executable; it must match the Terminal's path in config.yaml and may be left out.",
        ),
    ] = None,
    login: Annotated[
        int | None,
        Body(embed=True, description="Trading account number.", examples=[25115284]),
    ] = None,
    password: Annotated[
        str | None,
        Body(
            embed=True, description="Trading account password.", examples=["password"]
        ),
    ] = None,
    server: Annotated[
        str | None,
        Body(
            embed=True,
            description="Trade server name, as shown in the terminal.",
            examples=["MetaQuotes-Demo"],
        ),
    ] = None,
    timeout: Annotated[
        int | None,
        Body(
            embed=True,
            description="Connection timeout in milliseconds.",
            examples=[60000],
        ),
    ] = None,
    portable: Annotated[
        bool,
        Body(
            embed=True,
            description="Start the terminal in portable mode.",
            examples=[False],
        ),
    ] = False,
) -> JsonValue:
    """Establish a connection with the Terminal, starting its Terminal Process."""
    return MT5(terminal).Connection.initialize(
        path=path,
        login=login,
        password=password,
        server=server,
        timeout=timeout,
        portable=portable,
    )


@router.post(
    "/login",
    openapi_extra={
        "externalDocs": {
            "description": "login in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5login_py",
        }
    },
)
def login(
    terminal: Annotated[
        str,
        Body(
            embed=True,
            description="Name of a Terminal in MT5 Service's config.yaml, such as demo.",
            examples=["demo"],
        ),
    ],
    login: Annotated[
        int,
        Body(embed=True, description="Trading account number.", examples=[25115284]),
    ],
    password: Annotated[
        str | None,
        Body(
            embed=True, description="Trading account password.", examples=["password"]
        ),
    ] = None,
    server: Annotated[
        str | None,
        Body(
            embed=True,
            description="Trade server name, as shown in the terminal.",
            examples=["MetaQuotes-Demo"],
        ),
    ] = None,
    timeout: Annotated[
        int | None,
        Body(
            embed=True,
            description="Connection timeout in milliseconds.",
            examples=[60000],
        ),
    ] = None,
) -> JsonValue:
    """Connect to a trading account."""
    return MT5(terminal).Connection.login(
        login=login, password=password, server=server, timeout=timeout
    )


@router.post(
    "/shutdown",
    openapi_extra={
        "externalDocs": {
            "description": "shutdown in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5shutdown_py",
        }
    },
)
def shutdown(
    terminal: Annotated[
        str,
        Body(
            embed=True,
            description="Name of a Terminal in MT5 Service's config.yaml, such as demo.",
            examples=["demo"],
        ),
    ],
) -> JsonValue:
    """Close the connection to the Terminal and end its Terminal Process."""
    return MT5(terminal).Connection.shutdown()


@router.post(
    "/version",
    openapi_extra={
        "externalDocs": {
            "description": "version in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5version_py",
        }
    },
)
def version(
    terminal: Annotated[
        str,
        Body(
            embed=True,
            description="Name of a Terminal in MT5 Service's config.yaml, such as demo.",
            examples=["demo"],
        ),
    ],
) -> JsonValue:
    """Return the Terminal version, build, and release date as a Timestamp."""
    return MT5(terminal).Connection.version()


@router.post(
    "/last_error",
    openapi_extra={
        "externalDocs": {
            "description": "last_error in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5lasterror_py",
        }
    },
)
def last_error(
    terminal: Annotated[
        str,
        Body(
            embed=True,
            description="Name of a Terminal in MT5 Service's config.yaml, such as demo.",
            examples=["demo"],
        ),
    ],
) -> JsonValue:
    """Return the last error code and description."""
    return MT5(terminal).Connection.last_error()


@router.post(
    "/account_info",
    openapi_extra={
        "externalDocs": {
            "description": "account_info in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5accountinfo_py",
        }
    },
)
def account_info(
    terminal: Annotated[
        str,
        Body(
            embed=True,
            description="Name of a Terminal in MT5 Service's config.yaml, such as demo.",
            examples=["demo"],
        ),
    ],
) -> JsonValue:
    """Return info on the current trading account."""
    return MT5(terminal).Connection.account_info()


@router.post(
    "/terminal_info",
    openapi_extra={
        "externalDocs": {
            "description": "terminal_info in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5terminalinfo_py",
        }
    },
)
def terminal_info(
    terminal: Annotated[
        str,
        Body(
            embed=True,
            description="Name of a Terminal in MT5 Service's config.yaml, such as demo.",
            examples=["demo"],
        ),
    ],
) -> JsonValue:
    """Return the Terminal status and settings."""
    return MT5(terminal).Connection.terminal_info()
