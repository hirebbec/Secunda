from typing import Sequence

from fastapi import APIRouter, Depends, status

from schemas.activity import CreateActivitySchema, GetActivitySchema, UpdateActivitySchema
from schemas.mixins import IDSchema
from service.activity import ActivityService

router = APIRouter(prefix="/activities", tags=["Activities"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=IDSchema,
    summary="Создание новой деятельности",
    description="""
    Создаёт новый вид деятельности.

    **Поля:**
    - `name`: Название деятельности  
    - `parent_id`: Идентификатор родительской деятельности (опционально)
    """,
    response_description="Возвращает идентификатор созданной деятельности",
)
async def create_activity(activity: CreateActivitySchema, activity_service: ActivityService = Depends()) -> IDSchema:
    return await activity_service.create_activity(activity=activity)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=None,
    summary="Обновление деятельности",
    description="""
    Обновляет данные существующего вида деятельности по его идентификатору.

    **Поля:**
    - `id`: Идентификатор деятельности  
    - `name`, `parent_id`: новые значения
    """,
    response_description="Возвращает `200 OK` при успешном обновлении",
)
async def update_activity(activity: UpdateActivitySchema, activity_service: ActivityService = Depends()) -> None:
    return await activity_service.update_activity(activity=activity)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    summary="Удаление деятельности",
    description="""
    Удаляет вид деятельности по его идентификатору.

    **Параметры запроса:**
    - `id`: Идентификатор деятельности
    """,
    response_description="Возвращает `204 No Content` при успешном удалении",
)
async def delete_activity(id: int, activity_service: ActivityService = Depends()) -> None:
    return await activity_service.delete_activity(id=id)


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=GetActivitySchema,
    summary="Получение деятельности по ID",
    description="Возвращает информацию о деятельности по её уникальному идентификатору.",
    response_description="Возвращает объект деятельности",
)
async def get_activity_by_id(id: int, activity_service: ActivityService = Depends()) -> GetActivitySchema:
    return await activity_service.get_activity_by_id(id=id)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=Sequence[GetActivitySchema],
    summary="Получение списка деятельностей",
    description="Возвращает список всех видов деятельности",
    response_description="Массив объектов деятельностей",
)
async def get_activities(activity_service: ActivityService = Depends()) -> Sequence[GetActivitySchema]:
    return await activity_service.get_activities()
