from typing import Sequence

from sqlalchemy import delete, insert, select, update

from db.models import Building
from db.repository.base import BaseDatabaseRepository
from schemas.building import CreateBuildingSchema, GetBuildingSchema, UpdateBuildingSchema
from schemas.mixins import IDSchema


class BuildingRepository(BaseDatabaseRepository):
    async def create(self, building: CreateBuildingSchema) -> IDSchema:
        query = insert(Building).values(**building.model_dump()).returning(Building.id)

        result = await self._session.execute(query)
        return IDSchema(id=result.scalar_one())

    async def update(self, building: UpdateBuildingSchema) -> None:
        query = update(Building).values(**building.model_dump()).where(Building.id == building.id)

        await self._session.execute(query)
        await self._session.flush()

    async def delete(self, id: int) -> None:
        query = delete(Building).where(Building.id == id)

        await self._session.execute(query)
        await self._session.flush()

    async def get_by_id(self, id: int) -> GetBuildingSchema | None:
        query = select(Building).where(Building.id == id)

        result = await self._session.execute(query)
        building = result.scalars().first()

        return GetBuildingSchema.model_validate(building) if building else None

    async def get_buildings(self) -> Sequence[GetBuildingSchema]:
        query = select(Building)

        result = await self._session.execute(query)

        return [GetBuildingSchema.model_validate(building) for building in result.scalars().all()]
