"""Bootstrap: composes API from its runtime Configuration and serves every Group beneath its segment."""

from pathlib import Path
from typing import Any

import uvicorn
import yaml
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from logic.interface import MT5, Entity

from api import endpoints
from api.groups.entity import (
    account,
    account_group,
    asset,
    broker,
    currency,
    instance,
    user,
)
from api.groups.mt5 import (
    connection,
    constants,
    history,
    market_book,
    market_data,
    orders,
    positions,
    symbols,
)

CONFIGURATION: dict[str, Any] = yaml.safe_load(
    (Path(__file__).resolve().parents[1] / "config.yaml").read_text(encoding="utf-8")
)
BASE = f"/{CONFIGURATION['key']}" if CONFIGURATION["key"] else ""

GROUPS = {
    "entity": [
        user.router,
        instance.router,
        currency.router,
        broker.router,
        asset.router,
        account_group.router,
        account.router,
    ],
    "mt5": [
        connection.router,
        symbols.router,
        market_book.router,
        market_data.router,
        orders.router,
        positions.router,
        history.router,
        constants.router,
    ],
}
"""Every Group's segment and its Adapter routers."""

TAG_GROUPS = [
    {
        "name": "Entity",
        "tags": [tag for router in GROUPS["entity"] for tag in router.tags],
    },
    {
        "name": "MT5",
        "tags": [tag for router in GROUPS["mt5"] for tag in router.tags],
    },
]
"""The interactive documentation's sections: one per Group, holding one per Adapter."""


class Application(FastAPI):
    """The one running API; its served description gathers every Adapter's section under its Group."""

    def openapi(self) -> dict[str, Any]:
        schema = super().openapi()
        schema["x-tagGroups"] = TAG_GROUPS
        return schema


app = Application(
    title=CONFIGURATION["title"],
    description=CONFIGURATION["description"],
    docs_url=f"{BASE}/docs",
    redoc_url=f"{BASE}/redoc",
    openapi_url=f"{BASE}/openapi.json",
    default_response_class=endpoints.ResultResponse,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(Entity.database_error.DatabaseError, endpoints.problem)
app.add_exception_handler(MT5.MT5Error, endpoints.problem)
app.add_exception_handler(RequestValidationError, endpoints.problem)
app.add_exception_handler(Exception, endpoints.problem)
for segment, routers in GROUPS.items():
    for router in routers:
        app.include_router(router, prefix=f"{BASE}/{segment}")


def main() -> None:
    """Serve API on the configured host and port with the configured workers."""
    uvicorn.run(
        "api.bootstrap:app",
        host=CONFIGURATION["host"],
        port=CONFIGURATION["port"],
        workers=CONFIGURATION["workers"],
    )


if __name__ == "__main__":
    main()
