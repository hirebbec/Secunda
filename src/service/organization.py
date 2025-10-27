from typing import Sequence

from fastapi import Depends

from core.exceptions import activity_not_found_exception, building_not_found_exception, organization_not_found_exception
from db.repository.activity import ActivityRepository
from db.repository.building import BuildingRepository
from db.repository.organization import OrganizationRepository
from db.repository.organization_to_activity_relationship import OrganizationToActivityRelationshipRepository
from schemas.filter import FilterSchema
from schemas.mixins import IDSchema
from schemas.organization import CreateOrganizationSchema, GetOrganizationSchema, UpdateOrganizationSchema
from schemas.organization_to_activity_relationship import CreateOrganizationToActivityRelationshipSchema
from service.activity import ActivityService
from service.base import BaseService


class OrganizationService(BaseService):
    def __init__(
        self,
        organization_repository: OrganizationRepository = Depends(),
        building_repository: BuildingRepository = Depends(),
        activity_repository: ActivityRepository = Depends(),
        organization_to_activity_repository: OrganizationToActivityRelationshipRepository = Depends(),
        activity_service: ActivityService = Depends(),
    ):
        self._organization_repository = organization_repository
        self._building_repository = building_repository
        self._activity_repository = activity_repository
        self._organization_to_activity_repository = organization_to_activity_repository
        self._activity_service = activity_service

    async def create_organization(self, organization: CreateOrganizationSchema) -> IDSchema:
        if not await self._building_repository.get_by_id(id=organization.building_id):
            raise building_not_found_exception

        for activity_id in organization.activities_ids:
            if not await self._activity_repository.get_by_id(id=activity_id):
                raise activity_not_found_exception

        organization_id_schema = await self._organization_repository.create(organization=organization)

        for activity_id in organization.activities_ids:
            await self._organization_to_activity_repository.create(
                relationship=CreateOrganizationToActivityRelationshipSchema(
                    organization_id=organization_id_schema.id, activity_id=activity_id
                )
            )

        return organization_id_schema

    async def update_organization(self, organization: UpdateOrganizationSchema) -> None:
        if not await self._building_repository.get_by_id(id=organization.building_id):
            raise building_not_found_exception

        for activity_id in organization.activities_ids:
            if not await self._activity_repository.get_by_id(id=activity_id):
                raise activity_not_found_exception

        if not await self._organization_repository.get_by_id(id=organization.id):
            raise organization_not_found_exception

        await self._organization_repository.update(organization=organization)

        await self._organization_to_activity_repository.delete_by_organization_id(organization_id=organization.id)

        for activity_id in organization.activities_ids:
            await self._organization_to_activity_repository.create(
                relationship=CreateOrganizationToActivityRelationshipSchema(
                    organization_id=organization.id, activity_id=activity_id
                )
            )

    async def delete_organization_by_id(self, id: int) -> None:
        if not await self._organization_repository.get_by_id(id=id):
            raise organization_not_found_exception

        await self._organization_to_activity_repository.delete_by_organization_id(organization_id=id)

        await self._organization_repository.delete(id=id)

    async def get_organization_by_id(self, id: int) -> GetOrganizationSchema:
        organization = await self._organization_repository.get_by_id(id=id)

        if not organization:
            raise organization_not_found_exception

        relationships = await self._organization_to_activity_repository.get_by_organization_id(
            organization_id=organization.id
        )

        for relationship in relationships:
            activity = await self._activity_service.get_activity_by_id(id=relationship.activity_id)

            if activity:
                organization.activities.append(activity)

        return organization

    async def get_organizations(self, filter: FilterSchema) -> Sequence[GetOrganizationSchema]:
        activity_ids: list[int] = []

        if filter.activity_name:
            activity = await self._activity_service.get_activity_by_name(
                name=filter.activity_name, with_children=filter.with_children
            )

            if activity:
                activity_ids.append(activity.id)

                for child in activity.children:
                    activity_ids.append(child.id)
                    for grandchild in child.children:
                        activity_ids.append(grandchild.id)

        organizations = await self._organization_repository.get_organizations(filter=filter, activity_ids=activity_ids)

        for organization in organizations:
            relationships = await self._organization_to_activity_repository.get_by_organization_id(
                organization_id=organization.id
            )

            for relationship in relationships:
                organization.activities.append(
                    await self._activity_service.get_activity_by_id(id=relationship.activity_id)
                )

        return organizations
