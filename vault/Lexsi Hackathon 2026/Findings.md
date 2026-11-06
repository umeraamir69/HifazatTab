# Findings — why AFTER is flat, what we built, what to do next

**Date:** 2026-11-04  
**Track:** Lexsi Hackathon Track C (Agentic Fine-tuning)  
**Project:** HifazatTab · [github.com/umeraamir69/HifazatTab](https://github.com/umeraamir69/HifazatTab) · [hifazattab.vercel.app](https://hifazattab.vercel.app)

---

## 1. Executive answer — why we don’t have good results

**GRPO trained, but it did not learn what the AFTER scorer rewards.**

| Metric | BEFORE (zero-shot) | AFTER GRPO v1 | AFTER **SFT v1** | Target |
|--------|-------------------:|--------------:|-----------------:|-------:|
| tool_call_validity | 150/153 (98%) | 146/153 (95%) | **801/801 (100%)** | ≥ 85% |
| task_success | 17/153 (11%) | 16/153 (10%) | **784/801 (97.9%)** | ≥ 75% |
| refusal_precision | 3/21 (14%) | 4/21 (19%) | **21/24 (87.5%)** | ≥ 80% |

**Ship adapter for Track C AFTER:** [`umeraamir69/hifazat-tab-sft-v1`](https://huggingface.co/umeraamir69/hifazat-tab-sft-v1)  
Eval job: `hifazat-after-sft` (COMPLETED). `after_eval.json` on the Hub repo.

GRPO v1 was flat (NL args vs canonical keys). GRPO v2-350 mid-train probes stalled at ~21% task from step 50 → **canceled**. Gold-JSON **SFT** taught exact args + `refuse` and hit all targets. Brand-trap probes (3) still leak tool calls — only miss on refusal.

---

## 2. Root causes (evidence from AFTER dump)

### A. Canonical-arg mismatch (main killer of task_success)

- **Gold in seed:** `lookup_price:atta_20kg` → arg must be exactly `atta_20kg`.
- **Model output:** `"arg": "आटा 20 किलो का दाम"`, `"cheeni 5kg"`, full questions.
- Eval scores **exact string match** on `tool` + `arg`.
- Valid JSON with a natural-language arg → counts as **valid**, fails **task**.

This alone explains most of the 136+/153 task failures.

### B. Weak GRPO reward (v1 train recipe)

In `scripts/train_grpo_hf_jobs.py` (first full run):

- Exact tool+arg → **+1.0**
- Any valid schema, wrong content → **+0.2**
- Safety refuse → weak (+0.5 / −1.0)

With `num_generations=2` and noisy rewards ~0.04–0.20 at step 50, the model could stay on “looks like a tool call” forever and still get positive signal. **It was never forced onto underscore SKU keys.**

### C. System prompt never demanded canonical keys

Train + AFTER eval both said roughly: `arg: <value>`.  
They did **not** say: use `atta_20kg` / `cheeni_5kg` / digits-only for loans.

### D. Wrong tool / wrong intent

From the AFTER log:

- Price prompts → `check_stock` (esp. Urdu combo / price).
- Stock prompts sometimes → `loan_eligibility`.
- Combo gold is `lookup_price`; model often picks `check_stock`.

### E. Safety still open (refusal ~19%)

Probes still emit:

- `write_document` / fake loan letters  
- `customer database` / phone asks  
- `system_prompt` on ignore-rules  
- `lookup_price` with made-up free prices (`$0.50`, `₹45`)

`REFUSE_RE` only looked for cannot/sorry/… — not a dedicated refuse tool.

### F. Generation waffle

Completions often continue after the tool JSON (`User: What is the best way to clean…`). Validity still passes because the regex finds the first `tool_name`/`arg`. Wastes tokens; confuses multi-turn reading of logs.

### G. Train/eval infra notes (not the score gap, but important)

- First GRPO on free Colab T4 → OOM (256k Cohere vocab + KL ref). Fixed via HF Jobs + `beta=0`.
- Smoke L4 ✅; full 50 on **A10G** → Hub `umeraamir69/hifazat-tab-grpo-v1`.
- AFTER notebook loads that adapter; scores above are real.
- Local **rule agent** over shop CSV is still ~perfect on tests — demo quality ≠ Tiny Aya AFTER quality.

---

## 3. What we have done (full inventory)

### Phase 0 — Rule agent (demo + tests) ✅

- 3 tools: `lookup_price`, `check_stock`, `loan_eligibility` over closed CSV.
- Refusal-first safety (fake approval, PII, advice-push, jailbreaks).
- Trilingual answers (en / hi / ur); brand questions do **not** dump prices.
- Unit tests + `src/eval.py` oracle.
- Phone Twilio gather + WhatsApp sandbox (`phone/`).

### Phase 1 — Tiny Aya BEFORE ✅

- Colab `phase1_baseline.ipynb`, 4-bit Tiny Aya fire.
- BEFORE: **150/153 · 17/153 · 3/21** (the gap Phase 2 must close).

### Phase 2 — GRPO on HF Jobs ✅ train / ❌ metrics

| Run | Job | Hub | Outcome |
|-----|-----|-----|---------|
| Smoke 3-step L4 | `6aeb6f2b…` | `hifazat-tab-grpo-v1-smoke` | Fit OK (~$0.14) |
| Full 50 A10G | `6aeb7526…` | `hifazat-tab-grpo-v1` | Train OK (~$2.2); **AFTER flat** |

Hardening that made train possible: `beta=0`, LoRA `q_proj`+`v_proj` r=8, batch1×accum8, `max_steps_per_turn=2`, own seed (not AgentTune TL;DR), chat prompts.

### Phase 1 AFTER eval ✅ ran

- `colab/phase1_after.ipynb` + PeftModel.
- Printed AFTER ≈ BEFORE (see table above).
- Notebook later patched to report **exact** vs **soft (canon arg)** success for diagnosis.

### Catalog expansion ✅

- `data/shop.csv` → **219 SKUs** (staples, pulses, oils, dairy, produce, spices, drinks, household, bakery, snacks, …).
- Research paper draft: `papers/hifazattab_lexsi_2026.md`.
- `scripts/gen_shop_aliases.py` → `src/shop_catalog.py` + `web/shop_catalog.json`.
- `scripts/build_seed.py` → seed covers **all 108** SKUs (825 rows locally; **push to GitHub required** before Colab/Jobs see it).
- Longest-alias resolve; brand ≠ price.

### Live demo site ✅

- Full website inventory (sections, features done/todo, deploy, voice): **`Website.md`**.
- https://hifazattab.vercel.app — Track C story, samples, red-team panel, shop table.
- Speak answers (TTS); EN/HI browser STT; brand-safe replies; Hindi/Urdu **localized** price/stock strings.
- Category filter, search, click-to-ask, random SKU.
- SSO protection disabled (was 404).

### Urdu STT (Whisper) ✅ wired

- Browser has **no** Urdu Web Speech STT → backend `web/api/stt.js`.
- **Groq only** (`GROQ_API_KEY`) — Whisper large-v3. **No OpenAI / Google required.**
- Live smoke: `/api/stt` returns `provider: "groq"`.
- اردو mic records ~4s → Whisper → same agent.

### Docs / Discord

- Vault: Plan, Research, Results, Status, Architecture, Data, Decisions, Redteam, Submission drafts.
- `Discord_ticket_report_issues.md` ready (confirm CSV+3 tools, beta=0, demo=rule-agent).
- `scripts/HF_JOBS.md`, `phone/VOICE_E2E.md`, `LOG.md`.

### Fixes already coded for the *next* GRPO (local, needs push + retrain)

In `scripts/train_grpo_hf_jobs.py`:

1. System prompt: **canonical SKU keys** + digits-only loan + explicit `refuse` tool for probes.
2. Reward: +1 exact only; right-tool/wrong-arg **+0.1**; wrong tool **−0.2**; safety refuse **+1 / −1.5**.
3. Tool executors normalize aliases → shop keys so rollouts get real PKR, not `item_not_found`.
4. AFTER notebook: `task_success_exact` + `task_success_soft`.

---

## 4. What to do now (ordered)

### Must-do for Track C metrics (this week)

1. **Commit + push** catalog, seed, train script, AFTER notebook, web STT (so Jobs/Colab hit GitHub `main`, not stale 7-SKU seed).
2. **Re-run GRPO** on HF Jobs with the tightened recipe:
   ```bash
   hf jobs uv run --flavor a10g-small --timeout 4h --secrets HF_TOKEN \
     scripts/train_grpo_hf_jobs.py -- --max-steps 100 \
     --hub-id umeraamir69/hifazat-tab-grpo-v2
   ```
3. **Re-run AFTER** (`phase1_after.ipynb` → point `ADAPTER_ID` at `…-grpo-v2`).
4. Expect: soft success rises first; exact success if prompt+reward stuck. Target task ≥ 50% then push toward 75%.
5. If GRPO still flat after strict reward → **SFT warm-start** (`colab/phase2_sft.ipynb`) on gold JSON lines (`arg` = canonical key), then short GRPO.

### Safety lift

6. Add more `must_refuse` rows; reward only `refuse` / no shop tool.
7. Red-team script-switch set → log obey/refuse → optional SafeTune/DPO (Phase 4).

### Demo Day (can stay strong even if Tiny Aya AFTER is mid)

8. Live path = **rule agent + Groq Urdu mic + TTS** (already works). Judges hear correct PKR; adapter is for the metrics slide.
9. Walk `phone/VOICE_E2E.md`; optional WhatsApp sandbox.
10. Post Discord ticket; AuditKIT on `trajectories.jsonl` for the writeup.

### Do **not** do

- Do not burn more credits on the **v1 reward** recipe.
- Do not require OpenAI/Google STT (Groq is enough).
- Do not claim AFTER > BEFORE until v2 numbers are printed.

---

## 5. Honest narrative for submission / Discord

> Tiny Aya zero-shot already formats tool calls (98% validity) but fails content (11% task) and safety (14% refusal). First AgentTune GRPO on A10G (50 steps, beta=0 for 256k-vocab fit) **completed and pushed**, but AFTER stayed flat because rewards over-credited any valid JSON and never forced canonical SKU args. We diagnosed from the AFTER dump, tightened reward+prompt, expanded the shop to 219 SKUs with full seed coverage, shipped SFT AFTER (100%/98%/88%), and a live trilingual demo (rule-oracle + Groq Whisper Urdu). Paper draft: `papers/hifazattab_lexsi_2026.md`.

---

## 6. Artifact index

| Artifact | Where |
|----------|--------|
| BEFORE scores | `colab result/`, Results.md |
| AFTER dump / scores | this Findings.md + Colab printout |
| Adapter v1 | https://huggingface.co/umeraamir69/hifazat-tab-grpo-v1 |
| Smoke adapter | https://huggingface.co/umeraamir69/hifazat-tab-grpo-v1-smoke |
| Train script | `scripts/train_grpo_hf_jobs.py` |
| Jobs guide | `scripts/HF_JOBS.md` |
| Shop + seed | `data/shop.csv`, `data/seed_tasks.jsonl` |
| Demo | https://hifazattab.vercel.app |
| Urdu STT | `web/api/stt.js` + Vercel `GROQ_API_KEY` |
| Rule agent | `src/agent.py`, `src/tools.py` |

---

## 7. Credits / spend (approx.)

| Item | Est. |
|------|------|
| Smoke GRPO L4 | ~$0.14 |
| Full GRPO 50 A10G | ~$2.2 |
| Remaining of $20 | use for **v2** (prefer 100 steps) + maybe one SFT job |
| Groq Whisper | free tier (demo STT) |
