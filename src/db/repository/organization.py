from typing import Sequence

from sqlalchemy import insert, select

from db.models import Building, Organization
from db.repository.base import BaseDatabaseRepository
from schemas.mixins import IDSchema
from schemas.organization import CreateOrganizationSchema, GetOrganizationSchema


class OrganizationRepository(BaseDatabaseRepository):
    async def create(self, organization: CreateOrganizationSchema) -> IDSchema:
        query = insert(Organization).values(**organization.model_dump()).returning(Organization.id)

        result = await self._session.execute(query)
        return IDSchema(id=result.scalar_one())

    async def get_by_id(self, id: int) -> GetOrganizationSchema | None:
        query = (
            select(Organization, Building)
            .join(Building, Organization.building_id == Building.id)
            .where(Organization.id == id)
        )

        result = await self._session.execute(query)
        organization_row = result.first()

        return (
            GetOrganizationSchema.model_encode(organization_row[0], dict(building=organization_row[1]))
            if organization_row
            else None
        )

    async def get_organizations_by_name_or_building_id(self, name: str) -> Sequence[GetOrganizationSchema]:
        query = (
            select(Organization, Building)
            .join(Building, Organization.building_id == Building.id)
            .where(Organization.name == name)
        )

        result = await self._session.execute(query)

        return [
            GetOrganizationSchema.model_encode(organization_row[0], dict(building=organization_row[1]))
            for organization_row in result.all()
        ]

    async def get_organizations_by_building_id(self, building_id: int) -> Sequence[GetOrganizationSchema]:
        query = (
            select(Organization, Building)
            .join(Building, Organization.building_id == Building.id)
            .where(Organization.building_id == building_id)
        )

        result = await self._session.execute(query)

        return [
            GetOrganizationSchema.model_encode(organization_row[0], dict(building=organization_row[1]))
            for organization_row in result.all()
        ]
