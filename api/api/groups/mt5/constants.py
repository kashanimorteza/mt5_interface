"""Constants Adapter of MT5 Group: one Endpoint returning every Constant of MT5 Service."""

from fastapi import APIRouter
from logic.interface import MT5

from api.endpoints import PlainRoute

router = APIRouter(
    prefix="/constants", tags=["MT5 · Constants"], route_class=PlainRoute
)


@router.post("/all")
def all() -> dict[str, int]:
    """Return every Constant as Plain Data, a dictionary from name to value."""
    return MT5.Constants.all()
