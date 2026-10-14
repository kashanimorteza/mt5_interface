"""The constants Adapter: one Endpoint returning every Constant of MT5 Service by name and value."""

from typing import Any

from fastapi import APIRouter
from logic.interface import MT5

from api import endpoints

router = APIRouter(
    prefix="/constants",
    tags=["MT5 · constants"],
    route_class=endpoints.ResultRoute,
)


@router.get("/get", response_model=None)
def get() -> Any:
    """Return every Constant as Plain Data: a dictionary from its name to its value."""
    return MT5.Constants.get()
