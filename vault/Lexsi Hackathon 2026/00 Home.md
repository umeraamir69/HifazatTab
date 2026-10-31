# Lexsi Hackathon 2026 — HifazatTab

**Track C only:** Agentic Fine-tuning.  
**Project:** **HifazatTab** (حفاظت — safety/protection, Urdu / Pakistan) — trilingual tool-agent (Urdu · Hindi · English) over shop tables on Cohere **Tiny Aya**.  
**Stack:** AgentTune → AuditKIT (optional CuratorKIT / SafeTune).  
**Identity:** GitHub + HF **umeraamir69** only — never Cursor bot.  
**Code:** `Documents/Lexsi` · **Docs:** this vault folder.

Submit **Nov 14, 2026**. Demo Day **Nov 22**. Kickoff **Oct 31**.

---

## Form pitch (few lines)

HifazatTab post-trains Tiny Aya with AgentTune so a kiryana-shop agent makes reliable tool calls over price, stock, and loan fields in Urdu, Hindi, and English. AuditKIT scores before/after tool-call F1, validity, and task success from AgentTune trajectories. Script-switch jailbreaks are repaired in the weights and re-checked after 4-bit quant.

One-liner: *Trilingual Tiny Aya shop agent — AgentTune for tools, AuditKIT for proof, hifazat in the weights.*

---

## Map

| Note | Role |
|------|------|
| [[Plan]] | Complete build plan — read first |
| [[Research]] | Lexsi + Tiny Aya + Track C facts |
| [[Architecture]] | Loop diagram + file map |
| [[Decisions]] | Rules we do not break |
| [[Data]] | CSV + seed + curation gates |
| [[Redteam]] | Script-switch attacks + repair |
| [[Runbook]] | Commands: what/why/result |
| [[Status]] | Where the build is |
| [[Submission]] | Form copy-paste |
| [[sessions/2026-10-30]] | Tonight’s doc log + evaluator |

Repo mirror of the everything-log: `Documents/Lexsi/LOG.md`.

**Rule:** plan before train code. Document what / why / cause / result / better after every step. Evaluate meaning before moving on.
