from schemas.activity import GetActivitySchema
from schemas.base import BaseSchema
from schemas.building import GetBuildingSchema
from schemas.mixins import CreatedAtSchema, IDSchema, UpdatedAtSchema


class BaseOrganizationSchema(BaseSchema):
    name: str
    phone_number: list[str]


class CreateOrganizationSchema(BaseOrganizationSchema):
    building_id: int
    activity_id: int


class UpdateOrganizationSchema(CreateOrganizationSchema): ...


class GetOrganizationSchema(BaseOrganizationSchema, IDSchema, CreatedAtSchema, UpdatedAtSchema):
    building: GetBuildingSchema
    activities: list[GetActivitySchema] = []
