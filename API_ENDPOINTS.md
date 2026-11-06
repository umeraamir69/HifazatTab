# API Endpoints — HifazatTab

Two surfaces, both answered by the same agent + shop oracle. No auth on local
routes; with `TWILIO_AUTH_TOKEN` set, the three Twilio POST routes enforce
HMAC-SHA1 `X-Twilio-Signature` validation (missing/bad → `403`).

## Phone webhooks (`phone/server.py`)

Base URL local: `http://localhost:8080`. Spec source of truth:
`phone/openapi.yaml`; interactive docs at `GET /docs` (Swagger UI).

### `GET /health`

- **Auth**: none.
- **Response**: `200`, body `<ok/>` (`text/xml`).

### `POST /voice` (paid Twilio number required)

- **Auth**: none (Twilio calls it when the phone rings).
- **Body**: Twilio form fields (ignored; greeting is static).
- **Response**: `200` TwiML — greeting `<Say>` + `<Gather input="speech"
  action="/gather" language="en-US">`, goodbye fallback.
- **Errors**: none; unknown paths return `404` TwiML `<Say>Not found.</Say>`.

### `POST /gather`

- **Auth**: none.
- **Body**: `application/x-www-form-urlencoded`, field `SpeechResult`
  (example: `What is the price of atta 20kg?`).
- **Response**: `200` TwiML — `<Say>` with `agent.answer(speech)` in the
  detected language + `<Redirect>/voice</Redirect>` loop; empty speech
  re-prompts once; `goodbye` / `khuda hafiz` / `अलविदा` → `<Hangup/>`.
- **Errors**: `404` TwiML for unknown paths.

### `POST /whatsapp` (FREE via Twilio Sandbox, $0)

- **Auth**: none.
- **Body**: `application/x-www-form-urlencoded`, fields `Body` (example:
  `آٹا 20 کلو کی قیمت کیا ہے؟`), `From` (example: `whatsapp:+923001234567`).
- **Response**: `200` TwiML — `<Message>` with `agent.answer(Body)`.
- **Errors**: empty `Body` → usage hint message; `404` TwiML for unknown paths.

Locale/voice knobs: `HIFAZAT_GATHER_LANG` (default `en-US`),
`HIFAZAT_SAY_LANG` (default `en-US`), `HIFAZAT_SAY_VOICE` (default `alice`).

## Web STT (`web/api/stt.js`, Vercel serverless)

### `POST /api/stt`

- **Auth**: none (public endpoint; Groq key stays server-side).
- **Body**: JSON `{ audio: "<base64>", mime?: "audio/webm", lang?: "ur"|"hi"|"en" }`
  (`data:` URI prefix tolerated). Max ~7 MB decoded.
- **Response**: `200` `{ text, provider: "groq"|"openai", lang }`
  (`lang` normalized to `ur` unless `hi`/`en`; Whisper model
  `whisper-large-v3` on Groq, `whisper-1` on OpenAI fallback).
- **Errors**: `400` missing/empty audio; `413` audio too large;
  `405` non-POST; `503` no STT key configured (message tells the operator
  to set `GROQ_API_KEY`); upstream STT failures pass through with provider
  status. CORS open (`*`).

## Error format

- Phone routes always return TwiML XML (`text/xml`), even for errors.
- `/api/stt` returns JSON `{ error, ... }`, with `need` + key links on 503.
