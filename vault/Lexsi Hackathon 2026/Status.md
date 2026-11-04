# Status — HifazatTab

**Where we are:** Phase 1 Tiny Aya baseline **DONE** (2026-10-31). Phase 0 still green.

## Done

- Plan + Research + vault docs. Step-by-step guide in repo.
- Phase 0 stdlib: tools/agent/eval/redteam/demo/tests.
  Laptop rule-agent: task 13/13 · refusal 5/5 · redteam 9/9.
- Phase 1 Colab on T4 with `CohereLabs/tiny-aya-fire` (BitsAndBytesConfig 4-bit).
- Results saved under `Documents/Lexsi/colab result/`.

### Phase 1 BEFORE metrics

| Metric | Score |
|--------|------:|
| tool_call_validity | 150/153 (98%) |
| task_success | 17/153 (11%) |
| refusal_precision | 3/21 (14%) |

## Real baseline — Tiny Aya zero-shot (Colab, Oct 31)

Model: `CohereLabs/tiny-aya-fire`, 4-bit, greedy, fallback tool prompt.

| Metric | Score |
|--------|-------|
| tool_call_validity | 150/153 |
| task_success | 17/153 |
| refusal_precision | 3/21 |

Reading: format learned, content wrong, safety open. This is the gap Phase 2
must close. Targets: validity ≥ 0.85, task ≥ 75%, refusal ≥ 0.80.

## Still manual (you)

- [x] Hackathon registration + Discord ($20 HF credits) — done Oct 31
- [x] **$20 HF credits claimed** (Nov 3) — spend on HF Jobs GPU (not Colab T4)
- [ ] Oct 31 kickoff notes → update Plan if IDs/APIs shifted
- [x] Repo live as umeraamir69 (Phase 0, Phase 1 pack, site, phone, docs all pushed)
- [ ] Validate idea with team via Discord ticket (#report-issues) — site recommends it
- [ ] Registration closes Nov 5 (registered ✓) — submit by Nov 14, ONE submission only (last counts)

## Key dates (from tracks page)

- Nov 1–21 hackathon window · Nov 5 registration closes · Nov 14 submit
- Nov 16 shortlist (20 teams) · Nov 22 Demo Day

## Next

1. **HF Jobs smoke** — `scripts/HF_JOBS.md` → `train_grpo_hf_jobs.py --smoke` on `l4x1`
2. **HF Jobs full** — same script `--max-steps 50` → push `hifazat-tab-grpo-v1`
3. **AFTER eval** — `colab/phase1_baseline.ipynb` vs adapter (free T4 OK)
4. Fallback only: `phase2_sft.ipynb` on free Colab (no credits)
5. Phase 3 AuditKIT · Phase 4 red-team / quant
