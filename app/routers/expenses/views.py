"""
Routes principales des notes de frais.

Ce fichier gère :

- la liste des notes ;
- l'affichage du formulaire de création ;
- la création d'une note ;
- l'affichage du formulaire de modification ;
- la modification d'une note ;
- le détail d'une note.
"""

from fastapi import (APIRouter, Depends, HTTPException, Request,)
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.dependencies import get_current_user
from app.core.template import template_context
from app.database import get_db
from app.models.expense import Expense
from app.models.user import User
from app.schemas.expense import ExpenseCreate

from app.services.expense_service import (
    create_expense,
    update_expense,
)

from app.routers.expenses.common import templates

# routeur
# Le prefix /expenses sera ajouté dans __init__.py.
# Il ne faut donc pas le mettre ici.

router = APIRouter()

# LISTE DES NOTES DE FRAIS

@router.get(
    "/",
    response_class=HTMLResponse,
)
async def expense_list(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # ADMINISTRATEUR
    # L'administrateur voit toutes les notes.

    if current_user.is_admin:
        expenses = (
            db.query(Expense)
            .order_by(
                Expense.created_at.desc()
            )
            .all()
        )

    # utilisateur normal
    # L'utilisateur voit uniquement ses propres notes.

    else:
        expenses = (
            db.query(Expense)
            .filter(
                Expense.user_id == current_user.id
            )
            .order_by(
                Expense.created_at.desc()
            )
            .all()
        )

    # affichage

    return templates.TemplateResponse(
        "expenses/index.html",
        template_context(
            request,
            user=current_user,
            expenses=expenses,
        ),
    )
    
    
@router.get(
    "/export",
    response_class=HTMLResponse,
)
async def export_page(
    request: Request,
    current_user: User = Depends(get_current_user),
):

    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Accès interdit",
        )

    return templates.TemplateResponse(
        "expenses/export.html",
        template_context(
            request,
            user=current_user,
        ),
    )
    
    
    
    
    
    
    
    
    
    

# formulaire nouvelle note de frais

@router.get(
    "/new",
    response_class=HTMLResponse,
)
async def new_expense(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    return templates.TemplateResponse(
        "expenses/new.html",
        template_context(
            request,
            user=current_user,
            km_rate=settings.KM_RATE,
        ),
    )

# creation d'une nouvelle note

@router.post("/")
async def save_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    try:

        new_expense = create_expense(
            db=db,
            expense_data=expense,
            user_id=current_user.id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    return {
        "success": True,
        "expense_id": new_expense.id,
    }

# formulaire de modification d'une note

@router.get(
    "/{expense_id}/edit",
    response_class=HTMLResponse,
)
async def edit_expense(
    expense_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # recherche de la note
    # Seul le propriétaire peut modifier sa note.

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

    # affichage du formulaire

    return templates.TemplateResponse(
        "expenses/new.html",
        template_context(
            request,
            user=current_user,
            expense=expense,
            km_rate=settings.KM_RATE,
        ),
    )

# enregistrement de la modification

@router.put("/{expense_id}")
async def update_expense_route(
    expense_id: int,
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    updated = update_expense(
        db=db,
        expense_id=expense_id,
        expense_data=expense,
        user_id=current_user.id,
    )

    # note introuvable

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Note de frais introuvable",
        )

    # note supprimee
    # Le service supprime la note lorsqu'elle ne contient
    # plus aucune ligne.

    if updated == "deleted":
        return {
            "success": True,
            "deleted": True,
            "message": "Note de frais supprimée",
        }

    # note modifiee

    return {
        "success": True,
        "deleted": False,
        "expense_id": updated.id,
    }

# detail d'une note
# Le propriétaire peut voir sa note.
# L'administrateur peut voir toutes les notes.

@router.get(
    "/{expense_id}",
    response_class=HTMLResponse,
)
async def expense_detail(
    expense_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
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

    # verification des droits

    if (
        expense.user_id != current_user.id
        and not current_user.is_admin
    ):
        raise HTTPException(
            status_code=403,
            detail="Accès interdit",
        )

    # affichage

    return templates.TemplateResponse(
        "expenses/detail.html",
        template_context(
            request,
            user=current_user,
            expense=expense,
        ),
    )
