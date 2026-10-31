"""HifazatTab phone webhook (Twilio <Gather>/<Say> loop). Stdlib only.

Routes:
  POST /voice    -> greeting + <Gather> (speech to /gather). Needs Twilio
                    number/credit (NOT free — see phone/README.md).
  POST /gather   -> runs src.agent on SpeechResult, <Say>s answer, loops.
  POST /whatsapp -> Twilio WhatsApp Sandbox chat. FREE ($0).
  GET  /health   -> OK

Answers use the SAME agent + tools as the website, so a fix in weights
helps callers, web users, and the demo alike.

Run locally:  python3 phone/server.py  (then expose with ngrok for Twilio)
"""
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import agent  # noqa: E402

# Verify in the Twilio console before demo day: <Gather>/<Say> locale support.
# Defaults below are the safe universal pair; switch to hi-IN / ur-PK if your
# Twilio account lists them (prior art: kisan-saathi used Twilio IVR for
# 13 languages incl. Urdu).
GATHER_LANG = os.environ.get("HIFAZAT_GATHER_LANG", "en-US")
SAY_LANG = os.environ.get("HIFAZAT_SAY_LANG", "en-US")
SAY_VOICE = os.environ.get("HIFAZAT_SAY_VOICE", "alice")

GREETING = ("Welcome to Hifazat shop. Ask about a price, stock, or a loan. "
            "Say goodbye to hang up.")


def twiml(body):
    return ('<?xml version="1.0" encoding="UTF-8"?><Response>%s</Response>'
            % body)


def handle_voice():
    return twiml(
        "<Say voice=\"%s\" language=\"%s\">%s</Say>"
        "<Gather input=\"speech\" action=\"/gather\" method=\"POST\" "
        "language=\"%s\" speechTimeout=\"auto\">"
        "<Say voice=\"%s\" language=\"%s\">I am listening.</Say>"
        "</Gather>"
        "<Say voice=\"%s\" language=\"%s\">I did not hear you. Goodbye.</Say>"
        % (SAY_VOICE, SAY_LANG, escape(GREETING),
           GATHER_LANG, SAY_VOICE, SAY_LANG, SAY_VOICE, SAY_LANG))


def handle_whatsapp(form):
    """Free path: Twilio WhatsApp Sandbox ($0, no number to buy).

    User joins the sandbox once from their own phone, then chats.
    Same agent + tools as voice and web.
    """
    text = (form.get("Body") or [""])[0].strip()
    if not text:
        return twiml("<Message>Send a price, stock, or loan question.</Message>")
    out = agent.answer(text)
    return twiml("<Message>%s</Message>" % escape(out["answer"]))


def handle_gather(form):
    speech = (form.get("SpeechResult") or [""])[0].strip()
    if not speech:
        return twiml("<Say voice=\"%s\" language=\"%s\">Sorry, I heard nothing."
                     "</Say><Redirect method=\"POST\">/voice</Redirect>"
                     % (SAY_VOICE, SAY_LANG))
    low = speech.lower()
    if "goodbye" in low or "khuda hafiz" in low or "अलविदा" in low:
        return twiml("<Say voice=\"%s\" language=\"%s\">Khuda hafiz. Shukriya."
                     "</Say><Hangup/>" % (SAY_VOICE, SAY_LANG))
    out = agent.answer(speech)
    return twiml(
        "<Say voice=\"%s\" language=\"%s\">%s</Say>"
        "<Redirect method=\"POST\">/voice</Redirect>"
        % (SAY_VOICE, SAY_LANG, escape(out["answer"])))


class Handler(BaseHTTPRequestHandler):
    def _send(self, body, code=200):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/xml")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if urlparse(self.path).path == "/health":
            self._send("<ok/>")
        else:
            self._send(twiml("<Say>Not found.</Say>"), 404)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        form = parse_qs(self.rfile.read(length).decode("utf-8", "replace"))
        path = urlparse(self.path).path
        if path == "/voice":
            self._send(handle_voice())
        elif path == "/gather":
            self._send(handle_gather(form))
        elif path == "/whatsapp":
            self._send(handle_whatsapp(form))
        else:
            self._send(twiml("<Say>Not found.</Say>"), 404)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    print("HifazatTab phone webhook on :%d (/voice, /gather, /health)" % port)
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()
