# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "agenttune>=1.1.0",
#   "auditkit",
#   "transformers",
#   "accelerate",
#   "bitsandbytes",
#   "peft",
#   "trl",
#   "huggingface_hub",
#   "datasets",
#   "torch",
# ]
#
# [tool.hf-jobs]
# flavor = "l4x1"
# timeout = "2h"
# secrets = ["HF_TOKEN"]
# ///
"""HifazatTab Phase 2 — AgentTune GRPO on Hugging Face Jobs (paid GPU).

Spend the Lexsi $20 credits here — NOT on free Colab T4 (OOM on Cohere 256k vocab).

Launch from your laptop (logged in as umeraamir69):

  # 1) Smoke (~$0.30–0.80): prove GRPO fits before a long burn
  hf jobs uv run --flavor l4x1 --timeout 45m --secrets HF_TOKEN \\
    scripts/train_grpo_hf_jobs.py -- --smoke

  # 2) Full AFTER adapter (~$1–3 on l4x1)
  hf jobs uv run --flavor l4x1 --timeout 2h --secrets HF_TOKEN \\
    scripts/train_grpo_hf_jobs.py -- --max-steps 50

Watch: hf jobs logs JOB_ID
Cancel: hf jobs cancel JOB_ID

Hardening baked in (from Colab T4 failures):
  beta=0 (skip ref-model KL / 256k logits)
  LoRA q_proj+v_proj only, r=8 (no lm_head adapter)
  max_steps_per_turn=2 (default 20 freezes)
  chat-message prompts, report_to=none, single GPU
"""

from __future__ import annotations

import argparse
import csv
import gc
import json
import os
import re
import sys
import urllib.request

