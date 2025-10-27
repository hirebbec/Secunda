from typing import Sequence

from schemas.base import BaseSchema
from schemas.mixins import CreatedAtSchema, IDSchema, UpdatedAtSchema


class CreateActivitySchema(BaseSchema):
    name: str
    parent_id: int | None = None


class UpdateActivitySchema(IDSchema, CreateActivitySchema): ...


class GetActivitySchema(UpdateActivitySchema, CreatedAtSchema, UpdatedAtSchema):
    children: Sequence["GetActivitySchema"] | None = None
