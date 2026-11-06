/**
 * BYO catalog proxy — fetches a merchant's product API and normalizes to
 * HifazatTab shape: { catalog: { sku: {price, stock, category} }, aliases }.
 *
 * POST JSON:
 * {
 *   "baseUrl": "https://...",
 *   "listPath": "/api/mock-merchant",   // relative to baseUrl, or absolute
 *   "authHeader": "Authorization",     // optional
 *   "authValue": "Bearer …",           // optional — never echoed back
 *   "itemsPath": "items",              // dot path to array (default "items")
 *   "map": { "id":"sku", "price":"price_pkr", "stock":"quantity", "category":"aisle" }
 * }
 *
 * → { ok, catalog, aliases, count, source }
 */
export const config = { maxDuration: 20 };

function cors(res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
}

function dig(obj, path) {
  if (!path || path === "$" || path === ".") return obj;
  const parts = String(path).split(".").filter(Boolean);
  let cur = obj;
  for (const p of parts) {
    if (cur == null) return undefined;
    cur = cur[p];
  }
  return cur;
}

function joinUrl(base, path) {
  if (!path) return base;
  if (/^https?:\/\//i.test(path)) return path;
  const b = String(base || "").replace(/\/+$/, "");
  const p = String(path).startsWith("/") ? path : `/${path}`;
  return `${b}${p}`;
}

function toAliases(key, name) {
  const names = new Set();
  names.add(key);
  names.add(key.replace(/_/g, " "));
  if (name) names.add(String(name));
  const stem = key.replace(/_\d+(kg|g|L|ml|pack)?$/i, "").replace(/_/g, " ");
  if (stem.length >= 4) names.add(stem);
  return [...names].sort((a, b) => b.length - a.length);
}

function normalize(rawItems, map) {
  const m = {
    id: (map && map.id) || "sku",
    price: (map && map.price) || "price_pkr",
    stock: (map && map.stock) || "quantity",
    category: (map && map.category) || "aisle",
    name: (map && map.name) || "name",
  };
  const catalog = {};
  const aliases = {};
  for (const row of rawItems || []) {
    if (!row || typeof row !== "object") continue;
    const id = row[m.id] ?? row.sku ?? row.item ?? row.id;
    if (!id) continue;
    const key = String(id).trim().replace(/\s+/g, "_");
    const price = Number(row[m.price] ?? row.price ?? row.price_pkr ?? 0);
    const stock = Number(row[m.stock] ?? row.stock ?? row.quantity ?? 0);
    const category = String(row[m.category] ?? row.category ?? row.aisle ?? "general");
    const name = row[m.name] ?? row.name ?? key;
    catalog[key] = { price, stock, category };
    aliases[key] = toAliases(key, name);
  }
  return { catalog, aliases };
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
    const baseUrl = String(body.baseUrl || "").trim();
    const listPath = String(body.listPath || "/").trim();
    if (!baseUrl && !/^https?:\/\//i.test(listPath)) {
      res.status(400).json({
        error: "Need baseUrl (or absolute listPath)",
        hint: "Try baseUrl=https://hifazattab.vercel.app and listPath=/api/mock-merchant",
      });
      return;
    }

    const url = joinUrl(baseUrl, listPath);
    const headers = { Accept: "application/json" };
    if (body.authHeader && body.authValue) {
      headers[String(body.authHeader)] = String(body.authValue);
    }

    const upstream = await fetch(url, { method: "GET", headers });
    const text = await upstream.text();
    let data;
    try {
      data = JSON.parse(text);
    } catch {
      res.status(502).json({
        error: "Upstream did not return JSON",
        status: upstream.status,
        preview: text.slice(0, 200),
      });
      return;
    }
    if (!upstream.ok) {
      res.status(502).json({
        error: "Upstream error",
        status: upstream.status,
        body: typeof data === "object" ? data : { raw: text.slice(0, 200) },
      });
      return;
    }

    const itemsPath = body.itemsPath == null ? "items" : body.itemsPath;
    let raw = dig(data, itemsPath);
    if (!Array.isArray(raw) && Array.isArray(data)) raw = data;
    if (!Array.isArray(raw)) {
      res.status(422).json({
        error: "Could not find items array",
        itemsPath,
        topKeys: data && typeof data === "object" ? Object.keys(data) : [],
      });
      return;
    }

    const { catalog, aliases } = normalize(raw, body.map || {});
    const count = Object.keys(catalog).length;
    if (!count) {
      res.status(422).json({ error: "Normalized 0 items — check field map", sample: raw[0] || null });
      return;
    }

    res.status(200).json({
      ok: true,
      count,
      source: url,
      catalog,
      aliases,
      // never echo secrets
    });
  } catch (e) {
    res.status(500).json({ error: e.message || String(e) });
  }
}
