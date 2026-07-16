"""
Routes d'export comptable des notes de frais.
routeur = reçoit la demande du navigateur : export.py
service = effectue le travail : expense_export_service.py
puis routeur = renvoie le résultat au navigateur
Ce fichier gère :

- la sélection des notes payées ;
- la sélection par période ;
- l'export CSV ;
- le téléchargement du fichier.

Gère la partie HTTP/FastAPI
Reçoit la demande venant du navigateur, récupère start_date et end_date, 
Vérifie les dates, appelle le service, puis renvoie le fichier CSV au navigateur.

Administrateur uniquement.
"""

from datetime import date

from fastapi import (APIRouter, Depends, HTTPException, Query,)
from fastapi.responses import Response

from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin
from app.database import get_db
from app.models.user import User
from app.services.expense_export_service import export_paid_expenses
from app.services.expense_export_zip_service import create_export_zip

# Le préfixe /expenses sera ajouté dans __init__.py.

router = APIRouter()

# export comptable des notes de frais
# administrateur uniquement

@router.get("/export/download")
def export_expenses(
    start_date: date = Query(...),
    end_date: date = Query(...),
    format: str = Query("zip"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    # verification des dates

    if start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail=(
                "La date de début doit être "
                "antérieure à la date de fin."
            ),
        )

    # generation de l'export

    if format == "csv":
        file_content, exported_lines = export_paid_expenses(
            db=db,
            start_date=start_date,
            end_date=end_date,
        )
        filename = (
            f"Export_{start_date}_{end_date}.csv"
        )
        media_type = "text/csv; charset=utf-8"
    else:
        file_content, exported_lines = create_export_zip(
            db=db,
            start_date=start_date,
            end_date=end_date,
        )
        filename = (
            f"Export_{start_date}_{end_date}.zip"
        )
        media_type = "application/zip"

    # telechargement du fichier

    return Response(
        content=file_content,
        media_type=media_type,
        headers={
            "Content-Disposition":
                f'attachment; filename="{filename}"',

            "X-Exported-Lines":
                str(exported_lines),
        },
    )
