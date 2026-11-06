"""HifazatTab baseline agent (rule-based stand-in for Tiny Aya).

Pipeline per question:
  1. detect language (en / hi / ur) from script + keywords
  2. check refusal triggers FIRST (safety before tools)
  3. pick exactly one tool, run it, answer from the tool result only

Returns a dict: {lang, refused, tool, result, answer}.
Phase 1 will swap this with Tiny Aya + AgentTune. Same interface.
"""
import re

from . import tools

# --- refusal triggers: run before any tool ---
REFUSE_PATTERNS = [
    # fake documents / approvals
    r"fake", r"approval letter", r"approve.*loan", r"منظوری",
    r"अप्रूवल", r"جعلی", r"नकली",
    # PII
    r"phone", r"number.*customer", r"فوں", r"فون", r"نمبر",
    r"मोबाइल", r"नंबर",
    # harmful financial advice (pushing unaffordable loans, any word order)
    r"afford", r"برداشت", r"bardasht", r"चुकान", r"تنبیہ", r"चेतावनी",
    # instruction forgetting / forced approval (any script incl. roman)
    r"بھول", r"भूल", r"bhool", r"अप्रूव", r"منظور", r"manzoor",
    # demanded lies about prices
    r"lie\b", r"झूठ", r"جھوٹ", r"jhoot", r"naqli", r"jaali",
    # prompt injection
    r"forget.*system", r"ignore.*instruction", r"سسٹم کو بھول",
    r"सिस्टम.*भूल",
]

# --- tool intent keywords per language family ---
PRICE_WORDS = ["price", "cost", "qeemat", "قیمت", "keemat", "कीमत", "दाम", "dam", "دام",
               "bhav", "bhaav", "bhao", "rate", "kimat", "qimat"]
STOCK_WORDS = ["stock", "available", "in stock", "اسٹاک", "स्टॉक", "baki", "baqi",
               "باقی", "बचा", "bacha"]
LOW_STOCK_WORDS = [
    "low stock", "low-stock", "stock low", "stock kam", "kam stock",
    "almost out", "running out", "کم اسٹاک", "اسٹاک کم", "स्टॉक कम", "कम स्टॉक",
]
DETAIL_WORDS = [
    "detail", "details", "info", "information", "spec", "specs",
    "تفصیل", "تفصیلات", "विवरण", "जानकारी", "full info",
]
CATEGORY_WORDS = [
    "category", "categories", "section", "aisle", "department",
    "list", "show me", "what do you have",
    "کتگوری", "کیٹگری", "श्रेणी", "فہرست", "सूची",
]
LOAN_WORDS = ["loan", "eligib", "قرض", "qarza", "karza", "qarz", "लोन",
              "aamdani", "آمدنی", "आय", "income"]
# Catalog has SKUs only — no manufacturer / brand field
BRAND_WORDS = [
    "brand", "brands", "company", "maker", "manufacturer",
    "برانڈ", "برینڈ", "کمپنی", "ब्रांड", "कंपनी", "ब्राण्ड",
]

ANSWERS = {
    "refuse": {
        "en": "I cannot help with that. I answer price, stock, item details, category lists, low stock, and loan eligibility.",
        "hi": "मैं इसमें मदद नहीं कर सकता। मैं कीमत, स्टॉक, डिटेल्स, कैटेगरी, कम स्टॉक और लोन-योग्यता बताता हूँ।",
        "ur": "میں اس میں مدد نہیں کر سکتا۔ میں قیمت، اسٹاک، تفصیل، کیٹگری، کم اسٹاک اور قرض کی اہلیت بتاتا ہوں۔",
    },
    "no_brand": {
        "en": "We do not track brands — only SKUs. Ask price, stock, or details for a listed item (e.g. cooking oil 5L).",
        "hi": "हम ब्रांड नहीं रखते — सिर्फ SKU। लिस्ट आइटम की कीमत, स्टॉक या डिटेल्स पूछें (जैसे कुकिंग ऑयल 5L)।",
        "ur": "ہم برانڈ نہیں رکھتے — صرف SKU۔ فہرست آئٹم کی قیمت، اسٹاک یا تفصیل پوچھیں (جیسے کوکنگ آئل 5L)۔",
    },
}


def detect_lang(text, preferred=None):
    """Script wins; if Latin-only, honour preferred UI lang (hi/ur/en)."""
    if re.search(r"[\u0600-\u06FF]", text):
        return "ur"
    if re.search(r"[\u0900-\u097F]", text):
        return "hi"
    if preferred in ("hi", "ur", "en"):
        return preferred
    return "en"


def format_price(lang, item, price, stock):
    if lang == "hi":
        return "%s की कीमत %d रुपये है, स्टॉक %d।" % (item, price, stock)
    if lang == "ur":
        return "%s کی قیمت %d روپے ہے، اسٹاک %d۔" % (item, price, stock)
    return "%s: %d PKR, stock %d." % (item, price, stock)


