# HifazatTab — Track C Agentic Fine-tuning

Trilingual tool-agent (**Urdu / Hindi / English**) over tabular kiryana-shop data on Cohere [Tiny Aya](https://docs.cohere.com/docs/tiny-aya).  
Built for the [Lexsi AI Safety & Alignment Hackathon](https://hackathon.lexsi.ai/) (Nov 1–21, 2026 · submit Nov 14 · Demo Day Nov 22).

**Public identity:** GitHub + Hugging Face **umeraamir69** only.

## Form pitch

HifazatTab (حفاظت = protection) post-trains Tiny Aya with **AgentTune** so a shop agent makes reliable tool calls over price, stock, and loan fields in Urdu, Hindi, and English. **AuditKIT** scores before/after tool-call F1, validity, and task success from AgentTune `trajectories.jsonl`. Script-switch jailbreaks are repaired in the weights and re-checked after 4-bit quant.

One-liner: *Trilingual Tiny Aya shop agent — AgentTune for tools, AuditKIT for proof, hifazat in the weights.*

## Stack (Track C)

1. **AgentTune** — GRPO (or RLOO) with constrained tools + verifiable rewards  
2. **AuditKIT** — `episodes_from_agenttune` → tool_call_f1 / validity / task completion  
3. Optional support: CuratorKIT (curation), SafeTune (drift repair)

Base model: `CohereLabs/tiny-aya-fire` (South Asia) with `tiny-aya-global` fallback. Tiny Aya has no native tools chat-template; AgentTune injects `tools_fallback_prompt`.

## Status

**Plan complete** (Obsidian vault). Phase 0 stdlib baseline is next — train code waits until baseline + gated model load.

Docs (what / why / cause / result / better):
- Vault: `Documents/Obsidian Vault/Lexsi Hackathon 2026/` → start at `00 Home.md` / `Plan.md`
- Repo everything-log: [`LOG.md`](./LOG.md)

## Layout (current)

```
data/shop.csv           # oracle prices / stock / loan limits (PKR)
data/seed_tasks.jsonl   # tool tasks + safety probes (en/hi/ur)
LOG.md                  # running what/why/cause/result/evaluator log
requirements.txt        # stdlib now; Lexsi stack opt-in for Colab
```

Phase 0 will add `src/`, `demo.py`. Phase 2+ adds AgentTune train scripts + AuditKIT reports.

## Roadmap (short)

1. Phase 0 — stdlib tools/agent/eval/redteam + scores  
2. Phase 1 — baseline Tiny Aya (no train)  
3. Phase 2 — AgentTune GRPO  
4. Phase 3 — AuditKIT before/after (≥2 metrics)  
5. Phase 4 — script-switch red-team + repair + quant survival  
6. Phase 5 — HF push as umeraamir69 + submit  

Full plan: vault `Plan.md`.
