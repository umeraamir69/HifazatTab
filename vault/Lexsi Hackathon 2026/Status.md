# Status — HifazatTab

**Where we are (2026-11-05):** Phase 0 demo green · BEFORE done ·  
**AFTER SFT WINS** — targets met · GRPO v2 canceled (stalled) · site updated.

## Metrics snapshot

| | BEFORE | AFTER GRPO v1 | AFTER **SFT** |
|--|-------:|--------------:|--------------:|
| tool_call_validity | 150/153 (98%) | 146/153 | **801/801 (100%)** |
| task_success | 17/153 (11%) | 16/153 | **784/801 (97.9%)** |
| refusal_precision | 3/21 (14%) | 4/21 | **21/24 (87.5%)** |

Targets ≥85% / ≥75% / ≥80% — **met on SFT**.

## Ship

| Artifact | Link |
|----------|------|
| Demo | https://hifazattab.vercel.app |
| AFTER adapter | https://huggingface.co/umeraamir69/hifazat-tab-sft-v1 |
| Repo | https://github.com/umeraamir69/HifazatTab |
| Findings | `Findings.md` |

## Still open (Demo Day polish)

- [ ] Discord `#report-issues` (update ticket with SFT AFTER numbers)
- [ ] Voice E2E human walk (`phone/VOICE_E2E.md`)
- [ ] AuditKIT on trajectories / SFT writeup
- [ ] Optional: fix brand-trap refusals (3/24 misses)

## Key dates

- Nov 14 submit · Nov 16 shortlist · Nov 22 Demo Day
