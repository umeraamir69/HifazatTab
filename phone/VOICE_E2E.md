# End-to-end voice bot — done-when (flawless demo)

Track C thesis is AgentTune → AuditKIT. The **voice bot is the live proof** judges
touch in 30 seconds. It must not flake.

## Architecture (one brain, three mouths)

```
Caller / browser mic
        │
        ▼
  STT (browser Web Speech  OR  Twilio <Gather>)
        │
        ▼
  SAME agent logic (tools + refusal)
   · Browser: web/index.html  (Hifazat JS mirror)
   · Phone / WhatsApp: phone/server.py → src/agent.py
        │
        ▼
  TTS (browser speechSynthesis  OR  Twilio <Say>)
```

Tuned Tiny Aya adapter (`umeraamir69/hifazat-tab-grpo-v1`) is for **Track C
metrics / AFTER eval**, not for sub-second phone latency. Voice demo stays on the
deterministic shop agent so a call never waits on a GPU.

## Done-when gates (all must pass)

### A. Browser voice (primary — $0, public)

- [x] https://hifazattab.vercel.app returns **200** (no SSO / 404)
- [ ] Chrome: language EN → Mic → “price of atta 20kg” → spoken answer with **2850**
- [ ] Hindi → Mic → आटा कीमत → spoken answer
- [ ] Urdu → Mic → آٹا قیمت → spoken answer (or typed if STT weak)
- [ ] Fake letter attack → spoken **refusal** (no tool leak)
- [ ] Red-team button → **9/9 blocked**

### B. Phone voice (Twilio trial — optional wow)

- [ ] `python3 phone/server.py` + `ngrok http 8080`
- [ ] Twilio number webhook → `https://…/voice`
- [ ] Call → greeting → ask price → hear answer → say goodbye → hangup
- [ ] Trick on call → spoken refusal
- Recipe: `phone/TRIAL_CALL.md`

### C. WhatsApp free path (backup if call drops PK→US)

- [ ] Sandbox join + webhook `/whatsapp`
- [ ] Urdu price question → 2850 in reply
- [ ] Fake letter → refusal Message
- Recipe: `phone/README.md`

### D. Regression (run before every demo)

```bash
cd Documents/Lexsi
python3 -m unittest discover -s tests -v
curl -sI https://hifazattab.vercel.app   # expect 200
curl -sX POST --data-urlencode "SpeechResult=What is the price of atta 20kg?" \
  http://localhost:8080/gather | grep -E '2850|Say'
```

## Demo Day 60-second script

1. Open https://hifazattab.vercel.app on laptop (Chrome).
2. Voice replies ON · English · Mic · “What is the price of atta 20kg?”
3. Switch Urdu · Mic or sample · hear/see answer.
4. Click the fake-letter sample → refusal spoken.
5. (Optional) Live call or WhatsApp one line if tunnel is up.
6. Cut to AFTER metrics slide (AgentTune GRPO adapter Hub link).

## Failure playbook

| Fail | Fallback |
|------|----------|
| Mic denied / Safari STT | Click sample buttons + Voice replies |
| Urdu STT garbage | Type Urdu sample; still speak answer |
| Vercel 404 / SSO | `vercel project protection disable hifazattab --sso` + `vercel --prod` from `web/` |
| Twilio call drops | WhatsApp Sandbox or browser only — say so honestly |
| Wrong shop number | Fix `data/shop.csv` + mirror in `web/index.html` TABLE |

## Ownership

- Public voice site: `web/index.html` → Vercel project `hifazattab`
- Phone/WhatsApp: `phone/server.py` (stdlib)
- Agent truth: `src/agent.py` + `src/tools.py` (keep JS mirror in sync)
