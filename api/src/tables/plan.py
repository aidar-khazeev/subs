from decimal import Decimal
from datetime import datetime, timedelta
from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Plan(Base):
    __tablename__ = 'plan'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(default='Обычный')
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    duration: Mapped[timedelta] = mapped_column(default=timedelta(days=30))
    amount: Mapped[Decimal] = mapped_column(default=100.0)
    currency: Mapped[str] = mapped_column(default='RUB')
