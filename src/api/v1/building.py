from typing import Sequence

from fastapi import APIRouter, Depends, status

from schemas.building import CreateBuildingSchema, GetBuildingSchema, UpdateBuildingSchema
from schemas.mixins import IDSchema
from service.building import BuildingService

router = APIRouter(prefix="/buildings", tags=["Buildings"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=IDSchema,
    summary="Создание нового здания",
    description="""
    Создаёт новое здание.

    **Поля:**
    - `address`: Адрес здания  
    - `latitude`: Географическая широта (в метрах)  
    - `longitude`: Географическая долгота (в метрах)
    """,
    response_description="Возвращает идентификатор созданного здания",
)
async def create_building(
    building: CreateBuildingSchema,
    building_service: BuildingService = Depends(),
) -> IDSchema:
    return await building_service.create_building(building=building)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=None,
    summary="Обновление данных здания",
    description="""
    Обновляет информацию о здании по его идентификатору.

    **Поля:**
    - `id`: Идентификатор здания  
    - `address`, `latitude`, `longitude`: новые значения
    """,
    response_description="Возвращает `200 OK` при успешном обновлении",
)
async def update_building(building: UpdateBuildingSchema, building_service: BuildingService = Depends()) -> None:
    return await building_service.update_building(building=building)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    summary="Удаление здания",
    description="""
    Удаляет здание по его идентификатору.

    **Параметры запроса:**
    - `id`: Идентификатор здания
    """,
    response_description="Возвращает `204 No Content` при успешном удалении",
)
async def delete_building_by_id(id: int, building_service: BuildingService = Depends()) -> None:
    return await building_service.delete_building_by_id(id=id)


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=GetBuildingSchema,
    summary="Получение здания по ID",
    description="Возвращает данные о здании по его уникальному идентификатору.",
    response_description="Возвращает объект здания",
)
async def get_building_by_id(id: int, building_service: BuildingService = Depends()) -> GetBuildingSchema:
    return await building_service.get_building_by_id(id=id)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=Sequence[GetBuildingSchema],
    summary="Получение списка зданий",
    description="Возвращает список всех зданий, зарегистрированных в системе.",
    response_description="Массив объектов зданий",
)
async def get_buildings(building_service: BuildingService = Depends()) -> Sequence[GetBuildingSchema]:
    return await building_service.get_buildings()
