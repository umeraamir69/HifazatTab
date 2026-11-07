# HifazatTab — Everything Log

Running record of **what** we do, **why**, **cause**, **result**, **how to do better**, plus an **evaluator** pass/fail after each step.

**Standing rules**
- Track C only (Agentic Fine-tuning): AgentTune → AuditKIT.
- Languages: Urdu, Hindi, English.
- Plan before train code. Vault docs in `Documents/Obsidian Vault/Lexsi Hackathon 2026/`.
- GitHub + HF as **umeraamir69** only — never Cursor bot.
- Cut last: before/after metrics, live refusal demo, quant survival check.

---

## 2026-10-30 — Research Lexsi.ai + Track C facts

- **What:** Read hackathon.lexsi.ai, lexsi.ai, Tiny Aya docs, AgentTune v1.1 / AuditKIT agent_eval notes.
- **Why:** Form pitch and plan must match real rules (chain ≥2 track repos, Cohere dense models, HF artifacts, before/after metrics).
- **Cause:** User required research + plan-before-code; wrong track wastes the window.
- **Result:** Track C = AgentTune post-train tool agents + AuditKIT via `episodes_from_agenttune`. Tiny Aya has no native tools template → AgentTune `tools_fallback_prompt`. `tiny-aya-fire` best for South Asia; `global` is documented example. Submit Nov 14; Demo Day Nov 22; teams 1–3; identity must match HF for credits.
- **Better:** Re-verify sample problem statements when posted; pin exact Hub IDs after licence accept at kickoff.
- **Evaluator:** Meaningful? **Yes** — facts are actionable for pitch/plan. Gap: sample Track C problems still TBA (score risks 4/5 not 5).

## 2026-10-30 — Complete plan suite in Obsidian (no train code)

- **What:** Rewrote Research + Plan; added Architecture, Decisions, Data, Redteam, Runbook, Status, Submission, `sessions/2026-10-30`; refreshed Home. Synced this LOG + README pitch.
- **Why:** User: document each step with what/why/cause; proper complete plan first; docs live in vault; maintain one everything-file.
- **Cause:** Home already linked missing notes; empty plan = premature coding risk.
- **Result:** Form pitch locked. Plan phases 0–5 with done-when gates. Scope: 3 tools, 1 CSV, 3 langs. Deliverables + metric targets listed. Plan-before-code respected (no GRPO/agent train code).
- **Better:** Balance `seed_tasks.jsonl` lang counts (en-heavy) before Phase 1; twin-update Runbook whenever we run shell.
- **Evaluator (Plan checklist mean):** **4.9 / 5 → PASS.** Ready for Phase 0 stdlib scaffolding next; still no AgentTune train until Phase 1 baseline.

### Evaluator detail (Plan)

| Criterion | Score | Comment |
|-----------|-------|---------|
| Track C compliance | 5 | AgentTune+AuditKIT mandatory |
| Form pitch | 5 | Few lines + one-liner |
| Thesis clarity | 5 | what/why/cause |
| Scope lock | 5 | tools/langs/out-of-scope |
| Phased gates | 5 | done-when + calendar |
| Metrics ≥2 | 5 | F1, validity, task, refusal, consistency, quant |
| Naming HifazatTab | 5 | Urdu/Pakistan |
| Risks | 4 | TBA sample problems |
| umeraamir69 rule | 5 | explicit everywhere |
| Plan before code | 5 | no train this session |

## 2026-10-30 — Rename note (prior)

- **What:** SurakshaTab → HifazatTab.
- **Why:** User rule — Urdu / Pakistan-associated.
- **Cause:** حفاظت = protection/safety fits alignment thesis; Tab = tabular.
- **Result:** grep clean of old name in active docs.
- **Evaluator:** Meaningful — name matches audience + safety story.

---

## 2026-10-31 — APIs and access check
- What: verified what each company provides.
- Cohere: Tiny Aya `fire`/`global`/etc. live on Cohere API Chat endpoint (key needed,
  free tier rate-limited); open weights on HF (gated licence). No token charges
  until rate limit per third-party report — confirm in dashboard.
