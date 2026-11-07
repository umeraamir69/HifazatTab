# AuditKIT report — hifazat-tab-grpo-v1

Source: `umeraamir69/hifazat-tab-grpo-v1` (400 episodes, seed match 180/400).

| Metric | Score |
|--------|-------|
| tool_call_validity | 131/134 (97.76%) |
| task_success_exact | 38/180 (21.11%) |
| tool_name_accuracy | 132/180 (73.33%) |
| tool_call_f1_macro | 0.2176 |
| refusal_precision | 2/46 (4.35%) |

Method: AuditKIT episodes_from_agenttune over AgentTune trajectories.jsonl; gold joined from data/seed_tasks.jsonl by exact prompt; F1 is macro-averaged set-F1 over (tool, arg) pairs per episode.

Limits: Single gold call per episode; multi-turn credit only via set overlap; unmatched prompts excluded from task/F1.
