from schemas.base import BaseSchema
from schemas.mixins import CreatedAtSchema, IDSchema, UpdatedAtSchema, CoordinatesSchema


class CreateBuildingSchema(BaseSchema, CoordinatesSchema):
    address: str


class UpdateBuildingSchema(CreateBuildingSchema): ...


class GetBuildingSchema(UpdateBuildingSchema, IDSchema, CreatedAtSchema, UpdatedAtSchema): ...
