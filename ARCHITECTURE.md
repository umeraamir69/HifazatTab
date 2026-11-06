# Architecture — HifazatTab

One-paragraph overview: HifazatTab is a trilingual (Urdu / Hindi / English)
kiryana-shop tool agent. A closed CSV oracle holds prices, stock, and loan
tiers; a rule-based Python agent and a mirrored JavaScript agent answer only
through three tools (`lookup_price`, `check_stock`, `loan_eligibility`) and
refuse everything else. The same tool contract is used to fine-tune Cohere
Tiny Aya (LoRA SFT ships the Track C AFTER metrics) and to serve the live
voice/web/phone demo without GPU latency.

## Stack

| Layer | Technology | Version / note |
|-------|-----------|----------------|
| Rule agent + eval | Python stdlib only | any 3.10+ (`requirements.txt` is stdlib + comments) |
| Train / eval AFTER | `transformers`, `peft`, `trl`, `bitsandbytes`, `datasets`, `huggingface_hub` | Colab / HF Jobs only, never the laptop |
| Base model | `CohereLabs/tiny-aya-fire` (fallback `tiny-aya-global`) | gated HF repo, 4-bit via `BitsAndBytesConfig` |
| Winning adapter | `umeraamir69/hifazat-tab-sft-v1` | LoRA, gold-JSON SFT |
| Demo site | Static `web/index.html` + `web/shop_catalog.json` | Vercel static, `hifazattab.vercel.app` |
| Urdu STT | `web/api/stt.js` → Groq Whisper `large-v3` | needs `GROQ_API_KEY` on Vercel |
| Phone/WhatsApp | `phone/server.py` stdlib `http.server` | Twilio webhooks, no framework |
| Data | `data/shop.csv` + `data/seed_tasks.jsonl` | no database; CSV is the oracle |

There is no database layer, so there is no `DATABASE_SCHEMA.md`. The data
contract is the CSV schema below.

## Directory structure

```
data/            shop.csv (oracle: 219 SKUs + 2 loan-limit rows), seed_tasks.jsonl (1500 rows)
src/             tools.py, agent.py (+has_word boundaries), eval.py, redteam.py (8x3), shop_catalog.py (generated)
demo.py          2-minute CLI demo (5 scenes)
tests/           test_agent.py (12 tests, stdlib unittest)
scripts/         build_seed.py, gen_shop_aliases.py, train_*_hf_jobs.py, eval_after_hf_jobs.py, HF_JOBS.md
colab/           phase1_baseline / phase1_after / phase2 notebooks (+README)
colab result/    archived Phase-1 BEFORE outputs (md/json/full log)
web/             index.html (demo app), shop_catalog.json (generated), api/stt.js (Whisper)
phone/           server.py, openapi.yaml, API.md, README.md, VOICE_E2E.md, TRIAL_CALL.md
vault/           Obsidian docs (Plan, Status, Findings, Results, Website, Features, …)
papers/          research paper draft
```

`src/shop_catalog.py` and `web/shop_catalog.json` are generated — never edit
by hand. Regenerate with `python3 scripts/gen_shop_aliases.py` after editing
`data/shop.csv`.

## Data contract

`shop.csv`: `item,price_pkr,stock,category`. `item` is the canonical key
(`atta_20kg`); training and eval require exact key match. The last two rows
are `loan_limit_small/medium` config, not shop items, and are excluded from
the 219-SKU catalog. `seed_tasks.jsonl`: one JSON object per line with
`id, lang (en/hi/ur), type (tool-task/safety-probe), prompt, tool`
(`tool` = `name:canonical_arg`). Six legacy rows (`ok_0`–`ok_5`) lack `lang`
but are valid English tool-tasks (see `Features.md` cleanup item).

## Key flows

### Ask flow (Python, `src/agent.py:answer`)

1. `detect_lang` — Perso-Arabic script → `ur`, Devanagari → `hi`, else
   Latin honors `preferred_lang` (mic default) or `en`.
2. `must_refuse` — refusal regexes run BEFORE any tool (fake docs, PII,
   advice-push, jailbreak, lies, prompt injection).
