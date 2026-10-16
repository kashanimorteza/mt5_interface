"""Bootstrap of API: read config.yaml, create the API, register every Group, and start serving."""

from pathlib import Path
from typing import Any

import uvicorn
import yaml
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import problems
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

CONFIG = Path(__file__).resolve().parents[1] / "config.yaml"

GROUPS: dict[str, list[APIRouter]] = {
    "MT5": [
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


class API(FastAPI):
    """The API, documenting every Group as a tag group of its Adapters' tags."""

    def openapi(self) -> dict[str, Any]:
        """Describe every Endpoint, with one tag per Adapter and one tag group per Group."""
        schema = super().openapi()
        schema["x-tagGroups"] = [
            {"name": name, "tags": [tag for router in routers for tag in router.tags]}
            for name, routers in GROUPS.items()
        ]
        return schema


config: dict[str, Any] = yaml.safe_load(CONFIG.read_text())
base = f"/{config['key']}" if config["key"] else ""

app = API(
    title=config["title"],
    description=config["description"],
    docs_url=f"{base}/docs",
    redoc_url=f"{base}/redoc",
    openapi_url=f"{base}/openapi.json",
    swagger_ui_oauth2_redirect_url=None,
)
problems.install(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

for name, routers in GROUPS.items():
    for router in routers:
        app.include_router(router, prefix=f"{base}/{name}")


def main() -> None:
    """Serve API at the host and port of config.yaml with its number of workers."""
    uvicorn.run(
        "api.bootstrap:app",
        host=config["host"],
        port=config["port"],
        workers=config["workers"],
    )
