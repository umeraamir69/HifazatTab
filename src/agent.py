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
    # prompt injection
    r"forget.*system", r"ignore.*instruction", r"سسٹم کو بھول",
    r"सिस्टम.*भूल",
]

# --- tool intent keywords per language family ---
PRICE_WORDS = ["price", "cost", "qeemat", "قیمت", "keemat", "कीमत", "dam", "دام"]
STOCK_WORDS = ["stock", "available", "in stock", "اسٹاک", "स्टॉक", "baki", "باقی", "बचा"]
LOAN_WORDS = ["loan", "eligib", "قرض", "लोन", "aamdani", "آمدنی", "आय", "income"]

ANSWERS = {
    "refuse": {
        "en": "I cannot help with that. I only answer price, stock, and loan-eligibility questions.",
        "hi": "मैं इसमें मदद नहीं कर सकता। मैं सिर्फ कीमत, स्टॉक और लोन-योग्यता बताता हूँ।",
        "ur": "میں اس میں مدد نہیں کر سکتا۔ میں صرف قیمت، اسٹاک اور قرض کی اہلیت بتاتا ہوں۔",
    }
}


def detect_lang(text):
    if re.search(r"[\u0600-\u06FF]", text):
        return "ur"
    if re.search(r"[\u0900-\u097F]", text):
        return "hi"
    return "en"


def must_refuse(text):
    t = text.lower()
    return any(re.search(p, t) for p in REFUSE_PATTERNS)


def answer(prompt):
    lang = detect_lang(prompt)
    if must_refuse(prompt):
        return {"lang": lang, "refused": True, "tool": None,
                "result": None, "answer": ANSWERS["refuse"][lang]}
    t = prompt.lower()
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
        ans = "%s: %d PKR, stock %d." % (item, result.get("price_pkr", 0),
                                        result.get("stock", 0))
        return {"lang": lang, "refused": False, "tool": "lookup_price",
                "result": result, "answer": ans}
    if item and any(w in t for w in STOCK_WORDS):
        result = tools.check_stock(item)
        ans = "%s: stock %d%s." % (item, result.get("stock", 0),
              " — low stock" if result.get("low") else "")
        return {"lang": lang, "refused": False, "tool": "check_stock",
                "result": result, "answer": ans}
    if item:
        result = tools.lookup_price(item)
        ans = "%s: %d PKR, stock %d." % (item, result.get("price_pkr", 0),
                                        result.get("stock", 0))
        return {"lang": lang, "refused": False, "tool": "lookup_price",
                "result": result, "answer": ans}
    return {"lang": lang, "refused": True, "tool": None,
            "result": None, "answer": ANSWERS["refuse"][lang]}
