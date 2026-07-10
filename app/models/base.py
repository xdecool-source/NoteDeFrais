"""
Dédinition d'une classe de base commune à tous tes modèles SQLAlchemy. 
Son but est d’éviter de répéter les colonnes id, created_at et updated_at dans chaque modèle.

"""

from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class BaseModel(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    