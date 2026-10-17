"""Endpoints of API: the common rules every Group's Endpoints follow when they send a result or an error.

Every error is sent as RFC 9457 application/problem+json.
"""

import functools
from collections.abc import Awaitable, Callable
from typing import Any

from fastapi import FastAPI, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from pydantic import BaseModel, JsonValue
from starlette.exceptions import HTTPException

INVALID_INPUT = 422
UNNAMED = 500

STATUS_BY_NAME: dict[str, int] = {}
"""The status of every error the error table names by its name alone."""

STATUS_BY_CODE: dict[str, dict[int, int]] = {
    "MT5Error": {-2: INVALID_INPUT, -10005: 504},
}
"""The status of every error the error table names by its name and code."""


class Problem(BaseModel):
    """RFC 9457 Problem Details, the shape of every error API sends."""

    type: str
    title: str
    status: int
    code: int | None = None
    detail: JsonValue


PROBLEM_SCHEMA = {"$ref": "#/components/schemas/Problem"}
"""The reference to Problem Details, declared for every error response."""


def components() -> dict[str, object]:
    """Return the schema of Problem Details and the schemas it refers to, for the API description."""
    schema = Problem.model_json_schema(ref_template="#/components/schemas/{model}")
    found: dict[str, object] = dict(schema.pop("$defs", {}))
    found["Problem"] = schema
    return found


RESPONSES: dict[int | str, dict[str, object]] = {
    INVALID_INPUT: {
        "description": "Invalid input: the request does not match the Endpoint's Parameters, or the source refused it, such as an unknown Terminal (MT5Error code -2).",
        "content": {"application/problem+json": {"schema": PROBLEM_SCHEMA}},
    },
    504: {
        "description": "The Terminal did not answer within its call timeout (MT5Error code -10005).",
        "content": {"application/problem+json": {"schema": PROBLEM_SCHEMA}},
    },
    UNNAMED: {
        "description": "Any other failure the source reports, with its code and message in detail.",
        "content": {"application/problem+json": {"schema": PROBLEM_SCHEMA}},
    },
}
"""Every error response, as Problem Details, under every status the error table can produce."""


def status_of(error: Exception) -> int:
    """Return the status the error table sets for an error, by its name and code when it carries one."""
    kind = type(error).__name__
    code = getattr(error, "code", None)
    if isinstance(code, int) and code in STATUS_BY_CODE.get(kind, {}):
        return STATUS_BY_CODE[kind][code]
    return STATUS_BY_NAME.get(kind, UNNAMED)


def problem(error: Exception, status: int, detail: object) -> JSONResponse:
    """Send an error as Problem Details whose type is the error's class name, with its code when it has one."""
    kind = type(error).__name__
    body: dict[str, object] = {"type": kind, "title": kind, "status": status}
    code = getattr(error, "code", None)
    if isinstance(code, int) and not isinstance(code, bool):
        body["code"] = code
        detail = getattr(error, "message", detail)
    body["detail"] = jsonable_encoder(detail)
    return JSONResponse(
        body,
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


class PlainRoute(APIRoute):
    """Send a Handler's result as JSON directly, without validating it again.

    The source already guarantees that every result is a JSON value, so a large result, such as many
    ticks, is not checked a second time before it is sent.
    """

    def __init__(self, path: str, endpoint: Callable[..., Any], **kwargs: Any) -> None:
        @functools.wraps(endpoint)
        def sending(*args: Any, **values: Any) -> JSONResponse:
            return JSONResponse(endpoint(*args, **values))

        super().__init__(path, sending, **kwargs)
