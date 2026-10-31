# Runbook — commands we ran

Append-only. Each entry: **when**, **what**, **why**, **cause**, **command**, **result**, **better next**.

---

## 2026-10-30 — Research fetch (no code)

- **What:** Fetched hackathon.lexsi.ai, lexsi.ai, Tiny Aya docs, AgentTune / AuditKIT notes.
- **Why:** Lock Track C pitch + stack before coding.
- **Cause:** User required plan-before-code + document everything.
- **Result:** Track C = AgentTune → AuditKIT; Tiny Aya needs tools_fallback_prompt; fire = South Asia.
- **Better:** After Oct 31 kickoff, re-fetch sample problem statements and pin HF model IDs.

## 2026-10-30 — Vault plan suite written

- **What:** Wrote/updated Research, Plan, Architecture, Decisions, Data, Redteam, Runbook, Status, Submission, session log, Home.
- **Why:** Obsidian is the thinking log; LOG.md mirrors in repo.
- **Cause:** Home already linked missing notes — fill them before Phase 0 code.
- **Result:** Plan evaluator run recorded in session + LOG.
- **Better:** Keep Runbook and LOG in sync on every shell action.

## Pending (not run yet — plan gate)

```bash
# Phase 0 — after plan pass
cd /Users/umeraamir/Documents/Lexsi
python3 demo.py
python3 -m src.eval
python3 -m src.redteam

# Phase 2 sketch (Colab) — DO NOT run until Phase 1 baseline exists
# pip install agenttune auditkit transformers peft datasets
# hf auth login
# python train/grpo_hifazattab.py
```
