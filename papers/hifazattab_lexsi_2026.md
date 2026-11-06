# HifazatTab: Trilingual Tool-Calling for Pakistani Kiryana Shops via Constrained Fine-Tuning of Tiny Aya

**Authors:** Muhammad Umer Aamir (`umeraamir69`)  
**Venue draft:** Lexsi AI Safety & Alignment Hackathon 2026 — Track C (Agentic Fine-tuning)  
**Artifacts:** [GitHub](https://github.com/umeraamir69/HifazatTab) · [SFT adapter](https://huggingface.co/umeraamir69/hifazat-tab-sft-v1) · [Demo](https://hifazattab.vercel.app)

---

## Abstract

Multilingual shop assistants must ground answers in tabular inventory while refusing unsafe requests across scripts (Urdu, Hindi, English). We present **HifazatTab**, a Cohere Tiny Aya agent over a closed Pakistani kiryana catalog (≥200 SKUs) with three tools—`lookup_price`, `check_stock`, `loan_eligibility`. Zero-shot Tiny Aya already emits valid tool JSON (**98%** validity) but fails content (**11%** task success) and safety (**14%** refusal). AgentTune GRPO on paid GPUs completed but did not lift AFTER metrics when rewards over-credited any valid schema and arguments stayed natural-language rather than canonical SKU keys. A compact **gold-JSON LoRA SFT** that teaches underscore SKUs and an explicit `refuse` action achieves **100%** tool-call validity, **97.9%** task success, and **87.5%** refusal precision on an expanded multilingual seed (801 tool / 24 probe tasks at first AFTER; catalog now **219** SKUs). We release adapters, seed, and a live voice demo that mirrors the same tool contract for judges without GPU latency.

**Keywords:** tool calling, multilingual NLP, agentic fine-tuning, Urdu/Hindi, AI safety, GRPO, SFT

---

## 1. Introduction

Retail voice agents in South Asia must answer price and stock questions in **English, Hindi (Devanagari), and Urdu (Nastaliq/Arabic script)** while never inventing prices, approving loans, leaking PII, or complying with jailbreaks. Base multilingual LLMs often (i) invent SKUs/prices, (ii) emit free-form answers instead of structured tool calls, and (iii) **obey the same attack in one script and refuse in another** (script-switch failures).

**HifazatTab** (حفاظت = protection) targets Lexsi Track C: improve tool reliability with AgentTune-style training and report before/after metrics. Contributions:

1. A **closed-world shop oracle** (≥200 SKUs, PKR prices, trilingual aliases) and three constrained tools.
2. An honest **BEFORE** baseline on Tiny Aya (`CohereLabs/tiny-aya-fire`) showing format ≠ content ≠ safety.
3. Diagnosis that **first GRPO runs can look “trained” while AFTER stays flat** when rewards do not force canonical arguments.
4. A **winning AFTER** via gold-JSON SFT, with public adapter and a latency-safe live demo.

---

## 2. Related work (brief)

Tool-augmented LLMs and RL for tool use (ReAct-style agents, GRPO/RLOO in AgentTune) emphasize verifiable rewards. Multilingual safety literature highlights script-switch and Hinglish/Roman-Urdu jailbreaks. Our setting is deliberately **narrow and verifiable**: exact tool name + canonical argument match against a CSV oracle—suitable for hackathon AuditKIT-style scoring and for shopkeepers who need trustworthy numbers, not open chat.

---

## 3. Method

### 3.1 Environment

| Element | Design |
|---------|--------|
| Catalog | `shop.csv` — item key, PKR price, stock, category |
| Tools | `lookup_price(item)`, `check_stock(item)`, `loan_eligibility(income)` |
| Aliases | Auto + curated en/hi/ur surface forms; longest-alias match |
| Seed | Price/stock/combo prompts × langs + loan tiers + safety probes |

Loan tool returns **eligibility tiers only** (never approval). Brand questions must refuse (no manufacturer field).

### 3.2 Model & prompts

- Base: Tiny Aya Fire, 4-bit inference/train where needed.  
- Fallback tool prompt (Tiny Aya lacks a native tools template).  
- Required output: one JSON line  
  `[{"tool_name":"…","parameters":{"arg":"<CANONICAL>"}}]`  
  with SKU keys like `atta_20kg`, or `refuse` / `unsafe` for probes.

### 3.3 Training recipes tried

1. **AgentTune GRPO (v1):** exact match +1.0, any valid JSON +0.2, β=0 (skip KL; 256k vocab OOM otherwise).  
2. **GRPO v2:** stricter reward + mid-train Phase-1 probes every 50 steps; ship **best** checkpoint.  
3. **LoRA SFT:** supervised gold JSON over the full seed (canonical args + refuse lines).

### 3.4 Evaluation

Primary metrics (Phase-1 style):

- **tool_call_validity** — parseable tool JSON with name + arg  
- **task_success** — exact gold `tool:arg`  
- **refusal_precision** — safety probes must refuse / emit `refuse`

Live demo uses a **deterministic rule agent** over the same catalog (judge UX); LoRA is for Track C AFTER scores.

---

## 4. Experiments & results

### 4.1 BEFORE (zero-shot Tiny Aya)

| Metric | Score |
|--------|------:|
| tool_call_validity | 150/153 (**98%**) |
| task_success | 17/153 (**11%**) |
| refusal_precision | 3/21 (**14%**) |

Reading: the model learned the **shape** of tool calls but not canonical keys or refusals; probes often invented tools (`write_document`, `system_prompt`).

### 4.2 GRPO AFTER (v1)

| Metric | Score |
|--------|------:|
| validity | 146/153 (95%) |
| task success | 16/153 (**10%**) |
| refusal | 4/21 (**19%**) |

**Finding:** Generations used natural-language args (`"cheeni 5kg"`, Hindi phrases) while gold required `cheeni_5kg`. A **+0.2** reward for any valid JSON removed pressure to canonicalize.

### 4.3 GRPO v2 mid-train probes

Probe scores **frozen** from step 50→300 (~21% task, 62.5% refusal). Run canceled; best would have been step 50. Completions often long/clipped—another training inefficiency.

### 4.4 SFT AFTER (ship)

Evaluated on expanded seed (801 tool / 24 probe at eval time; catalog since grown to **219** SKUs):

| Metric | BEFORE | AFTER SFT | Target |
|--------|-------:|----------:|-------:|
| validity | 98% | **100%** (801/801) | ≥85% |
| task success | 11% | **97.9%** (784/801) | ≥75% |
| refusal | 14% | **87.5%** (21/24) | ≥80% |

Adapter: `umeraamir69/hifazat-tab-sft-v1`. Remaining misses: **brand-trap** probes (3) still emit price/brand tools.

### 4.5 System demo

Public site: trilingual UI, 200+ SKU oracle, browser STT (en/hi), **Groq Whisper** for Urdu, TTS, script-switch red-team panel. Phone/WhatsApp share the same Python tool contract.

---

## 5. Discussion

1. **Validity ≠ success.** High JSON validity can mask wrong tools/args—report both.  
2. **Reward design dominates GRPO.** Soft credit for “valid but wrong” stall learning on small seeds.  
3. **Canonical interfaces help.** Underscore SKUs + refuse tool make supervision and scoring crisp.  
4. **SFT can beat under-specified GRPO** on exact-match tool tasks when gold labels are cheap.  
5. **Split demo vs metrics** is honest for Track C: latency-safe oracle for judges; LoRA for BEFORE/AFTER.

**Limitations:** Closed catalog; SFT may memorize seed phrasings (mitigate with paraphrase diversity); brand refusals incomplete; full AuditKIT F1 on AgentTune trajectories still complementary; quant re-eval of SFT probes pending.

---

## 6. Conclusion

HifazatTab shows that Tiny Aya can become a **reliable trilingual shop tool agent** when arguments are canonical and safety is an explicit action. Gold-JSON SFT delivered Track C target metrics after GRPO alone did not. We release code, ≥200-SKU data, adapter, and a live demo for replication and Demo Day.

---

## Acknowledgments

Lexsi Hackathon mentors & Discord; Hugging Face Jobs credits; Cohere Tiny Aya.

## References (indicative)

- Lexsi AgentTune / AuditKIT documentation (2026).  
- Cohere Labs Tiny Aya model card.  
- Work on tool-use RL and multilingual jailbreaks (to be expanded for camera-ready).

## Appendix A — Artifact URLs

- Repo: https://github.com/umeraamir69/HifazatTab  
- SFT: https://huggingface.co/umeraamir69/hifazat-tab-sft-v1  
- GRPO v1 (negative result): https://huggingface.co/umeraamir69/hifazat-tab-grpo-v1  
- Demo: https://hifazattab.vercel.app  
- Findings log: `vault/Lexsi Hackathon 2026/Findings.md`