os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="HifazatTab AgentTune GRPO on HF Jobs")
    p.add_argument("--smoke", action="store_true", help="3 steps only — fit test")
    p.add_argument("--max-steps", type=int, default=50, help="GRPO max_steps (ignored if --smoke)")
    p.add_argument("--hub-id", default="umeraamir69/hifazat-tab-grpo-v1")
    p.add_argument("--model", default="CohereLabs/tiny-aya-fire")
    p.add_argument(
        "--data-base",
        default="https://raw.githubusercontent.com/umeraamir69/HifazatTab/main/data",
    )
    p.add_argument("--output-dir", default="./hifazat-grpo")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    max_steps = 3 if args.smoke else args.max_steps

    import torch
    from datasets import Dataset
    from huggingface_hub import login
    from agenttune import create_agentic_trainer

    print("=== HifazatTab GRPO ===")
    print("smoke:", args.smoke, "max_steps:", max_steps, "hub:", args.hub_id)
    print("cuda:", torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else "NONE")
    assert torch.cuda.is_available(), "No CUDA on this Job — pick --flavor l4x1 or a10g-small"

    tok = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
    assert tok, "HF_TOKEN missing — launch with: hf jobs uv run --secrets HF_TOKEN ..."
    login(tok)

    # --- data + rewards (same contract as colab/phase2_grpo.ipynb) ---
    shop_raw = urllib.request.urlopen(args.data_base + "/shop.csv").read().decode()
    shop = {r["item"]: r for r in csv.DictReader(shop_raw.splitlines())}

    seed = []
    with urllib.request.urlopen(args.data_base + "/seed_tasks.jsonl") as f:
        for line in f:
            line = line.decode("utf-8").strip()
            if line:
                seed.append(json.loads(line))

    train_rows = []
    for row in seed:
        msg = [{"role": "user", "content": row["prompt"]}]
        if row.get("type") == "tool-task":
            tool, _, arg = row["tool"].partition(":")
            train_rows.append({"prompt": msg, "want_tool": tool, "want_arg": arg, "must_refuse": 0})
        else:
            train_rows.append({"prompt": msg, "want_tool": "", "want_arg": "", "must_refuse": 1})
    train_dataset = Dataset.from_list(train_rows)
    print("train rows:", len(train_dataset))

    tool_re = re.compile(r'"tool_name"\s*:\s*"(\w+)"')
    arg_re = re.compile(r'"arg"\s*:\s*"([^"]+)"')
    refuse_words = (
        "cannot",
        "sorry",
        "unable",
        "\u0645\u0639\u0630\u0631",
        "\u0646\u06c1\u06cc\u06ba",
        "\u092e\u093e\u092b",
        "\u0928\u0939\u0940\u0902",
    )

    def _text(c):
        if isinstance(c, str):
            return c
        parts = []
        for m in c or []:
            if isinstance(m, dict):
                if m.get("content"):
                    parts.append(str(m["content"]))
                if m.get("tool_calls"):
                    parts.append(json.dumps(m["tool_calls"]))
        return " ".join(parts)

    def _col(vals, i, n):
        if not isinstance(vals, list):
            return vals
        if len(vals) == n:
            return vals[i]
        if len(vals) and n % len(vals) == 0:
            return vals[i // (n // len(vals))]
        return vals[0]

    def _refused(t):
        low = t.lower()
        return (not tool_re.search(t)) or any(w in low for w in refuse_words)

    def reward_task(prompts, completions, **kwargs):
        n = len(completions)
        out = []
        for i, c in enumerate(completions):
            if _col(kwargs.get("must_refuse"), i, n):
                out.append(0.0)
                continue
            t = _text(c)
            m1, m2 = tool_re.search(t), arg_re.search(t)
            if not (m1 and m2):
                out.append(0.0)
                continue
            if m1.group(1) not in ("lookup_price", "check_stock", "loan_eligibility"):
                out.append(-0.5)
                continue
            wt = _col(kwargs.get("want_tool"), i, n)
            wa = _col(kwargs.get("want_arg"), i, n)
            out.append(1.0 if (m1.group(1) == wt and m2.group(1) == wa) else 0.2)
        return out

    def reward_safety(prompts, completions, **kwargs):
        n = len(completions)
        out = []
        for i, c in enumerate(completions):
            if _col(kwargs.get("must_refuse"), i, n):
                out.append(0.5 if _refused(_text(c)) else -1.0)
            else:
                out.append(0.0)
        return out

    system = (
        "You answer shop questions with a tool call. Reply one line: "
        '[{"tool_name": "<lookup_price|check_stock|loan_eligibility>", '
        '"parameters": {"arg": "<value>"}}]'
    )

    def lookup_price(arg):
        if arg in shop:
            return "%s: %d PKR, stock %d." % (arg, int(shop[arg]["price_pkr"]), int(shop[arg]["stock"]))
        return "item_not_found: " + str(arg)

    def check_stock(arg):
        if arg in shop:
            return "%s: stock %d." % (arg, int(shop[arg]["stock"]))
        return "item_not_found: " + str(arg)

    def loan_eligibility(arg):
        digits = re.sub(r"[^0-9]", "", str(arg))
        if not digits:
            return "bad_income"
        inc = int(digits)
        tier = "medium" if inc >= 150000 else ("small" if inc >= 40000 else "none")
        return "tier=%s (eligibility_only_no_approval)" % tier

    gc.collect()
    torch.cuda.empty_cache()
    free_gb = torch.cuda.mem_get_info()[0] / 1e9
    print("GPU free GB before train:", round(free_gb, 2))
    assert free_gb > 10.0, "GPU almost full (%.2f GB free) — abort" % free_gb

    # L4/A10G = 24 GB: slightly longer completions than T4; still slim LoRA + beta=0
    trainer = create_agentic_trainer(
        algorithm="grpo",
        model=args.model,
        load_in_4bit=True,
        use_vllm=False,
        peft_config=dict(
            r=8,
            lora_alpha=16,
            lora_dropout=0.05,
            target_modules=["q_proj", "v_proj"],
            task_type="CAUSAL_LM",
        ),
        tools=[lookup_price, check_stock, loan_eligibility],
        system_prompt=system,
        reward_funcs=[reward_task, reward_safety],
        output_dir=args.output_dir,
        train_dataset=train_dataset,
        max_steps=max_steps,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=8,
        gradient_checkpointing=True,
        num_generations=2,
        beta=0.0,
        max_prompt_length=128,
        max_completion_length=48,
        max_steps_per_turn=2,
        max_new_tokens=48,
        logging_steps=1,
        optim="paged_adamw_8bit",
        report_to="none",
        log_completions=False,
        save_steps=max(1, max_steps // 2),
    )

    print("training…")
    trainer.train()
    print("local save:", args.output_dir)

    hub = args.hub_id + ("-smoke" if args.smoke else "")
    print("pushing:", hub)
    trainer.push_to_hub(hub)
    print("DONE. Adapter:", hub)
    print("Next: re-run colab/phase1_baseline.ipynb against this adapter for AFTER metrics.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print("FATAL:", type(e).__name__, e, file=sys.stderr)
        raise
