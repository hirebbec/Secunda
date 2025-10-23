from sqlalchemy import insert, select

from db.models import Building
from db.repository.base import BaseDatabaseRepository
from schemas.building import CreateBuildingSchema, GetBuildingSchema
from schemas.mixins import IDSchema


class BuildingRepository(BaseDatabaseRepository):
    async def create(self, building: CreateBuildingSchema) -> IDSchema:
        query = insert(Building).values(**building.model_dump()).returning(Building.id)

        result = await self._session.execute(query)
        return IDSchema(id=result.scalar_one())

    async def get_by_id(self, id: int) -> GetBuildingSchema | None:
        query = select(Building).where(Building.id == id)

        result = await self._session.execute(query)
        building = result.scalars().first()

        return GetBuildingSchema.model_validate(building) if building else None
