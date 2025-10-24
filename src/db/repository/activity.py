from typing import Sequence

from sqlalchemy import insert, select

from db.models import Activity
from db.repository.base import BaseDatabaseRepository
from schemas.activity import CreateActivitySchema, GetActivitySchema
from schemas.mixins import IDSchema


class ActivityRepository(BaseDatabaseRepository):
    async def create(self, activity: CreateActivitySchema) -> IDSchema:
        query = insert(Activity).values(**activity.model_dump()).returning(Activity.id)

        result = await self._session.execute(query)
        return IDSchema(id=result.scalar_one())

    async def get_by_id(self, id: int) -> GetActivitySchema | None:
        query = select(Activity).where(Activity.id == id)

        result = await self._session.execute(query)
        activity = result.scalars().first()

        return GetActivitySchema.model_validate(activity) if activity else None

    async def get_activities(self) -> Sequence[GetActivitySchema]:
        query = select(Activity)

        result = await self._session.execute(query)
        return [GetActivitySchema.model_validate(activity) for activity in result.scalars().all()]

    async def get_by_parent_id(self, parent_id: int | None) -> Sequence[GetActivitySchema]:
        query = select(Activity).where(Activity.parent_id == parent_id)

        result = await self._session.execute(query)
        return [GetActivitySchema.model_validate(activity) for activity in result.scalars().all()]
