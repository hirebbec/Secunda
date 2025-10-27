from typing import Sequence

from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from core.exceptions import (
    building_not_found_exception,
    building_with_organization_exception,
    duplicated_building_address_exception,
)
from db.repository.building import BuildingRepository
from db.repository.organization import OrganizationRepository
from schemas.building import CreateBuildingSchema, GetBuildingSchema, UpdateBuildingSchema
from schemas.mixins import IDSchema
from service.base import BaseService


class BuildingService(BaseService):
    def __init__(
        self,
        building_repository: BuildingRepository = Depends(),
        organization_repository: OrganizationRepository = Depends(),
    ):
        self._building_repository = building_repository
        self._organization_repository = organization_repository

    async def create_building(self, building: CreateBuildingSchema) -> IDSchema:
        try:
            building_id = await self._building_repository.create(building=building)

        except IntegrityError:
            raise duplicated_building_address_exception

        return building_id

    async def update_building(self, building: UpdateBuildingSchema) -> None:
        if not await self._building_repository.get_by_id(id=building.id):
            raise building_not_found_exception

        await self._building_repository.update(building=building)

    async def delete_building_by_id(self, id: int) -> None:
        if not await self._building_repository.get_by_id(id=id):
            raise building_not_found_exception

        if await self._organization_repository.get_by_building_id(building_id=id):
            raise building_with_organization_exception

        await self._building_repository.delete(id=id)

    async def get_building_by_id(self, id: int) -> GetBuildingSchema:
        building = await self._building_repository.get_by_id(id=id)

        if not building:
            raise building_not_found_exception

        return building

    async def get_buildings(self) -> Sequence[GetBuildingSchema]:
        return await self._building_repository.get_buildings()
