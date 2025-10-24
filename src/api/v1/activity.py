from typing import Sequence

from fastapi import APIRouter, Depends, status

from schemas.activity import CreateActivitySchema, GetActivitySchema
from schemas.mixins import IDSchema
from service.activity import ActivityService

router = APIRouter(prefix="/activities", tags=["Activities"])


@router.post("/", status_code=status.HTTP_200_OK, response_model=IDSchema)
async def create_activity(activity: CreateActivitySchema, activity_service: ActivityService = Depends()) -> IDSchema:
    return await activity_service.create_activity(activity=activity)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=GetActivitySchema)
async def get_activity_by_id(id: int, activity_service: ActivityService = Depends()) -> GetActivitySchema:
    return await activity_service.get_activity_by_id(id=id)


@router.get("/", status_code=status.HTTP_200_OK, response_model=Sequence[GetActivitySchema])
async def get_activities(activity_service: ActivityService = Depends()) -> Sequence[GetActivitySchema]:
    return await activity_service.get_activities()
