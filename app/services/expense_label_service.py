"""
Service de construction des libellés dans les exports excel
des notes de frais.
"""

from app.models.expense import Expense


def build_expense_label(expense: Expense) -> str:
    """
    Construit le libellé utilisé
    dans les exports.
    """

    if not expense.items:
        return expense.user.full_name

    note_type = expense.items[0].item_type.name
    full_name = expense.user.full_name

    if note_type == "KM":
        total_km = sum(
            item.kilometers or 0
            for item in expense.items
        )

        departure = (
            expense.items[0].departure or "?"
        )

        arrival = (
            expense.items[-1].arrival or "?"
        )

        return (
            f"{full_name} - Déplacement : "
            f"{departure} → "
            f"{arrival} "
            f"({total_km:.1f} km)"
        )

    if note_type == "HOTEL":
        return (
            f"{full_name} - Hôtel : "
            f"{expense.label}"
        )

    if note_type == "REPAS":
        return (
            f"{full_name} - Repas : "
            f"{expense.label}"
        )

    if note_type == "FOURNITURE":
        return (
            f"{full_name} - Fournitures : "
            f"{expense.label}"
        )

    if note_type == "PEAGE":
        return (
            f"{full_name} - Péage : "
            f"{expense.label}"
        )

    if note_type == "PARKING":
        return (
            f"{full_name} - Parking : "
            f"{expense.label}"
        )

    return (
        f"{full_name} - "
        f"{expense.label}"
    )
    
    