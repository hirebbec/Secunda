from schemas.base import BaseSchema
from schemas.mixins import CreatedAtSchema, IDSchema, UpdatedAtSchema


class CreateOrganizationToActivityRelationshipSchema(BaseSchema):
    organization_id: int
    activity_id: int


class UpdateOrganizationToActivityRelationshipSchema(IDSchema, CreateOrganizationToActivityRelationshipSchema): ...


class GetOrganizationToActivityRelationshipSchema(
    UpdateOrganizationToActivityRelationshipSchema, CreatedAtSchema, UpdatedAtSchema
): ...
