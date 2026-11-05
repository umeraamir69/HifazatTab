# Discord `#report-issues` — idea validation ticket

Paste into Lexsi Discord → **#report-issues**. Keep identity **umeraamir69**.

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
- Phase 1 BEFORE (zero-shot Tiny Aya, Colab): validity ~98%, task success ~11%, refusal ~14%
- Phase 2: AgentTune GRPO on HF Jobs (L4 smoke ✅; full 50-step A10G in progress) → adapter `umeraamir69/hifazat-tab-grpo-v1(-smoke)`
- Repo: https://github.com/umeraamir69/HifazatTab
- Live voice demo: https://hifazattab.vercel.app

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
