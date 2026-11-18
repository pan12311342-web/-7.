from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: Optional[str] = None
    unit: Optional[str] = None
    quantity: Optional[Decimal] = None
    price: Optional[Decimal] = None
    amount: Optional[Decimal] = None

class Invoice(BaseModel):
    document_type: str
    invoice_number: Optional[str] = None
    date: Optional[str] = None
    valid_until: Optional[str] = None
    supplier_name: Optional[str] = None
    supplier_code: Optional[str] = None
    supplier_iban: Optional[str] = None
    buyer_name: Optional[str] = None
    buyer_code: Optional[str] = None
    items: list[Item] = Field(default_factory=list)
    total_without_vat: Optional[Decimal] = None
    vat: Optional[Decimal] = None
    total_to_pay: Optional[Decimal] = None
