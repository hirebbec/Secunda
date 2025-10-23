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
