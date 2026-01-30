from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from .base import Base
from .plan import Plan


class Subscription(Base):
    __tablename__ = 'subscription'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(index=True)
    plan_id: Mapped[UUID] = mapped_column(ForeignKey(Plan.id), index=True)
    starts_at: Mapped[datetime] = mapped_column()
    ends_at: Mapped[datetime] = mapped_column()
    payment_id: Mapped[UUID | None] = mapped_column(nullable=False)
