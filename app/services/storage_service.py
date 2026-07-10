"""
Service de stockage Cloudflare R2.
envoyer un fichier ;
télécharger un fichier ;
supprimer un fichier ;
vérifier son existence

Toutes les opérations sur les fichiers
passent par ce service.
"""

from io import BytesIO
from botocore.client import Config
from app.core.config import settings
from app.core.file_utils import normalize_filename

import boto3

# client r2 cloudflare

_client = boto3.client(
    "s3",
    endpoint_url=settings.R2_ENDPOINT,
    aws_access_key_id=settings.R2_ACCESS_KEY,
    aws_secret_access_key=settings.R2_SECRET_KEY,
    config=Config(
        signature_version="s3v4",
    ),
    region_name="auto",
)

# envoi d'un fichier

def upload_file(
    *,
    content: bytes,
    key: str,
    content_type: str,
):

    _client.upload_fileobj(
        Fileobj=BytesIO(content),
        Bucket=settings.R2_BUCKET,
        Key=key,
        ExtraArgs={
            "ContentType": content_type,
        },
    )

# telechargement

def download_file(
    key: str,
) -> bytes:
    buffer = BytesIO()
    _client.download_fileobj(
        settings.R2_BUCKET,
        key,
        buffer,
    )
    return buffer.getvalue()

# suppression

def delete_file(
    key: str,
):
    _client.delete_object(
        Bucket=settings.R2_BUCKET,
        Key=key,
    )

# existence

def file_exists(
    key: str,
) -> bool:
    try:
        _client.head_object(
            Bucket=settings.R2_BUCKET,
            Key=key,
        )
        return True
    except Exception:
        return False
    
# enregistrement d'un justificatif

def save_receipt(
    *,
    expense,
    receipt_id: int,
    filename: str,
    content: bytes,
    content_type: str,
) -> str:

    year = expense.expense_date.strftime("%Y")
    month = expense.expense_date.strftime("%Y-%m")
    # Nettoyage du nom de fichier
    safe_filename = normalize_filename(filename)
    
    storage_key = (
        f"{settings.R2_PREFIX}/"
        f"{settings.R2_EXPENSE_FOLDER}/"
        f"{year}/"
        f"{month}/"
        f"NDF-{expense.id:06d}/"
        f"JUSTIF-{receipt_id:06d}_{safe_filename}"
    )

    upload_file(
        content=content,
        key=storage_key,
        content_type=content_type,
    )

    return storage_key

# lecture d'un justificatif

def load_receipt(
    storage_key: str,
) -> bytes:

    return download_file(storage_key)

# suppression d'un justificatif

def remove_receipt(
    storage_key: str,
):

    delete_file(storage_key)
