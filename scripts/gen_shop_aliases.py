#!/usr/bin/env python3
"""Regenerate src/shop_aliases.py + web shop snippet from data/shop.csv.

Run: python3 scripts/gen_shop_aliases.py
"""
from __future__ import annotations

import csv
import json
import os
import re
import textwrap

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
CSV_PATH = os.path.join(ROOT, "data", "shop.csv")
OUT_PY = os.path.join(ROOT, "src", "shop_catalog.py")

# Extra human names (en / roman / ur / hi) layered on top of auto SKU aliases.
EXTRA = {
    "atta_20kg": ["atta", "atta 20kg", "flour", "آٹا", "आटा"],
    "maida_5kg": ["maida", "میدہ", "मैदा"],
    "suji_1kg": ["suji", "semolina", "سوجی", "सूजी"],
    "besan_1kg": ["besan", "gram flour", "بیسن", "बेसन"],
    "chaawal_5kg": ["chaawal", "rice", "chawal", "چاول", "चावल"],
    "cheeni_5kg": ["cheeni", "sugar", "چینی", "चीनी"],
    "namak_1kg": ["namak", "salt", "نمک", "नमक"],
    "daal_moong_1kg": ["daal moong", "moong", "moong dal", "مونگ دال", "मूंग दाल"],
    "daal_masoor_1kg": ["daal masoor", "masoor", "مسور", "मसूर"],
    "daal_chana_1kg": ["daal chana", "chana dal", "چنا دال", "चना दाल"],
    "daal_mash_1kg": ["daal mash", "mash", "ماش", "माश"],
    "chana_white_1kg": ["white chana", "kabuli chana", "سفید چنا", "सफेद चना"],
    "cooking_oil_5L": ["cooking oil", "oil", "کوکنگ آئل", "कुकिंग ऑयल"],
    "ghee_1kg": ["ghee", "گھی", "घी"],
    "butter_200g": ["butter", "مکھن", "मक्खन"],
    "olive_oil_500ml": ["olive oil", "زیتون کا تیل", "जैतून तेल"],
    "chai_950g": ["chai", "tea", "چائے", "चाय"],
    "coffee_200g": ["coffee", "قهوه", "کافی", "कॉफी"],
    "green_tea_100g": ["green tea", "سبز چائے", "ग्रीन टी"],
    "milk_1L": ["milk", "doodh", "دودھ", "दूध"],
    "yogurt_1kg": ["yogurt", "dahi", "دہی", "दही"],
    "eggs_dozen": ["eggs", "anda", "انڈے", "अंडे"],
    "bread_loaf": ["bread", "ڈبل روٹی", "ब्रेड"],
    "onion_1kg": ["onion", "pyaz", "پیاز", "प्याज"],
    "potato_1kg": ["potato", "aloo", "آلو", "आलू"],
    "tomato_1kg": ["tomato", "tamatar", "ٹماٹر", "टमाटर"],
    "soap_4pack": ["soap", "sabun", "saboon", "صابن", "साबुन"],
    "detergent_1kg": ["detergent", "washing powder", "ڈٹرجنٹ", "डिटर्जेंट"],
}


def auto_names(key: str) -> list[str]:
    spaced = key.replace("_", " ")
    names = {key, spaced, spaced.replace(" 5l", " 5L"), key.replace("_", "-")}
    # drop unit-less short stems carefully later via word-boundary match
    stem = re.sub(r"_\d+(kg|g|L|ml|pack|dozen)?$", "", key, flags=re.I)
    stem = stem.replace("_", " ").strip()
    if stem and len(stem) >= 4:
        names.add(stem)
    return sorted(names, key=len, reverse=True)


def main() -> None:
    rows = []
    with open(CSV_PATH, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["category"] == "loan":
                continue
            rows.append(row)

    aliases = {}
    for row in rows:
        key = row["item"]
        names = list(auto_names(key))
        for extra in EXTRA.get(key, []):
            if extra not in names:
                names.append(extra)
        # longest first for matching
        aliases[key] = sorted(set(names), key=len, reverse=True)

    catalog = {
        r["item"]: {
            "price": int(r["price_pkr"]),
            "stock": int(r["stock"]),
            "category": r["category"],
        }
        for r in rows
    }

    with open(OUT_PY, "w", encoding="utf-8") as f:
        f.write('"""Auto-generated from data/shop.csv — do not edit by hand.\n')
        f.write("Regenerate: python3 scripts/gen_shop_aliases.py\n")
        f.write('"""\n')
        f.write("CATALOG = ")
        json.dump(catalog, f, ensure_ascii=False, indent=2)
        f.write("\n\nALIASES = ")
        json.dump(aliases, f, ensure_ascii=False, indent=2)
        f.write("\n")

    # JSON for the website fetch-free embed
    web_json = os.path.join(ROOT, "web", "shop_catalog.json")
    with open(web_json, "w", encoding="utf-8") as f:
        json.dump({"catalog": catalog, "aliases": aliases}, f, ensure_ascii=False, indent=2)

    print("items:", len(rows))
    print("wrote", OUT_PY)
    print("wrote", web_json)


if __name__ == "__main__":
    main()