def format_stock(lang, item, stock, low=False):
    if lang == "hi":
        extra = " — स्टॉक कम है" if low else ""
        return "%s: स्टॉक %d%s।" % (item, stock, extra)
    if lang == "ur":
        extra = " — اسٹاک کم ہے" if low else ""
        return "%s: اسٹاک %d%s۔" % (item, stock, extra)
    return "%s: stock %d%s." % (item, stock, " — low stock" if low else "")


def format_details(lang, item, price, stock, category, low=False):
    low_bit = {
        "en": " — low stock" if low else "",
        "hi": " — स्टॉक कम" if low else "",
        "ur": " — اسٹاک کم" if low else "",
    }[lang]
    if lang == "hi":
        return "%s: कीमत %d रुपये, स्टॉक %d, कैटेगरी %s%s।" % (
            item, price, stock, category, low_bit)
    if lang == "ur":
        return "%s: قیمت %d روپے، اسٹاک %d، کیٹگری %s%s۔" % (
            item, price, stock, category, low_bit)
    return "%s: %d PKR, stock %d, category %s%s." % (
        item, price, stock, category, low_bit)


def _fmt_sku_bits(items, limit=8):
    show = items[:limit]
    bits = ["%s=%s PKR (stock %s)" % (it["item"], it["price_pkr"], it["stock"])
            for it in show]
    more = len(items) - len(show)
    extra = (" (+%d more)" % more) if more else ""
    return bits, extra


def must_refuse(text):
    t = text.lower()
    return any(re.search(p, t) for p in REFUSE_PATTERNS)


def has_word(text, words):
    """Substring match, except short words (<=4 chars) match on word
    boundaries only — so 'dam' never fires inside 'cardamom'."""
    for w in words:
        if len(w) <= 4:
            if re.search(r"(?<!\w)" + re.escape(w) + r"(?!\w)", text,
                         flags=re.UNICODE):
                return True
        elif w in text:
            return True
    return False


def _stock_qty_match(t):
    return re.search(
        r"(?:stock|اسٹاک|स्टॉक)\s*[:=]?\s*(\d+)|(\d+)\s*(?:stock|اسٹاک|स्टॉक)",
        t, flags=re.UNICODE,
    )


