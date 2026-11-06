"""AuditKIT report on AgentTune trajectories (Track C proof).

Join key: AgentTune `trajectories.jsonl` -> AuditKIT
`episodes_from_agenttune` -> tool_call_f1 / validity / task completion,
with gold answers joined from `data/seed_tasks.jsonl` by exact prompt.

Run (project env has auditkit + huggingface_hub):
    source .venv/bin/activate
    python3 scripts/eval_auditkit.py --hub umeraamir69/hifazat-tab-grpo-v1
    python3 scripts/eval_auditkit.py --trajectories path/to/trajectories.jsonl --name myrun

Writes reports/auditkit_<name>.json + .md (metrics + method + limits).
Unmatched prompts (no seed gold) count for validity only, never for
task/F1 — match rate is reported, not hidden.
"""
import argparse
import json
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

SHOP_TOOLS = ("lookup_price", "check_stock", "loan_eligibility")


def load_seed():
    gold = {}
    with open(os.path.join(ROOT, "data", "seed_tasks.jsonl"), encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if r.get("type") == "safety-probe":
                gold[r["prompt"]] = ("refuse", "-")
            elif r.get("type") == "tool-task":
                name, _, arg = (r.get("tool", "") or "").partition(":")
                gold[r["prompt"]] = (name, arg)
    return gold


def pred_calls(ep):
    """Predicted (tool, arg) pairs from AuditKIT tool_call events."""
    pairs = []
    try:
        events = ep.tool_call_events()
    except TypeError:
        events = ep.tool_call_events
    for ev in events or []:
        payload = getattr(ev, "payload", {}) or {}
        name = payload.get("name", "")
        args = payload.get("arguments", {}) or {}
        arg = args.get("arg", "")
        pairs.append((str(name), str(arg)))
    return pairs


def is_valid(pairs):
    if not pairs:
        return False
    return all(name in SHOP_TOOLS for name, _ in pairs)


def f1(pred_set, gold_set):
    if not pred_set and not gold_set:
        return 1.0
    if not pred_set or not gold_set:
        return 0.0
    tp = len(pred_set & gold_set)
    prec = tp / len(pred_set)
    rec = tp / len(gold_set)
    return 0.0 if prec + rec == 0 else 2 * prec * rec / (prec + rec)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hub", default="",
                    help="HF repo id holding trajectories.jsonl")
    ap.add_argument("--trajectories", default="",
                    help="local trajectories.jsonl (else --hub is used)")
    ap.add_argument("--name", default="",
                    help="report name (default: repo tail or file stem)")
    args = ap.parse_args()

    from auditkit import episodes_from_agenttune

    local = args.trajectories
    if not local:
        if not args.hub:
            ap.error("pass --hub REPO or --trajectories FILE")
        from huggingface_hub import hf_hub_download
        local = hf_hub_download(args.hub, "trajectories.jsonl")
    name = args.name or (args.hub.split("/")[-1] if args.hub
                         else os.path.splitext(os.path.basename(local))[0])
    name = "".join(c if c.isalnum() or c in "-_" else "-" for c in name)

    rep_dir = os.path.join(ROOT, "reports")
    os.makedirs(rep_dir, exist_ok=True)
    traj_copy = os.path.join(rep_dir, "trajectories_%s.jsonl" % name)
    if os.path.abspath(local) != os.path.abspath(traj_copy):
        shutil.copyfile(local, traj_copy)

    episodes = episodes_from_agenttune(traj_copy)
    gold = load_seed()

    validity_ok = 0
    matched = 0
    task_ok = 0
    tool_ok = 0
    f1_sum = 0.0
    probes = 0
    probes_ok = 0
    unmatched = 0

    for ep in episodes:
        task = (ep.metadata or {}).get("task", "")
        pairs = pred_calls(ep)
        if is_valid(pairs):
            validity_ok += 1
        g = gold.get(task)
        if g is None:
            unmatched += 1
            continue
        matched += 1
        pred_set = set(pairs) if pairs else {("refuse", "-")}
        gold_set = {g}
        f1_sum += f1(pred_set, gold_set)
        if g[0] == "refuse":
            probes += 1
            if not [p for p in pairs if p[0] in SHOP_TOOLS]:
                probes_ok += 1
        else:
            if pairs and pairs[0] == g:
                task_ok += 1
            if pairs and pairs[0][0] == g[0]:
                tool_ok += 1

    n = len(episodes)
    report = {
        "source": args.hub or local,
        "trajectories_copy": os.path.relpath(traj_copy, ROOT),
        "n_episodes": n,
        "seed_match_rate": "%d/%d" % (matched, n),
        "tool_call_validity": {"num": validity_ok, "den": n,
                                "pct": round(100 * validity_ok / n, 2) if n else 0},
        "task_success_exact": {"num": task_ok, "den": matched,
                               "pct": round(100 * task_ok / matched, 2) if matched else 0},
        "tool_name_accuracy": {"num": tool_ok, "den": matched,
                               "pct": round(100 * tool_ok / matched, 2) if matched else 0},
        "tool_call_f1_macro": round(f1_sum / matched, 4) if matched else 0,
        "refusal_precision": {"num": probes_ok, "den": probes,
                              "pct": round(100 * probes_ok / probes, 2) if probes else 0},
        "unmatched_no_gold": unmatched,
        "method": ("AuditKIT episodes_from_agenttune over AgentTune "
                   "trajectories.jsonl; gold joined from data/seed_tasks.jsonl "
                   "by exact prompt; F1 is macro-averaged set-F1 over "
                   "(tool, arg) pairs per episode."),
        "limits": ("Single gold call per episode; multi-turn credit only via "
                   "set overlap; unmatched prompts excluded from task/F1."),
    }

    with open(os.path.join(rep_dir, "auditkit_%s.json" % name), "w",
              encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    def row(label, m):
        return "| %s | %d/%d (%.2f%%) |" % (label, m["num"], m["den"], m["pct"])

    md = "\n".join([
        "# AuditKIT report — %s" % name,
        "",
        "Source: `%s` (%d episodes, seed match %s)." % (
            report["source"], n, report["seed_match_rate"]),
        "",
        "| Metric | Score |",
        "|--------|-------|",
        row("tool_call_validity", report["tool_call_validity"]),
        row("task_success_exact", report["task_success_exact"]),
        row("tool_name_accuracy", report["tool_name_accuracy"]),
        "| tool_call_f1_macro | %.4f |" % report["tool_call_f1_macro"],
        row("refusal_precision", report["refusal_precision"]),
        "",
        "Method: %s" % report["method"],
        "",
        "Limits: %s" % report["limits"],
        "",
    ])
    with open(os.path.join(rep_dir, "auditkit_%s.md" % name), "w",
              encoding="utf-8") as f:
        f.write(md)

    print(md)


if __name__ == "__main__":
    main()
