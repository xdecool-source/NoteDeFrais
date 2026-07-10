"""
Utilitaires de gestion des noms de fichiers.
"""

import re
import unicodedata


def normalize_filename(filename: str) -> str:
    """
    Nettoie un nom de fichier afin qu'il soit
    compatible avec tous les systèmes de stockage.
    """

    if not filename:
        return ""

    # Suppression des accents
    filename = unicodedata.normalize("NFKD", filename)
    filename = filename.encode("ascii", "ignore").decode("ascii")

    # Suppression des espaces inutiles
    filename = filename.strip()

    # Caractères interdits
    filename = re.sub(
        r'[\\/:*?"<>|]',
        "_",
        filename,
    )

    # Espaces -> underscore
    filename = re.sub(
        r"\s+",
        "_",
        filename,
    )

    return filename
