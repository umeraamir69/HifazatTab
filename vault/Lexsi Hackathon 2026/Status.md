# Status — HifazatTab

**Where we are (2026-11-06):** Phase 0 demo green · BEFORE done ·  
**AFTER SFT WINS** — targets met · catalog **219 SKUs** · research draft in `papers/` ·  
code docs at repo root (`ARCHITECTURE.md`, `API_ENDPOINTS.md`) · backlog in `Features.md` (F7–F16 done).  
Rule agent hardened: seed **1500 rows**, eval **1476/1476** task · **24/24** refusal · 0 over-refusal · red-team **24/24** · unit tests **15/16** (1 failure is collateral of in-flight uncommitted shop.csv stock edits — not this session's work, see LOG).  
AuditKIT F1 done: GRPO v1 400 episodes → validity 98.50% · task 21.11% · F1 0.2176 (`reports/`, script `scripts/eval_auditkit.py`).

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
- [x] AuditKIT on GRPO trajectories (report in `reports/`; SFT-episode AFTER side + writeup still open)
- [ ] SFT re-train for brand-trap refusals (3/24 misses; rule-agent half fixed + tested)
- [ ] HF dataset push + model card · `/api/stt` rate limit · 30–50 red-team corpus

## Key dates

- Nov 14 submit · Nov 16 shortlist · Nov 22 Demo Day
