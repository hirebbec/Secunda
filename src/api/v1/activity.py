from fastapi import APIRouter, Depends, status

from schemas.activity import CreateActivitySchema
from schemas.mixins import IDSchema
from service.activity import ActivityService

router = APIRouter(prefix="/activities", tags=["Activities"])


@router.post("/", status_code=status.HTTP_200_OK, response_model=IDSchema)
async def create_activity(activity: CreateActivitySchema, activity_service: ActivityService = Depends()) -> IDSchema:
    return await activity_service.create_activity(activity=activity)
