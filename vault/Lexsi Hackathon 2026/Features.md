# Features — where we stand + what to build next

**Date:** 2026-11-06 · **Owner:** umeraamir69 · **Docs home:** this vault.
Root code docs: `ARCHITECTURE.md`, `API_ENDPOINTS.md` (repo root).

Effort legend: **S** = one sitting · **M** = a day · **L** = multi-day / GPU credits.

---

## 1. Where we stand (verified 2026-11-06)

| Area | State |
|------|-------|
| Rule agent + eval + redteam | Green: **12/12** unit tests pass (`python3 -m unittest discover -s tests`) |
| Catalog | **219 SKUs** + 2 loan-config rows in `data/shop.csv` (221 rows); `shop_catalog.json` holds `catalog` + `aliases` (219 each) |
| Seed | **1491 rows**: 1467 tool-task (760 price / 691 stock / **16 loan**) + 24 probes; langs balanced **495 en / 495 hi / 495 ur** (+ 6 legacy `ok_N` rows missing `lang`) |
| BEFORE (Tiny Aya zero-shot) | validity 150/153 · task 17/153 · refusal 3/21 |
| AFTER (SFT `hifazat-tab-sft-v1`) | **validity 801/801 · task 784/801 (97.9%) · refusal 21/24 (87.5%)** — targets met |
| AFTER (GRPO v1/v2) | Flat / stalled ~21% — negative result, documented in `Findings.md` |
| Live demo | https://hifazattab.vercel.app (public, SSO off); EN/HI mic, Urdu Groq Whisper STT, TTS, red-team panel, SFT metric bars filled |
| Paper draft | `papers/hifazattab_lexsi_2026.md` (SFT-after story complete) |
| Root docs (new) | `ARCHITECTURE.md` (system, flows, deploy) · `API_ENDPOINTS.md` (phone + STT) |

**Still open:** AuditKIT run on trajectories · quant-survival re-eval for the
SFT adapter · 3 brand-trap refusal misses · HF dataset push + model card ·
Discord ticket update · human voice E2E walk (`phone/VOICE_E2E.md`).

---

## 2. Must-do before Nov 14 submit

- [x] **F1 — AuditKIT on trajectories (S).** Done 2026-11-06:
  `.venv` (project env) + `auditkit` + `scripts/eval_auditkit.py`
  (`episodes_from_agenttune` → validity / task / tool-name / macro-F1 /
  refusal, gold joined from seed by exact prompt). GRPO v1 (400 episodes,
  seed match 180/400): validity **131/134 (97.8%)** · task **38/180
  (21.1%)** · tool-name **132/180 (73.3%)** · macro-F1 **0.2176** · refusal
  **2/46 (4.4%)**. Reports in `reports/` (trajectories copy gitignored).
  `--seed` flag added (committed compact-unit seed matches train phrasings;
  working regen uses spaced units — see Results). SFT side: `--after-eval`
  converter ready (`--after-eval` synthetic-tested); `eval_after_hf_jobs.py`
  now saves full per-prompt `records`. BLOCKED 2026-11-06: HF Jobs returned
  **402 — prepaid credits exhausted**, $0 spent, nothing launched. Unblock:
  add credits, or human runs `colab/phase1_after.ipynb` (PeftModel AFTER eval)
  and drops the resulting after_summary.json here — converter takes it from
  there.
- [x] **F2 — Quant survival for the SFT adapter (S).** Done 2026-11-06 by evidence: the AFTER numbers (801/801 · 784/801 · 21/24) were measured with the base loaded in **4-bit nf4** (`BitsAndBytesConfig` in `eval_after_hf_jobs.py`, which produced the Hub `after_eval.json`) — absolute quant numbers meet all targets. Caveat: no full-precision run exists, so the full→quant Δ is unmeasured. Re-run recipe (GPU): `hf jobs uv run ... scripts/eval_after_hf_jobs.py -- --adapter umeraamir69/hifazat-tab-sft-v1`.
- [ ] **F3 — Fix the 3 brand-trap misses (S).** Rule-agent half done
  (refuse + SKU tip, no price digits — `test_brand_no_price_dump`); seed
  half done 2026-11-06 (brand_price_combo + brand_stock_combo probes × 3
  langs → refusal 30/30, no price leak). Retrain half BLOCKED on the same
  402 credits issue. Recipe (new adapter, never overwrite sft-v1):
  `hf jobs uv run ... scripts/train_sft_hf_jobs.py -- --hub-id
  umeraamir69/hifazat-tab-sft-v2` then the eval job.
