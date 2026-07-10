"""
Configuration Base de Donnée
Connexion à la base de données avec SQLAlchemy 
Moteur, Sessions, Classe Base, Dépendance FastAPI et Création des tables.

1. Se connecter à PostgreSQL
2. Gérer le pool de connexions
3. Créer les sessions SQLAlchemy
4. Fournir une session aux routes FastAPI avec get_db()
5. Créer les tables inexistantes avec create_tables()
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.core.config import settings

# Création du moteur SQLAlchemy
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=10,
)

# Fabrique de sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Classe de base des modèles
class Base(DeclarativeBase):
    pass

# Dépendance FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def create_tables():
    Base.metadata.create_all(bind=engine)
