from fastapi import Depends

from db.repository.activity import ActivityRepository
from schemas.activity import CreateActivitySchema
from schemas.mixins import IDSchema
from service.base import BaseService


class ActivityService(BaseService):
    def __init__(
        self,
        activity_repository: ActivityRepository = Depends(),
    ):
        self._activity_repository = activity_repository

    async def create_activity(self, activity: CreateActivitySchema) -> IDSchema:
        return await self._activity_repository.create(activity=activity)
