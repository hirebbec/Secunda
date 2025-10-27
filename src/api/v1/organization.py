from typing import Sequence

from fastapi import APIRouter, Depends, status

from schemas.filter import FilterSchema
from schemas.mixins import IDSchema
from schemas.organization import CreateOrganizationSchema, GetOrganizationSchema, UpdateOrganizationSchema
from service.organization import OrganizationService

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=IDSchema,
    summary="Создание новой организации",
    description="""
    Создаёт новую организацию и сохраняет её в системе.

    **Поля:**
    - `name`: Название организации  
    - `phone_number`: Список контактных телефонов  
    - `building_id`: Идентификатор здания, в котором находится организация  
    - `activities_ids`: Список идентификаторов видов деятельности (можно пустой)
    """,
    response_description="Возвращает идентификатор созданной организации",
)
async def create_organization(
    organization: CreateOrganizationSchema, organization_service: OrganizationService = Depends()
) -> IDSchema:
    return await organization_service.create_organization(organization=organization)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=None,
    summary="Обновление данных организации",
    description="""
    Обновляет данные существующей организации.

    **Поля:**
    - `id`: Идентификатор организации  
    - `name`, `phone_number`, `building_id`, `activities_ids`: новые значения
    """,
    response_description="Возвращает `200 OK` при успешном обновлении",
)
async def update_organization(
    organization: UpdateOrganizationSchema, organization_service: OrganizationService = Depends()
) -> None:
    return await organization_service.update_organization(organization=organization)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    summary="Удаление организации",
    description="""
    Удаляет организацию по её идентификатору.

    **Параметры запроса:**
    - `id`: Идентификатор организации
    """,
    response_description="Возвращает `204 No Content` при успешном удалении",
)
async def delete_organization_by_id(id: int, organization_service: OrganizationService = Depends()) -> None:
    return await organization_service.delete_organization_by_id(id=id)


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=GetOrganizationSchema,
    summary="Получение организации по ID",
    description="Возвращает подробную информацию об организации по её уникальному идентификатору.",
    response_description="Возвращает объект организации с данными о здании и деятельности",
)
async def get_organization_by_id(
    id: int, organization_service: OrganizationService = Depends()
) -> GetOrganizationSchema:
    return await organization_service.get_organization_by_id(id=id)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=Sequence[GetOrganizationSchema],
    summary="Получение списка организаций",
    description="""
    Возвращает список организаций с возможностью фильтрации.

    **Поля фильтра:**
    - `name`: Название организации (поиск по подстроке)  
    - `address`: Адрес здания  
    - `activity_name`: Название вида деятельности  
    - `with_children`: Включать связанные объекты (по умолчанию — `True`)  
    - `center_latitude`, `center_longitude`, `radius`: Географический поиск организаций в радиусе  
    - `min_latitude`, `max_latitude`, `min_longitude`, `max_longitude`: Географический фильтр по координатам
    """,
    response_description="Массив объектов организаций",
)
async def get_organizations(
    filter: FilterSchema = Depends(),
    organization_service: OrganizationService = Depends(),
) -> Sequence[GetOrganizationSchema]:
    return await organization_service.get_organizations(filter=filter)
