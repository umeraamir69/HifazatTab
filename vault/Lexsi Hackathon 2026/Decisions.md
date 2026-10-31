# Decisions — rules we do not break

Each decision: **what** we chose, **why**, **cause** (constraint that forced it), **revisit when**.

---

### D1 — Track C only
- **What:** Submit Agentic Fine-tuning only.
- **Why:** Highest impact; AgentTune+AuditKIT is the clearest chain; absorbs curation + red-team as stages.
- **Cause:** Multi-track dilutes Demo Day story; site recommends one preferred track.
- **Revisit:** Never, unless organizers force a sample problem that blocks C.

### D2 — Name HifazatTab
- **What:** Project name HifazatTab (حفاظت = protection/safety, Urdu, Pakistan-associated) + Tab for tabular.
- **Why:** User rule; authentic to kiryana audience; safety thesis in the name.
- **Cause:** Earlier working name was SurakshaTab (Hindi/Sanskrit lean) — replaced.
- **Revisit:** Only if HF slug collision; then `hifazat-tab` / `hifazattab-agent`.

### D3 — Three languages: Urdu, Hindi, English
- **What:** Every tool task exists in all three where feasible.
- **Why:** Tiny Aya strength; script-switch jailbreak is unique demo; real shop code-switching.
- **Cause:** Bilingual-only wastes Tiny Aya’s South Asia edge.
- **Revisit:** Cut Urdu *depth* if late — never drop Urdu entirely.

### D4 — AgentTune + AuditKIT as mandatory pair
- **What:** Training via AgentTune; proof via AuditKIT `episodes_from_agenttune`.
- **Why:** Track C official chain; trajectories.jsonl is the join key.
- **Cause:** Custom-only eval won’t read as “using the stack.”
- **Revisit:** If AuditKIT import breaks, still emit compatible JSONL and document adapter.

### D5 — Three tools, one CSV
- **What:** `lookup_price`, `check_stock`, `loan_eligibility` over `shop.csv`.
- **Why:** Verifiable rewards need a closed world; more tools = noisier GRPO.
- **Cause:** Hackathon window is two weeks of real work after kickoff.
- **Revisit:** Add `list_items` only if baseline tool selection is hopeless.

### D6 — Plan before train code
- **What:** No GRPO / LoRA / HF push until Plan evaluator mean ≥ 4.
- **Why:** User rule; prevents thrash.
- **Cause:** Premature coding on shifting Lexsi APIs wastes GPU credits.
- **Revisit:** Phase 0 *stdlib* scaffolding is allowed after plan gate — still no train.

### D7 — GitHub identity umeraamir69
- **What:** All commits, PRs, HF uploads as umeraamir69. Never Cursor bot / agent CI identity.
- **Why:** User rule; ownership + HF credit eligibility (usernames must match registration).
- **Cause:** Bot commits can disqualify credits / confuse judges.
- **Revisit:** Never.

### D8 — Prefer tiny-aya-fire, fallback global
- **What:** Train `fire` for South Asia; fall back to `global` if gate/load fails.
- **Why:** Docs mark fire as best for South Asian languages.
- **Cause:** AgentTune examples use `global` — both valid.
- **Revisit:** Oct 31 after licence + load test.

### D9 — Document everything in LOG + vault
- **What:** Every step gets what / why / cause / result / how-to-do-better + evaluator note.
- **Why:** User rule; submission write-up writes itself.
- **Cause:** Demo Day Q&A needs a paper trail.
- **Revisit:** Never skip.

### D10 — Weights over wrappers
- **What:** Safety fixes land in adapters/weights; system prompt is not the final fix.
- **Why:** Lexsi lab thesis; matches SafeTune narrative if we stretch Phase 4.
- **Cause:** Prompt-only demos lose to teams who show drift repair.
- **Revisit:** Prompt still used as AgentTune tools fallback (required by Tiny Aya) — that’s infrastructure, not the safety claim.
