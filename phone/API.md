# HifazatTab Webhook API

Base URL (local): `http://localhost:8080`. Public demo: laptop + ngrok,
or Render free tier. All routes stdlib-only, no auth (Twilio signs its own
requests — validate `X-Twilio-Signature` before production).

## `GET /health`

Liveness check.

```bash
curl http://localhost:8080/health   # -> <ok/>
```

## `POST /voice` — start a call (needs paid Twilio number, NOT free)

Twilio calls this when the phone rings. Replies with TwiML: greeting +
`<Gather>` that sends speech to `/gather`.

```bash
curl -X POST http://localhost:8080/voice
```

Response (trimmed): greeting `<Say>`, then
`<Gather input="speech" action="/gather" language="en-US">`.
Set `HIFAZAT_GATHER_LANG` / `HIFAZAT_SAY_LANG` (e.g. `hi-IN`) after checking
your Twilio console lists them; `HIFAZAT_SAY_VOICE` picks the voice.

## `POST /gather` — answer a spoken question, loop the call

Twilio posts form-encoded speech results.

| Field | Meaning |
|-------|---------|
| `SpeechResult` | Transcribed caller speech (any of en/hi/ur) |

```bash
curl -X POST --data-urlencode "SpeechResult=What is the price of atta 20kg?" \
  http://localhost:8080/gather
# -> <Say>atta_20kg: 2850 PKR, stock 40.</Say> + <Redirect>/voice</Redirect>
```

Saying goodbye (`goodbye`, `khuda hafiz`, `अलविदा`) ends the call with `<Hangup/>`.
Tricks (fake letters, PII, forced loans) get a spoken refusal, same as the website.

## `POST /whatsapp` — chat bot (FREE via Twilio Sandbox, $0)

Twilio posts form-encoded WhatsApp messages.

| Field | Meaning |
|-------|---------|
| `Body` | Message text (Urdu, Hindi, English, Roman Urdu) |
| `From` | Sender, e.g. `whatsapp:+923001234567` (used for logging only) |

```bash
curl -X POST --data-urlencode "Body=آٹا 20 کلو کی قیمت کیا ہے؟" \
  http://localhost:8080/whatsapp
# -> <Response><Message>atta_20kg: 2850 PKR, stock 40.</Message></Response>
```

Sandbox setup: Twilio Console → Messaging → WhatsApp Sandbox → join from your
phone → set webhook to `https://YOUR-NGROK-URL/whatsapp`.

## Errors

| Code | When |
|------|------|
| 404 + spoken "Not found" | Unknown path |
| Empty `SpeechResult`/`Body` | Polite re-prompt, stays in the loop (no crash) |

All answers come from `src/agent.py` + `data/shop.csv` — one fix helps the
website, WhatsApp, and calls together.
