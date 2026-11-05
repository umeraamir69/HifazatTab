# Phase 2 on Hugging Face Jobs ($20 credits)

**Run this — not Colab free T4.** T4 OOMs on Tiny Aya GRPO (256k vocab logits).

Script: `scripts/train_grpo_hf_jobs.py`  
Hardware: `l4x1` (24 GB, ~$0.80/hr) — best $/VRAM for us.

## Before you launch

1. Accept licence: https://huggingface.co/CohereLabs/tiny-aya-fire  
2. Laptop: `hf auth login` as **umeraamir69** (write token).  
3. Confirm credits: https://huggingface.co/settings/billing  
4. Repo root: `cd Documents/Lexsi`

## Live runs

| Run | Job ID | Result |
|-----|--------|--------|
| smoke v1 | [`6aeb6f2b…`](https://huggingface.co/jobs/umeraamir69/6aeb6f2b0e0338d1bb80117d) | **COMPLETED** · ~$0.14 · [`…-grpo-v1-smoke`](https://huggingface.co/umeraamir69/hifazat-tab-grpo-v1-smoke) |
| full 50 v1 A10G | [`6aeb7526…`](https://huggingface.co/jobs/umeraamir69/6aeb7526c78863f9c632d1f4) | **COMPLETED** · ~$2.2 · [`…-grpo-v1`](https://huggingface.co/umeraamir69/hifazat-tab-grpo-v1) · AFTER **flat** |
| **v2 100** (strict reward) | (launch after push) | target [`…-grpo-v2`](https://huggingface.co/umeraamir69/hifazat-tab-grpo-v2) |

Do **not** re-run v1 reward. See `vault/.../Findings.md`.

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

## Step 2 — GRPO v2 (strict canonical-arg reward)

## GRPO v2 — 350 steps + mid-train probes (current)

Every 50 steps: save checkpoint, score Phase-1-style probes (core SKUs + all
safety), keep **BEST** checkpoint (not last). Logs `REWARD_CURVE` and
`PROBE_SCORES` lines — paste those for stop-or-continue.

```bash
hf jobs uv run --detach --flavor a10g-small --timeout 18h --secrets HF_TOKEN \
  --name hifazat-grpo-v2-350 \
  scripts/train_grpo_hf_jobs.py -- --max-steps 350 --eval-every 50 \
  --hub-id umeraamir69/hifazat-tab-grpo-v2
```

Watch:
```bash
hf jobs logs -f JOB_ID | egrep 'REWARD_CURVE|PROBE_SCORES|BEST_CHECKPOINT|MEMORIZATION'
```

~3.4 epochs on 825 rows — stop if task stalls while loss drops.

### Older one-shot 100-step recipe


Prefer **a10g-small** if L4 queues. Pushes `umeraamir69/hifazat-tab-grpo-v2`.

```bash
hf jobs uv run --detach --flavor a10g-small --timeout 5h --secrets HF_TOKEN \
  --name hifazat-grpo-v2-100 \
  scripts/train_grpo_hf_jobs.py -- --max-steps 100 \
  --hub-id umeraamir69/hifazat-tab-grpo-v2
```

Budget rough: ~$3–6. Watch: `hf jobs logs -f JOB_ID`

## Step 3 — AFTER metrics (free Colab T4)

Open `colab/phase1_after.ipynb`, set `ADAPTER_ID = "umeraamir69/hifazat-tab-grpo-v2"`, Run all.  
Record exact + soft scores in Results.md + Findings.md; update site bars.

## Do not

| Path | Why |
|------|-----|
| `phase2_grpo.ipynb` on free T4 | Known OOM |
| Spend credits on SFT | SFT fits free T4 (`phase2_sft.ipynb`) |
| ZeroGPU Spaces | Inference demos, not GRPO train |
| `t4-small` Jobs flavor | Same 16 GB trap |

## Optional notebook

`colab/phase2_grpo.ipynb` is a Colab mirror of the same settings — only if you already have an L4+ Colab GPU. Prefer Jobs.
