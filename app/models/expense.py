"""
Modele SQLAlchemy Expense
Représentation Python note de frais stockée dans la base de données.
Concrètement, cette classe correspond à la table expenses.
Expense (Python)
      ↓
SQLAlchemy ORM
      ↓
Table "expenses" (Base de données)

"""


from datetime import datetime

from sqlalchemy import (
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base import BaseModel
from app.models.enums import ExpenseStatus

class Expense(BaseModel):

    __tablename__ = "expenses"

    # informations de la note

    expense_date: Mapped[Date] = mapped_column(
        Date,
        nullable=False,
    )
    label: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    status: Mapped[ExpenseStatus] = mapped_column(
        Enum(ExpenseStatus),
        default=ExpenseStatus.DRAFT,
        nullable=False,
    )
    total_amount: Mapped[float] = mapped_column(
        Float,
        default=0,
        nullable=False,
    )
    exported_at: Mapped[datetime | None] = mapped_column(
    DateTime(timezone=True),
    nullable=True,
    )

    # workflow

    submitted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    approved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    paid_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    rejection_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    
    # utilisateur

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    user = relationship(
        "User",
        back_populates="expenses",
    )
    
    # LIGNES DE FRAIS

    items = relationship(
        "ExpenseItem",
        back_populates="expense",
        cascade="all, delete-orphan",
    )