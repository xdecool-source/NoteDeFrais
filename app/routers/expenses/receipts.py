"""
Routes de gestion des justificatifs.

Ce fichier gère :

- l'ajout d'un justificatif ;
- l'affichage d'un justificatif ;
- le téléchargement d'un justificatif ;
- la suppression d'un justificatif.
"""

import hashlib
import time

from urllib.parse import quote

from fastapi import (APIRouter, Depends, File, HTTPException, UploadFile,)
from fastapi.responses import Response

from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db

from app.models.expense import Expense
from app.models.expense_item import ExpenseItem
from app.models.expense_receipt import ExpenseReceipt
from app.models.enums import ExpenseStatus
from app.models.user import User

from app.services.storage_service import (
    save_receipt,
    load_receipt,
    remove_receipt,
)

# routeur
# Le préfixe /expenses sera ajouté dans __init__.py.

router = APIRouter()

import time

def chrono(t0, etape):
    t1 = time.perf_counter()
    print(f"{etape:<30} : {t1 - t0:.3f} s")
    return t1

# ajouter un justificatif
t0 = time.perf_counter()
@router.post(
    "/{expense_id}/items/{item_id}/receipts"
)
    
async def upload_receipt(
    expense_id: int,
    item_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # recherche de la note
    # Seul le propriétaire peut ajouter un justificatif.

    expense = (
        db.query(Expense)
        .filter(
            Expense.id == expense_id,
            Expense.user_id == current_user.id,
        )
        .first()
    )

    # note introuvable

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Note de frais introuvable",
        )

    # verification du statut
    # Un justificatif peut uniquement être ajouté
    # à une note en brouillon.

    if expense.status != ExpenseStatus.DRAFT:

        raise HTTPException(
            status_code=400,
            detail=(
                "Les justificatifs peuvent uniquement "
                "être ajoutés à une note en brouillon"
            ),
        )

    # recherche de la ligne de frais

    expense_item = (
        db.query(ExpenseItem)
        .filter(
            ExpenseItem.id == item_id,
            ExpenseItem.expense_id == expense.id,
        )
        .first()
    )

    # ligne introuvable

    if expense_item is None:
        raise HTTPException(
            status_code=404,
            detail="Ligne de frais introuvable",
        )

    # types de fichiers autorises

    allowed_content_types = {
        "application/pdf",
        "image/jpeg",
        "image/png",
    }

    if file.content_type not in allowed_content_types:
        raise HTTPException(
            status_code=400,
            detail=(
                "Format de fichier non autorisé. "
                "Formats acceptés : PDF, JPEG, PNG."
            ),
        )

    # lecture du fichier
    t0 = time.perf_counter()

    file_data = await file.read()
    # chrono(t0,"Lecture fichier")
    
    # fichier vide

    if not file_data:
        raise HTTPException(
            status_code=400,
            detail="Le fichier est vide",
        )

    # taille maximale : 10 mo

    max_file_size = 10 * 1024 * 1024


    if len(file_data) > max_file_size:
        raise HTTPException(
            status_code=400,
            detail=(
                "Le fichier dépasse la taille maximale "
                "autorisée de 10 Mo"
            ),
        )

    # calcul du hash sha-256

    file_hash = hashlib.sha256(
        file_data
    ).hexdigest()
    # chrono(t0,"Calcul SHA256")
    

    # creation du justificatif
    
    receipt = ExpenseReceipt(
        expense_item_id=expense_item.id,
        original_filename=(
            file.filename or "justificatif"),
        content_type=file.content_type,
        file_size=len(file_data),
        file_hash=file_hash,
    )
    # chrono(t0,"Création objet Receipt")
    # enregistrement
    # premier enregistrement
    # permet d'obtenir l'identifiant

    db.add(receipt)
    # chrono(t0,"db.add")
    db.commit()
    # chrono(t0,"1er commit")
    db.refresh(receipt)
    # chrono(t0,"db.refresh")

    # stockage du fichier

    receipt.storage_key = save_receipt(
        expense=expense,
        receipt_id=receipt.id,
        filename=receipt.original_filename,
        content=file_data,
        content_type=receipt.content_type,
    )
    
    # chrono(t0,"Upload Cloudflare") 
    db.commit()
    # chrono(t0,"Commit final")
    db.refresh(receipt)
    
    return {
        "success": True,
        "receipt_id": receipt.id,
        "filename": receipt.original_filename,
        "file_size": receipt.file_size,
    }
    
    
# liste des justificatifs d'une ligne de frais

