from schemas.base import BaseSchema
from schemas.mixins import CreatedAtSchema, IDSchema, UpdatedAtSchema


class CreateActivitySchema(BaseSchema):
    name: str
    parent_id: int | None = None


class UpdateActivitySchema(CreateActivitySchema): ...


class GetActivitySchema(UpdateActivitySchema, IDSchema, CreatedAtSchema, UpdatedAtSchema): ...