- Lexsi: stack on GitHub + PyPI (`pip install agenttune`, `pip install auditkit`,
  core is zero-dep stdlib). Note licence is source-available, not OSI open-source.
- Hugging Face: hosts everything; hackathon gives $20 credits (Discord teams),
  +$200 if shortlisted, usable on ZeroGPU.
- Test: claims match docs pages fetched today. Evaluator: meaningful, unblocks Phase 1.

## 2026-10-31 — Phase 2 notebook written + Results doc
- What: `colab/phase2_grpo.ipynb` (inspect API → login → rewards → train 100
  steps → push adapter) + vault `Results.md` (Phase 0/1 what+scores, Phase 2
  plan+targets). Committed 1477f4d, pushed.
- Honest caveat: untested locally (no GPU). Cell 1 prints the installed
  signature so we adapt if kickoff changed it. Reward-func interface is best
  guess from docs — user pastes any error back.
- Evaluator: notebook JSON valid. Meaningful pending Colab run.

## 2026-10-31 — REAL BASELINE from Colab (tiny-aya-fire)
- What: user ran phase1 notebook. Validity 150/153, task 17/153, refusal 3/21.
- Why it matters: proves the thesis opening — format OK, answers wrong, safety
  hole open. Recorded in vault Status. Nothing to fix; this IS the before photo.
- Evaluator: meaningful. Phase 2 authorized next.

## 2026-10-31 — Site 404 fixed (Deployment Protection)
- What: hifazattab.vercel.app went 404 for the public. Cause: Vercel Deployment
  Protection was on (SSO redirect proven by headers). Fix: user disabled it in
  dashboard + fresh redeploy to apply. Verified 200, 10775 bytes.
- Evaluator: live marker check passed. Meaningful.

## 2026-10-31 — Can voice calls be free? (answered)
- What: yes for demo, no forever. Twilio trial credit (~$15) covers ~100 min
  at $0.15/min PK rates — plenty for Demo Day. Budget needed after trial.
  $0-forever paths stay: browser voice + WhatsApp Sandbox.
- Caveats logged: no PK numbers (US number), trial-number verification needed,
  possible PK-mobile drop reports — test before Demo Day.
- Evaluator: claims match fetched Twilio pricing; trial-credit figure flagged
  verify-in-console.

## 2026-10-31 — Swagger UI at /docs
- What: `phone/openapi.yaml` (validated with pyyaml, all 4 paths) + `/docs`
  serves Swagger UI, `/openapi.yaml` serves the spec. 7/7 tests OK.
- Run `python3 phone/server.py`, open http://localhost:8080/docs.
- Committed 7712c37, pushed, tree clean.

## 2026-10-31 — $0 rule + WhatsApp path + API docs
- What: user rule — everything must be free. PSTN calls parked (no PK numbers,
  ~$0.15/min). Added free WhatsApp Sandbox route, `phone/README.md` ($0 recipe
  + honest limits), `phone/API.md` (all 4 routes with curl examples).
- Test: 6/6 unit tests OK (handlers pure, no server needed). Committed 26eb6bc,
  pushed, tree clean. No live-server probe (macOS sandbox blocks backgrounding).
- Evaluator: meaningful.

## 2026-10-31 — Voice agent live
- What: Mic input (SpeechRecognition per-language) + spoken replies
  (speechSynthesis, voice matched by lang). Still one file, no keys/servers.
- Bug in rollout: first redeploy raced the alias; redeployed, verified live
  marker "Mic: speak" + 10775 bytes. Committed c3b55e6, pushed.
- Evaluator: node harness SMOKE OK incl. mic fallback + voice-on ask.

## 2026-10-31 — Deployed to Vercel
- What: `vercel --prod` from `web/` as fresh project `hifazattab`
  (first attempt linked a stale Next.js project — deleted link, redeployed).
  Live: https://hifazattab.vercel.app (200, 9066 bytes, exact artifact).
