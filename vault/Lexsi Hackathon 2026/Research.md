# Research — Lexsi.ai + Tiny Aya + Track C

**What:** Facts that drive HifazatTab.  
**Why:** Every build choice must cite a verified source, not vibes.  
**Cause:** Wrong track / wrong stack = weak submission even if demos look cool.

---

## 1. What Lexsi.ai is

Lexsi Labs builds frontier-model science for alignment, interpretability, safety correction, evaluation, and tabular foundation models. Labs in Paris, Mumbai, London. Public site: https://lexsi.ai/

**Alignment & Safety Stack (open source):** CuratorKIT, AlignTune, SafeTune, CircuitKIT, AuditKIT, AgentTune, plus MANSU unlearning research. Thesis of the stack: find a failure → correct it **in the weights** → verify the fix survives adaptation / quantisation. Not wrappers alone.

**Hackathon:** Lexsi AI Safety and Alignment Hackathon, with Cohere Labs + Hugging Face.  
Source: https://hackathon.lexsi.ai/

| Item | Fact |
|------|------|
| Dates | Online Nov 1–21, 2026 |
| Submit | End of day Nov 14 |
| Shortlist | Up to 20 teams by Nov 16 |
| Demo Day | Nov 22 (in-person or online) |
| Kickoff | Oct 31, Polaris School of Tech, Bengaluru (online option) |
| Team size | 1–3; one team per person |
| Register | Opens Oct 12, closes Nov 5 |
| Credits | $20 HF for Discord-registered teams (≤800); $200 more if shortlisted |
| Prizes | $30k+ credits/prizes + Lexsi hiring interviews |

**Hackathon goal (verbatim intent):** chain the open stack into a real pipeline and show **before-and-after metrics** that a small open-weights model becomes meaningfully better, safer, or more reliable for a real use case. Artifacts stay open on Hugging Face.

---

## 2. Tracks — why Track C only

| Track | Chain (min) | What it rewards |
|-------|-------------|-----------------|
| A Fine-tuning + Data Curation | CuratorKIT → AlignTune → AuditKIT | Static data quality + post-train |
| B Red Teaming / Safety | CuratorKIT → SafeTune → CircuitKIT → AuditKIT | Drift audit + weight repair + circuits |
| **C Agentic Fine-tuning** | **AgentTune → AuditKIT** | Reliable tool calls, syntax, efficiency |

Rules: focus on one preferred track. Min **2 repos from the track used together** (preferred 3+). Exception wording on site for “Track 3” — we still ship **AgentTune + AuditKIT** as the mandatory Track C pair so judges see a real chain.

**Why C wins for us**
- Direct stack match: AgentTune trains tool-calling; AuditKIT scores tool-call F1 / validity / redundancy / loops via `episodes_from_agenttune`.
- Tiny Aya has **no native tools chat-template** — AgentTune’s fallback (schemas in system prompt + tool results as user turns) is exactly the hard problem Track C wants solved.
- Trilingual tabular shop agent = clear before/after on tool accuracy + refusal, live demoable.
- We can still *borrow* CuratorKIT / SafeTune ideas as supporting stages without claiming Track A/B as primary.

**What we will not do:** split effort across A+B+C submissions. One Track C submission.

---

## 3. Tiny Aya (Cohere Labs)

Source: https://docs.cohere.com/docs/tiny-aya

- 3.35B params, 70 languages, 8k context. Runs on-device / Colab / modest GPU.
- Languages include **Urdu, Hindi, English** (plus Arabic, Persian — helpful for Urdu script).
- Variants:
  - `tiny-aya-base` — pretrained; good SFT start if we need raw capacity
  - `tiny-aya-global` — balanced instruction-tuned (AgentTune docs example uses this)
  - `tiny-aya-fire` — **best for South Asian languages** (our quality reference / preferred IT start)
  - `tiny-aya-earth` / `tiny-aya-water` — other regions
- HF open weights (gated: accept licence + `hf auth login`). GGUF quants exist for edge demo.
- **Tool calling caveat (AgentTune v1.1.0):** Tiny Aya / Aya Expanse templates ignore `tools`. AgentTune injects `tools_fallback_prompt` asking for `[{"tool_name":...,"parameters":{...}}]` and returns results as user turns. Rollout also parses Cohere `<|START_ACTION|>...<|END_ACTION|>` if emitted.

**Model pick for HifazatTab**
- Primary train target: `CohereLabs/tiny-aya-fire` (South Asia) **or** `tiny-aya-global` if fire is harder to gate/load — pin exact ID at Oct 31 kickoff after licence check.
- Fallback for CPU smoke: rule-based agent (no GPU) so Phase 0 metrics exist tonight.

