# Website — HifazatTab live demo

**URL:** https://hifazattab.vercel.app  
**Source:** `web/` (Vercel project root)  
**Status:** Public (SSO protection **off** — was returning 404)  
**Last updated:** 2026-11-04

This page is the **Demo Day voice/path judges hit**. It does **not** run Tiny Aya in the browser. It mirrors the same **3-tool + shop CSV contract** as training, with a deterministic client agent so latency and PKR numbers stay reliable.

Training metrics (BEFORE/AFTER) live on Hugging Face + Colab; the site *shows* those numbers and links the adapter.

---

## 1. What the site is for

| Goal | How the site helps |
|------|--------------------|
| 30–60s live demo | Mic / samples / spoken answers without GPU |
| Prove tool contract | Same price/stock/loan tools as AgentTune (answer chip shows `tool:item`) |
| Show safety | In-page red-team (24 script-switch attacks incl. roman-Urdu + brand trap) |
| Show scale | 108-SKU shop oracle, filterable |
| Point to Track C | Story chain + HF adapter + metrics bars |

**Not on the site:** loading the LoRA adapter in-browser, AuditKIT charts, Twilio UI (phone is separate under `phone/`).

---

## 2. File layout

```
web/
  index.html          # single-page app (UI + Hifazat agent JS)
  shop_catalog.json   # 108 SKUs + aliases (loaded at runtime)
  api/stt.js          # Vercel serverless — Groq Whisper STT
  .vercel/            # project link (hifazattab)
  .gitignore
```

Deploy: `cd web && vercel --prod --yes`  
Env (Vercel): `GROQ_API_KEY` (production / preview / development).  
Optional fallback in code: `OPENAI_API_KEY` — **not required** (we use Groq only).

---

## 3. Page sections (top → bottom)

| Section | ID | What it does |
|---------|-----|----------------|
| Top nav | — | Jump links + GitHub + HF adapter |
| Hero | — | Brand **HifazatTab**, lede with live SKU count, CTAs |
| Try agent | `#try` | Lang tabs, samples, ask box, mic, speak, answer panel |
| Why Track C | `#track` | CSV → Tiny Aya → GRPO → AuditKIT → script-switch |
| Three tools | `#tools` | lookup_price / check_stock / loan_eligibility cards |
| Before → after | `#metrics` | BEFORE bars filled (98/11/14); AFTER placeholders |
| 60-second demo | `#demo` | Judge script (EN price → UR → refuse → red-team → HF) |
| Safety | `#safety` | Button runs 9 attacks; prints blocked count |
| Shop oracle | — | Filter, category chips, scrollable table, click-to-ask, random SKU |
| Artifacts | — | Links: repo, adapters, base model, Lexsi hackathon |
| Footer | — | Track C credit line |

---

## 4. Features — done

### Agent (client-side `Hifazat`)

- [x] Load catalog from `shop_catalog.json` (108 items)
- [x] Longest-alias resolve across en / hi / ur (word-boundary for short aliases)
- [x] Tools: price, stock, loan eligibility (same tiers as Python: 40k / 150k)
- [x] Refusal-first: fake approval, PII, afford-push, jailbreak, lie, brand traps
- [x] Brand questions refuse **without** dumping PKR (may point to closest SKU)
- [x] Answers localized: Hindi/Urdu price & stock strings (not English-only)
- [x] Preferred UI lang when mic returns Latin script (hi/ur tabs stick)

### Voice

- [x] **Speak answers** (Web Speech TTS); prefers `hi-IN` / `ur-PK` voices when installed
- [x] **EN / HI mic** — browser `SpeechRecognition` (`en-US` / `hi-IN`)
- [x] **UR mic** — MediaRecorder → POST `/api/stt` → Groq Whisper large-v3 (`lang=ur`)
- [x] ~8s record window for Urdu with Stop button; status line shows provider (`groq`)
- [x] Mic blocked / no-speech / service-not-allowed tips for browser STT

### UX / shop

- [x] Language tabs + sample prompts (en/hi/ur), including attacks as last sample
- [x] Enter-to-ask, copy answer, chips (answered/refused + tool + lang)
- [x] Shop table: item, category, price PKR, stock
- [x] Filter by SKU name / alias / category text
- [x] Category chips (staples, pulses, oils, …)
- [x] Click row → ask price in current UI language
- [x] Ask random SKU
- [x] Scrollable oracle (max-height) so hero stays usable on mobile

### Design

- [x] Custom fonts (Fraunces + Sora), green ink / paper atmosphere (not purple AI defaults)
- [x] Motion: rise / flash / metric bar draw
- [x] Responsive ask row on narrow screens