- Evaluator: curl confirms reachability + correct bytes. In-browser rendering
  unverified (no browser on laptop); JS logic harness-verified.

## 2026-10-31 — 100+ rows + showcase site (user's 3 asks)
- What: researched reuse sets (HinglishAssistBench, Urdu-Instruct/Alpaca, logged
  in Research §7b). `scripts/build_seed.py` generates 174 rows deterministically.
  `web/index.html` single-file showcase: ask in 3 langs, red-team runner, scores.
- Evaluator run found + fixed 2 bugs: rice-in-price substring, missing Devanagari
  दाम. Scores: task 153/153, refusal 21/21, consistency 5/5, redteam 9/9,
  unit tests 5/5. Node harness smoke of exact artifact: SMOKE OK (init, Hindi
  ask, Urdu ask, 9/9 blocked). Committed d01fc6f, pushed.
- Evaluator: meaningful. Chromium absent on laptop — in-browser rendering
  unverified; logic verified via harness.

## 2026-10-31 — Colab bugfix (ARG regex group)
- What: Gemini/Colab flagged real bug — `m2.group(2)` on a 1-group regex.
  Fixed to `group(1)` in ipynb + py. Committed bcd9d86, pushed.
- Note: user ran an older notebook copy (getpass version). Told to re-open
  from GitHub. Config URL 401 = gated repo, correct with token.
- Evaluator: grep confirms no group(2) left, JSON valid. Meaningful.

## 2026-10-31 — HF token in .env + Colab Secrets wiring
- What: HF token stored in `.env` (gitignored). Notebook login cell now reads
  Colab Secrets `HF_TOKEN`, fallback hidden paste. Token never in code/git.
  Committed 414fe0f, pushed. README Cell 2 updated.
- Evaluator: notebook JSON valid, login cell verified by string check. Meaningful.

## 2026-10-31 — Cell guide as separate doc
- What: user stopped inline notebook explainers; wrote `colab/README.md`
  instead (one plain-words section per cell: why + cause). Notebook reverted
  to clean 4-cell version. Committed d88823e, pushed.
- Evaluator: notebook JSON valid, tree clean. Meaningful.

## 2026-10-31 — Committed + pushed as umeraamir69
- What: `git commit` (root-commit c815bbf, 26 files) + new public repo
  `umeraamir69/HifazatTab`, pushed to main. Author verified: umeraamir69.
  Tree clean, `.env` excluded.
- Evaluator: meaningful — deliverable checklist item "public GitHub repo" done.

## 2026-10-31 — Vault moved into repo + key in .env
- What: `Lexsi Hackathon 2026` notes moved from main Obsidian vault to
  `Documents/Lexsi/vault/` (own vault, open that folder in Obsidian).
  Key stored in `.env`, gitignored and verified ignored by git.
- Why: user rule — docs with the repo; secrets out of notes/git.
- Evaluator: `git status` shows no `.env`. Meaningful.

## 2026-10-31 — Cohere key verified (value NOT stored)
- What: user supplied a Cohere key in chat. Verified live: `tiny-aya-fire`
  answered OK via API. Key exists only in chat, never in files/git/memory.
- Note: laptop python3.16 SSL was broken (CERTIFICATE_VERIFY_FAILED). Fixed by
  running `/Applications/Python 3.16/Install Certificates.command` (certifi +
  cert.pem symlink). Verified: Python TLS handshake to api.cohere.com now works
  (401 = correct auth reply, not SSL fail). Colab unaffected.
  Recommend user rotate key (shared in plaintext) and use `.env` going forward.
- Evaluator: meaningful — Phase 1 quick-tests unblocked.

## 2026-10-31 — Phase 0 built and green
- What: `src/tools.py`, `agent.py`, `eval.py`, `redteam.py`, `demo.py`,
  `tests/test_agent.py`. Fixed 3 bugs found by evaluator run: lowercased table
  key broke `cooking_oil_5L`; stock keyword beat price keyword; Devanagari कीमत
  missing; hi/ur advice-push bypassed (order-dependent patterns).
