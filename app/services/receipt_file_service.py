"""
Service de gestion des justificatifs.

Ce service masque l'emplacement réel
des fichiers (base de données, Cloudflare R2...).

Ce code est le point d'entrée unique pour les justificatifs.

Cela signifie que :

 Upload
 Affichage
 Téléchargement
 Export ZIP

Interet c'est que l'appli ne sait pas ou sont stoché les fichiers 
"""

from app.models.expense_receipt import ExpenseReceipt

from app.services.storage_service import (
    save_receipt,
    load_receipt,
    remove_receipt,
)

# enregistrement

def store_receipt(
    *,
    receipt: ExpenseReceipt,
    expense,
    content: bytes,
):

    storage_key = save_receipt(
        expense=expense,
        receipt_id=receipt.id,
        filename=receipt.original_filename,
        content=content,
        content_type=receipt.content_type,
    )
    receipt.storage_key = storage_key
    
    # On ne conserve plus le binaire en base

    receipt.file_data = None

# lecture

def read_receipt(
    receipt: ExpenseReceipt,
) -> bytes:
    if receipt.storage_key:
        return load_receipt(
            receipt.storage_key
        )
    if receipt.file_data:
        return receipt.file_data
    raise FileNotFoundError(
        "Justificatif introuvable."
    )

# suppression

def erase_receipt(
    receipt: ExpenseReceipt,
):
    if receipt.storage_key:
        remove_receipt(
            receipt.storage_key
        )
