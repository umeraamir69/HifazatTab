/**
 * Urdu (and hi/en) speech-to-text via Whisper.
 *
 * Required env (set one):
 *   GROQ_API_KEY   — recommended, free tier: https://console.groq.com/keys
 *   OPENAI_API_KEY — alternative: https://platform.openai.com/api-keys
 *
 * POST JSON: { audio: "<base64>", mime?: "audio/webm", lang?: "ur"|"hi"|"en" }
 * → { text, provider, lang }
 */
export const config = {
  api: { bodyParser: { sizeLimit: "8mb" } },
  maxDuration: 30,
};

function cors(res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
}

function b64ToBuffer(b64) {
  const cleaned = String(b64 || "").replace(/^data:[^;]+;base64,/, "");
  return Buffer.from(cleaned, "base64");
}

function extForMime(mime) {
  const m = (mime || "").toLowerCase();
  if (m.includes("mp4") || m.includes("m4a")) return "m4a";
  if (m.includes("mpeg") || m.includes("mp3")) return "mp3";
  if (m.includes("wav")) return "wav";
  if (m.includes("ogg")) return "ogg";
  return "webm";
}

async function transcribeGroq(buf, mime, lang) {
  const key = process.env.GROQ_API_KEY;
  if (!key) return null;
  const form = new FormData();
  const blob = new Blob([buf], { type: mime || "audio/webm" });
  form.append("file", blob, `audio.${extForMime(mime)}`);
  form.append("model", "whisper-large-v3");
  form.append("response_format", "json");
  if (lang && lang !== "auto") form.append("language", lang === "ur" ? "ur" : lang);
  const r = await fetch("https://api.groq.com/openai/v1/audio/transcriptions", {
    method: "POST",
    headers: { Authorization: `Bearer ${key}` },
    body: form,
  });
  const data = await r.json().catch(() => ({}));
  if (!r.ok) {
    const err = new Error(data.error?.message || data.message || `Groq ${r.status}`);
    err.status = r.status;
    throw err;
  }
  return { text: data.text || "", provider: "groq" };
}

async function transcribeOpenAI(buf, mime, lang) {
  const key = process.env.OPENAI_API_KEY;
  if (!key) return null;
  const form = new FormData();
  const blob = new Blob([buf], { type: mime || "audio/webm" });
  form.append("file", blob, `audio.${extForMime(mime)}`);
  form.append("model", "whisper-1");
  form.append("response_format", "json");
  if (lang && lang !== "auto") form.append("language", lang === "ur" ? "ur" : lang);
  const r = await fetch("https://api.openai.com/v1/audio/transcriptions", {
    method: "POST",
    headers: { Authorization: `Bearer ${key}` },
    body: form,
  });
  const data = await r.json().catch(() => ({}));
  if (!r.ok) {
    const err = new Error(data.error?.message || data.message || `OpenAI ${r.status}`);
    err.status = r.status;
    throw err;
  }
  return { text: data.text || "", provider: "openai" };
}

export default async function handler(req, res) {
  cors(res);
  if (req.method === "OPTIONS") {
    res.status(204).end();
    return;
  }
  if (req.method !== "POST") {
    res.status(405).json({ error: "POST only" });
    return;
  }

  try {
    const body = typeof req.body === "string" ? JSON.parse(req.body || "{}") : (req.body || {});
    const { audio, mime, lang } = body;
    if (!audio) {
      res.status(400).json({ error: "missing audio (base64)" });
      return;
    }
    const buf = b64ToBuffer(audio);
    if (!buf.length) {
      res.status(400).json({ error: "empty audio" });
      return;
    }
    if (buf.length > 7.5 * 1024 * 1024) {
      res.status(413).json({ error: "audio too large (max ~7MB)" });
      return;
    }

    const sttLang = lang === "hi" ? "hi" : lang === "en" ? "en" : "ur";
    let out = await transcribeGroq(buf, mime || "audio/webm", sttLang);
    if (!out) out = await transcribeOpenAI(buf, mime || "audio/webm", sttLang);
    if (!out) {
      res.status(503).json({
        error: "No STT key configured",
        need: "Set GROQ_API_KEY (recommended) or OPENAI_API_KEY in Vercel project env, then redeploy.",
        links: {
          groq: "https://console.groq.com/keys",
          openai: "https://platform.openai.com/api-keys",
        },
      });
      return;
    }
    res.status(200).json({ text: String(out.text || "").trim(), provider: out.provider, lang: sttLang });
  } catch (e) {
    res.status(e.status || 500).json({ error: e.message || String(e) });
  }
}
