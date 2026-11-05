"""HifazatTab tools — the 3 calculator buttons.

The agent may ONLY answer using one of these. Facts come from shop.csv,
never from model memory. Language-agnostic: same call works for en/hi/ur.

Catalog: ~100 SKUs. Aliases auto-generated — regenerate with
`python3 scripts/gen_shop_aliases.py` after editing data/shop.csv.
"""
import re

from .shop_catalog import ALIASES, CATALOG

TABLE = {
    key: {
        "item": key,
        "price_pkr": str(meta["price"]),
        "stock": str(meta["stock"]),
        "category": meta["category"],
    }
    for key, meta in CATALOG.items()
}


def resolve_item(text):
    """Map free text (any language) to a canonical item key. Returns None.

    Short aliases (rice, oil, tea...) match on word boundaries only,
    so "price" never resolves to rice.
    """
    t = text.lower()
    # Collect all (alias, key) and try longest alias first across the catalog
    pairs = []
    for key, names in ALIASES.items():
        for name in names:
            pairs.append((name.lower(), key))
    pairs.sort(key=lambda x: len(x[0]), reverse=True)
    for name, key in pairs:
        if len(name) <= 4:
            if re.search(r"(?<!\w)" + re.escape(name) + r"(?!\w)", t, flags=re.UNICODE):
                return key
        elif name in t:
            return key
    return None


def lookup_price(item_key):
    row = TABLE.get(item_key)
    if row is None:
        return {"ok": False, "error": "item_not_found"}
    return {"ok": True, "item": item_key,
            "price_pkr": int(row["price_pkr"]), "stock": int(row["stock"])}


def check_stock(item_key):
    row = TABLE.get(item_key)
    if row is None:
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


def catalog_size():
    return len(CATALOG)
