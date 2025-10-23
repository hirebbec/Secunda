from typing import Sequence

from fastapi import APIRouter, Depends, status

from schemas.mixins import IDSchema
from schemas.organization import CreateOrganizationSchema, GetOrganizationSchema
from service.organization import OrganizationService

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.post("/", status_code=status.HTTP_200_OK, response_model=IDSchema)
async def create_organization(
    organization: CreateOrganizationSchema, organization_service: OrganizationService = Depends()
) -> IDSchema:
    return await organization_service.create_organization(organization=organization)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=GetOrganizationSchema)
async def get_organizations_by_id(
    id: int, organization_service: OrganizationService = Depends()
) -> GetOrganizationSchema:
    return await organization_service.get_organizations_by_id(id=id)


@router.get("/", status_code=status.HTTP_200_OK, response_model=Sequence[GetOrganizationSchema])
async def get_organizations_by_name_or_building_id(
    name: str | None = None, building_id: int | None = None, organization_service: OrganizationService = Depends()
) -> Sequence[GetOrganizationSchema]:
    return await organization_service.get_organizations_by_name_or_building_id(name=name, building_id=building_id)
