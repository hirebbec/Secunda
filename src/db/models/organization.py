from sqlalchemy import ARRAY, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import BaseModel
from db.models.mixins import CreatedAtMixin, IDMixin, UpdatedAtMixin


class Organization(BaseModel, IDMixin, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "organisations"

    name: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    building_id: Mapped[int] = mapped_column(Integer, ForeignKey("buildings.id"), nullable=False)
    activities_ids: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False)