3. Brand questions refuse without dumping prices (there is no brand field).
4. Loan keywords → `loan_eligibility(income)`; price keywords + resolved SKU
   → `lookup_price`; stock keywords + SKU → `check_stock`; bare SKU →
   price; anything else → refuse.
5. Answer rendered in the detected language from the tool result only.

### Eval flow (`src/eval.py`)

Independent oracle calls the tool directly from the seed `tool` spec and
compares full `(tool, result)` equality: `task_success`, `refusal_precision`
(probes must refuse), `over_refusal` (tool-tasks must not refuse, want 0),
and cross-lingual `consistency` (same base id across langs → same tool and
result). Run: `python3 -m src.eval`. Red-team: `python3 -m src.redteam`
(8 families × 3 scripts incl. roman + brand trap, blocked in all three = pass).

### AuditKIT report (Track C proof)

`scripts/eval_auditkit.py` (run in project `.venv`, needs `auditkit` +
`huggingface_hub`): loads AgentTune `trajectories.jsonl` via AuditKIT
`episodes_from_agenttune`, joins gold from the seed by exact prompt, writes
`reports/auditkit_<name>.json/.md` (validity / exact task / tool-name /
macro-F1 / refusal). GRPO v1: 400 episodes, validity 98.50%, task 21.11%,
F1 0.2176. The trajectories copy (`reports/trajectories_*.jsonl`, ~4 MB) is
gitignored; the small reports are committed.

### Note: in-flight uncommitted work (not this doc's contract)

As of 2026-11-06 the working tree also holds another hand's uncommitted
changes: `src/tools.py` gains `list_category`, `list_low_stock`,
`find_by_stock` + `CATEGORY_ALIASES`, and `data/shop.csv` lowers several
stocks (e.g. cooking_oil_5L 15 → 1). Until that lands, the committed contract
above (3 tools, CSV as printed) stands; `test_mixed_case_key_resolves`
currently fails (1 ≠ 15) as collateral of those stock edits.

### Train flow (HF Jobs, `scripts/train_grpo_hf_jobs.py`)

Seed → verifiable rewards (exact tool+arg match) → LoRA adapter +
`trajectories.jsonl` → push to `umeraamir69/...`. SFT path
(`scripts/train_sft_hf_jobs.py`) trains on gold JSON lines (canonical args
+ `refuse`) and produced the shipping adapter. AFTER eval
(`colab/phase1_after.ipynb`, `scripts/eval_after_hf_jobs.py`) replays the
Phase-1 prompts against base + adapter with identical scoring.

### Voice flow (web)

EN/HI: mic → browser `SpeechRecognition` → `Hifazat.answer` → Web Speech
TTS. UR: mic → `MediaRecorder` (~4.5 s) → `POST /api/stt` (Groq Whisper)
→ `Hifazat.answer(text, "ur")` → TTS. The JS `Hifazat` object mirrors the
Python agent contract (same tools, tiers, refusal-first, brand-safe).

## Configuration

| File / env | Controls |
|------------|----------|
| `.env` (gitignored) | `HF_TOKEN` for Colab/Jobs; never committed |
| Vercel `GROQ_API_KEY` | Urdu Whisper STT; without it `/api/stt` returns 503 |
| `HIFAZAT_GATHER_LANG` / `HIFAZAT_SAY_LANG` / `HIFAZAT_SAY_VOICE` | Twilio gather/say locale + voice |
| `PORT` | `phone/server.py` listen port (default 8080) |

## Deployment

- Demo: `cd web && vercel --prod --yes` (project `hifazattab`; Deployment
  Protection / SSO must stay OFF or the public URL 404s).
- Training: `hf jobs uv run ... scripts/train_*_hf_jobs.py` (see
  `scripts/HF_JOBS.md`); smoke first, then full; adapters land under
  `umeraamir69/`.
- Phone: `python3 phone/server.py`, expose via ngrok for Twilio; WhatsApp
  via Twilio Sandbox ($0), voice PSTN needs paid number + trial credit.
