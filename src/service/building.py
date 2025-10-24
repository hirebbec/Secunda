from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from core.exceptions import duplicated_building_address_exception
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

    async def create(self, building: CreateBuildingSchema) -> IDSchema:
        try:
            building_id = await self._building_repository.create(building=building)

        except IntegrityError:
            raise duplicated_building_address_exception

        return building_id
