from typing import Sequence

from sqlalchemy import insert, or_, select, true

from db.models import Activity, Building, Organization
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

    async def get_by_name_or_address(self, name: str | None, address: str | None) -> Sequence[GetOrganizationSchema]:
        query = (
            select(Organization, Building)
            .join(Building, Organization.building_id == Building.id)
            .where(or_(Organization.name == name if name else true(), Building.address == address if name else true()))
        )

        result = await self._session.execute(query)

        return [
            GetOrganizationSchema.model_encode(organization_row[0], dict(building=organization_row[1]))
            for organization_row in result.all()
        ]

    async def get_by_activity(self, activity: str) -> Sequence[GetOrganizationSchema]:
        query = (
            select(Organization, Activity)
            .join(Building, Organization.building_id == Building.id)
            .where(or_(Organization.name == name if name else true(), Building.address == address if name else true()))
        )
