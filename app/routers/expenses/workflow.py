"""
Workflow des notes de frais.

Ce fichier gère :

- la soumission d'une note ;
- la validation d'une note ;
- le refus d'une note ;
- le paiement d'une note.
"""

from datetime import datetime, timezone

from fastapi import (APIRouter, Depends, HTTPException,)

from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_current_admin,
    get_current_user,
)
from app.database import get_db
from app.models.expense import Expense
from app.models.enums import ExpenseStatus
from app.models.user import User
from app.schemas.expense import ExpenseReject

# routeur
# Le préfixe /expenses sera ajouté dans __init__.py.

router = APIRouter()

# soumettre une note de frais

@router.post("/{expense_id}/submit")
async def submit_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # recherche de la note
    # L'utilisateur peut uniquement soumettre
    # ses propres notes.

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

    if expense.status != ExpenseStatus.DRAFT:
        raise HTTPException(
            status_code=400,
            detail=(
                "Seule une note en brouillon "
                "peut être soumise"
            ),
        )

    # verification des lignes

    if not expense.items:
        raise HTTPException(
            status_code=400,
            detail=(
                "Impossible de soumettre "
                "une note vide"
            ),
        )

    # modification du statut

    expense.status = ExpenseStatus.SUBMITTED
    expense.submitted_at = datetime.now(
        timezone.utc
    )

    # enregistrement

    db.commit()
    db.refresh(expense)
    return {
        "success": True,
        "expense_id": expense.id,
        "status": expense.status.value,
    }

# valider une note de frais
# administrateur uniquement

@router.post("/{expense_id}/approve")
async def approve_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    # recherche de la note

    expense = (
        db.query(Expense)
        .filter(
            Expense.id == expense_id
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

    if expense.status != ExpenseStatus.SUBMITTED:
        raise HTTPException(
            status_code=400,
            detail=(
                "Seule une note soumise "
                "peut être validée"
            ),
        )

    # modification du statut

    expense.status = ExpenseStatus.APPROVED
    expense.approved_at = datetime.now(
        timezone.utc
    )
    expense.rejection_reason = None

    # enregistrement

    db.commit()
    db.refresh(expense)

    # retour

    return {
        "success": True,
        "expense_id": expense.id,
        "status": expense.status.value,
    }

# refuser une note de frais
# administrateur uniquement

@router.post("/{expense_id}/reject")
async def reject_expense(
    expense_id: int,
    reject_data: ExpenseReject,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    # recherche de la note

    expense = (
        db.query(Expense)
        .filter(
            Expense.id == expense_id
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

    if expense.status != ExpenseStatus.SUBMITTED:
        raise HTTPException(
            status_code=400,
            detail=(
                "Seule une note soumise "
                "peut être refusée"
            ),
        )

    # modification du statut

    expense.status = ExpenseStatus.REJECTED
    expense.rejection_reason = (
        reject_data.rejection_reason.strip()
    )

    # enregistrement

    db.commit()
    db.refresh(expense)

    # retour

    return {
        "success": True,
        "expense_id": expense.id,
        "status": expense.status.value,
        "rejection_reason":
            expense.rejection_reason,
    }

# marquer une note comme payee
# administrateur uniquement

@router.post("/{expense_id}/pay")
async def pay_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    # recherche de la note

    expense = (
        db.query(Expense)
        .filter(
            Expense.id == expense_id
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

    if expense.status != ExpenseStatus.APPROVED:
        raise HTTPException(
            status_code=400,
            detail=(
                "Seule une note validée "
                "peut être payée"
            ),
        )

    # modification du statut

    expense.status = ExpenseStatus.PAID
    expense.paid_at = datetime.now(
        timezone.utc
    )

    # enregistrement

    db.commit()
    db.refresh(expense)

    # retour

    return {
        "success": True,
        "expense_id": expense.id,
        "status": expense.status.value,
    }
