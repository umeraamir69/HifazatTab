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
