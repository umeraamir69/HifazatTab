# Discord `#report-issues` — idea validation ticket

Paste into Lexsi Discord → **#report-issues**. Keep identity **umeraamir69**.

> **Update (2026-11-06, NOT YET POSTED — human to paste):** the new
> "Progress update" ticket below supersedes the original idea-check above.
> Post the new one; leave the old for history.

---

## Progress update (post this, 2026-11-06)

```
[Track C / umeraamir69] HifazatTab update: SFT AFTER wins, AuditKIT + dataset live

Hi team — progress since the idea check:

AFTER (SFT, ships): validity 801/801 (100%) · task 784/801 (97.9%) ·
refusal 21/24 (87.5%) on Tiny Aya fire + LoRA
(https://huggingface.co/umeraamir69/hifazat-tab-sft-v1).
Measured under 4-bit nf4 base — absolute quant numbers meet targets.

AuditKIT proof: episodes_from_agenttune on GRPO v1 trajectories (400 eps):
validity 131/134 (97.8%) · task 38/180 (21.1%) · tool-name 132/180 (73.3%) ·
macro-F1 0.2176 · refusal 2/46. Report: repo reports/auditkit_hifazat-tab-grpo-v1.md.
GRPO confirmed flat (canonical-arg mismatch) — honest negative result, SFT won.

New: versioned seed dataset (1506 rows, 219 SKUs, provenance card):
https://huggingface.co/datasets/umeraamir69/hifazat-tab-seed
Real model card on the SFT adapter (recipe, metrics, limits).
Rule agent hardened: 1476/1476 task · 30/30 refusal (incl. new brand+price
combo probes) · red-team 24/24 · demo https://hifazattab.vercel.app

Still open on our side: SFT-side AuditKIT episode report (needs one GPU
AFTER re-run — script saves full records now), brand-trap SFT retrain
(3 misses), AuditKIT F1 chart for the writeup.

Questions: (1) Is the AuditKIT trajectories report above the right Track C
evidence shape, or do you want a specific notebook/metric set? (2) OK that
the live demo stays rule-agent while the adapter carries metrics?
```

---

## Ticket title

```
[Track C] Idea check — HifazatTab: Tiny Aya shop agent (Urdu/Hindi/English) via AgentTune→AuditKIT
```

## Ticket body (copy below)

```
Hi Lexsi team — validating our Track C idea before we lock submission direction.

**Team / HF:** umeraamir69
**Track:** C — Agentic Fine-tuning (AgentTune → AuditKIT)
**Project:** HifazatTab (حفاظت = protection)

**Idea (1 paragraph)**
Post-train Cohere Tiny Aya (`tiny-aya-fire`) so a Pakistani kiryana-shop agent makes reliable tool calls over a closed CSV (price / stock / loan-eligibility) in Urdu, Hindi, and English. Tiny Aya has no native tools template → we use AgentTune `tools_fallback_prompt` + GRPO with verifiable rewards, then AuditKIT `episodes_from_agenttune` for before/after (tool-call validity, F1, task success). Bonus: script-switch jailbreaks (Urdu↔Hindi) repaired in weights and re-checked after 4-bit quant. Live demo: browser voice + WhatsApp/Twilio using the same tool contract.

**Why this fits Track C**
- Mandatory chain: AgentTune train → AuditKIT on trajectories
- Constrained tools + exact-match rewards (not open-ended chat)
- Safety is in-scope: refusal probes + cross-script attacks, not just task accuracy

**Where we are (facts)**
- BEFORE (zero-shot Tiny Aya): 150/153 · 17/153 · 3/21
- GRPO v1 AFTER flat (canonical-arg mismatch). GRPO v2 mid-train stalled → canceled.
- **AFTER SFT (ship):** validity **801/801 (100%)**, task **784/801 (97.9%)**, refusal **21/24 (87.5%)** on 108-SKU seed
- Adapter: https://huggingface.co/umeraamir69/hifazat-tab-sft-v1
- Live demo (rule agent + Groq Urdu STT): https://hifazattab.vercel.app
- Repo: https://github.com/umeraamir69/HifazatTab

**Questions for mentors (please flag if off-track)**
1. Is a closed-world shop CSV + 3 tools (lookup_price, check_stock, loan_eligibility) a valid Track C problem scope, or too narrow / too “product demo”?
2. Is `beta=0` GRPO (skip KL / ref model) acceptable for Tiny Aya’s huge vocab on 24GB, as long as rewards + AuditKIT before/after are honest?
3. For AFTER metrics: is re-running our Phase 1 regex eval + AuditKIT on AgentTune `trajectories.jsonl` enough, or do you require a specific AuditKIT notebook/metric set?
4. Voice/WhatsApp demo is rule-agent for latency; tuned adapter is for Track C metrics — OK to keep that split, or should the live demo load the LoRA?
5. Any must-fix in the Nov 14 submission we might be missing (HF article format, team size, chaining ≥2 Lexsi repos)?

Happy to adjust scope if this isn’t what judges want. Thanks!
```

---

## Shorter alt (if channel prefers brief)

```
[Track C / umeraamir69] HifazatTab — Tiny Aya fire + AgentTune GRPO + AuditKIT for trilingual (ur/hi/en) shop tools (price/stock/loan) + script-switch refusal. BEFORE: task ~11%. Smoke GRPO on HF Jobs L4 done; full run on A10G. Repo github.com/umeraamir69/HifazatTab · demo hifazattab.vercel.app

Please confirm: (1) closed CSV+3 tools OK for Track C? (2) beta=0 GRPO OK if AuditKIT before/after solid? (3) live demo can stay rule-agent while adapter is for metrics?
```
