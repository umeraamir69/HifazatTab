# Phase 1 Notebook — What Each Cell Does (plain words)

File: `phase1_baseline.ipynb`. Goal: get the real "before" number from Tiny Aya.

## Cell 0 — Title (markdown, does nothing)

Instructions only. Reminds you: T4 GPU, run top to bottom, accept the model
licence first, send scores back. Why: Colab resets every session, so the
checklist lives where you see it.

## Cell 1 — Install

```
!pip install transformers accelerate bitsandbytes huggingface_hub
```

Why each one:

- `transformers` loads and runs Tiny Aya. No model without it.
- `accelerate` spreads the model across GPU memory.
- `bitsandbytes` loads the model in 4-bit, ~4x smaller, so it fits a free T4.
  Same shrinking trick our quant-survival test uses later.
- `huggingface_hub` logs in and downloads the gated weights.

Cause: Colab gives you a fresh machine each time, so installs run first, always.

## Cell 2 — Login

Asks for your Hugging Face token with `getpass` (typing stays hidden).

Why: Tiny Aya is gated. You accept the licence on its page, then the token
proves who you are. No licence + no token means the download is refused.
Hidden typing means the token never lands in outputs or screenshots.

## Cell 3 — Baseline run

Five jobs in one cell:

1. **Load in 4-bit** (`load_in_4bit`, `device_map="auto"`). Only way 3.35B
   params fit a free T4.
2. **Fallback prompt.** Tiny Aya has no native tool template, so we describe
   the tool JSON in the prompt (`SYSTEM` + `Tool call:`) and let the model
   complete the pattern. This workaround is exactly the gap Phase 2 trains away.
3. **Same seed tasks** as the laptop eval, fetched from our GitHub repo.
   Same questions = fair before/after comparison.
4. **Regex scoring.** Pulls `tool_name` + `arg` out of each reply. Valid JSON
   counts as validity, right tool + right arg counts as task success, no tool
   call on a probe counts as a held refusal.
5. **Greedy decoding** (`do_sample=False`). No randomness, so the number is
   reproducible.

Cause: judges score the gap between this number and the tuned number.
A weak-but-honest baseline beats a flattering one.

## What to send back

The last printed block: validity, task success, refusal precision, model name.
