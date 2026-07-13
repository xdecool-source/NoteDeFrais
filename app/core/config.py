"""
COOKIE_NAME: str = "auth_token" 
Definition  du nom du cookie utilisé pour stocker le token JWT dans le navigateur.
Attention les valeurs viennent de .env donc fictives dans ce fichier 
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    
    # Application
    
    APP_NAME: str = "Note de Frais"
    APP_VERSION: str = "1.2 Xdc TT Thuirinois"
    DEBUG: bool = True

    # Sécurité
    
    SECRET_KEY: str = "change-moi-par-une-cle-secrete"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    
    COOKIE_NAME: str = "auth_token"
    RECEIPT_ARCHIVE_PATH: str = "archives"
    KM_RATE: float = 0.35
    R2_PREFIX: str = "repository"
    R2_EXPENSE_FOLDER: str = "depenses"

    # Base de données
    
    DATABASE_URL: str
    
    # Cloudflare R2

    R2_ACCOUNT_ID: str = ""
    R2_ENDPOINT: str = ""
    R2_BUCKET: str = ""
    R2_ACCESS_KEY: str = ""
    R2_SECRET_KEY: str = ""
    
    # Chargement du fichier .env
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
settings = Settings()
