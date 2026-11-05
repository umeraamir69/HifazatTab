# Status — HifazatTab

**Where we are (2026-11-04):** Phase 0 demo green · Phase 1 BEFORE done ·  
Phase 2 GRPO **trained** but AFTER **flat** · demo site + Groq Urdu STT live.  
**Read:** `Findings.md` for why metrics failed and what to do next.

## Metrics snapshot

| | BEFORE (zero-shot) | AFTER v1 GRPO |
|--|-------------------:|--------------:|
| tool_call_validity | 150/153 | 146/153 |
| task_success | 17/153 | **16/153** |
| refusal_precision | 3/21 | **4/21** |

Targets: validity ≥ 0.85 · task ≥ 75% · refusal ≥ 0.80 — **not met on v1**.

## Done

- Plan + Research + vault docs; Phase 0 stdlib agent/tools/eval/redteam/tests.
- Phase 1 Colab BEFORE on Tiny Aya fire (4-bit).
- HF Jobs: smoke L4 + full 50 A10G → `hifazat-tab-grpo-v1`.
- AFTER notebook run → flat scores diagnosed (canonical arg / weak reward).
- Shop expanded to **108 SKUs**; seed builder covers all; web catalog + filters.
- Live demo https://hifazattab.vercel.app (SSO off); Hindi/Urdu spoken answers.
- Urdu mic via **Groq Whisper** (`/api/stt`) — no OpenAI/Google needed.
- v2 train recipe coded (strict reward + canonical prompt) — **not launched yet**.

## Still open

- [ ] Push local catalog/seed/train/AFTER patches to GitHub `main`
- [ ] Launch GRPO **v2** (`hifazat-tab-grpo-v2`, prefer 100 steps) on remaining credits
- [ ] Re-run AFTER; paste new scores into Results + Findings
- [ ] Optional SFT warm-start if v2 still weak on exact args
- [ ] AuditKIT on trajectories; Discord `#report-issues` ticket
- [ ] Voice E2E human walk (`phone/VOICE_E2E.md`) before Demo Day

## Live artifacts

| What | Link |
|------|------|
| Demo | https://hifazattab.vercel.app |
| Repo | https://github.com/umeraamir69/HifazatTab |
| Adapter v1 | https://huggingface.co/umeraamir69/hifazat-tab-grpo-v1 |
| Smoke | https://huggingface.co/umeraamir69/hifazat-tab-grpo-v1-smoke |
| Findings | `Findings.md` (this folder) |
| Website docs | `Website.md` (features done + todo) |

## Credits

~$2.3 spent on GRPO so far of $20. Reserve rest for **v2**, not another v1.

## Key dates

- Nov 5 registration closes · Nov 14 submit · Nov 16 shortlist · Nov 22 Demo Day
