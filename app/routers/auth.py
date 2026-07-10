"""
Gestion connexion déconnexion 
Création d’un administrateur
Chiffre le mot de passe avant de l’enregistrer.
Définit is_admin=True et is_active=True.
Enregistre l’administrateur dans la base de données.

"""

from fastapi import APIRouter, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import SessionLocal
from app.models.user import User
from app.services.auth_service import authenticate_user

from app.core.template import template_context
from app.core.config import settings
from app.core.security import get_password_hash

router = APIRouter(
    prefix="/auth",
    tags=["Authentification"]
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):

    return templates.TemplateResponse(
        "auth/login.html",
        template_context(request),
    )

@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):

    db = SessionLocal()
    try:
        token = authenticate_user(
            db,
            username,
            password,
        )
        if token is None:
            return templates.TemplateResponse(
            "auth/login.html",
            template_context(
                request,
                error="Utilisateur ou mot de passe incorrect, ou compte désactivé.",
            ),
            status_code=401,
        )   
        response = RedirectResponse(
            url="/dashboard",
            status_code=status.HTTP_302_FOUND,
        )

        response.set_cookie(
            key=settings.COOKIE_NAME,
            value=token,
            httponly=True,
            samesite="lax",
            secure=False,      # True en production HTTPS
        )
        return response
    finally:
        db.close()
                
@router.get("/create-admin")
def create_admin():
    db: Session = SessionLocal()
    try:
        # Vérifie si l'admin existe déjà
        admin = db.scalar(
            select(User).where(User.username == "admin")
        )
        if admin:
            return {
                "message": "L'administrateur existe déjà."
            }
        admin = User(
            username="admin",
            full_name="Administrateur",
            email="admin@local.fr",
            hashed_password=get_password_hash("admin123"),
            is_admin=True,
            is_active=True,
        )
        db.add(admin)
        db.commit()
        return {
            "message": "Administrateur créé.",
            "username": "admin",
            "password": "admin123",
        }
    finally:
        db.close()
        
@router.get("/logout")
def logout():
    response = RedirectResponse(
        url="/auth/login",
        status_code=302,
    )
    response.delete_cookie(
        settings.COOKIE_NAME
    )
    return response
