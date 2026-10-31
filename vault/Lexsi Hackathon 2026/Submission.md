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

## Metrics (fill after runs)
| Metric | Before | After |
|--------|--------|-------|
| Task success | TBD | TBD |
| tool_call_f1 | TBD | TBD |
| tool_call_validity | TBD | TBD |
| Refusal precision | TBD | TBD |
| Cross-lingual consistency | TBD | TBD |
| Post-quant safety Δ | — | TBD |

## Links (fill at ship)
- GitHub: `https://github.com/umeraamir69/...`
- HF model: `https://huggingface.co/umeraamir69/...`
- HF dataset: `https://huggingface.co/datasets/umeraamir69/...`
- HF article / Space: TBD

## Team
- Lead HF username: **umeraamir69** (must match registration for credits)
