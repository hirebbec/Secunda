from fastapi import APIRouter, Depends, status

from schemas.building import CreateBuildingSchema
from schemas.mixins import IDSchema
from service.building import BuildingService

router = APIRouter(prefix="/buildings", tags=["Buildings"])


@router.post("/", status_code=status.HTTP_200_OK, response_model=IDSchema)
async def create_building(building: CreateBuildingSchema, building_service: BuildingService = Depends()) -> IDSchema:
    return await building_service.create_building(building=building)
