"""
Routeur principal des notes de frais.

Ce fichier rassemble les différents routeurs :

- vues et gestion des notes ;
- administration ;
- workflow ;
- justificatifs ;
- export comptable ;
- archivage.
"""

from fastapi import APIRouter

from app.routers.expenses.admin import (router as admin_router,)
from app.routers.expenses.export import (router as export_router,)
from app.routers.expenses.archive import (router as archive_router,)
from app.routers.expenses.workflow import (router as workflow_router,)
from app.routers.expenses.receipts import (router as receipts_router,)
from app.routers.expenses.views import (router as views_router,)

# routeur principal

router = APIRouter(
    prefix="/expenses",
    tags=["Notes de frais"],
)

# routes specifiques
# on place les routes spécifiques en premier.

router.include_router(admin_router)
router.include_router(export_router)
router.include_router(archive_router)

# workflow

router.include_router(workflow_router)

# justificatifs

router.include_router(receipts_router)

# routes generales
#
# views_router contient notamment :
# /
# /new
# /{expense_id}/edit
# /{expense_id}
# on le place donc en dernier.

router.include_router(views_router)