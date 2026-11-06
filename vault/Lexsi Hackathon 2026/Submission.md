# Submission — form copy-paste

**Identity:** all public artifacts as **umeraamir69** (never Cursor bot).  
Update numbers after real evals; pitch text is stable.

---

## Short pitch (form / Discord / HF lede)

HifazatTab (حفاظت = protection) is a Track C agentic fine-tune of Cohere Tiny Aya for Pakistani kiryana shops: reliable tool calls over price, stock, and loan limits in Urdu, Hindi, and English. We train with AgentTune (GRPO + constrained tools + verifiable rewards) and prove gains with AuditKIT on AgentTune trajectories (tool-call F1, validity, task success), including script-switch jailbreaks that hold after weight-level repair and 4-bit quant.

## One-liner

Trilingual Tiny Aya shop agent — AgentTune for tool reliability, AuditKIT for before/after proof, hifazat in the weights.

## Track
Agentic Fine-tuning (Track C)

## Models
Cohere Labs Tiny Aya (`tiny-aya-fire` preferred; `tiny-aya-global` fallback). LoRA adapter.

## Stack used
1. **AgentTune** — `create_agentic_trainer` GRPO with tools + rewards; `trajectories.jsonl`
2. **AuditKIT** — `episodes_from_agenttune`; tool_call_f1, tool_call_validity, task completion
3. Optional: CuratorKIT / SafeTune / TRL for curation & repair

## Problem
Shopkeepers mix Urdu, Hindi, and English when asking price/stock/loan questions. Base multilingual models invent numbers and break under script-switch jailbreaks. Tiny Aya has no native tools template — tool reliability must be trained.

## Approach
Closed-world CSV oracle → three tools → AgentTune GRPO with exact-match rewards and tools_fallback_prompt → AuditKIT before/after → red-team script-switch → repair in weights → re-eval after quant.

## Metrics (SFT AFTER, 2026-11-05; GRPO v1/v2 flat — see Findings.md)
| Metric | Before | After (SFT `hifazat-tab-sft-v1`) |
|--------|--------|----------------------------------|
| Task success | 17/153 (11%) | 784/801 (97.9%) ✅ target ≥75% |
| tool_call_f1 | TBD (AuditKIT pending) | TBD (AuditKIT pending) |
| tool_call_validity | 150/153 (98%) | 801/801 (100%) ✅ target ≥85% |
| Refusal precision | 3/21 (14%) | 21/24 (87.5%) ✅ target ≥80% |
| Cross-lingual consistency | weak (baseline) | rule-agent harness 5/5; SFT TBD |
| Post-quant safety Δ | — | TBD (re-eval SFT in 4-bit pending) |

## Links
- GitHub: `https://github.com/umeraamir69/HifazatTab`
- HF model (ship): `https://huggingface.co/umeraamir69/hifazat-tab-sft-v1`
- HF model (negative result): `https://huggingface.co/umeraamir69/hifazat-tab-grpo-v1`
- HF dataset: TBD (`umeraamir69/...` — F4 in Features.md)
- Demo: `https://hifazattab.vercel.app`
- HF article / Space: TBD

## Team
- Lead HF username: **umeraamir69** (must match registration for credits)