- Scores: task 13/13, refusal 5/5, over-refusal 0, consistency 4/4, redteam 9/9,
  unit tests 4/4 OK.
- Why: need a "before" number + live demo before gated Tiny Aya download.
- Evaluator (Plan §9): pass. Baseline is meaningful — real trilingual tool loop
  with independent oracle, not hard-coded answers.

## 2026-10-31 — STEP_BY_STEP.md written
- What: complete beginner guide (accounts → setup → Phases 0–5 → ship → fixes).
- Why: user rule — document everything, explain so a newcomer can follow.
- Test: file exists, commands reference real repo paths. Evaluator: meaningful.

## 2026-10-31 — Phase 1 Colab SUCCESS — results archived

- **What:** Captured finished Phase 1 Colab stdout into `colab result/`:
  `colab_result_phase_1.md`, `.json`, `_full_log.txt`.
- **Scores (Tiny Aya fire, zero-shot, T4):**
  tool_call_validity **150/153 (98%)** · task_success **17/153 (11%)** ·
  refusal_precision **3/21 (14%)**.
- **Why:** Need durable BEFORE metrics for before/after write-up + Phase 2 target.
- **Cause:** Notebook private-outputs UI; pulled stdout from Colab cell model via browser CDP.
- **Evaluator:** Meaningful weak baseline — high validity, low exact task match, poor refusal.
  Exactly the gap AgentTune GRPO should close. **PASS** as Phase 1 gate.
- **Better next:** notebook should also `json.dump` replies + scores to `/content/...`
  so we don't scrape the UI.

## 2026-10-31 — Phase 1 Colab error: `load_in_4bit` TypeError

- **What:** Colab cell 3 crashed: `TypeError: Cohere2ForCausalLM.__init__() got an unexpected keyword argument 'load_in_4bit'`. Fixed local `phase1_baseline.ipynb` + `.py` to use `BitsAndBytesConfig`; also `DEVICE = next(model.parameters()).device` instead of `model.device`.
- **Why:** Need a real Tiny Aya "before" number; broken load blocks Phase 1.
- **Cause:** Newer `transformers` no longer accepts `load_in_4bit=` as a direct `from_pretrained` kwarg for Cohere2 — it must go through `quantization_config=BitsAndBytesConfig(...)`.
- **Result:** Repo fixed. **Colab Drive copy still needs the same paste** (Drive ≠ git until re-upload/sync).
- **Better:** Pin a transformers version in the install cell after first green run; always re-sync Drive notebook from repo after fixes.
- **Evaluator:** Meaningful fix — matches the exact traceback on screen. PASS if re-run loads model without TypeError.

## 2026-11-03 — HF $20 credits claimed
- **What:** Lexsi Discord / registration $20 Hugging Face compute credits are live.
- **Why:** Free Colab T4 OOMs on AgentTune GRPO (Cohere 256k logits). Credits buy bigger GPUs.
- **Cause:** Need ≥24 GB VRAM headroom for Tiny Aya tool-rollout GRPO.
- **How to spend:** Hugging Face **Jobs** (pay-per-minute), not ZeroGPU Spaces.
  Prefer `l4x1` (~$0.80/hr, 24 GB) or `a10g-small` (~$1/hr, 24 GB). Avoid burning
  credits on T4-class. ZeroGPU is for Spaces demos / short inference.
- **Budget:** ~20h on L4 or ~20h on A10G-small. Plan: 1–2 GRPO smoke runs (30–50
  steps) + one AFTER eval + keep leftover for Demo Day polish if shortlisted.
- **Evaluator:** Meaningful unblock. Do SFT on free Colab in parallel if needed;
  use credits for GRPO that actually fits.
- **Better:** Pin flavor + timeout before launch; push adapter every N steps so a
  killed job still leaves an artifact.

## 2026-11-04 — HF Jobs GRPO script ready
- **What:** Added `scripts/train_grpo_hf_jobs.py` + `scripts/HF_JOBS.md`. Hardened
  `colab/phase2_grpo.ipynb` to point at Jobs (not free T4).