### Ops

- [x] Vercel production alias `hifazattab.vercel.app`
- [x] Deployment Protection / SSO disabled for public 200
- [x] `GROQ_API_KEY` set; STT smoke returns `provider: "groq"`

---

## 5. Features — in progress / next

| Item | Status | Notes |
|------|--------|--------|
| Fill AFTER metric bars with real numbers | **Done** | SFT AFTER live: 100 / 98 / 88, now wired from `web/metrics.json` (`loadMetrics`, hardcoded fallback) |
| Push `web/` + catalog to GitHub `main` | **Todo** | Local deploy works; repo may lag |
| Hindi TTS voice quality | Depends on OS | Prompt if no `hi` voice installed |
| Urdu TTS | Depends on OS | Whisper STT works; speak-back needs system Urdu voice |
| Hold-to-talk / stop button for Urdu | **Done** | Stop button + 8 s auto-stop note under ask row |
| Wire AFTER from JSON/config | **Done** | `web/metrics.json` — update file, no HTML edit |
| Show “live = rule agent; HF = metrics” callout | **Done** | Present in `#try` panel |
| AuditKIT embed / screenshots | **Part-done** | GRPO report in `reports/auditkit_hifazat-tab-grpo-v1.md`; site embed + SFT side later |
| WhatsApp deep-link on site | **Done** | Artifacts link to SFT adapter + WhatsApp $0 guide |

---

## 6. Voice architecture

```
EN/HI:  Mic → Web Speech STT → Hifazat.answer(text, curLang) → TTS
UR:     Mic → MediaRecorder (webm) → POST /api/stt (Groq Whisper)
              → Hifazat.answer(text, "ur") → TTS
```

`/api/stt` body: `{ audio: base64, mime, lang }` → `{ text, provider, lang }`  
If no key: `503` with message to set `GROQ_API_KEY`.

**We do not need OpenAI or Google** for this path.

---

## 7. Agent contract (must stay aligned with Python)

| Behavior | Web | Python `src/agent.py` |
|----------|-----|------------------------|
| Catalog source | `shop_catalog.json` | `shop_catalog.py` ← `shop.csv` |
| Price/stock/loan | Yes | Yes |
| Brand refuse | Yes | Yes |
| Localized answers | Yes (hi/ur) | Yes |
| Preferred lang | `answer(prompt, preferred)` | `preferred_lang=` |

Regenerate catalog after CSV edits:

```bash
python3 scripts/gen_shop_aliases.py
# copies/writes web/shop_catalog.json + src/shop_catalog.py
```

---

## 8. Demo script (judges)

1. English sample → atta price → **2850** (spoken).
2. اردو tab → mic or sample → same SKU, Urdu answer + TTS.
3. Fake loan sample → **refused**, no approval text.
4. Red-team → blocked count across scripts.
5. Scroll shop / filter `daal` → click row → ask.
6. Point to HF adapter + BEFORE gap; AFTER story per `Findings.md`.

Full checklist: `phone/VOICE_E2E.md`.

---

## 9. Deploy / env cheat sheet

```bash
cd web
vercel env ls                          # expect GROQ_API_KEY
vercel --prod --yes                    # ship
curl -sS -X POST https://hifazattab.vercel.app/api/stt \
  -H 'Content-Type: application/json' \
  -d '{"audio":"<base64>","mime":"audio/wav","lang":"ur"}'
```

Local: static `index.html` works for agent/UI; Urdu STT needs deployed `/api/stt` (or `vercel dev` with env).

---

## 10. Changelog (website)

| When | Change |
|------|--------|
| Earlier | Single-page demo, 7 SKUs hardcoded, EN mic, basic TTS |
| Nov 4 | Track C story, metrics bars, demo script, artifacts, design pass |
| Nov 4 | Brand-safe answers; Urdu mic tip (browser STT missing) |
| Nov 4 | 108 SKUs via `shop_catalog.json`; filter, categories, random ask |
| Nov 4 | Localized hi/ur price/stock; preferred lang for mic |
| Nov 4 | `/api/stt` + Groq Whisper for real Urdu STT |
| Nov 6 | 219 SKUs; 24-attack red-team (roman+brand); `tool:item` chip; `metrics.json` wiring; SFT/WhatsApp artifact links; Stop-button Urdu mic |
| Next | GitHub sync; AuditKIT embed |

---

## 11. Related docs

- `Findings.md` — why Tiny Aya AFTER is flat; overall project inventory  
- `Status.md` / `Results.md` — metrics  
- `phone/VOICE_E2E.md` — voice done-when gates  
- `scripts/HF_JOBS.md` — training (not the website)
