from decimal import Decimal
from datetime import date, datetime
import re

OUR_NAME = "Сузір'я Рітейл"

def iban_valid(iban):
    if not iban: return False
    s = re.sub(r"\s+", "", iban).upper()
    if not re.fullmatch(r"[A-Z]{2}\d{2}[A-Z0-9]{10,30}", s): return False
    moved = s[4:] + s[:4]
    num = ''.join(str(ord(c)-55) if c.isalpha() else c for c in moved)
    return int(num) % 97 == 1

def code_valid(code):
    return bool(code and re.fullmatch(r"\d{8}|\d{10}", str(code)))

def money(v):
    return Decimal(str(v)) if v is not None else None

def validate(inv, supplier_reference=None):
    problems = []
    critical = ["supplier_name","supplier_code","supplier_iban","buyer_name","buyer_code","date","total_to_pay"]
    if inv.document_type != "invoice":
        return ["Документ не є рахунком на оплату."], "reject"

    for f in critical:
        if getattr(inv, f) is None:
            problems.append(f"{f}: обов'язкове поле відсутнє.")

    if inv.supplier_iban is not None and not iban_valid(inv.supplier_iban):
        problems.append("supplier_iban: IBAN не проходить формат або контрольну суму.")

    for f in ("supplier_code","buyer_code"):
        if getattr(inv, f) is not None and not code_valid(getattr(inv, f)):
            problems.append(f"{f}: некоректна довжина коду.")

    if inv.buyer_name and OUR_NAME.lower() not in inv.buyer_name.lower():
        problems.append("buyer_name: покупець не збігається із «Сузір'я Рітейл».")

    for i, item in enumerate(inv.items):
        if item.quantity is not None and item.price is not None and item.amount is not None:
            expected = (item.quantity * item.price).quantize(Decimal("0.01"))
            if abs(expected - item.amount) > Decimal("0.01"):
                problems.append(f"items[{i}].amount: кількість × ціна не дорівнює сумі рядка.")

    amounts = [x.amount for x in inv.items if x.amount is not None]
    if amounts and inv.total_without_vat is not None:
        total = sum(amounts, Decimal("0")).quantize(Decimal("0.01"))
        if abs(total - inv.total_without_vat) > Decimal("0.01"):
            problems.append("total_without_vat: сума позицій не збігається з підсумком без ПДВ.")

    if inv.total_without_vat is not None and inv.vat is not None and inv.total_to_pay is not None:
        expected = (inv.total_without_vat + inv.vat).quantize(Decimal("0.01"))
        if abs(expected - inv.total_to_pay) > Decimal("0.01"):
            problems.append("total_to_pay: підсумок + ПДВ не збігається з до сплати.")

    if supplier_reference:
        ref = supplier_reference.get(inv.supplier_name or "")
        if ref and inv.supplier_iban and ref.get("iban") != re.sub(r"\s+","",inv.supplier_iban).upper():
            problems.append("supplier_iban: IBAN не збігається з довідником постачальників.")

    decision = "auto" if not problems else "review"
    return problems, decision
