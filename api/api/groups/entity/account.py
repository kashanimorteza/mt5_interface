"""The account Adapter: one Endpoint for every Action of the Account Child Service."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Path
from logic.interface import Entity

from api import endpoints

bound = Entity.Entity.Account
service = Entity.Service.Account()
router = APIRouter(
    prefix="/account",
    tags=["Entity · account"],
    route_class=endpoints.ResultRoute,
)


@router.post("/add", response_model=None)
def add(
    entity: Annotated[Any, Depends(endpoints.entity_in(bound))],
    instance: Annotated[Any, Depends(endpoints.instance_in_body)],
) -> Any:
    """Store one complete new Entity and return it as stored, with generated values."""
    return service.add(entity, instance)


@router.put("/update", response_model=None)
def update(
    entity: Annotated[Any, Depends(endpoints.entity_in(bound))],
    instance: Annotated[Any, Depends(endpoints.instance_in_body)],
) -> Any:
    """Replace every mutable Field of the record the Entity's id locates, or return None."""
    return service.update(entity, instance)


@router.post("/list", response_model=None)
def list(
    filters: Annotated[Any, Depends(endpoints.filters_in(bound))],
    combination: Annotated[Any, Depends(endpoints.combination_in_body)],
    orders: Annotated[Any, Depends(endpoints.orders_in(bound))],
    limit: Annotated[Any, Depends(endpoints.limit_in_body)],
    instance: Annotated[Any, Depends(endpoints.instance_in_body)],
) -> Any:
    """Return the matching Entities, ordered and bounded by a positive limit."""
    return service.list(filters, combination, orders, limit, instance)


@router.get("/get_by_id/{id}", response_model=None)
def get_by_id(
    id: Annotated[int, Path()],
    instance: Annotated[Any, Depends(endpoints.instance_in_query)],
) -> Any:
    """Return the Entity with this id, or None."""
    return service.get_by_id(id, instance)


@router.delete("/delete/{id}", response_model=None)
def delete(
    id: Annotated[int, Path()],
    instance: Annotated[Any, Depends(endpoints.instance_in_query)],
) -> Any:
    """Delete the Entity with this id and return it as it was, or None."""
    return service.delete(id, instance)


@router.patch("/enable/{id}", response_model=None)
def enable(
    id: Annotated[int, Path()],
    instance: Annotated[Any, Depends(endpoints.instance_in_body)],
) -> Any:
    """Set only is_active to true and return the final Entity, or None."""
    return service.enable(id, instance)


@router.patch("/disable/{id}", response_model=None)
def disable(
    id: Annotated[int, Path()],
    instance: Annotated[Any, Depends(endpoints.instance_in_body)],
) -> Any:
    """Set only is_active to false and return the final Entity, or None."""
    return service.disable(id, instance)


@router.post("/count", response_model=None)
def count(
    filters: Annotated[Any, Depends(endpoints.filters_in(bound))],
    combination: Annotated[Any, Depends(endpoints.combination_in_body)],
    instance: Annotated[Any, Depends(endpoints.instance_in_body)],
) -> Any:
    """Return the number of matching records."""
    return service.count(filters, combination, instance)


@router.post("/sum", response_model=None)
def sum(
    field: Annotated[Any, Depends(endpoints.field_in(bound))],
    filters: Annotated[Any, Depends(endpoints.filters_in(bound))],
    combination: Annotated[Any, Depends(endpoints.combination_in_body)],
    instance: Annotated[Any, Depends(endpoints.instance_in_body)],
) -> Any:
    """Return the total of one numeric Field over matching records, or zero."""
    return service.sum(field, filters, combination, instance)


@router.post("/min", response_model=None)
def min(
    field: Annotated[Any, Depends(endpoints.field_in(bound))],
    filters: Annotated[Any, Depends(endpoints.filters_in(bound))],
    combination: Annotated[Any, Depends(endpoints.combination_in_body)],
    instance: Annotated[Any, Depends(endpoints.instance_in_body)],
) -> Any:
    """Return the smallest value of one Field over matching records, or None."""
    return service.min(field, filters, combination, instance)


@router.post("/max", response_model=None)
def max(
    field: Annotated[Any, Depends(endpoints.field_in(bound))],
    filters: Annotated[Any, Depends(endpoints.filters_in(bound))],
    combination: Annotated[Any, Depends(endpoints.combination_in_body)],
    instance: Annotated[Any, Depends(endpoints.instance_in_body)],
) -> Any:
    """Return the largest value of one Field over matching records, or None."""
    return service.max(field, filters, combination, instance)


@router.delete("/truncate", response_model=None)
def truncate(
    instance: Annotated[Any, Depends(endpoints.instance_in_query)],
) -> Any:
    """Delete every record of the Entity, keeping its Table, and return the count."""
    return service.truncate(instance)
