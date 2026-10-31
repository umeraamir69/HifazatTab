# Architecture — HifazatTab

**What:** How pieces connect.  
**Why:** Judges + future-us need one diagram, not scattered scripts.  
**Cause:** Track C is a *pipeline*, not a single notebook cell.

---

## Loop (Track C)

```mermaid
flowchart LR
  Q["User Q\n(en / hi / ur)"] --> A["Tiny Aya\n+ tools_fallback_prompt"]
  A -->|"JSON tool call"| T["Tools\nlookup_price\ncheck_stock\nloan_eligibility"]
  T --> CSV[(shop.csv)]
  T -->|"tool result as user turn"| A
  A --> ANS[Final answer]
  A -.->|rollouts| TR[trajectories.jsonl]
  TR --> AK[AuditKIT agent_eval]
  AK --> M["Metrics\nF1 · validity · task · refusal"]
```

## Train path

```mermaid
flowchart TB
  SEED[seed_tasks.jsonl] --> TRAIN[AgentTune create_agentic_trainer GRPO]
  TOOLS[3 Python tools] --> TRAIN
  REW[reward_funcs] --> TRAIN
  TRAIN --> AD[LoRA adapter]
  TRAIN --> TJ[trajectories.jsonl]
  TRAIN --> PROV[lexsi_provenance.json]
  TJ --> AK[AuditKIT episodes_from_agenttune]
  AD --> HF[HF Hub umeraamir69]
  TJ --> HF
  AK --> HF
```

## Repo file map (target — after Phase 0 code)

```
Documents/Lexsi/
  README.md          # pitch + quick start
  LOG.md             # everything log (what/why/result/better)
  requirements.txt
  data/
    shop.csv
    seed_tasks.jsonl
  src/               # Phase 0+
    tools.py
    agent.py
    eval.py
    redteam.py
  demo.py
  train/             # Phase 2+ — AgentTune scripts
  eval/              # AuditKIT runners
  reports/           # before/after tables
```

Vault stays the thinking log; code stays in Lexsi. No secrets in either.

## Tool contracts (frozen)

| Tool | Args | Returns |
|------|------|---------|
| `lookup_price` | `item: str` | price_pkr, stock, category |
| `check_stock` | `item: str` | stock, low_stock flag |
| `loan_eligibility` | `amount: int`, `tier: str` | eligible bool + limit (never invent KYC) |

Schema is JSON-only. Free-text “advice” without tool = fail for tool tasks.
