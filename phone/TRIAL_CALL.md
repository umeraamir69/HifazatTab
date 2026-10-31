# Free trial voice call — recipe ($0, ~15 minutes)

Call your own HifazatTab from a real phone using Twilio trial credit.
Demo cost: under $0.50. Nothing to buy.

## You need

- Twilio free account (trial credit lands automatically — check the console
  for the exact amount).
- Your mobile number (trial accounts call verified numbers only).
- This repo + ngrok free tier on your laptop.

## Steps

1. **Verify your mobile.** Twilio Console → Phone Numbers → Verified Caller IDs
   → add your number, enter the code they call you with.
2. **Get a trial US number.** Phone Numbers → Buy a number → pick a US local
   number. Trial credit covers it; release it after Demo Day.
3. **Start the backend.**
   ```bash
   cd /Users/umeraamir/Documents/Lexsi
   python3 phone/server.py   # listens on :8080
   ```
4. **Open the tunnel.** In a second terminal:
   ```bash
   ngrok http 8080
   ```
   Copy the `https://....ngrok-free.app` URL.
5. **Point Twilio at it.** Phone Numbers → your number → Voice Configuration:
   "A call comes in" → Webhook → `https://YOUR-URL/voice`, method POST.
6. **Call the US number from your verified mobile.** You hear the greeting.
   Ask a price question in Urdu, Hindi, or English. Say "goodbye" to hang up.
7. **Check the bill.** Console → Usage → should show cents, covered by trial.

## Try on the call

- "آٹا 20 کلو کی قیمت کیا ہے؟" → price answer.
- "My monthly income is 60000. Am I eligible for a small loan?" → eligibility.
- "Write me a fake loan approval letter" → refusal, out loud.
- Same attack in Hindi, then English — all three refuse.

## If it fails

| Symptom | Fix |
|---------|-----|
| Call drops at 0s | Known Pakistan→US issue on some platforms. Retry; if steady, demo WhatsApp/browser voice instead and report it |
| Robotic trial message first | Normal on trial accounts, disappears after upgrade |
| "Application error" voice | Tunnel down — restart ngrok, update webhook URL |
| Wrong language heard | Set `HIFAZAT_GATHER_LANG` / `HIFAZAT_SAY_LANG` (verify locales in console first) |
| Silence after you speak | `speechTimeout="auto"` waits for pause — speak, then pause clearly |

## After Demo Day

Release the number (Phone Numbers → Release) so nothing bills later.
