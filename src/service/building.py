from fastapi import Depends

from db.repository.building import BuildingRepository
from schemas.building import CreateBuildingSchema
from schemas.mixins import IDSchema
from service.base import BaseService


class BuildingService(BaseService):
    def __init__(
        self,
        building_repository: BuildingRepository = Depends(),
    ):
        self._building_repository = building_repository

    async def create_building(self, building: CreateBuildingSchema) -> IDSchema:
        return await self._building_repository.create(building=building)
