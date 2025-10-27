from schemas.base import BaseSchema


class FilterSchema(BaseSchema):
    name: str | None = None
    address: str | None = None
    activity_name: str | None = None
    with_children: bool = True
    center_latitude: float | None = None
    center_longitude: float | None = None
    radius: int | None = None
    min_latitude: float | None = None
    max_latitude: float | None = None
    min_longitude: float | None = None
    max_longitude: float | None = None
