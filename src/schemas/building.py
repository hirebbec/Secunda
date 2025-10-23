from schemas.base import BaseSchema
from schemas.mixins import CreatedAtSchema, IDSchema, UpdatedAtSchema


class CreateBuildingSchema(BaseSchema):
    address: str


class UpdateBuildingSchema(CreateBuildingSchema): ...


class GetBuildingSchema(UpdateBuildingSchema, IDSchema, CreatedAtSchema, UpdatedAtSchema): ...
