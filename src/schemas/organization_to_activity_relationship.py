from schemas.base import BaseSchema
from schemas.mixins import CreatedAtSchema, IDSchema, UpdatedAtSchema


class CreateOrganizationToActivityRelationshipSchema(BaseSchema):
    organization_id: int
    activity_id: int


class UpdateOrganizationToActivityRelationshipSchema(CreateOrganizationToActivityRelationshipSchema): ...


class GetOrganizationToActivityRelationshipSchema(
    UpdateOrganizationToActivityRelationshipSchema, IDSchema, CreatedAtSchema, UpdatedAtSchema
): ...
