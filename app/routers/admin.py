"""
- Maintenance (/maintenance)
Affiche une page de maintenance.
Ppage d'administration.
- Purge (/purge)
Affiche un formulaire demandant une année.
Lorsque le formulaire est envoyé (POST /purge), 
il appelle purge_receipts(db, year) qui supprime les reçus correspondant à cette année 
(ou selon la logique définie dans ce service).
Affiche ensuite le nombre d'éléments supprimés.
- Export Excel (/excel)
Affiche un formulaire avec une date de début et une date de fin.
Lors de la validation, il appelle create_excel_export(...).
Génère un fichier Excel et le renvoie automatiquement au navigateur pour téléchargement.
- Nettoyage de la base (/cleanup)
Affiche une page de nettoyage.
Au clic sur le bouton, appelle cleanup_database(db).
Effectue un nettoyage de la base de données (par exemple suppression d'enregistrements inutiles, 
orphelins, etc.) et affiche combien d'éléments ont été supprimés.

"""

from datetime import date, datetime

from fastapi import (APIRouter, Depends, Form, Request,)
from fastapi.templating import Jinja2Templates
from fastapi.responses import (HTMLResponse, Response, RedirectResponse,)

from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin
from app.database import get_db
from app.models.user import User
from app.services.receipt_purge_service import (purge_receipts,)
from app.services.excel_export_service import (create_excel_export,)
from app.services.database_cleanup_service import (cleanup_database,)

router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)

# page maintenance

@router.get(
    "/maintenance",
    response_class=HTMLResponse,
)
def maintenance(
    request: Request,
    current_admin: User = Depends(get_current_admin),
):
    return templates.TemplateResponse(
        "admin/maintenance.html",
        {
            "request": request,
        },
    )

# page purge

@router.get(
    "/purge",
    response_class=HTMLResponse,
)
def purge_page(
    request: Request,
    current_admin: User = Depends(get_current_admin),
):
    return templates.TemplateResponse(
        "admin/purge.html",
        {
            "request": request,
            "current_year": datetime.now().year,
        },
    )

# execution purge

@router.post("/purge")
def purge_execute(
    request: Request,
    year: int = Form(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    count = purge_receipts(
        db=db,
        year=year,
    )
    return templates.TemplateResponse(
        "admin/purge.html",
        {
            "request": request,
            "current_year": datetime.now().year,
            "count": count,
        },
    )
    

# page export excel

@router.get(
    "/excel",
    response_class=HTMLResponse,
)
def excel_page(
    request: Request,
    current_admin: User = Depends(get_current_admin),
):
    return templates.TemplateResponse(
        "admin/excel.html",
        {
            "request": request,
            "current_year": datetime.now().year,
        },
    )

# telechargement excel

@router.post("/excel")
def excel_download(
    start_date: date = Form(...),
    end_date: date = Form(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    content = create_excel_export(
        db=db,
        start_date=start_date,
        end_date=end_date,
    )
    filename = (
        f"Export_{start_date}_{end_date}.xlsx"
    )
    return Response(
        content=content,
        media_type=(
            "application/vnd.openxmlformats-"
            "officedocument.spreadsheetml.sheet"
        ),
        headers={
            "Content-Disposition":
                f'attachment; filename="{filename}"'
        },
    )
    
# page nettoyage de la base

@router.get(
    "/cleanup",
    response_class=HTMLResponse,
)
def cleanup_page(
    request: Request,
    current_admin: User = Depends(get_current_admin),
):
    return templates.TemplateResponse(
        "admin/cleanup.html",
        {
            "request": request,
        },
    )

# execution du nettoyage

@router.post("/cleanup")
def cleanup_execute(
    request: Request,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    deleted = cleanup_database(db)
    return templates.TemplateResponse(
        "admin/cleanup.html",
        {
            "request": request,
            "deleted": deleted,
        },
    )
