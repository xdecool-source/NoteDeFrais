"""
Ce fichier est le routeur d’administration des utilisateurs
Permet à l'admin de gérer les comptes utilisateurs depuis l’interface web.

Il gère principalement quatre fonctionnalités : 
afficher les utilisateurs
créer un utilisateur
modifier un utilisateur
réinitialiser son mot de passe

"""

from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    Request,
    status,
)

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin
from app.core.template import template_context
from app.database import get_db
from app.models.user import User
from app.core.security import get_password_hash

# router

router = APIRouter(
    prefix="/users",
    tags=["Utilisateurs"],
)

# templates

templates = Jinja2Templates(
    directory="app/templates"
)

# liste des utilisateurs

@router.get(
    "/",
    response_class=HTMLResponse,
)
async def users_list(
    request: Request,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    # recherche des utilisateurs

    users = db.scalars(
        select(User)
        .order_by(
            User.full_name
        )
    ).all()

    # affichage du template

    return templates.TemplateResponse(
        "users/list.html",
        template_context(
            request,
            user=current_admin,
            users=users,
        ),
    )
    
# formulaire nouvel utilisateur

@router.get(
    "/new",
    response_class=HTMLResponse,
)
async def new_user_form(
    request: Request,
    current_admin: User = Depends(get_current_admin),
):

    return templates.TemplateResponse(
        "users/form.html",
        template_context(
            request,
            user=current_admin,
            account=None,
        ),
    )

# creation d'un utilisateur

@router.post("/new")
async def create_user(
    username: str = Form(...),
    email: str = Form(...),
    full_name: str = Form(...),
    password: str = Form(...),
    password_confirmation: str = Form(...),
    is_active: bool = Form(False),
    is_admin: bool = Form(False),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    # nettoyage

    username = username.strip()
    email = email.strip().lower()
    full_name = full_name.strip()

    # verification des mots de passe

    if password != password_confirmation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Les mots de passe ne correspondent pas",
        )

    # verification identifiant

    existing_username = db.scalar(
        select(User).where(
            User.username == username
        )
    )
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cet identifiant existe déjà",
        )

    # verification email

    existing_email = db.scalar(
        select(User).where(
            User.email == email
        )
    )
    if existing_email:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cette adresse email existe déjà",
        )

    # creation

    account = User(
        username=username,
        email=email,
        full_name=full_name,
        hashed_password=get_password_hash(password),
        is_active=is_active,
        is_admin=is_admin,
    )
    db.add(account)
    db.commit()
    return RedirectResponse(
        url="/users/",
        status_code=status.HTTP_303_SEE_OTHER,
    )
    
# formulaire modification utilisateur

@router.get(
    "/{user_id}/edit",
    response_class=HTMLResponse,
    )
async def edit_user_form(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
    ):
    account = db.get(
        User,
        user_id,
    )
    if account is None:
        raise HTTPException(
            status_code=404,
            detail="Utilisateur introuvable",
        )
    return templates.TemplateResponse(
        "users/edit.html",
        template_context(
            request,
            user=current_admin,
            account=account,
        ),
    )

# modification utilisateur

@router.post("/{user_id}/edit")
async def update_user(
    user_id: int,
    username: str = Form(...),
    email: str = Form(...),
    full_name: str = Form(...),
    is_active: bool = Form(False),
    is_admin: bool = Form(False),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    # RECHERCHE DE L'UTILISATEUR

    account = db.get(
        User,
        user_id,
    )
    if account is None:
        raise HTTPException(
            status_code=404,
            detail="Utilisateur introuvable",
        )

    # nettoyage

    username = username.strip()
    email = email.strip().lower()
    full_name = full_name.strip()

    # verification identifiant

    existing_username = db.scalar(
        select(User).where(
            User.username == username,
            User.id != user_id,
        )
    )
    if existing_username:
        raise HTTPException(
            status_code=400,
            detail="Cet identifiant existe déjà",
        )

    # verification email

    existing_email = db.scalar(
        select(User).where(
            User.email == email,
            User.id != user_id,
        )
    )
    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Cette adresse email existe déjà",
        )

    # securite : admin connecte

    if account.id == current_admin.id:

        # L'administrateur connecté ne peut pas
        # désactiver son propre compte.
        is_active = True
        # L'administrateur connecté ne peut pas
        # retirer son propre rôle administrateur.
        is_admin = True

    # modification

    account.username = username
    account.email = email
    account.full_name = full_name
    account.is_active = is_active
    account.is_admin = is_admin
    db.commit()
    return RedirectResponse(
        url="/users/",
        status_code=303,
    )
    
# reinitialisation du mot de passe

@router.post("/{user_id}/reset-password")
async def reset_user_password(
    user_id: int,
    password: str = Form(...),
    password_confirmation: str = Form(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    account = db.get(
        User,
        user_id,
    )
    if account is None:
        raise HTTPException(
            status_code=404,
            detail="Utilisateur introuvable",
        )
    if password != password_confirmation:
        raise HTTPException(
            status_code=400,
            detail="Les mots de passe ne correspondent pas",
        )
    if len(password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Le mot de passe doit contenir au moins 8 caractères",
        )
    account.hashed_password = get_password_hash(
        password
    )
    db.commit()
    return RedirectResponse(
        url=f"/users/{user_id}/edit",
        status_code=303,
    )
    