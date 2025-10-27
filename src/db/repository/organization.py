from typing import Sequence

from sqlalchemy import and_, delete, func, insert, select, true, update
from sqlalchemy.orm import Mapped

from core.config import settings
from db.models import Building, Organization, OrganizationToActivityRelationship
from db.repository.base import BaseDatabaseRepository
from schemas.filter import FilterSchema
from schemas.mixins import IDSchema
from schemas.organization import CreateOrganizationSchema, GetOrganizationSchema, UpdateOrganizationSchema


class OrganizationRepository(BaseDatabaseRepository):
    async def create(self, organization: CreateOrganizationSchema) -> IDSchema:
        query = (
            insert(Organization)
            .values(
                name=organization.name, phone_number=organization.phone_number, building_id=organization.building_id
            )
            .returning(Organization.id)
        )

        result = await self._session.execute(query)
        return IDSchema(id=result.scalar_one())

    async def update(self, organization: UpdateOrganizationSchema) -> None:
        query = update(Organization).values(**organization.model_dump()).where(Organization.id == organization.id)

        await self._session.execute(query)
        await self._session.flush()

    async def delete(self, id: int) -> None:
        query = delete(Organization).where(Organization.id == id)

        await self._session.execute(query)
        await self._session.flush()

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

    async def get_by_building_id(self, building_id: int) -> Sequence[GetOrganizationSchema]:
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

    async def get_organizations(self, filter: FilterSchema, activity_ids: list[int]) -> Sequence[GetOrganizationSchema]:
        query = (
            select(Organization, Building)
            .join(Building, Organization.building_id == Building.id)
            .join(
                OrganizationToActivityRelationship,
                OrganizationToActivityRelationship.organization_id == Organization.id,
            )
            .where(
                and_(
                    Organization.name == filter.name if filter.name else true(),
                    Building.address == filter.address if filter.address else true(),
                    OrganizationToActivityRelationship.activity_id.in_(activity_ids) if activity_ids else true(),
                    self.__is_in_radius(
                        building_latitude=Building.latitude,
                        building_longitude=Building.longitude,
                        center_latitude=filter.center_latitude,
                        center_longitude=filter.center_longitude,
                        radius=filter.radius,
                    )
                    if filter.center_longitude and filter.center_latitude and filter.radius
                    else true(),
                    self.__is_in_bounding_box(
                        building_latitude=Building.latitude,
                        building_longitude=Building.longitude,
                        min_latitude=filter.min_latitude,
                        max_latitude=filter.max_latitude,
                        min_longitude=filter.min_longitude,
                        max_longitude=filter.max_longitude,
                    )
                    if filter.min_latitude and filter.max_latitude and filter.min_longitude and filter.max_longitude
                    else true(),
                )
            )
            .distinct()
        )

        result = await self._session.execute(query)

        return [
            GetOrganizationSchema.model_encode(organization_row[0], dict(building=organization_row[1]))
            for organization_row in result.all()
        ]

    def __is_in_radius(
        self,
        building_latitude: Mapped[float],
        building_longitude: Mapped[float],
        center_latitude: float,
        center_longitude: float,
        radius: int,
    ):
        return (
            2
            * settings().EARTH_RADIUS_IN_METERS
            * func.asin(
                func.sqrt(
                    func.pow(
                        func.sin(func.radians((building_latitude - center_latitude) / 2)),
                        2,
                    )
                    + func.cos(func.radians(center_latitude))
                    * func.cos(func.radians(building_latitude))
                    * func.pow(
                        func.sin(func.radians((building_longitude - center_longitude) / 2)),
                        2,
                    )
                )
            )
            <= radius
        )

    def __is_in_bounding_box(
        self,
        building_latitude: Mapped[float],
        building_longitude: Mapped[float],
        min_latitude: float,
        max_latitude: float,
        min_longitude: float,
        max_longitude: float,
    ):
        return and_(
            building_latitude >= min_latitude,
            building_latitude <= max_latitude,
            building_longitude >= min_longitude,
            building_longitude <= max_longitude,
        )
