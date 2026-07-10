"""
Prapartion des données à envoyées aux templates HTML Jinja2.
Ajoute request au contexte, puis les autres données comme user, expenses, km_rate, etc.

"""

from fastapi import Request
from app.core.config import settings

def template_context(request: Request, **kwargs):
    """
    Contexte commun à tous les templates.
    """
    context = {
        "request": request,
        "APP_VERSION": settings.APP_VERSION,
    }
    context.update(kwargs)
    return context