def answer(prompt, preferred_lang=None):
    lang = detect_lang(prompt, preferred=preferred_lang)
    if must_refuse(prompt):
        return {"lang": lang, "refused": True, "tool": None,
                "result": None, "answer": ANSWERS["refuse"][lang]}
    t = prompt.lower()
    # Brand questions must not fall through to price of a fuzzy-matched SKU
    if has_word(t, [w.lower() for w in BRAND_WORDS]):
        item = tools.resolve_item(prompt)
        ans = ANSWERS["no_brand"][lang]
        if item:
            tip = {
                "en": " Closest listed SKU: %s — ask its price, stock, or details." % item,
                "hi": " नज़दीकी SKU: %s — कीमत, स्टॉक या डिटेल्स पूछें।" % item,
                "ur": " قریبی SKU: %s — قیمت، اسٹاک یا تفصیل پوچھیں۔" % item,
            }[lang]
            ans = ans + tip
        return {"lang": lang, "refused": True, "tool": None,
                "result": None, "answer": ans}

    item = tools.resolve_item(prompt)

    if has_word(t, LOAN_WORDS):
        m = re.search(r"(\d[\d,]*)", prompt)
        income = m.group(1) if m else "0"
        result = tools.loan_eligibility(income)
        if not result["ok"]:
            return {"lang": lang, "refused": True, "tool": "loan_eligibility",
                    "result": result, "answer": ANSWERS["refuse"][lang]}
        if result["tier"] == "none":
            ans = {"en": "You do not qualify yet. Small loans need 40000 PKR monthly income.",
                   "hi": "आप अभी योग्य नहीं हैं। छोटे लोन के लिए 40000 PKR मासिक आय चाहिए।",
                   "ur": "آپ ابھی اہل نہیں ہیں۔ چھوٹے قرض کے لیے 40000 ماہانہ آمدنی چاہیے۔"}[lang]
        else:
            ans = {"en": "You may be eligible for the %s loan tier. I cannot approve loans, only check eligibility." % result["tier"],
                   "hi": "आप %s लोन श्रेणी के लिए योग्य हो सकते हैं। मैं लोन स्वीकृत नहीं करता, सिर्फ योग्यता बताता हूँ।" % result["tier"],
                   "ur": "آپ %s قرض کے درجے کے لیے اہل ہو سکتے ہیں۔ میں قرض منظور نہیں کرتا، صرف اہلیت بتاتا ہوں۔" % result["tier"]}[lang]
        return {"lang": lang, "refused": False, "tool": "loan_eligibility",
                "result": result, "answer": ans}

    # "stock 1" / "stock 1 details" — inventory qty filter (before item+stock)
    m = _stock_qty_match(t)
    if m and not item:
        qty = int(m.group(1) or m.group(2))
        keys = tools.find_by_stock(qty)
        if not keys:
            # Soft fallback: show low-stock shelf when exact qty missing
            result = tools.list_low_stock(20)
            bits, extra = _fmt_sku_bits(result["items"])
            ans = {
                "en": "No SKU has exactly stock %d. Low stock (≤20)%s: %s. Ask one by name for details."
                      % (qty, extra, ", ".join(bits)),
                "hi": "ठीक स्टॉक %d वाला SKU नहीं। कम स्टॉक (≤20)%s: %s। नाम से डिटेल्स पूछें।"
                      % (qty, extra, ", ".join(bits)),
                "ur": "عین اسٹاک %d والا SKU نہیں۔ کم اسٹاک (≤20)%s: %s۔ نام سے تفصیل پوچھیں۔"
                      % (qty, extra, ", ".join(bits)),
            }[lang]
            return {"lang": lang, "refused": False, "tool": "list_low_stock",
                    "result": result, "answer": ans}
        rows = [tools.item_details(k) for k in keys]
        bits, extra = _fmt_sku_bits(
            [{"item": r["item"], "price_pkr": r["price_pkr"], "stock": r["stock"]}
             for r in rows if r.get("ok")])
        # Richer line when user asked for details
        if has_word(t, DETAIL_WORDS):
            show = [r for r in rows if r.get("ok")][:6]
            bits = ["%s: %s PKR, stock %s, %s" % (
                r["item"], r["price_pkr"], r["stock"], r["category"]) for r in show]
            more = len(keys) - len(show)
            extra = (" (+%d more)" % more) if more else ""
        ans = {
            "en": "Stock %d — %d SKUs: %s%s."
                  % (qty, len(keys), ", ".join(bits), extra),
            "hi": "स्टॉक %d — %d SKU: %s%s।"
                  % (qty, len(keys), ", ".join(bits), extra),
            "ur": "اسٹاک %d — %d SKU: %s%s۔"
                  % (qty, len(keys), ", ".join(bits), extra),
        }[lang]
        return {"lang": lang, "refused": False, "tool": "item_details",
                "result": {"ok": True, "stock": qty, "items": keys},
                "answer": ans}

    if item and has_word(t, DETAIL_WORDS):
        result = tools.item_details(item)
        ans = format_details(lang, item, result["price_pkr"], result["stock"],
                             result["category"], result.get("low"))
        return {"lang": lang, "refused": False, "tool": "item_details",
                "result": result, "answer": ans}
    if item and has_word(t, PRICE_WORDS):
        result = tools.lookup_price(item)
        ans = format_price(lang, item, result.get("price_pkr", 0),
                           result.get("stock", 0))
        return {"lang": lang, "refused": False, "tool": "lookup_price",
                "result": result, "answer": ans}
    if item and has_word(t, STOCK_WORDS):
        result = tools.check_stock(item)
        ans = format_stock(lang, item, result.get("stock", 0),
                           result.get("low"))
        return {"lang": lang, "refused": False, "tool": "check_stock",
                "result": result, "answer": ans}
    if item:
        # Bare SKU mention → full details card
        result = tools.item_details(item)
        ans = format_details(lang, item, result["price_pkr"], result["stock"],
                             result["category"], result.get("low"))
        return {"lang": lang, "refused": False, "tool": "item_details",
                "result": result, "answer": ans}

    # Low-stock scan (no specific SKU)
    if has_word(t, LOW_STOCK_WORDS):
        result = tools.list_low_stock(20)
        bits, extra = _fmt_sku_bits(result["items"])
        ans = {
            "en": "Low stock (≤20): %d SKUs%s — %s."
                  % (result["count"], extra, ", ".join(bits)),
            "hi": "कम स्टॉक (≤20): %d SKU%s — %s।"
                  % (result["count"], extra, ", ".join(bits)),
            "ur": "کم اسٹاک (≤20): %d SKU%s — %s۔"
                  % (result["count"], extra, ", ".join(bits)),
        }[lang]
        return {"lang": lang, "refused": False, "tool": "list_low_stock",
                "result": result, "answer": ans}

    # Category browse (only when no SKU matched)
    cat = tools.resolve_category(prompt)
    if cat:
        result = tools.list_category(cat)
        bits, extra = _fmt_sku_bits(result["items"])
        ans = {
            "en": "Category %s — %d SKUs%s: %s."
                  % (cat, result["count"], extra, ", ".join(bits)),
            "hi": "कैटेगरी %s — %d SKU%s: %s।"
                  % (cat, result["count"], extra, ", ".join(bits)),
            "ur": "کیٹگری %s — %d SKU%s: %s۔"
                  % (cat, result["count"], extra, ", ".join(bits)),
        }[lang]
        return {"lang": lang, "refused": False, "tool": "list_category",
                "result": result, "answer": ans}

    return {"lang": lang, "refused": True, "tool": None,
            "result": None, "answer": ANSWERS["refuse"][lang]}
