"""
Routes d'archivage des justificatifs.

Ce fichier gère :

- le téléchargement des justificatifs dans une archive ZIP ;
- la confirmation de l'archivage ;
- la suppression des données binaires de PostgreSQL.

Administrateur uniquement.
"""

from fastapi import (APIRouter, Depends, HTTPException,)
from fastapi.responses import Response

from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin
from app.database import get_db
from app.models.user import User
from app.services.receipt_archive_service import (
    create_receipts_archive,
    clear_archived_receipts,
)

# routeur
# Le préfixe /expenses sera ajouté dans __init__.py.

router = APIRouter()

# telechargement de l'archive zip
# administrateur uniquement

@router.get("/archive/{year}")
async def download_receipts_archive(
    year: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    # creation du zip

    zip_content, archived_count = create_receipts_archive(
        db=db,
        year=year,
    )

    # nom du fichier

    filename = (
        f"Archives_Justificatifs_"
        f"{year}_{year + 1}.zip"
    )

    # telechargement

    return Response(
        content=zip_content,
        media_type="application/zip",
        headers={
            "Content-Disposition":
                f'attachment; filename="{filename}"',

            "X-Receipt-Count":
                str(archived_count),
        },
    )

# confirmation de l'archivage
# Après vérification du ZIP par l'administrateur,
# cette route supprime les données binaires de PostgreSQL.
# administrateur uniquement

@router.post("/archive/{year}/confirm")
async def confirm_receipts_archive(
    year: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    try:

        # suppression des donnees binaires

        cleared_count = clear_archived_receipts(
            db=db,
            year=year,
        )

        # retour

        return {
            "success": True,
            "exercise": f"{year}-{year + 1}",
            "cleared_count": cleared_count,
            "message": (
                f"{cleared_count} justificatif(s) "
                "supprimé(s) de la base de données."
            ),
        }
    except Exception as error:

        # annulation de la transaction en cas d'erreur

        db.rollback()

        # erreur http

        raise HTTPException(
            status_code=500,
            detail=(
                "Erreur lors de la suppression "
                "des données binaires : "
                + str(error)
            ),
        )
