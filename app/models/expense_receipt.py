"""
Modele ExpenseReceipt représente un justificatif de dépense :
facture PDF, ticket de restaurant, photo d’un reçu, etc.

Il est directement relié au modèle ExpenseItem.

Expense
        ExpenseItem
           ExpenseReceipt
           ExpenseReceipt
           ExpenseReceipt
"""

from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    LargeBinary,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from app.models.base import BaseModel

class ExpenseReceipt(BaseModel):

    __tablename__ = "expense_receipts"

    # ligne de frais
    
    expense_item_id: Mapped[int] = mapped_column(
        ForeignKey(
            "expense_items.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # informations du fichier
    
    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    content_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    file_size: Mapped[int] = mapped_column(
        nullable=False,
    )
    file_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True,
    )
    # colonne por cloudflare
    storage_key: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        index=True,
    )
    # contenu binaire
    
    file_data: Mapped[bytes | None] = mapped_column(
        LargeBinary,
        nullable=True,
    )
    
    # archivage
    
    archived_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    archive_path: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
    
    # relation avec la ligne de frais
    
    expense_item = relationship(
        "ExpenseItem",
        back_populates="receipts",
    )
    
