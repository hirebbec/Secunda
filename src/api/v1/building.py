from typing import Sequence

from fastapi import APIRouter, Depends, status

from schemas.building import CreateBuildingSchema, GetBuildingSchema, UpdateBuildingSchema
from schemas.mixins import IDSchema
from service.building import BuildingService

router = APIRouter(prefix="/buildings", tags=["Buildings"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=IDSchema)
async def create_building(building: CreateBuildingSchema, building_service: BuildingService = Depends()) -> IDSchema:
    return await building_service.create_building(building=building)


@router.put("/", status_code=status.HTTP_200_OK, response_model=None)
async def update_building(building: UpdateBuildingSchema, building_service: BuildingService = Depends()) -> None:
    return await building_service.update_building(building=building)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_building_by_id(id: int, building_service: BuildingService = Depends()) -> None:
    return await building_service.delete_building_by_id(id=id)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=GetBuildingSchema)
async def get_building_by_id(id: int, building_service: BuildingService = Depends()) -> GetBuildingSchema:
    return await building_service.get_building_by_id(id=id)


@router.get("/", status_code=status.HTTP_200_OK, response_model=Sequence[GetBuildingSchema])
async def get_buildings(building_service: BuildingService = Depends()) -> Sequence[GetBuildingSchema]:
    return await building_service.get_buildings()
