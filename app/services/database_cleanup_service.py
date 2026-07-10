from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models.expense import Expense


def cleanup_database(
    db: Session,
) -> int:
    """
    Supprime toutes les notes de frais
    et remet les séquences à zéro.
    Les utilisateurs sont conservés.
    """

    # Nombre de notes avant suppression
    deleted_count = db.query(Expense).count()

    # Suppression complète + remise à zéro
    db.execute(
        text(
            """
            TRUNCATE TABLE
                expense_receipts,
                expense_items,
                expenses
            RESTART IDENTITY CASCADE;
            """
        )
    )

    db.commit()

    return deleted_count