- [x] **F4 — HF dataset + model card (S).** Done 2026-11-06:
  https://huggingface.co/datasets/umeraamir69/hifazat-tab-seed (1506 rows +
  oracle + provenance card); real model card on
  https://huggingface.co/umeraamir69/hifazat-tab-sft-v1 (recipe, metrics,
  limits, links).
- [x] **F5 — Submission form numbers (S).** Why: `Submission.md` metrics
  were TBD — filled with SFT AFTER numbers 2026-11-06; copy to the real
  form at ship.
- [ ] **F6 — Discord ticket + voice walk (S, human).** Draft ready
  2026-11-06 (progress-update text in `Discord_ticket_report_issues.md`,
  NOT YET POSTED); voice walk `phone/VOICE_E2E.md` still needs a human.

## 3. Demo polish (Demo Day leverage, each S)

- [x] **F7 — Hold-to-talk Urdu mic.** Why: fixed ~4.5 s window clips long
  questions. Done 2026-11-06: Stop button (`micStop` → `stopUrduRec`) +
  8 s auto-stop note under the ask row.
- [x] **F8 — AFTER bars from JSON config.** Why: bars are hardcoded in
  `web/index.html`. Done 2026-11-06: `web/metrics.json` + `loadMetrics()`
  fetch with hardcoded-bar fallback.
- [x] **F9 — Tool-trace display.** Why: judges trust what they see — show the
  emitted `tool:arg` JSON chip under each answer. Done 2026-11-06: answer
  chip shows `tool:item`; `answer()` returns `item`.
- [x] **F10 — WhatsApp deep-link on site.** Why: the $0 path exists in
  `phone/`. Done 2026-11-06: Artifacts links SFT adapter + WhatsApp $0
  guide (`phone/README.md`).
- [x] **F11 — "Live = rule agent, HF = metrics" callout.** Why: recommended
  in `Website.md`. Already present above the ask box (`#try` panel).

## 4. Robustness (correctness + safety depth)

- [x] **F12 — Roman-Urdu / Roman-Hindi keywords (S).** Done 2026-11-06:
  roman refusal (`bhool`, `manzoor`, `bardasht`, `jhoot`, `naqli/jaali`) +
  intent words (`bhav`, `rate`, `qarza`…) + `doodh`/`sabun` aliases, mirrored
  in page JS; `has_word` boundary matching both sides; locked by
  `test_roman_*`. Also fixed real bug found by new seed: `dam` fired inside
  `cardamom` (3 stock misses → 0).
- [x] **F13 — Loan-seed depth (S).** Done 2026-11-06: incomes
  5 → 8 incl. tier edges (39999/40000, 149999/150000) + zero; loan rows
  15 → 24. Eval: **1476/1476 task, 24/24 refusal, 0 over-refusal.**
- [x] **F14 — Seed hygiene (S).** Done 2026-11-06: `ok_N` → `spot_*` ids with
  inferred `lang`; seed now 1500 rows, 219/219 SKU coverage.
- [x] **F15 — Webhook hardening (S).** Done 2026-11-06: `TWILIO_AUTH_TOKEN`
  signature gate on `/voice`/`/gather`/`/whatsapp` (403 otherwise, open for
  local dev); locked by `test_twilio_signature`; `/api/stt` rate limit still
  open.
- [x] **F16 — Red-team 9 → 24 attacks (S).** Done 2026-11-06: 8 families × 3
  scripts in `src/redteam.py` AND page `ATTACKS` (incl. roman + brand trap);
  **24/24 blocked** both sides. 30–50 corpus remains Phase-4 stretch.

## 5. Stretch (only after submit / with leftover credits)

- [ ] **F17 — SafeTune/DPO repair loop (L).** Failures from F16 become
  refusal pairs → retrain → re-attack → re-quant. The weights-over-wrappers
  story (D10).
- [ ] **F18 — GRPO from the SFT checkpoint (L + credits).** Why: strict
  reward + canonical-arg prompt may now work where v1/v2 failed — but only
  on SFT's shoulders, never the v1 recipe (see `Findings.md` §4).
- [ ] **F19 — AuditKIT charts on site (M).** Embed before/after F1 bars from
  the F1 report instead of linking out.

## 6. Explicitly not doing

- OpenAI/Google STT (Groq covers Urdu; EN/HI are browser-native).
- More GRPO on the v1 reward recipe (proven flat — Findings §4).
- New tools / multi-domain ERP (scope lock D5: 3 tools, 1 CSV).
- Posting or pushing as any identity but **umeraamir69** (D7).
