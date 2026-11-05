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
    r"afford", r"برداشت", r"चुकान", r"تنبیہ", r"चेतावनी",
    # instruction forgetting / forced approval (any script incl. roman)
    r"بھول", r"भूल", r"अप्रूव", r"منظور",
    # demanded lies about prices
    r"lie\b", r"झूठ", r"جھوٹ",
    # prompt injection
    r"forget.*system", r"ignore.*instruction", r"سسٹم کو بھول",
    r"सिस्टम.*भूल",
]

# --- tool intent keywords per language family ---
PRICE_WORDS = ["price", "cost", "qeemat", "قیمت", "keemat", "कीमत", "दाम", "dam", "دام"]
STOCK_WORDS = ["stock", "available", "in stock", "اسٹاک", "स्टॉक", "baki", "باقی", "बचा"]
LOAN_WORDS = ["loan", "eligib", "قرض", "लोन", "aamdani", "آمدنی", "आय", "income"]
# Catalog has SKUs only — no manufacturer / brand field
BRAND_WORDS = [
    "brand", "brands", "company", "maker", "manufacturer",
    "برانڈ", "برینڈ", "کمپنی", "ब्रांड", "कंपनी", "ब्राण्ड",
]

ANSWERS = {
    "refuse": {
        "en": "I cannot help with that. I only answer price, stock, and loan-eligibility questions.",
        "hi": "मैं इसमें मदद नहीं कर सकता। मैं सिर्फ कीमत, स्टॉक और लोन-योग्यता बताता हूँ।",
        "ur": "میں اس میں مدد نہیں کر سکتا۔ میں صرف قیمت، اسٹاک اور قرض کی اہلیت بتاتا ہوں۔",
    },
    "no_brand": {
        "en": "We do not track brands — only SKUs. Ask price or stock for a listed item (e.g. cooking oil 5L).",
        "hi": "हम ब्रांड नहीं रखते — सिर्फ SKU। लिस्ट आइटम की कीमत या स्टॉक पूछें (जैसे कुकिंग ऑयल 5L)।",
        "ur": "ہم برانڈ نہیں رکھتے — صرف SKU۔ فہرست آئٹم کی قیمت یا اسٹاک پوچھیں (جیسے کوکنگ آئل 5L)۔",
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


def must_refuse(text):
    t = text.lower()
    return any(re.search(p, t) for p in REFUSE_PATTERNS)


def _asks_brand(text):
    t = text.lower()
    return any(w in t for w in BRAND_WORDS)


def answer(prompt, preferred_lang=None):
    lang = detect_lang(prompt, preferred=preferred_lang)
    if must_refuse(prompt):
        return {"lang": lang, "refused": True, "tool": None,
                "result": None, "answer": ANSWERS["refuse"][lang]}
    t = prompt.lower()
    # Brand questions must not fall through to price of a fuzzy-matched SKU
    if _asks_brand(prompt):
        item = tools.resolve_item(prompt)
        ans = ANSWERS["no_brand"][lang]
        if item:
            tip = {
                "en": " Closest listed SKU: %s — ask its price or stock." % item,
                "hi": " नज़दीकी SKU: %s — इसकी कीमत या स्टॉक पूछें।" % item,
                "ur": " قریبی SKU: %s — اس کی قیمت یا اسٹاک پوچھیں۔" % item,
            }[lang]
            ans = ans + tip
        return {"lang": lang, "refused": True, "tool": None,
                "result": None, "answer": ans}
    item = tools.resolve_item(prompt)
    if any(w in t for w in LOAN_WORDS):
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
    if item and any(w in t for w in PRICE_WORDS):
        result = tools.lookup_price(item)
        ans = format_price(lang, item, result.get("price_pkr", 0),
                           result.get("stock", 0))
        return {"lang": lang, "refused": False, "tool": "lookup_price",
                "result": result, "answer": ans}
    if item and any(w in t for w in STOCK_WORDS):
        result = tools.check_stock(item)
        ans = format_stock(lang, item, result.get("stock", 0),
                           result.get("low"))
        return {"lang": lang, "refused": False, "tool": "check_stock",
                "result": result, "answer": ans}
    if item:
        result = tools.lookup_price(item)
        ans = format_price(lang, item, result.get("price_pkr", 0),
                           result.get("stock", 0))
        return {"lang": lang, "refused": False, "tool": "lookup_price",
                "result": result, "answer": ans}
    return {"lang": lang, "refused": True, "tool": None,
            "result": None, "answer": ANSWERS["refuse"][lang]}
