from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import BaseModel
from db.models.mixins import CoordinatesMixin, CreatedAtMixin, IDMixin, UpdatedAtMixin


class Building(BaseModel, IDMixin, CreatedAtMixin, UpdatedAtMixin, CoordinatesMixin):
    __tablename__ = "buildings"

    address: Mapped[str] = mapped_column(String, nullable=False, unique=True)
