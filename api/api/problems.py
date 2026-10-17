"""Problem Details of API: every Endpoint error sent as RFC 9457 application/problem+json."""

from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

INVALID_INPUT = 422
UNNAMED = 500

STATUS_BY_NAME: dict[str, int] = {}
"""The status of every error the error table names by its name alone."""

STATUS_BY_CODE: dict[str, dict[int, int]] = {
    "MT5Error": {-2: INVALID_INPUT, -10005: 504},
}
"""The status of every error the error table names by its name and code."""


def status_of(error: Exception) -> int:
    """Return the status the error table sets for an error, by its name and code when it carries one."""
    kind = type(error).__name__
    code = getattr(error, "code", None)
    if isinstance(code, int) and code in STATUS_BY_CODE.get(kind, {}):
        return STATUS_BY_CODE[kind][code]
    return STATUS_BY_NAME.get(kind, UNNAMED)


def problem(error: Exception, status: int, detail: object) -> JSONResponse:
    """Send an error as Problem Details whose type is the error's class name."""
    kind = type(error).__name__
    return JSONResponse(
        {
            "type": kind,
            "title": kind,
            "status": status,
            "detail": jsonable_encoder(detail),
        },
        status_code=status,
        media_type="application/problem+json",
    )


async def invalid_input(request: Request, error: Exception) -> Response:
    """Send a request that does not match its Endpoint's Parameters as Invalid Input."""
    assert isinstance(error, RequestValidationError)
    return problem(error, INVALID_INPUT, error.errors())


async def http_error(request: Request, error: Exception) -> Response:
    """Send an HTTP error raised while routing with its own status."""
    assert isinstance(error, HTTPException)
    return problem(error, error.status_code, error.detail)


async def every_error(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """Send any other error, such as MT5Error, with the status the error table sets for it."""
    try:
        return await call_next(request)
    except Exception as error:  # noqa: BLE001 - every error must reach the client as Problem Details
        return problem(error, status_of(error), str(error))


def install(app: FastAPI) -> None:
    """Send every error of the API as Problem Details."""
    app.add_exception_handler(RequestValidationError, invalid_input)
    app.add_exception_handler(HTTPException, http_error)
    app.middleware("http")(every_error)
