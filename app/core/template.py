"""
Prapartion des données à envoyées aux templates HTML Jinja2.
Ajoute request au contexte, puis les autres données comme user, expenses, km_rate, etc.

"""

from fastapi import Request

def template_context(request: Request, **kwargs):
    """
    Contexte commun à tous les templates.
    """
    context = {
        "request": request,
    }
    context.update(kwargs)
    return context