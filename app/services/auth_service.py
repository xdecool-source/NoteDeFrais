"""
Authentifie l’utilisateur
Vérifie  mot de passe 
Génère un JWT avec durée de vie : voir ACCESS_TOKEN_EXPIRE_MINUTES

"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import (
    verify_password,
    create_access_token,
)

def authenticate_user(
    db: Session,
    username: str,
    password: str,
) -> str | None:
    
    """
    Vérifie les identifiants et retourne un JWT.
    """

    user = db.scalar(
        select(User).where(User.username == username)
    )
    if user is None:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return create_access_token(
        {
            "sub": user.username,
            "is_admin": user.is_admin,
        }
    )