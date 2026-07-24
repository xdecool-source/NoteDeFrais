"""
Création tables si necessaire  
Configuration fichiers statiques, 
Ajout les routes (auth, dashboard, expenses)
et définit quelques endpoints comme /, /db et /me.

"""

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.exceptions import HTTPException

from sqlalchemy import text

from app.core.config import settings
from app.core.dependencies import get_current_user
from app.database import create_tables, engine
from app.models.user import User

from app.routers import auth, dashboard, expenses, users, admin

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print("")
    print("✅ NoteDeFrais : Tables créées/vérifiées")
    print("")
    yield
    print("👋 Arrêt de l'application")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(expenses.router)
app.include_router(users.router)
app.include_router(admin.router,prefix="/admin",tags=["Administration"],)


@app.get("/")
async def root():
    return RedirectResponse(
        url="/auth/login",
        status_code=302,
    )

@app.get("/db")
def db_test():
    with engine.connect() as conn:
        version = conn.execute(text("SELECT version()")).scalar()
    return {
        "database": "OK",
        "version": version,
    }

@app.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {
        "username": current_user.username,
        "email": current_user.email,
        "admin": current_user.is_admin,
    }
    

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):

    if exc.status_code == 401:

        # Requête AJAX
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JSONResponse(
                status_code=401,
                content={"detail": "Session expirée"},
            )

        # Requête fetch JSON
        accept = request.headers.get("accept", "")
        if "application/json" in accept:
            return JSONResponse(
                status_code=401,
                content={"detail": "Session expirée"},
            )

        # Navigation normale
        return RedirectResponse(
            "/auth/login",
            status_code=302,
        )

    raise exc