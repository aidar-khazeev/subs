from .base import Base
from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column


class Subscription(Base):
    __tablename__ = 'subscription'

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[UUID] = mapped_column(index=True)
    created_at: Mapped[datetime] = mapped_column()