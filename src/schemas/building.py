from schemas.mixins import CoordinatesSchema, CreatedAtSchema, IDSchema, UpdatedAtSchema


class CreateBuildingSchema(CoordinatesSchema):
    address: str


class UpdateBuildingSchema(IDSchema, CreateBuildingSchema): ...


class GetBuildingSchema(UpdateBuildingSchema, CreatedAtSchema, UpdatedAtSchema): ...
