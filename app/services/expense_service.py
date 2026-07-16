"""
Service qui va créer la note de frais dans la base 
Service de création et de modification
des notes de frais.
"""

from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.expense_item import ExpenseItem
from app.schemas.expense import ExpenseCreate
from app.core.config import settings

from fastapi import HTTPException

from app.services.receipt_file_service import (
    erase_receipt,
)


# calcul du montant d'une ligne

def calculate_item_amount(
    item,
    km_rate: float,
) -> float:

    # deplacement

    if item.item_type == "KM":
        kilometers = item.kilometers or 0
        toll_amount = item.toll_amount or 0
        other_amount = item.other_amount or 0

        # Montant kilométrique

        kilometer_amount = (
            kilometers * km_rate
        )

        # Majoration véhicule électrique de 20 %
        # uniquement sur le montant kilométrique

        if item.is_electric_vehicle:
            kilometer_amount *= 1.20

        # Montant total du déplacement

        amount = (
            kilometer_amount
            + toll_amount
            + other_amount
        )
        return round(amount, 2)

    # autres types de frais

    return round(
        item.amount or 0,
        2,
    )   

# validation du type unique de depense

def validate_single_item_type(items) -> None:
    """
    Une note de frais ne peut contenir
    qu'un seul type de dépense.
    """

    if not items:
        return
    first_type = items[0].item_type
    # print("Premier :", first_type)
    for item in items[1:]:

        if item.item_type != first_type:

            raise ValueError(
                "Une note de frais ne peut contenir "
                "qu'un seul type de dépense. "
                "Créez une nouvelle note de frais."
            )
            
# creation d'une note de frais

def create_expense(
    db: Session,
    expense_data: ExpenseCreate,
    user_id: int,
) -> Expense:
    validate_single_item_type(
        expense_data.items
    )
    expense = Expense(
        expense_date=expense_data.expense_date,
        label=expense_data.label,
        total_amount=0,
        user_id=user_id,
    )

    # Vérification : une note ne peut contenir
    # qu'un seul type de dépense.

    db.add(expense)
    db.flush()
    total_amount = 0

    for item in expense_data.items:
        # Pour une nouvelle ligne KM :
        # on utilise toujours le tarif actuel de configuration.
        if item.item_type == "KM":
            km_rate = settings.KM_RATE
        else:
            km_rate = 0
        amount = calculate_item_amount(
            item,
            km_rate or 0,
        )
        expense_item = ExpenseItem(
            expense_id=expense.id,
            item_type=item.item_type,
            description=item.description,
            departure=item.departure,
            arrival=item.arrival,
            kilometers=item.kilometers,
            is_electric_vehicle=item.is_electric_vehicle,
            km_rate=km_rate,
            toll_amount=item.toll_amount,
            other_amount=item.other_amount,
            amount=amount,
        )
        db.add(expense_item)
        total_amount += amount
    expense.total_amount = round(
        total_amount,
        2,
    )
    db.commit()
    db.refresh(expense)
    return expense

# modification d'une note de frais

def update_expense(
    db: Session,
    expense_id: int,
    expense_data: ExpenseCreate,
    user_id: int,
):

    expense = (
        db.query(Expense)
        .filter(
            Expense.id == expense_id,
            Expense.user_id == user_id,
        )
        .first()
    )

    if expense is None:
        return None

    # Plus aucune ligne :
    # suppression de la note.

    if not expense_data.items:

        for item in expense.items:
            for receipt in item.receipts:
                erase_receipt(receipt)

        db.delete(expense)

        db.commit()

        return "deleted"

    # Vérification du type unique

    validate_single_item_type(
        expense_data.items
    )

    # Mise à jour de l'entête

    expense.expense_date = (
        expense_data.expense_date
    )

    expense.label = (
        expense_data.label
    )

    # Lignes existantes

    existing_items = {
        item.id: item
        for item in expense.items
    }

    # Lignes conservées

    received_ids = set()

    total_amount = 0

    # ------------------------------------
    # Parcours des lignes du formulaire
    # ------------------------------------

    for item in expense_data.items:

        # Tarif kilométrique

        if item.item_type == "KM":

            if (
                item.km_rate is not None
                and item.km_rate > 0
            ):
                km_rate = item.km_rate
            else:
                km_rate = settings.KM_RATE

        else:
            km_rate = 0

        # Calcul du montant

        amount = calculate_item_amount(
            item,
            km_rate or 0,
        )

        # ==============================
        # Ligne existante
        # ==============================

        if item.id is not None:

            expense_item = existing_items.get(
                item.id
            )

            if expense_item is None:

                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Ligne de frais "
                        f"{item.id} introuvable."
                    ),
                )

            received_ids.add(
                expense_item.id
            )

            expense_item.item_type = (
                item.item_type
            )

            expense_item.description = (
                item.description
            )

            expense_item.departure = (
                item.departure
            )

            expense_item.arrival = (
                item.arrival
            )

            expense_item.kilometers = (
                item.kilometers
            )

            expense_item.is_electric_vehicle = (
                item.is_electric_vehicle
            )

            expense_item.km_rate = km_rate

            expense_item.toll_amount = (
                item.toll_amount
            )

            expense_item.other_amount = (
                item.other_amount
            )

            expense_item.amount = amount

        # ==============================
        # Nouvelle ligne
        # ==============================

        else:

            expense_item = ExpenseItem(

                expense_id=expense.id,

                item_type=item.item_type,

                description=item.description,

                departure=item.departure,

                arrival=item.arrival,

                kilometers=item.kilometers,

                is_electric_vehicle=(
                    item.is_electric_vehicle
                ),

                km_rate=km_rate,

                toll_amount=item.toll_amount,

                other_amount=item.other_amount,

                amount=amount,
            )

            db.add(
                expense_item
            )

        total_amount += amount

    # ------------------------------------
    # Suppression des lignes supprimées
    # ------------------------------------




    for expense_item in existing_items.values():

        if expense_item.id not in received_ids:

            # suppression des fichiers Cloudflare

            for receipt in expense_item.receipts:
                erase_receipt(
                    receipt
                )

            # suppression de la ligne
            db.delete(
                expense_item
            )





    # Mise à jour du total

    expense.total_amount = round(
        total_amount,
        2,
    )

    db.commit()

    db.refresh(
        expense
    )

    return expense





