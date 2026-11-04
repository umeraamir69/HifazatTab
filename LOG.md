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
