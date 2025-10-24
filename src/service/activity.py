from typing import Sequence

from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from core.config import settings
from core.exceptions import (
    activity_not_found_exception,
    duplicated_activity_name_exception,
    max_activity_depth_exception,
)
from db.repository.activity import ActivityRepository
from schemas.activity import CreateActivitySchema, GetActivitySchema
from schemas.mixins import IDSchema
from service.base import BaseService


class ActivityService(BaseService):
    def __init__(
        self,
        activity_repository: ActivityRepository = Depends(),
    ):
        self._activity_repository = activity_repository

    async def create_activity(self, activity: CreateActivitySchema) -> IDSchema:
        parent_activity = await self._activity_repository.get_by_id(id=activity.parent_id)

        if not parent_activity:
            raise activity_not_found_exception()

        depth = await self._get_activity_depth(activity=parent_activity)

        if depth >= settings().MAX_ACTIVITY_DEPTH:
            raise max_activity_depth_exception

        try:
            activity_id = await self._activity_repository.create(activity=activity)

        except IntegrityError:
            raise duplicated_activity_name_exception

        return activity_id

    async def get_activity_by_id(self, id: int) -> GetActivitySchema:
        activity = await self._activity_repository.get_by_id(id=id)

        if not activity:
            raise activity_not_found_exception

        activity.children = await self._get_children_recursive(parent_id=activity.id)

        return GetActivitySchema.model_validate(activity)

    async def get_activities(self) -> Sequence[GetActivitySchema]:
        roots = await self._activity_repository.get_by_parent_id(parent_id=None)

        for root in roots:
            root.children = await self._get_children_recursive(parent_id=root.id)

        return [GetActivitySchema.model_validate(root) for root in roots]

    async def _get_children_recursive(self, parent_id: int) -> Sequence[GetActivitySchema]:
        children = await self._activity_repository.get_by_parent_id(parent_id=parent_id)

        for child in children:
            child.children = await self._get_children_recursive(parent_id=child.id)

        return children

    async def _get_activity_depth(self, activity: GetActivitySchema) -> int:
        depth = 1

        while activity.parent_id:
            activity = await self._activity_repository.get_by_id(id=activity.parent_id)

            if not activity:
                break

            depth += 1

        return depth