- **Why:** User has credit balance; Colab notebooks are the wrong spend path.
- **Cause:** Need one PEP-723 UV script with beta=0, slim LoRA, max_steps_per_turn=2,
  chat prompts, `--smoke` then `--max-steps 50` on `l4x1`.
- **Result:** Dry-run OK via `hf jobs uv run`. Smoke → `…-grpo-v1-smoke`; full →
  `umeraamir69/hifazat-tab-grpo-v1`. SFT stays free-Colab fallback.
- **Evaluator:** PASS for packaging. Real PASS = smoke job COMPLETED without OOM.

## 2026-11-04 — Smoke GRPO PASSED on HF Jobs L4; full 50 launched
- **What:** Verified HF browser login (umeraamir69) + billing **$20.00** / $0 used;
  gated access to `CohereLabs/tiny-aya-fire` granted. Launched Jobs myself via CLI.
- **Smoke Job:** `6aeb6f2b0e0338d1bb80117d` name=`hifazat-grpo-smoke`
  URL: https://huggingface.co/jobs/umeraamir69/6aeb6f2b0e0338d1bb80117d
  - Flavor `l4x1`, CUDA: **NVIDIA L4**, free VRAM before train **23.46 GB**
  - Stage COMPLETED. scheduling ~79s, running **623s** (~10.4 min)
  - Est. cost ≈ **$0.14** (623/3600 × $0.80)
  - Train 3/3 steps; `tools_fallback_prompt` fired (Tiny Aya ignores tools template)
  - Rewards mean ≈ 0.1–0.2; loss/grad_norm reported 0 on smoke (few steps / low
    within-group variance — expected for 3-step fit test, not a failure)
  - Hub artifact: https://huggingface.co/umeraamir69/hifazat-tab-grpo-v1-smoke
    `adapter_model.safetensors` ~7.7 MB + `trajectories.jsonl` + ckpts 1–3
- **Full Job (in flight):** `6aeb720ac78863f9c632cde3` name=`hifazat-grpo-full50`
  URL: https://huggingface.co/jobs/umeraamir69/6aeb720ac78863f9c632cde3
  - `--max-steps 50`, timeout 4h, same L4. Target hub: `umeraamir69/hifazat-tab-grpo-v1`
  - ETA ~2–2.5h at ~150–180s/step; est. cost ~$1.5–2.5
- **Why:** Prove GRPO fits paid 24 GB before burning a long run; then train AFTER.
- **Cause:** Free T4 OOM path dead; Jobs + credits is the real Phase 2 path.
- **Evaluator:** Smoke **PASS**. Full pending. Next AFTER = Phase 1 notebook vs adapter.
- **Better:** Watch completion lengths (smoke mean ~288 tokens, clipped_ratio up to
  0.375) — tighten generation caps if full run wastes steps on long waffle.

## 2026-11-04 — phase1_after.ipynb (PEFT AFTER eval)
- **What:** New Colab notebook loads base Tiny Aya 4-bit + Hub LoRA
  `umeraamir69/hifazat-tab-grpo-v1`, same seed/scoring as Phase 1 BEFORE.
- **Why:** Baseline notebook is zero-shot only; AFTER needs PeftModel.
- **Cause:** Fair before/after requires identical prompts + metrics.
- **Result:** File `colab/phase1_after.ipynb`. User runs on free T4, pastes scores.
- **Evaluator:** PASS when AFTER block printed; compare to 150/153 · 17/153 · 3/21.

## 2026-11-04 — Full GRPO 50 COMPLETED on A10G
- **What:** Job `6aeb7526c78863f9c632d1f4` finished 50/50 steps; pushed
  https://huggingface.co/umeraamir69/hifazat-tab-grpo-v1 (adapter + trajectories).
- **Why:** Phase 2 AFTER artifact for Track C metrics.
- **Cause:** Smoke proved fit; A10G avoided L4 queue stall.
- **Result:** running ~8028s (~2.2h), est. ~$2.23. train_loss ≈ -0.004.
  Last-step reward ~0.04–0.20 (noisy; need AFTER eval). Site 200.
