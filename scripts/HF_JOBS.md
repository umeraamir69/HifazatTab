# Phase 2 on Hugging Face Jobs ($20 credits)

**Run this — not Colab free T4.** T4 OOMs on Tiny Aya GRPO (256k vocab logits).

Script: `scripts/train_grpo_hf_jobs.py`  
Hardware: `l4x1` (24 GB, ~$0.80/hr) — best $/VRAM for us.

## Before you launch

1. Accept licence: https://huggingface.co/CohereLabs/tiny-aya-fire  
2. Laptop: `hf auth login` as **umeraamir69** (write token).  
3. Confirm credits: https://huggingface.co/settings/billing  
4. Repo root: `cd Documents/Lexsi`

## Step 1 — smoke (do this first)

```bash
hf jobs uv run --flavor l4x1 --timeout 45m --secrets HF_TOKEN \
  scripts/train_grpo_hf_jobs.py -- --smoke
```

Expect: CUDA ok → train 3 steps → push `umeraamir69/hifazat-tab-grpo-v1-smoke`.  
Cost: roughly $0.30–0.80. If this OOMs, stop and say so — do not start full.

```bash
hf jobs logs JOB_ID   # stream / re-read
hf jobs cancel JOB_ID # if stuck
```

## Step 2 — full AFTER adapter

```bash
hf jobs uv run --flavor l4x1 --timeout 2h --secrets HF_TOKEN \
  scripts/train_grpo_hf_jobs.py -- --max-steps 50
```

Pushes `umeraamir69/hifazat-tab-grpo-v1`. Budget ~$1–3.

## Step 3 — AFTER metrics (free Colab T4)

Open `colab/phase1_baseline.ipynb`, point it at the Hub adapter, Run all.  
Record validity / task / refusal in Results.md.

## Do not

| Path | Why |
|------|-----|
| `phase2_grpo.ipynb` on free T4 | Known OOM |
| Spend credits on SFT | SFT fits free T4 (`phase2_sft.ipynb`) |
| ZeroGPU Spaces | Inference demos, not GRPO train |
| `t4-small` Jobs flavor | Same 16 GB trap |

## Optional notebook

`colab/phase2_grpo.ipynb` is a Colab mirror of the same settings — only if you already have an L4+ Colab GPU. Prefer Jobs.
