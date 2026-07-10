"""
Service d'archivage des justificatifs.

Le service permet :

1. de rechercher les justificatifs d'un exercice ;
2. de créer une archive ZIP en mémoire ;
3. de télécharger cette archive sur le PC de l'administrateur ;
4. après confirmation, de supprimer les données binaires
   de PostgreSQL afin d'alléger la base.

Aucun fichier n'est écrit sur le disque du serveur.
"""

import io
import zipfile

from datetime import date

from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.expense_item import ExpenseItem
from app.models.expense_receipt import ExpenseReceipt

# dates de l'exercice

def get_exercise_dates(
    year: int,
) -> tuple[date, date]:

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
    return start_date, end_date

# recherche des justificatifs d'un exercice

def get_exercise_receipts(
    db: Session,
    year: int,
):
    start_date, end_date = get_exercise_dates(year)
    receipts = (
        db.query(ExpenseReceipt)
        .join(ExpenseItem)
        .join(Expense)
        .filter(
            Expense.expense_date >= start_date,
            Expense.expense_date <= end_date,
        )
        .order_by(
            Expense.id,
            ExpenseItem.id,
            ExpenseReceipt.id,
        )
        .all()
    )
    return receipts

# creation de l'archive zip

def create_receipts_archive(
    db: Session,
    year: int,
) -> tuple[bytes, int]:

    # recherche des justificatifs

    receipts = get_exercise_receipts(
        db=db,
        year=year,
    )

    # creation du zip en memoire

    zip_buffer = io.BytesIO()
    archived_count = 0

    # ecriture du zip

    with zipfile.ZipFile(
        zip_buffer,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
    ) as zip_file:

        # parcours des justificatifs
        for receipt in receipts:

            # ignorer les fichiers sans donnees binaires
            if not receipt.file_data:
                continue
            expense_item = receipt.expense_item
            expense = expense_item.expense

            # dossier de la note de frais

            expense_directory = (
                f"NDF_{expense.id}"
            )

            # nom du fichier

            filename = (
                f"{receipt.id}_"
                f"{receipt.original_filename}"
            )

            # chemin dans le zip

            archive_filename = (
                f"{expense_directory}/"
                f"{filename}"
            )

            # ajout au zip

            zip_file.writestr(
                archive_filename,
                receipt.file_data,
            )
            archived_count += 1

        # aucun justificatif disponible

        if archived_count == 0:
            zip_file.writestr(
                "AUCUN_JUSTIFICATIF.txt",
                (
                    "Aucun justificatif disponible "
                    f"pour l'exercice {year}-{year + 1}."
                ),
            )

    # recuperation du zip

    zip_buffer.seek(0)
    zip_content = zip_buffer.getvalue()
    zip_buffer.close()
    return zip_content, archived_count

# suppression des donnees binaires
# apres confirmation de l'administrateur

def clear_archived_receipts(
    db: Session,
    year: int,
) -> int:
    receipts = get_exercise_receipts(
        db=db,
        year=year,
    )
    print("====================================")
    print("CONFIRMATION ARCHIVAGE")
    print("Exercice :", year, "-", year + 1)
    print("Nombre de justificatifs trouvés :", len(receipts))
    cleared_count = 0
    for receipt in receipts:
        print(
            "Justificatif :",
            receipt.id,
            receipt.original_filename,
            "file_data présent :",
            receipt.file_data is not None,
        )
        if receipt.file_data is not None:
            receipt.file_data = None
            cleared_count += 1

    print("Nombre de binaires supprimés :", cleared_count)
    db.commit()
    print("COMMIT effectué")
    return cleared_count