- **Evaluator:** Train path PASS. Score PASS only after Phase 1 AFTER + AuditKIT.

## 2026-11-04 — Voice bot E2E locked (public site was 404)
- **What:** Confirmed `hifazattab.vercel.app` returned 404 under Vercel SSO
  (`ssoProtection: all_except_custom_domains`). Disabled SSO, redeployed `web/`,
  hardened mic UX (voice-on-by-default, clearer errors), wrote
  `phone/VOICE_E2E.md` done-when checklist.
- **Why:** User requires end-to-end flawless voice bot at the end; judges need a
  30s live path that never waits on GPU.
- **Cause:** Voice demo = browser STT/TTS + deterministic shop agent (same tools
  as phone). Tuned Tiny Aya is for AFTER metrics, not call latency.
- **Result:** Site **200** again. Unittest 7/7 OK. GRPO A10G still training in
  parallel. Phone/WhatsApp paths documented as B/C gates.
- **Evaluator:** PASS for unblocking public voice. Remaining: human mic walk of
  EN/HI/UR + optional Twilio trial call before Demo Day.

## How we can do better (standing backlog)

1. Keep seed small until baseline scores exist; then scale.
2. Never cut: before/after metrics, live refusal, quant check.
3. Urdu auto-eval is weak → 30-sample human check, reported separately.
4. Every HF push under umeraamir69; double-check `git config user` before commit/push.
5. After Oct 31 kickoff: pin model ID + Lexsi API versions in Requirements freeze section below.

## Requirements freeze (fill at kickoff)

| Package / model | Version / ID | Date pinned |
|-----------------|--------------|-------------|
| agenttune | TBD | |
| auditkit | TBD | |
| Tiny Aya HF id | TBD (`fire` or `global`) | |

## 2026-10-31 — Remember for LinkedIn

- **Fact:** bitsandbytes 4-bit path does not exist on Apple Silicon (CUDA-only).
- Phase 1 Tiny Aya baseline ran on **Colab T4**, not the Mac.
- OK to post about this friction. Do not imply a local Mac 4-bit load worked.

## 2026-11-04 — AFTER flat; Findings documented; Groq Urdu STT live
- **What:** AFTER eval on `hifazat-tab-grpo-v1` ≈ BEFORE (validity 146/153,
  task **16/153**, refusal **4/21**). Wrote
  `vault/Lexsi Hackathon 2026/Findings.md` + updated Results/Status. Root cause:
  gold canonical args vs NL args; v1 reward +0.2 for any valid JSON. Tightened
  train script for v2; 108-SKU catalog + seed; site features; `GROQ_API_KEY` on
  Vercel — Urdu Whisper works (`provider: groq`). No OpenAI/Google STT needed.
- **Why:** User asked why results are bad and to document everything done.
- **Cause:** Train completed but objective mismatch with scorer.
- **Result:** Docs complete. Next = push + GRPO v2 + re-AFTER.
- **Evaluator:** Diagnosis PASS. Metric PASS only after v2 AFTER lift.

## 2026-11-04 — Website.md (demo site inventory)
- **What:** `vault/Lexsi Hackathon 2026/Website.md` — all sections, features
  done vs todo, voice architecture (EN/HI browser STT, UR Groq Whisper),
  deploy/env, agent contract vs Python, demo script, changelog.
- **Why:** User asked to document everything we do/are doing for the website.
- **Result:** Linked from Status + Findings.

## 2026-11-06 — GPU close-out attempted, blocked on credits (402)

- **What:** Tried to close the GPU remainder (SFT-side AFTER eval job for the
  episode report; SFT-v2 brand-trap retrain next). `hf jobs uv run` for
  `eval_after_hf_jobs.py` on a10g-small returned **402 Payment Required —
  prepaid credits exhausted**. Verified: `hf jobs list` shows nothing running
  ($0 spent, nothing launched). Auth as umeraamir69 works; `hf` CLI fine.
