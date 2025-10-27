from typing import Sequence

from sqlalchemy import delete, insert, select

from db.models import OrganizationToActivityRelationship
from db.repository.base import BaseDatabaseRepository
from schemas.organization_to_activity_relationship import (
    CreateOrganizationToActivityRelationshipSchema,
    GetOrganizationToActivityRelationshipSchema,
)


class OrganizationToActivityRelationshipRepository(BaseDatabaseRepository):
    async def create(self, relationship: CreateOrganizationToActivityRelationshipSchema) -> None:
        query = insert(OrganizationToActivityRelationship).values(**relationship.model_dump())

        await self._session.execute(query)
        await self._session.flush()

    async def delete_by_activity_id(self, activity_id: int) -> None:
        query = delete(OrganizationToActivityRelationship).where(
            OrganizationToActivityRelationship.activity_id == activity_id
        )

        await self._session.execute(query)
        await self._session.flush()

    async def delete_by_organization_id(self, organization_id: int) -> None:
        query = delete(OrganizationToActivityRelationship).where(
            OrganizationToActivityRelationship.organization_id == organization_id
        )

        await self._session.execute(query)
        await self._session.flush()

    async def get_by_organization_id(
        self, organization_id: int
    ) -> Sequence[GetOrganizationToActivityRelationshipSchema]:
        query = select(OrganizationToActivityRelationship).where(
            OrganizationToActivityRelationship.organization_id == organization_id
        )

        results = await self._session.execute(query)
        return [
            GetOrganizationToActivityRelationshipSchema.model_validate(relationship)
            for relationship in results.scalars().all()
        ]
