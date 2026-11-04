# Phase 2 on Hugging Face Jobs ($20 credits)

**Run this — not Colab free T4.** T4 OOMs on Tiny Aya GRPO (256k vocab logits).

Script: `scripts/train_grpo_hf_jobs.py`  
Hardware: `l4x1` (24 GB, ~$0.80/hr) — best $/VRAM for us.

## Before you launch

1. Accept licence: https://huggingface.co/CohereLabs/tiny-aya-fire  
2. Laptop: `hf auth login` as **umeraamir69** (write token).  
3. Confirm credits: https://huggingface.co/settings/billing  
4. Repo root: `cd Documents/Lexsi`

## Live runs (Nov 4, 2026) — agent launched these

| Run | Job ID | Result |
|-----|--------|--------|
| smoke | [`6aeb6f2b0e0338d1bb80117d`](https://huggingface.co/jobs/umeraamir69/6aeb6f2b0e0338d1bb80117d) | **COMPLETED** · L4 · ~623s · ~$0.14 · Hub [`…-grpo-v1-smoke`](https://huggingface.co/umeraamir69/hifazat-tab-grpo-v1-smoke) |
| full 50 | [`6aeb720ac78863f9c632cde3`](https://huggingface.co/jobs/umeraamir69/6aeb720ac78863f9c632cde3) | launched · timeout 4h · target `…-grpo-v1` |

```bash
hf jobs logs -f umeraamir69/6aeb720ac78863f9c632cde3
hf jobs inspect umeraamir69/6aeb720ac78863f9c632cde3
```

## Step 1 — smoke (already done Nov 4)

```bash
hf jobs uv run --detach --flavor l4x1 --timeout 45m --secrets HF_TOKEN \
  --name hifazat-grpo-smoke \
  scripts/train_grpo_hf_jobs.py -- --smoke
```

Expect: CUDA NVIDIA L4 → train 3 steps → push `umeraamir69/hifazat-tab-grpo-v1-smoke`.  
Actual: COMPLETED, ~$0.14. If a future smoke OOMs, stop — do not start full.

```bash
hf jobs logs JOB_ID   # stream / re-read
hf jobs cancel JOB_ID # if stuck
```

## Step 2 — full AFTER adapter (running)

```bash
hf jobs uv run --detach --flavor l4x1 --timeout 4h --secrets HF_TOKEN \
  --name hifazat-grpo-full50 \
  scripts/train_grpo_hf_jobs.py -- --max-steps 50
```

Pushes `umeraamir69/hifazat-tab-grpo-v1`. Budget ~$1.5–3 (steps ~150–180s each).

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
