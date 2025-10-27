from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from db.models import BaseModel
from db.models.mixins import IDMixin


class OrganizationToActivityRelationship(BaseModel, IDMixin):
    __tablename__ = "organizations_to_activities_relationship"

    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    activity_id: Mapped[int] = mapped_column(Integer, ForeignKey("activities.id"), nullable=False)

    __table_args__ = (UniqueConstraint(organization_id, activity_id),)
