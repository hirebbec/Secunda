from typing import Sequence

from fastapi import Depends

from core.exceptions import activity_not_found_exception, building_not_found_exception, organization_not_found_exception
from db.repository.activity import ActivityRepository
from db.repository.building import BuildingRepository
from db.repository.organization import OrganizationRepository
from db.repository.organization_to_activity_relationship import OrganizationToActivityRelationshipRepository
from schemas.mixins import IDSchema
from schemas.organization import CreateOrganizationSchema, GetOrganizationSchema
from schemas.organization_to_activity_relationship import CreateOrganizationToActivityRelationshipSchema
from service.base import BaseService


class OrganizationService(BaseService):
    def __init__(
        self,
        organization_repository: OrganizationRepository = Depends(),
        building_repository: BuildingRepository = Depends(),
        activity_repository: ActivityRepository = Depends(),
        organization_to_activity_repository: OrganizationToActivityRelationshipRepository = Depends(),
    ):
        self._organization_repository = organization_repository
        self._building_repository = building_repository
        self._activity_repository = activity_repository
        self._organization_to_activity_repository = organization_to_activity_repository

    async def create_organization(self, organization: CreateOrganizationSchema) -> IDSchema:
        if not await self._building_repository.get_by_id(id=organization.building_id):
            raise building_not_found_exception

        if not await self._activity_repository.get_by_id(id=organization.activity_id):
            raise activity_not_found_exception

        organization_id_schema = await self._organization_repository.create(organization=organization)

        await self._organization_to_activity_repository.create(
            relationship=CreateOrganizationToActivityRelationshipSchema(
                organization_id=organization_id_schema.id, activity_id=organization.activity_id
            )
        )

        return organization_id_schema

    async def get_organizations_by_id(self, id: int) -> GetOrganizationSchema:
        organization = await self._organization_repository.get_by_id(id=id)

        if not organization:
            raise organization_not_found_exception

        relationships = await self._organization_to_activity_repository.get_by_organization_id(
            organization_id=organization.id
        )

        for relationship in relationships:
            organization.activities += await self._activity_repository.get_by_id(id=relationship.activity_id)

        return organization

    async def get_organizations_by_name_or_address(
        self, name: str | None, address: str | None
    ) -> Sequence[GetOrganizationSchema]:
        organizations = await self._organization_repository.get_by_name_or_address(name=name, address=address)

        for organization in organizations:
            relationships = await self._organization_to_activity_repository.get_by_organization_id(
                organization_id=organization.id
            )

            for relationship in relationships:
                organization.activities += await self._activity_repository.get_by_id(id=relationship.activity_id)

        return organizations

    async def get_organizations_by_activity(
        self,
        activity: str | None,
    ) -> Sequence[GetOrganizationSchema]:
        return await self._organization_repository.get_organizations_by_activity
