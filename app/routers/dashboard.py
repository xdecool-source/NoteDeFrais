"""
Définition route du tableau de bord
Son fonctionnement :

Utilisateur
GET /dashboard/
Vérification de l'utilisateur connecté
Chargement du template dashboard/index.html
Envoi de l'utilisateur au template
Affichage de la page HTML

"""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.dependencies import get_current_user
from app.core.template import template_context
from app.models.user import User

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    return templates.TemplateResponse(
            "dashboard/index.html",
            template_context(
                request,
                user=current_user,
            ),
        )
