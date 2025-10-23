from sqlalchemy import ARRAY, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import BaseModel
from db.models.building import Building
from db.models.mixins import CreatedAtMixin, IDMixin, UpdatedAtMixin


class Organization(BaseModel, IDMixin, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "organisations"

    name: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    building: Mapped[Building] = mapped_column(Integer, ForeignKey("buildings.id"), nullable=False)
    activities: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False)
