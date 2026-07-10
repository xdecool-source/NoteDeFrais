"""
Routes d'administration des notes de frais.

Ce fichier gère :
- l'affichage des notes en attente de validation ;
- l'accès à la page d'export comptable ;
- l'accès à l'archivage des justificatifs.
Administrateur uniquement.
"""

from datetime import datetime

from fastapi import (APIRouter, Depends, Request,)
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin
from app.core.template import template_context
from app.database import get_db
from app.models.expense import Expense
from app.models.enums import ExpenseStatus
from app.models.user import User
from app.routers.expenses.common import templates


# routeur
# Le préfixe /expenses sera ajouté dans __init__.py.

router = APIRouter()

# notes a valider
# administrateur uniquement

@router.get(
    "/validate",
    response_class=HTMLResponse,
)
async def expenses_to_validate(
    request: Request,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    # recherche des notes soumises

    expenses = (
        db.query(Expense)
        .filter(
            Expense.status == ExpenseStatus.SUBMITTED
        )
        .order_by(
            Expense.created_at.desc()
        )
        .all()
    )

    # affichage

    return templates.TemplateResponse(
        "expenses/validate.html",
        template_context(
            request,
            user=current_admin,
            expenses=expenses,
            current_year=datetime.now().year,
        ),
    )
