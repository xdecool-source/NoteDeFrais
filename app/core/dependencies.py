"""
Récupère le token JWT dans le cookie
Vérifie et décode le token
Récupère le username contenu dans "sub" 
Cherche l’utilisateur correspondant dans la base de données 
Retourne l’utilisateur connecté avec get_current_user
Vérifie si l’utilisateur est administrateur avec get_current_admin
Identification de l’utilisateur connecté et contrôle les droits administrateur.

"""

from typing import Annotated

from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.database import get_db
from app.models.user import User

DBSession = Annotated[
    Session,
    Depends(get_db),
]

def get_current_user(
    db: DBSession,
    auth_token: str | None = Cookie(default=None),
) -> User:
    if auth_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Non authentifié",
        )
    payload = decode_access_token(auth_token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Jeton invalide",
        )

    username = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Jeton invalide",
        )
    user = db.scalar(
        select(User).where(
            User.username == username
        )
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur introuvable",
        )
        
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Compte utilisateur désactivé",
        )
        
    return user

def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès réservé aux administrateurs",
        )
    return current_user
