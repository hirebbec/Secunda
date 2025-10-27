from typing import Sequence

from fastapi import APIRouter, Depends, status

from schemas.mixins import IDSchema
from schemas.organization import CreateOrganizationSchema, GetOrganizationSchema, UpdateOrganizationSchema
from service.organization import OrganizationService

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=IDSchema)
async def create_organization(
    organization: CreateOrganizationSchema, organization_service: OrganizationService = Depends()
) -> IDSchema:
    return await organization_service.create_organization(organization=organization)


@router.put("/", status_code=status.HTTP_200_OK, response_model=None)
async def update_organization(
    organization: UpdateOrganizationSchema, organization_service: OrganizationService = Depends()
) -> None:
    return await organization_service.update_organization(organization=organization)


@router.put("/", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_organization_by_id(id: int, organization_service: OrganizationService = Depends()) -> None:
    return await organization_service.delete_organization_by_id(id=id)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=GetOrganizationSchema)
async def get_organization_by_id(
    id: int, organization_service: OrganizationService = Depends()
) -> GetOrganizationSchema:
    return await organization_service.get_organization_by_id(id=id)


@router.get("/", status_code=status.HTTP_200_OK, response_model=Sequence[GetOrganizationSchema])
async def get_organizations_by_name_or_address(
    name: str | None = None, address: str | None = None, organization_service: OrganizationService = Depends()
) -> Sequence[GetOrganizationSchema]:
    return await organization_service.get_organizations_by_name_or_address(name=name, address=address)


@router.get("/", status_code=status.HTTP_200_OK, response_model=Sequence[GetOrganizationSchema])
async def get_organizations_by_activity(
    activity: str, organization_service: OrganizationService = Depends()
) -> Sequence[GetOrganizationSchema]:
    return await organization_service.get_organizations_by_activity(activity=activity)