---

## 4. AgentTune — what Track C actually trains

Docs: https://agenttune.lexsi.ai/ · PyPI `agenttune` ≥1.1.0 · GitHub `Lexsi-Labs/AgentTune`

- Entry: `create_agentic_trainer(algorithm="grpo"|ppo|dpo|rloo|bco, ...)`
- With `tools=[...]`, GRPO/RLOO writes `trajectories.jsonl` + `lexsi_provenance.json` under `output_dir`.
- Agentic spine: strategies (ReAct, Plan-and-Solve, …), EventLog, distill, heal, DECIDE YAML (optional stretch).
- For Tiny Aya on Mac/CPU: `use_vllm=False`, LoRA via `peft_config`.

**Our use:** GRPO (or RLOO) with 3 constrained tools + verifiable rewards; keep trajectories for AuditKIT.

---

## 5. AuditKIT — how we prove before/after

Docs / GitHub: `Lexsi-Labs/AuditKIT`

- `auditkit.agent_eval.episodes_from_agenttune(".../trajectories.jsonl")`
- Scorers to report: `tool_call_f1`, `tool_call_validity`, redundant/loop diagnostics, task completion.
- Also: red-team runner, exact-match / judge metrics for answers.
- Core is stdlib-friendly; heavy backends optional.

**Submission requirement:** more than one metric, before vs after, written rationale.

---

## 6. Form pitch (few lines) — copy for registration / HF article lede

**HifazatTab** (حفاظت = protection) is a Track C agentic fine-tune of Cohere Tiny Aya for a Pakistani kiryana shop: reliable tool calls over a price/stock/loan table in **Urdu, Hindi, and English**. We train with **AgentTune** (GRPO + constrained tools + verifiable reward), evaluate with **AuditKIT** (`episodes_from_agenttune`: tool-call F1, validity, task success), and show script-switch jailbreaks (Urdu↔Hindi) failing before and holding after weight-level repair — including after 4-bit quant. Artifacts on Hugging Face under **umeraamir69**.

One-liner: *Trilingual Tiny Aya shop agent — AgentTune for tool reliability, AuditKIT for before/after proof, Hifazat in the weights not the wrapper.*

---

## 7. Prior art — does this exist already? (researched Oct 31)

Short answer: pieces exist, the combination does not.

- **aya-act (closest method):** distills verified tool-use trajectories from a
  stronger teacher (North Mini Code) into `tiny-aya-global` with QLoRA SFT.
  Same family as our Phase 1–2. No safety angle, no red-team, no repair, not trilingual.
- **TRL tool-calling notebook:** Hugging Face shows training Tiny Aya into a
  tool-calling agent with TRL. Proves the base model can learn tools.
  Not Urdu/Hindi, no tabular shop domain.
- **IndicShield:** filter/gateway blocking Hinglish prompt injections in front of
  the model. Wrapper fix — exactly what our thesis argues is insufficient.
- **HinGlyph attacks:** cross-script (homoglyph + Hinglish) jailbreaks, ~46% success.
  Confirms script-switch is a real hole.
- **LangGap (Global South Safety Hackathon):** Urdu/non-English prompts widen the
  safety gap; 15–46% over-refusal on legit requests. Confirms Urdu is both
  bypassable and over-refused — our consistency test targets both.
- **STEER / spikee:** code-switching jailbreaks (90%+ on small models); spikee ships
  a `digraphic_translate` attacker incl. hindi-urdu script mixing. We can borrow
  it for Phase 4 red-teaming.

Our gap in one line: nobody has built a trilingual Urdu/Hindi/English tool-agent
on Tiny Aya that tunes, red-teams script-switch jailbreaks, repairs in weights,
and proves survival after quant.

## 8. Open questions (resolve at kickoff Oct 31)

1. Exact HF IDs + licence gates for `tiny-aya-fire` vs `global`.
2. Whether judges prefer `fire` for Indic or `global` for balance.
3. Sample problem statements for Track C (site: TBA before start).
4. Any change to “min 2 repos / Track 3 exception” wording.
5. GPU path: Discord $20 HF ZeroGPU vs Colab/Kaggle free tier.

Until then: plan locked; code waits for Phase 0 only after plan evaluation pass.

## Sources

- https://lexsi.ai/
- https://hackathon.lexsi.ai/
- https://docs.cohere.com/docs/tiny-aya
- https://agenttune.lexsi.ai/
- https://pypi.org/project/agenttune/
- https://github.com/Lexsi-Labs/AuditKIT
- https://github.com/fscm44xyz/aya-act
- https://huggingface.co/posts/qgallouedec/326351655871382
- https://github.com/ph4ntom-0x/indicshield
