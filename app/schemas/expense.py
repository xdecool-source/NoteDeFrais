"""
Validation des notes de frais.

"""

from datetime import date
from typing import Optional
from pydantic import BaseModel, Field

class ExpenseItemCreate(BaseModel):
    id: int | None = None
    item_type: str
    description: Optional[str] = None
    departure: Optional[str] = None
    arrival: Optional[str] = None
    kilometers: Optional[float] = None
    km_rate: float | None = None
    is_electric_vehicle: bool = False
    toll_amount: float = 0
    other_amount: float = 0
    amount: float = 0

class ExpenseCreate(BaseModel):

    expense_date: date
    label: str
    items: list[ExpenseItemCreate]
    
# REFUS D'UNE NOTE

class ExpenseReject(BaseModel):

    rejection_reason: str = Field(
        min_length=3,
        max_length=1000,
    )
    