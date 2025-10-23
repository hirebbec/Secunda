from schemas.mixins import CoordinatesSchema, CreatedAtSchema, IDSchema, UpdatedAtSchema


class CreateBuildingSchema(CoordinatesSchema):
    address: str


class UpdateBuildingSchema(CreateBuildingSchema): ...


class GetBuildingSchema(UpdateBuildingSchema, IDSchema, CreatedAtSchema, UpdatedAtSchema): ...
