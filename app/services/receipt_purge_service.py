"""
Service de purge des justificatifs.

Supprime uniquement les données binaires des justificatifs
d'un exercice comptable.

Les informations suivantes sont conservées :

- nom du fichier ;
- type MIME ;
- taille ;
- date d'ajout ;
- liaison avec la ligne de frais.

Seul le contenu (file_data) est supprimé.
"""

from datetime import date

from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.expense_item import ExpenseItem
from app.models.expense_receipt import ExpenseReceipt


def purge_receipts(
    db: Session,
    year: int,
) -> int:

    # periode de l'exercice

    start_date = date(
        year,
        7,
        1,
    )

    end_date = date(
        year + 1,
        6,
        30,
    )

    # recherche des justificatifs

    receipts = (
        db.query(ExpenseReceipt)
        .join(ExpenseItem)
        .join(Expense)
        .filter(
            Expense.expense_date >= start_date,
            Expense.expense_date <= end_date,
            ExpenseReceipt.file_data.is_not(None),
        )
        .all()
    )

    # purge

    count = 0
    for receipt in receipts:
        receipt.file_data = None
        count += 1
    db.commit()
    return count
