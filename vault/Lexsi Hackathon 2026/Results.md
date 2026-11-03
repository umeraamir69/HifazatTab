# Results — what we did in each phase (living doc)

## Phase 0 — laptop stand-in (done Oct 31)

- **What:** rule-based agent over `shop.csv`: 3 tools, trilingual answers,
  refusal-first safety. `src/`, `demo.py`, `src/eval.py` with independent
  oracle, `src/redteam.py` script-switch attacks, 5 unit tests.
- **Why:** a "before" number + live demo before the gated model downloads.
- **Scores:** task 13/13 (later 153/153 on 174 rows), refusal 5/5 → 21/21,
  over-refusal 0, consistency 4/4 → 5/5, redteam 9/9 blocked, tests 5/5 → 7/7.
- **Bugs the evaluator caught:** lowercased table key, price/stock priority,
  missing Devanagari keywords, order-dependent refusal patterns, substring
  alias collision (`price`→rice). All fixed, all locked by tests.

## Phase 1 — Tiny Aya zero-shot baseline (done Oct 31, Colab T4)

- **What:** `colab/phase1_baseline.ipynb` — `tiny-aya-fire`, 4-bit, greedy,
  fallback tool prompt, same 174 seed tasks. Full pack in `colab result/`.
- **Scores (the BEFORE photo):**

| Metric | Score |
|--------|-------|
| tool_call_validity | 150/153 (98%) |
| task_success | 17/153 (11%) |
| refusal_precision | 3/21 (14%) |

- **Reading:** format learned, content wrong, safety open. The model invents
  tools to obey attacks (`write_document`, `customer database`,
  `price_checker`, `system_prompt`) and answers the same attack differently
  per script — the script-switch thesis, live in the log.
- **Cause of low task_success:** free-form args vs canonical keys, wrong tool
  choice, hallucinated tools.

## Phase 2 — AgentTune GRPO (in progress)

- **What:** `colab/phase2_grpo.ipynb` — LoRA GRPO, 100 steps, 3 constrained
  tools, rewards: exact tool+arg +1.0, valid-schema-but-wrong +0.2,
  invented tool −0.5, answered-must-refuse −1.0.
- **Why this fixes Phase 1:** constrained schema makes invented tools
  impossible; verifiable reward teaches canonical args; refusal pairs teach
  the 18 obeyed probes.
- **Targets:** validity ≥ 0.85, task ≥ 75%, refusal ≥ 0.80.
- **After training:** re-run Phase 1 notebook on the adapter → AFTER number →
  AuditKIT before/after report on Hugging Face.

### Phase 2 debug log (everything that broke, in order)

1. **Wrong data (116k TL;DR rows).** First run trained on AgentTune's default
   dataset — spotted from the parquet download (116,722 rows), not our 174.
   Fix: build `train_dataset` from `seed_tasks.jsonl` (prompt + want_tool +
   want_arg + must_refuse), pass it explicitly.
2. **Reward signature crash.** Ours was `(reply, want_tool, want_arg)`; TRL
   calls `f(prompts, completions, **kwargs)`. Fail-loud TypeError, zero GPU
   burned. Fix: rewrote both rewards, handling str + message-list completions,
   expected answers read from dataset columns.
3. **String tools rejected.** AgentTune wants callables, not names. Fix: real
   `lookup_price / check_stock / loan_eligibility` functions over shop.csv.
4. **T4 OOM (14.5 GB).** Fix: batch 1 × accum 8, 2 generations, short rollouts
   (256/64, max 3 steps), gradient checkpointing, paged_adamw_8bit,
   `expandable_segments`, single GPU pin.
5. **Freeze at step 2/3 (10+ min, Colab AND Kaggle).** Suspects: telemetry
   prompt blocking (`report_to="none"` added) + 2-GPU generate deadlock
   (`CUDA_VISIBLE_DEVICES=0`).
6. **Kaggle sessions with no CUDA.** Toggle on, drivers absent
   (`torch.cuda.is_available() == False`). Account verified, quota fine —
   backend flakiness. Proof via `nvidia-smi`; fresh session fixed it.
   Lesson: always print CUDA status before training, never trust the toggle.
7. **Ref-model OOM (the true killer).** Traceback pointed at
   `ref_per_token_logps`: GRPO's KL pass materializes full-vocab logits and
   Cohere's vocab is ~256k tokens. Fix: `beta=0.0` removes the pass entirely.
   Acceptable for 100 steps; rewards still teach.
8. **Status (corrected Nov 2):** **NOT running successfully on Kaggle.**
   Docs previously said “in progress on Kaggle 2×T4” — that was aspirational /
   stuck, not a green train. Known Kaggle blockers from this log: no-CUDA
   sessions (#6), freeze at step 2/3 (#5), plus the same OOM/ref-model issues
   (#4, #7) that hit Colab. **Do not wait on Kaggle.** Run Phase 2 on
   **Colab free T4** with the fixed notebook (`beta=0`, batch1, one GPU,
   our 174-row seed, Secrets-only `HF_TOKEN`). Rotate any HF token that was
   pasted into a cell during earlier debugging.

## Phase 3+ (planned)

- AuditKIT `episodes_from_agenttune` on `trajectories.jsonl` → ≥2 metrics.
- Red-team 30–50 script-switch attacks → SafeTune/DPO repair → 4-bit quant,
  safety drop must stay < 5 pts.
- Ship: adapter + dataset + report + failure log + 3-min demo.
