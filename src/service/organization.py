from typing import Sequence

from fastapi import Depends

from core.exceptions import activity_not_found_exception, building_not_found_exception, organization_not_found_exception
from db.repository.activity import ActivityRepository
from db.repository.building import BuildingRepository
from db.repository.organization import OrganizationRepository
from schemas.mixins import IDSchema
from schemas.organization import CreateOrganizationSchema, GetOrganizationSchema
from service.base import BaseService


class OrganizationService(BaseService):
    def __init__(
        self,
        organization_repository: OrganizationRepository = Depends(),
        building_repository: BuildingRepository = Depends(),
        activity_repository: ActivityRepository = Depends(),
    ):
        self._organization_repository = organization_repository
        self._building_repository = building_repository
        self._activity_repository = activity_repository

    async def create_organization(self, organization: CreateOrganizationSchema) -> IDSchema:
        if not await self._building_repository.get_by_id(id=organization.building_id):
            raise building_not_found_exception

        for activity_id in organization.activities_ids:
            if not await self._activity_repository.get_by_id(id=activity_id):
                raise activity_not_found_exception

        return await self._organization_repository.create(organization=organization)

    async def get_organizations_by_id(self, id: int) -> GetOrganizationSchema:
        organization = await self._organization_repository.get_by_id(id=id)

        if not organization:
            raise organization_not_found_exception

        return organization

    async def get_organizations_by_name_or_building_id(
        self, name: str | None, building_id: int | None
    ) -> Sequence[GetOrganizationSchema]:
        organizations: list[GetOrganizationSchema] = []

        if name:
            organizations += await self._organization_repository.get_organizations_by_name_or_building_id(name=name)

        if building_id:
            organizations += await self._organization_repository.get_organizations_by_building_id(
                building_id=building_id
            )

        unique_organizations: dict[int, GetOrganizationSchema] = {org.id: org for org in organizations}

        return list(unique_organizations.values())
