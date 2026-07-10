"""
Définition du modèle SQLAlchemy ExpenseItem
c’est-à-dire une ligne de dépense appartenant à une note de frais.

Expense (note de frais)
│
├── ExpenseItem (trajet)
├── ExpenseItem (repas)
├── ExpenseItem (hôtel)
└── ExpenseItem (parking)

"""

from sqlalchemy import Enum, Float, ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel
from app.models.enums import ExpenseItemType

class ExpenseItem(BaseModel):  # ce modele herite de BaseModel 
    __tablename__ = "expense_items"

    expense_id: Mapped[int] = mapped_column(
        ForeignKey("expenses.id"),
        nullable=False,
    )
    item_type: Mapped[ExpenseItemType] = mapped_column(
        Enum(ExpenseItemType),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        String(255),
    )
    departure: Mapped[str | None] = mapped_column(
        String(150),
    )
    arrival: Mapped[str | None] = mapped_column(
        String(150),
    )
    kilometers: Mapped[float | None] = mapped_column(
        Float,
    )
    km_rate: Mapped[float] = mapped_column(
    Float,
    default=0.35,
    nullable=False,
    )
    is_electric_vehicle: Mapped[bool] = mapped_column(
    Boolean,
    default=False,
    nullable=False,
    )
    toll_amount: Mapped[float] = mapped_column(
        Float,
        default=0,
    )
    other_amount: Mapped[float] = mapped_column(
        Float,
        default=0,
    )
    amount: Mapped[float] = mapped_column(
        Float,
        default=0,
    )
    receipts = relationship(
        "ExpenseReceipt",
        back_populates="expense_item",
        cascade="all, delete-orphan",
    )
    expense = relationship(
        "Expense",
        back_populates="items",
    )
    