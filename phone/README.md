# HifazatTab on your phone — the $0 setup

## What is free (use these)

| Thing | Cost | Notes |
|-------|------|-------|
| Browser voice site | $0 forever | https://hifazattab.vercel.app, mic + spoken replies |
| WhatsApp bot (Twilio Sandbox) | $0 | Test sandbox, no number to buy. Works on your real phone |
| This backend (`phone/server.py`) | $0 | Stdlib only, runs on your laptop |
| ngrok (tunnel for webhooks) | $0 tier | Exposes laptop to Twilio while you demo |
| Render free tier | $0 | If you want the backend online 24/7 |

## What is NOT free (skip for now)

- Real voice calls: Twilio sells **no Pakistani numbers**. A foreign number +
  per-minute Pakistan rates (~$0.15/min) + possible call drops. Needs a paid
  account. The `/voice` route is built and ready for the day there's budget —
  do not demo it on trial credit to a Pakistani mobile without testing first.
- WhatsApp Sandbox limits: session windows and templates for business-initiated
  messages; fine for a hackathon demo, not for production.

## $0 demo recipe (10 minutes)

1. `python3 phone/server.py` (laptop, port 8080).
2. `ngrok http 8080` → copy the `https://...` URL.
3. Twilio Console (free account) → Messaging → Try it out → WhatsApp Sandbox:
   follow "join" instructions from your phone, set webhook to
   `https://YOUR-URL/whatsapp`.
4. Message the sandbox number in Urdu, Hindi, or English. Try a trick too —
   it refuses like the website.

## Honest limits

- Sandbox is shared and rate-limited; one demo phone at a time.
- Voice calls stay parked until there's call budget — the judges' track is
  Track C (agentic tuning), and the phone demo is a bonus, not the thesis.
