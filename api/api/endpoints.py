"""Endpoints of API: the common rule every Group's Endpoints follow when they send a result."""

import functools
from collections.abc import Callable
from typing import Any

from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute


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
