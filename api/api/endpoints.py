"""Endpoints: the common HTTP rules API applies to every Group's Endpoints around their Handlers."""

import datetime as dt
import decimal
import functools
import json
import uuid
from collections.abc import Callable
from typing import Any

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from logic.interface import MT5

PROBLEM_MEDIA_TYPE = "application/problem+json"

ERROR_STATUS = {
    "RequestValidationError": 422,
}
"""The status of every error the error table names; any other error is answered with 500."""


# --- Errors -----------------------------------------------------------------------------


def problem(request: Request, error: Exception) -> JSONResponse:
    """Answer an error as RFC 9457 Problem Details whose type is the error's class name."""
    kind = type(error).__name__
    status = ERROR_STATUS.get(kind, 500)
    detail = (
        "; ".join(
            f"{'.'.join(str(part) for part in item['loc'])}: {item['msg']}"
            for item in error.errors()
        )
        if isinstance(error, RequestValidationError)
        else str(error)
        if isinstance(error, MT5.MT5Error)
        else "The request could not be completed."
    )
    return JSONResponse(
        {"type": kind, "title": kind, "status": status, "detail": detail},
        status_code=status,
        media_type=PROBLEM_MEDIA_TYPE,
    )


# --- Results ----------------------------------------------------------------------------


def _encoded(value: Any) -> Any:
    if isinstance(value, list):
        return [_encoded(item) for item in value]
    if isinstance(value, (decimal.Decimal, uuid.UUID)):
        return str(value)
    if isinstance(value, (dt.datetime, dt.date, dt.time)):
        return value.isoformat()
    return value


class ResultResponse(JSONResponse):
    """Sends an Action's result unchanged as JSON."""

    def render(self, content: Any) -> bytes:
        return json.dumps(
            _encoded(content), ensure_ascii=False, allow_nan=False
        ).encode()


class ResultRoute(APIRoute):
    """Serves every Handler's result through ResultResponse, never through the generic encoder."""

    def __init__(self, path: str, endpoint: Callable[..., Any], **kwargs: Any) -> None:
        @functools.wraps(endpoint)
        def serving(*args: Any, **values: Any) -> ResultResponse:
            return ResultResponse(endpoint(*args, **values))

        super().__init__(path, serving, **kwargs)
