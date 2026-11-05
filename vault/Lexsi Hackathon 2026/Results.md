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

## Phase 2 — GRPO v1 flat; SFT AFTER wins (Nov 5) — see Findings.md

- **GRPO v1** (50 A10G → `hifazat-tab-grpo-v1`): AFTER flat 146/153 · 16/153 · 4/21
  (NL args vs canonical keys; weak +0.2 reward).
- **GRPO v2-350** (strict reward + mid-train probes): probes stuck ~21% task from
  step 50 → **canceled**; best would have been step 50.
- **SFT v1** (gold JSON, 3 epochs → `hifazat-tab-sft-v1`): **AFTER win**

| Metric | BEFORE | AFTER SFT |
|--------|-------:|----------:|
| tool_call_validity | 150/153 (98%) | **801/801 (100%)** |
| task_success | 17/153 (11%) | **784/801 (97.9%)** |
| refusal_precision | 3/21 (14%) | **21/24 (87.5%)** |

- **Ship:** https://huggingface.co/umeraamir69/hifazat-tab-sft-v1 (+ `after_eval.json`)
- Targets ≥85% / ≥75% / ≥80% — **met**. Misses: 3 brand-trap probes.

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

9. **Colab Drive copy was stale (Nov 2 night).** Live run loaded the model
   (GPU ~13/15 GB) and hit tools_fallback (good), but the Drive cell used
   `num_steps` + **no `max_steps_per_turn`** (defaults to 20 → freeze) and
   LoRA without `target_modules`. Repo notebook fixed to match AgentTune
   Tiny Aya docs: chat-message prompts, `max_steps=50`, `max_steps_per_turn=2`,
   `peft_config=dict(...)`, CUDA assert, `logging_steps=1`.
   **Interrupt the stuck Drive run and re-open from GitHub.**
10. **OOM #2: policy loss pass (Nov 3).** Same 262 MB at `lm_head`, this time
    in `_compute_loss` — fp32 full-vocab logits over the 256k Cohere vocab.
    Fix: LoRA targets cut to `["q_proj", "v_proj"]`, rank 16 → 8 (drops the
    ~1B-param lm_head adapter and its optimizer states).
11. **Fallback ready:** `colab/phase2_sft.ipynb` — plain LoRA SFT on the same
    174 rows, no rollouts, no ref model. If slim GRPO still OOMs, run SFT for
    the AFTER number and return to GRPO only with bigger GPU.
12. **CUDA device-side assert (Nov 2 ~22:49).** Warning: `input_ids` on CUDA,
    model on **CPU**, then `AcceleratorError: device-side assert`. Cause: GPU
    already full (~0.09 GB free) so policy offloaded to CPU. Fix in train cell:
    free-GB assert (>8), empty_cache, assert model device is cuda, shorter
    completions. **Must Runtime → Restart session** after this error (CUDA stays
    poisoned until restart).
13. **$20 credits claimed (Nov 3–4).** Spend path locked: Hugging Face **Jobs**
    `l4x1` via `scripts/train_grpo_hf_jobs.py` (see `scripts/HF_JOBS.md`). Smoke
    (`--smoke`, 3 steps) then full (`--max-steps 50`). Do **not** retry GRPO on
    free T4. SFT notebook remains free-tier backup only.
14. **Smoke GRPO SUCCESS (Nov 4).** Job `6aeb6f2b0e0338d1bb80117d` on `l4x1`
    COMPLETED in ~623s running (~$0.14). GPU NVIDIA L4, 23.46 GB free pre-train.
    Pushed `umeraamir69/hifazat-tab-grpo-v1-smoke` (adapter ~7.7 MB + trajectories).
15. **Full GRPO 50 A10G COMPLETED (Nov 4).** Job `6aeb7526c78863f9c632d1f4`
    (~$2.2) → `umeraamir69/hifazat-tab-grpo-v1`. AFTER eval **flat** vs BEFORE
    (Findings.md). Do not spend more credits on v1 reward.
16. **Catalog + demo (Nov 4).** 108 SKUs, alias catalog, seed 825 rows (local),
    site features, Groq Whisper Urdu STT (`GROQ_API_KEY` on Vercel). Rule-agent
    demo remains the live voice path.

## Phase 3+ (planned)

- AuditKIT `episodes_from_agenttune` on `trajectories.jsonl` → ≥2 metrics.
- Red-team 30–50 script-switch attacks → SafeTune/DPO repair → 4-bit quant,
  safety drop must stay < 5 pts.
- Ship: adapter + dataset + report + failure log + 3-min demo.
