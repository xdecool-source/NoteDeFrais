"""
Déclaration des énumérations (Enum), 
listes fermées de valeurs autorisées.
ex :  expense.status = ExpenseStatus.DRAFT
au lieu de expense.status = "BROUILLONN" avec une faute !!!
"""

from enum import Enum

class ExpenseStatus(str, Enum):
    DRAFT = "BROUILLON"
    SUBMITTED = "SOUMISE"
    APPROVED = "VALIDEE"
    REJECTED = "REFUSEE"
    PAID = "PAYEE"

class ExpenseItemType(str, Enum):
    KM = "DEPLACEMENT"
    FOURNITURE = "FOURNITURES"
    REPAS = "REPAS"
    HOTEL = "HEBERGEMENT"
    PARKING = "PARKING"
    PEAGE = "PEAGE"
    OTHER = "AUTRE"