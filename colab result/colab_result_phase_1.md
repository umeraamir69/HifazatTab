# Colab Result — Phase 1 (zero-shot Tiny Aya)

**Status:** SUCCESS (run completed on T4 GPU)  
**Captured:** 2026-10-31T15:07:45.855952+00:00  
**Notebook:** [phase1_baseline Colab](https://colab.research.google.com/drive/1OtKcZI4mT1WIXiJuZabouk-nEOnHOU3L)  
**Model:** `CohereLabs/tiny-aya-fire`

## Headline metrics (BEFORE number)

| Metric | Score | % |
|--------|------:|--:|
| tool_call_validity | 150/153 | 98.04% |
| task_success | 17/153 | 11.11% |
| refusal_precision | 3/21 | 14.29% |

```
--- BASELINE (zero-shot Tiny Aya) ---
tool_call_validity: 150/153
task_success: 17/153
refusal_precision: 3/21
MODEL: CohereLabs/tiny-aya-fire
```

## Evaluator read

- **Meaningful?** Yes — weak-but-honest baseline. Validity is high (tool-shaped lines) but **task success ~11%** means args/tool choice rarely match the oracle. **Refusal ~14%** means repair/red-team will matter.
- **Cause of low task_success:** free-form args vs canonical keys; wrong tool; hallucinated tools (`price_checker`, `write_document`, `system_prompt`).
- **Next:** Phase 2 AgentTune GRPO with constrained schemas + verifiable reward.

## Files

- `colab_result_phase_1_full_log.txt` — full stdout
- `colab_result_phase_1.json` — machine-readable summary
- `colab_result_phase_1.md` — this note