- **Why:** User said do the still-open backlog; GPU items were the only path.
- **Cause:** $20 Hackathon credits fully consumed by earlier smoke/full/SFT
  Job runs (see Findings spend notes).
- **Unblock paths (human):** (a) add HF credits → re-run the exact launched
  command (eval ~$0.30 on a10g-small; SFT-v2 retrain ~$1–1.5 + eval ~$0.30);
  (b) free path: run `colab/phase1_after.ipynb` (PeftModel AFTER eval, T4
  inference fits) and save after_summary.json — the `--after-eval` converter
  is synthetic-tested and waiting. Brand-trap retrain recipe pinned in
  Features F3 (new `sft-v2` id, never overwrite sft-v1).
- **Still human-only:** Discord post (draft ready, not posted), voice E2E walk.
- **Evaluator:** blocked with $0 damage and recipes ready — honest stop.

## 2026-11-06 — Backlog done: F2/F4/GPU-prep, brand probes, dataset + card live

- **What:** (1) Seed: added brand_price_combo + brand_stock_combo probes × 3
  langs → 1506 rows; eval **1476/1476 task, 30/30 refusal**, combo probes
  refuse with no price digits. (2) `eval_after_hf_jobs.py` now saves full
  per-prompt `records`; `eval_auditkit.py` gained `--seed` + `--after-eval`
  (synthetic-tested) — SFT-side episode report needs only one GPU AFTER
  re-run. (3) F2 closed by evidence: Hub `after_eval.json` came from the 4-bit
  nf4 pipeline → absolute quant numbers meet targets (Δ vs full precision
  unmeasured); re-run recipe documented. (4) F4 pushed:
  https://huggingface.co/datasets/umeraamir69/hifazat-tab-seed (seed + oracle
  + provenance card) and real model card on `hifazat-tab-sft-v1` (recipe,
  metrics, limits, links). `languages`→`language` YAML fix needed for Hub
  validation. (5) F6: progress-update ticket drafted in
  `Discord_ticket_report_issues.md` (NOT YET POSTED — human pastes).
- **Correction:** validity definition tightened to tool-task episodes with
  gold (Phase-1 convention): GRPO report is 131/134 (97.8%), not 394/400.
  Re-ran to confirm. Also found: committed (compact-unit) seed matches train
  phrasings at 180/400; working regen (spaced `300 ml` from new alias
  pipeline) matches 96/400 — pinned compact seed for AuditKIT; alias/seed
  unification is the peer's area.
