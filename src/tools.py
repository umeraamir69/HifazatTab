"""HifazatTab tools — the 3 calculator buttons.

The agent may ONLY answer using one of these. Facts come from shop.csv,
never from model memory. Language-agnostic: same call works for en/hi/ur.
"""
import csv
import os
import re

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "shop.csv")


def _load_table():
    table = {}
    with open(os.path.normpath(DATA_PATH), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            table[row["item"].strip()] = row
    return table


TABLE = _load_table()

# Human names in 3 languages -> canonical item key.
ALIASES = {
    "atta_20kg": ["atta", "atta 20kg", "atta 20 kg", "آٹا", "आटा", "flour"],
    "cheeni_5kg": ["cheeni", "cheeni 5kg", "sugar", "چینی", "चीनी"],
    "chai_950g": ["chai", "tea", "چائے", "चाय"],
    "cooking_oil_5L": ["cooking oil", "oil", "کوکنگ آئل", "कुकिंग ऑयल", "cooking oil 5l"],
    "daal_moong_1kg": ["daal", "daal moong", "moong", "دال", "दाल", "lentil"],
    "chaawal_5kg": ["chaawal", "rice", "چاول", "चावल"],
    "soap_4pack": ["soap", "صابن", "साबुन"],
}


def resolve_item(text):
    """Map free text (any language) to a canonical item key. Returns None."""
    t = text.lower()
    for key, names in ALIASES.items():
        for name in names:
            if name in t:
                return key
    return None


def lookup_price(item_key):
    row = TABLE.get(item_key)
    if row is None or row["category"] == "loan":
        return {"ok": False, "error": "item_not_found"}
    return {"ok": True, "item": item_key,
            "price_pkr": int(row["price_pkr"]), "stock": int(row["stock"])}


def check_stock(item_key):
    row = TABLE.get(item_key)
    if row is None or row["category"] == "loan":
        return {"ok": False, "error": "item_not_found"}
    stock = int(row["stock"])
    return {"ok": True, "item": item_key, "stock": stock,
            "low": stock < 20}


def loan_eligibility(monthly_income_pkr):
    """Eligibility check only. This tool NEVER approves a loan."""
    try:
        income = int(re.sub(r"[^\d]", "", str(monthly_income_pkr)))
    except ValueError:
        return {"ok": False, "error": "bad_income"}
    if income >= 150000:
        tier = "medium"
    elif income >= 40000:
        tier = "small"
    else:
        tier = "none"
    return {"ok": True, "income_pkr": income, "tier": tier,
            "note": "eligibility_only_no_approval"}
