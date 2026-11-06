"""HifazatTab tools — calculator buttons for the shop agent.

The agent may ONLY answer using one of these. Facts come from shop.csv,
never from model memory. Language-agnostic: same call works for en/hi/ur.

Catalog: ~200 SKUs. Aliases auto-generated — regenerate with
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

CATEGORIES = sorted({meta["category"] for meta in CATALOG.values()})

# Human labels → canonical category key
CATEGORY_ALIASES = {
    "staples": ["staples", "staple", "flour", "آٹا", "आटा", "rasad", "راشن", "राशन"],
    "pulses": ["pulses", "pulse", "daal", "dal", "دال", "दाल"],
    "oils": ["oils", "oil", "cooking oil", "تیل", "तेल"],
    "dairy": ["dairy", "milk", "دودھ", "दूध", "ڈیری", "डेयरी"],
    "spices": ["spices", "spice", "masala", "مصالحہ", "मसाला"],
    "snacks": ["snacks", "snack", "nimco", "نشتہ", "नाश्ता"],
    "beverages": ["beverages", "beverage", "tea", "coffee", "مشروب", "पेय"],
    "drinks": ["drinks", "drink", "juice", "جوس", "जूस"],
    "produce": ["produce", "vegetables", "fruit", "سبزی", "सब्जी", "پھل", "फल"],
    "bakery": ["bakery", "bread", "روٹی", "रोटी", "نان", "बेकरी"],
    "household": ["household", "cleaning", "گھر", "घर", "صفائی"],
    "packaged": ["packaged", "packet", "پیکٹ", "पैकेट"],
}


def normalize_query(text):
    """Collapse '10 kg' / '10 kilo' → '10kg' so size aliases match."""
    t = text.lower()
    t = re.sub(
        r"(\d+)\s*(kilo(?:gram)?s?|کلو|किलो|kg)\b",
        r"\1kg", t, flags=re.UNICODE | re.IGNORECASE)
    t = re.sub(
        r"(\d+)\s*(litres?|liters?|لیٹر|लीटर|ltr)\b",
        r"\1l", t, flags=re.UNICODE | re.IGNORECASE)
    t = re.sub(
        r"(\d+)\s*(millilitres?|milliliters?|ml)\b",
        r"\1ml", t, flags=re.UNICODE | re.IGNORECASE)
    t = re.sub(
        r"(\d+)\s*(grams?|گرام|ग्राम|g)\b",
        r"\1g", t, flags=re.UNICODE | re.IGNORECASE)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def _size_tokens(t):
    """Size hints from the query: {'10kg', '5l', ...} and bare nums {'10'}."""
    sizes = set()
    for m in re.finditer(r"(\d+)\s*(kg|g|ml|l)\b", t, flags=re.IGNORECASE):
        sizes.add(m.group(1) + m.group(2).lower())
    nums = set(re.findall(r"(?<![.\d])(\d+)(?![.\d])", t))
    # Drop huge numbers (loan incomes) — sizes in this shop are < 10000
    nums = {n for n in nums if len(n) <= 4}
    return sizes, nums


def _key_fits_size(key, sizes, nums):
    """When the user named a size, don't fall through to another pack size."""
    k = key.lower()
    if sizes:
        return any(s in k for s in sizes)
    if nums:
        return any(
            re.search(r"(?:^|_)" + re.escape(n) + r"(?:kg|g|ml|l|pack)?(?:_|$)", k)
            for n in nums
        )
    return True


def resolve_item(text):
    """Map free text (any language) to a canonical item key. Returns None.

    Short aliases (rice, oil, tea...) match on word boundaries only,
    so "price" never resolves to rice. Size in the query (e.g. 10 kg)
    must match the SKU — 'atta 10 kg' never returns atta_20kg.
    """
    t = normalize_query(text)
    sizes, nums = _size_tokens(t)
    pairs = []
    for key, names in ALIASES.items():
        for name in names:
            pairs.append((name.lower(), key))
    pairs.sort(key=lambda x: len(x[0]), reverse=True)
    for name, key in pairs:
        if not _key_fits_size(key, sizes, nums):
            continue
        if len(name) <= 4:
            if re.search(r"(?<!\w)" + re.escape(name) + r"(?!\w)", t,
                         flags=re.UNICODE):
                return key
        elif name in t:
            return key
    # If size filter blocked every hit, retry without filter (last resort)
    if sizes or nums:
        for name, key in pairs:
            if len(name) <= 4:
                if re.search(r"(?<!\w)" + re.escape(name) + r"(?!\w)", t,
                             flags=re.UNICODE):
                    return key
            elif name in t:
                return key
    return None


def resolve_category(text):
    """Map free text to a catalog category, or None."""
    t = text.lower()
    # Prefer longest alias across categories
    pairs = []
    for cat, names in CATEGORY_ALIASES.items():
        if cat not in CATEGORIES:
            continue
        for name in names:
            pairs.append((name.lower(), cat))
    for cat in CATEGORIES:
        pairs.append((cat.lower(), cat))
    pairs.sort(key=lambda x: len(x[0]), reverse=True)
    for name, cat in pairs:
        if len(name) <= 4:
            if re.search(r"(?<!\w)" + re.escape(name) + r"(?!\w)", t, flags=re.UNICODE):
                return cat
        elif name in t:
            return cat
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


def item_details(item_key):
    """Full SKU card: price, stock, category."""
    row = TABLE.get(item_key)
    if row is None:
        return {"ok": False, "error": "item_not_found"}
    return {
        "ok": True,
        "item": item_key,
        "price_pkr": int(row["price_pkr"]),
        "stock": int(row["stock"]),
        "category": row["category"],
        "low": int(row["stock"]) < 20,
    }


def list_category(category):
    """All SKUs in a category with price + stock."""
    cat = (category or "").strip().lower()
    if cat not in CATEGORIES:
        # try alias resolution
        cat = resolve_category(cat) or cat
    if cat not in CATEGORIES:
        return {"ok": False, "error": "category_not_found",
                "categories": CATEGORIES}
    items = []
    for key, row in sorted(TABLE.items()):
        if row["category"] == cat:
            items.append({
                "item": key,
                "price_pkr": int(row["price_pkr"]),
                "stock": int(row["stock"]),
            })
    return {"ok": True, "category": cat, "count": len(items), "items": items}


def list_low_stock(threshold=20):
    """SKUs at or below threshold (default 20 = shop low-stock bar)."""
    try:
        thr = int(threshold)
    except (TypeError, ValueError):
        thr = 20
    items = []
    for key, row in sorted(TABLE.items(), key=lambda kv: int(kv[1]["stock"])):
        stock = int(row["stock"])
        if stock <= thr:
            items.append({
                "item": key,
                "price_pkr": int(row["price_pkr"]),
                "stock": stock,
                "category": row["category"],
            })
    return {"ok": True, "threshold": thr, "count": len(items), "items": items}


def find_by_stock(qty):
    """SKUs whose on-hand stock equals qty (inventory filter, not a product name)."""
    try:
        n = int(qty)
    except (TypeError, ValueError):
        return []
    return sorted(
        k for k, row in TABLE.items() if int(row["stock"]) == n
    )


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