@router.get(
    "/{expense_id}/items/{item_id}/receipts"
)
async def list_receipts(
    expense_id: int,
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # recherche de la ligne de frais

    expense_item = (
        db.query(ExpenseItem)
        .join(Expense)
        .filter(
            ExpenseItem.id == item_id,
            Expense.id == expense_id,
        )
        .first()
    )

    # ligne introuvable

    if expense_item is None:
        raise HTTPException(
            status_code=404,
            detail="Ligne de frais introuvable",
        )

    # vérification des droits

    if (
        expense_item.expense.user_id != current_user.id
        and not current_user.is_admin
    ):
        raise HTTPException(
            status_code=403,
            detail="Accès interdit",
        )

    # retour JSON

    return [
        {
            "id": receipt.id,
            "filename": receipt.original_filename,
            "size": receipt.file_size,
            "content_type": receipt.content_type,
        }
        for receipt in expense_item.receipts
    ]
    
# voir un justificatif

@router.get(
    "/{expense_id}/receipts/{receipt_id}/view"
)
async def view_receipt(
    expense_id: int,
    receipt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # recherche du justificatif

    receipt = (
        db.query(ExpenseReceipt)
        .join(ExpenseItem)
        .join(Expense)
        .filter(
            ExpenseReceipt.id == receipt_id,
            Expense.id == expense_id,
        )
        .first()
    )

    # justificatif introuvable

    if receipt is None:
        raise HTTPException(
            status_code=404,
            detail="Justificatif introuvable",
        )

    # verification des droits
    # Le propriétaire de la note et l'administrateur
    # peuvent consulter le justificatif.

    if (
        receipt.expense_item.expense.user_id
        != current_user.id
        and not current_user.is_admin
    ):

        raise HTTPException(
            status_code=403,
            detail="Accès interdit",
        )

    # fichier archive

    if receipt.storage_key is None:

        raise HTTPException(
            status_code=404,
            detail=(
                "Le fichier n'est plus "
                "disponible en base"
            ),
        )

    # affichage dans le navigateur

    file_data = load_receipt(receipt.storage_key)

    return Response(
        content=file_data,
        media_type=receipt.content_type,
        headers={
            "Content-Disposition":
                "inline; filename*=UTF-8''"
                + quote(receipt.original_filename)
        },
    )

# telecharger un justificatif

@router.get(
    "/{expense_id}/receipts/{receipt_id}/download"
)
async def download_receipt(
    expense_id: int,
    receipt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    
    # recherche du justificatif

    receipt = (
        db.query(ExpenseReceipt)
        .join(ExpenseItem)
        .join(Expense)
        .filter(
            ExpenseReceipt.id == receipt_id,
            Expense.id == expense_id,
        )
        .first()
    )

    # justificatif introuvable

    if receipt is None:
        raise HTTPException(
            status_code=404,
            detail="Justificatif introuvable",
        )

    # verification des droits

    if (
        receipt.expense_item.expense.user_id
        != current_user.id
        and not current_user.is_admin
    ):

        raise HTTPException(
            status_code=403,
            detail="Accès interdit",
        )

    # fichier archive

    if receipt.storage_key is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Le fichier n'est plus "
                "disponible en base"
            ),
        )

    # telechargement

    file_data = load_receipt(receipt.storage_key)

    return Response(
        content=file_data,
        media_type=receipt.content_type,
        headers={
            "Content-Disposition":
                "attachment; filename*=UTF-8''"
                + quote(receipt.original_filename)
        },
    )

# supprimer un justificatif

@router.delete(
    "/{expense_id}/receipts/{receipt_id}"
)
async def delete_receipt(
    expense_id: int,
    receipt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # recherche du justificatif
    # Seul le propriétaire de la note peut le supprimer.

    receipt = (
        db.query(ExpenseReceipt)
        .join(ExpenseItem)
        .join(Expense)
        .filter(
            ExpenseReceipt.id == receipt_id,
            Expense.id == expense_id,
            Expense.user_id == current_user.id,
        )
        .first()
    )

    # justificatif introuvable

    if receipt is None:
        raise HTTPException(
            status_code=404,
            detail="Justificatif introuvable",
        )

    # recuperation de la note

    expense = receipt.expense_item.expense

    # verification du statut

    if expense.status != ExpenseStatus.DRAFT:
        raise HTTPException(
            status_code=400,
            detail=(
                "Un justificatif peut uniquement "
                "être supprimé d'une note en brouillon"
            ),
        )

    # suppression

    # suppression du fichier (Cloudflare R2 ou autre)

    if receipt.storage_key:
        remove_receipt(receipt.storage_key)
        
    # suppression de l'enregistrement en base

    db.delete(receipt)

    db.commit()

    # retour

    return {
        "success": True,
        "receipt_id": receipt_id,
    }
