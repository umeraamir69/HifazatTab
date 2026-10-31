# HifazatTab — Complete Step-by-Step Guide

Beginner-friendly. Follow top to bottom. Tick boxes as you go.

---

## Step 0 — Accounts and keys (30 min, do first)

- [ ] Register for the hackathon: https://hackathon.lexsi.ai/
- [ ] Join the hackathon Discord (this unlocks $20 Hugging Face credits).
- [ ] Create a Hugging Face account. Create a write token. Save it in your
      password manager — never paste tokens into vault notes or git.
- [ ] Accept the gated-model licence for `CohereLabs/tiny-aya-fire`
      (fallback: `tiny-aya-global`). Run `hf auth login` in Colab later.
- [ ] Get a Cohere API key (free tier) for quick tests: dashboard → API keys.
- [ ] Attend the Oct 31 kickoff. Write down: exact model IDs, any Lexsi API
      changes, sample problem statements. Update `Plan.md` if anything shifted.

Why: no keys = no training, no hosting. Do this before any code.

---

## Step 1 — Laptop setup (10 min)

```bash
cd /Users/umeraamir/Documents/Lexsi
python3 --version        # any 3.10+ is fine
git config user.name     # must print: umeraamir69 (local repo config)
```

Phase 0 needs only stdlib Python. Heavy packages (torch, trl, peft) install
later on Colab, never on this laptop.

---

## Step 2 — Phase 0 baseline on laptop (the `go` build)

Say `go` and I build these files:

| File | What it does |
|------|--------------|
| `src/tools.py` | The 3 calculator buttons: price, stock, loan check over `shop.csv` |
| `src/agent.py` | Rule-based stand-in: picks a tool, answers in en/hi/ur, refuses tricks |
| `src/eval.py` | Scores task success + refusal precision + cross-lingual consistency |
| `src/redteam.py` | Script-switch jailbreaks: same attack in Urdu vs Hindi vs English |
| `demo.py` | 2-minute demo: success case + refusal case + one live jailbreak |

Run and record:

```bash
python3 demo.py
python3 -m src.eval
python3 -m src.redteam
```

Copy the printed scores into the vault `Status` note and `LOG.md`.
Evaluator rule: mean ≥ 4, no 1s — else fix before continuing.

---

## Step 3 — Data scale-up (Colab, free GPU)

1. Open Colab, GPU runtime (T4). Install: `torch transformers datasets trl peft
   bitsandbytes agenttune auditkit huggingface_hub`.
2. Expand `seed_tasks.jsonl`: 80–120 tool scenarios + 60 safety probes.
   Rule: one task, three renderings (translate, never invent new tasks).
3. Run the AgentTune loop: strong model proposes trajectories → executor runs
   tools → verifier keeps only exact tool-output matches.
4. CuratorKIT pass: dedupe, drop PII, drop advice without disclaimer.
5. Target: 800–1500 clean SFT samples + 400 DPO refusal pairs.
6. Push versioned dataset to Hugging Face under `umeraamir69`.

---

## Step 4 — Tune v1 with LoRA (Colab)

1. SFT with LoRA on `tiny-aya-fire` (cheap add-on, not full retrain).
2. DPO pass on the 400 refusal pairs.
3. Evaluate held-out 100 tasks + 100 probes. Targets: task success ≥ 75%,
   refusal precision ≥ 0.80, consistency ≥ 0.85.
4. Push adapter + eval report to Hugging Face.

---

## Step 5 — Agentic RFT with GRPO (50–150 steps)

Reward: tool output match +1.0, valid schema +0.2, safety fail −1.0.
Short traces, JSON tool calls only. Expect +5–10 pts over SFT.

---

## Step 6 — Break it, repair it, shrink it

1. Red-team v1 with 30–50 script-switch attacks. Log every failure:
   attack text, language, script, model trace.
2. Repair: failures become new training examples (SafeTune or DPO pass).
3. Re-eval. Then quantize to 4-bit and re-eval again.
4. Pass bar: safety drop after quant < 5 pts. This is your demo climax.

---

## Step 7 — Ship (before Nov 14)

- [ ] Public GitHub repo, every commit as `umeraamir69`, no bot identities.
- [ ] HF adapter + model card, dataset + provenance note, AuditKIT report.
- [ ] Failure log (red-team cases with traces).
- [ ] 3-min demo: base fails → tuned succeeds + refuses → still safe after quant.
- [ ] Submission form text from the vault `Submission` note.

---

## If something breaks

| Symptom | Fix |
|---------|-----|
| Gated model 401/403 | Accept licence on the model page, `hf auth login` again |
| Tiny Aya ignores tools | Use AgentTune fallback prompt (schemas in system prompt) |
| Lexsi import error after kickoff | Fall back to TRL trainer, keep AuditKIT-readable JSONL |
| Out of GPU memory | Smaller batch, LoRA rank 8, 4-bit base load |
| Urdu scores weird | Expected — 30-sample human check, report separately |

## Schedule

Now → Oct 31: Steps 0–2. Nov 1–7: Steps 3–4. Nov 8–12: Steps 5–6.
Nov 13–14: Step 7. Nov 16–21: only if shortlisted. Nov 22: Demo Day.
