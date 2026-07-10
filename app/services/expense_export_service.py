"""
Service d'export comptable des notes de frais.

Règles :

- Exporte uniquement les notes PAYEES.
- Une ligne CSV = une note de frais.
- Le détail est exporté dans export_details.csv
  (créé par expense_export_zip_service.py).
"""

import csv
import io

from datetime import date

from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.enums import ExpenseStatus


# ==========================================================
# EXPORT DES NOTES DE FRAIS
# ==========================================================

def export_paid_expenses(
    db: Session,
    start_date: date,
    end_date: date,
) -> tuple[bytes, int]:

    # ======================================================
    # RECHERCHE DES NOTES
    # ======================================================

    expenses = (
        db.query(Expense)
        .filter(
            Expense.expense_date >= start_date,
            Expense.expense_date <= end_date,
            Expense.status == ExpenseStatus.PAID,
        )
        .order_by(
            Expense.expense_date,
            Expense.id,
        )
        .all()
    )

    # ======================================================
    # CREATION DU CSV
    # ======================================================

    output = io.StringIO()

    writer = csv.writer(
        output,
        delimiter=";",
        lineterminator="\n",
    )

    # ======================================================
    # ENTETE
    # ======================================================

    writer.writerow(
        [
            "NDF",
            "DATE",
            "BENEFICIAIRE",
            "MONTANT",
            "LIBELLE",
        ]
    )

    # ======================================================
    # COMPTEUR
    # ======================================================

    exported_lines = 0

    # ======================================================
    # PARCOURS DES NOTES
    # ======================================================

    for expense in expenses:

        writer.writerow(
            [
                f"NDF-{expense.id:06d}",
                expense.expense_date.strftime("%d/%m/%Y"),
                expense.user.username,
                f"{expense.total_amount:.2f}",
                expense.label,
            ]
        )

        exported_lines += 1

    # ======================================================
    # CONVERSION EN UTF-8
    # ======================================================

    file_content = output.getvalue().encode(
        "utf-8-sig"
    )

    output.close()

    # ======================================================
    # RETOUR
    # ======================================================

    return (
        file_content,
        exported_lines,
    )