from typing import Sequence

from sqlalchemy import delete, insert, select, update

from db.models import Activity
from db.repository.base import BaseDatabaseRepository
from schemas.activity import CreateActivitySchema, GetActivitySchema, UpdateActivitySchema
from schemas.mixins import IDSchema


class ActivityRepository(BaseDatabaseRepository):
    async def create(self, activity: CreateActivitySchema) -> IDSchema:
        query = insert(Activity).values(**activity.model_dump()).returning(Activity.id)

        result = await self._session.execute(query)
        return IDSchema(id=result.scalar_one())

    async def update(self, activity: UpdateActivitySchema) -> None:
        query = update(Activity).values(**activity.model_dump()).where(Activity.id == activity.id)

        await self._session.execute(query)
        await self._session.flush()

    async def delete(self, id: int) -> None:
        query = delete(Activity).where(Activity.id == id)

        await self._session.execute(query)
        await self._session.flush()

    async def get_by_id(self, id: int) -> GetActivitySchema | None:
        query = select(Activity).where(Activity.id == id)

        result = await self._session.execute(query)
        activity = result.scalars().first()

        return GetActivitySchema.model_validate(activity) if activity else None

    async def get_by_name(self, name: str) -> GetActivitySchema | None:
        query = select(Activity).where(Activity.name == name)

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