- **Evaluator:** all five backlog items closed to the extent possible without
  GPU/human. 23/23 tests green (peer's atta-disambiguation work included).

## 2026-11-06 — F1 AuditKIT run + docs sweep

- **What:** Built `scripts/eval_auditkit.py` (AuditKIT `episodes_from_agenttune`
  → validity / exact task / tool-name / macro-F1 / refusal, gold joined from
  seed by exact prompt). Ran on Hub `hifazat-tab-grpo-v1` (400 episodes, seed
  match 180/400): validity **394/400 (98.50%)** · task **38/180 (21.11%)** ·
  tool-name **132/180 (73.33%)** · macro-F1 **0.2176** · refusal **2/46
  (4.35%)**. Reports: `reports/auditkit_hifazat-tab-grpo-v1.json/.md`;
  trajectories copy gitignored (~4 MB). Project `.venv` now holds auditkit +
  huggingface_hub (`.gitignore` updated for `.venv/` + trajectories copies).
  Docs swept: Features F1 done, Results (new AuditKIT section), Status,
  Website (part-done), ARCHITECTURE (report flow + in-flight note).
- **Why:** User: finish the still-open items where possible (F1), document
  all things.
- **Cause:** F1 needed no GPU — only the Hub artifact + pip. F2/F3 need GPU;
  F4 needs a push decision; F6 needs a human (see Features).
- **Important (not my work):** mid-session the tree gained uncommitted
  edits from another hand — `src/tools.py` (+`list_category`,
  `list_low_stock`, `find_by_stock`, `CATEGORY_ALIASES`) and `data/shop.csv`
  stock lowers (cooking_oil_5L 15→1, olive/canola/baby-diaper/extension-board
  similar). Now `test_mixed_case_key_resolves` fails (1 ≠ 15) and generated
  catalogs carry stock 1. I touched neither file nor the failing assertion;
  eval/redteam stay green (shared TABLE). Owner of those edits: update the
  test expectation or the data, then re-run.
- **Evaluator:** F1 numbers corroborate two other harnesses (validity≈98%,
  task≈11–21%, refusal≈open) — meaningful third route. Docs complete and
  honest about ownership of the red test.

## 2026-11-06 — Built backlog items F7–F16 (rule agent, site, phone)

- **What:** Implemented 10 backlog features, all verified in-session.
  Seed: `ok_N` → `spot_*` ids + `lang` (F14); loan incomes 5 → 8 incl. tier
  edges, rows 15 → 24 (F13); regen → 1500 rows, 219/219 coverage.
  Agent: roman refusal/intent words + `doodh`/`sabun` aliases, mirrored in
  page JS; new `has_word` boundary matching fixed a real `dam`-in-`cardamom`
  bug the bigger seed exposed (3 stock misses → 0) (F12).
  Red-team 3 → 8 families, 9 → 24 attacks, mirrored on the page (F16).
  Site: `web/metrics.json` + `loadMetrics()` (F8), `tool:item` answer chip
  (F9), SFT-adapter + WhatsApp artifact links (F10); callout + Stop-button
  mic already present (F7/F11 confirmed). Phone: `TWILIO_AUTH_TOKEN`
  signature gate, 403 on bad/missing (F15).
- **Scores (all observed):** 16/16 unit tests · eval 1476/1476 task, 24/24
  refusal, 0 over-refusal, 8/8 consistency · redteam 24/24 (Python) and 24/24
  (page JS via node harness) · webhook gate probed 403/403/200/200, open
  without token.
- **Why:** User asked to build what we can from the backlog (no-GPU items).
- **Cause:** Bigger seed + roman mic traffic exposed real matching gaps;
  Demo Day needs the site/phone story closed.
- **Better:** Next: AuditKIT (F1), SFT quant re-eval (F2), SFT brand-trap
  re-train (F3), HF dataset + card (F4) — all need GPU/human/credits.
- **Evaluator:** Meaningful. Docs synced: Features checkboxes, Status,
  Results (new hardening section), Website, Submission links unchanged.

## 2026-11-06 — Code docs + feature backlog; numbers verified

- **What:** New `ARCHITECTURE.md` (stack, flows, deploy) + `API_ENDPOINTS.md`
  (phone webhooks, `/api/stt`) at repo root, generated from actual code.
  New `vault/Lexsi Hackathon 2026/Features.md`: where-we-stand + 19
  prioritized features (F1–F19) + not-doing list. Filled `Submission.md`
  metrics/links (was TBD), marked Website AFTER-bars done, linked backlog
  from `Status.md`.
- **Verified this session:** 12/12 unit tests OK; 219 SKUs (+2 loan-config
  rows) in `shop.csv`; seed 1491 rows, langs 495/495/495, tools
  760 price / 691 stock / **16 loan**; 6 legacy `ok_N` rows lack `lang`.
- **Why:** User asked where we stand, more features, document everything.
- **Evaluator:** Meaningful. Gaps found while documenting: loan seed thin
  (F13), `ok_N` hygiene (F14), no Twilio signature check / STT rate limit
  (F15), SFT quant re-eval still open (F2), AuditKIT still open (F1).

## 2026-11-05 — AFTER SFT wins Track C metrics
- **What:** Canceled stalled GRPO v2-350. AFTER eval on `hifazat-tab-sft-v1`:
  validity 801/801 · task 784/801 (97.9%) · refusal 21/24 (87.5%).
  Updated Findings/Results/Status/Website bars + Discord ticket; redeployed site.
- **Why:** Gold-JSON SFT taught canonical args; GRPO probes never moved past ~21%.
- **Evaluator:** Targets met. Ship SFT adapter for submission.
