/**
 * Demo merchant API — stand-in for a real shop backend.
 * Use this URL in the Dashboard "Connect API" form to try BYO-API without
 * wiring your own server first.
 *
 * GET /api/mock-merchant          → { items: [...] }
 * GET /api/mock-merchant?sku=X    → one item or 404
 */
function cors(res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Api-Key");
}

const ITEMS = [
  { sku: "atta_20kg", price_pkr: 2850, quantity: 40, aisle: "staples", name: "Atta 20kg" },
  { sku: "cooking_oil_5L", price_pkr: 7200, quantity: 15, aisle: "oils", name: "Cooking oil 5L" },
  { sku: "olive_oil_500ml", price_pkr: 1650, quantity: 1, aisle: "oils", name: "Olive oil 500ml" },
  { sku: "milk_1L", price_pkr: 280, quantity: 55, aisle: "dairy", name: "Milk 1L" },
  { sku: "basmati_1kg", price_pkr: 780, quantity: 28, aisle: "staples", name: "Basmati 1kg" },
  { sku: "daal_moong_1kg", price_pkr: 480, quantity: 50, aisle: "pulses", name: "Moong dal 1kg" },
  { sku: "extension_board", price_pkr: 890, quantity: 1, aisle: "household", name: "Extension board" },
  { sku: "potato_1kg", price_pkr: 120, quantity: 80, aisle: "produce", name: "Potato 1kg" },
];

export default function handler(req, res) {
  cors(res);
  if (req.method === "OPTIONS") {
    res.status(204).end();
    return;
  }
  if (req.method !== "GET") {
    res.status(405).json({ error: "GET only" });
    return;
  }
  const sku = (req.query && (req.query.sku || req.query.item)) || null;
  if (sku) {
    const hit = ITEMS.find((x) => x.sku === String(sku));
    if (!hit) {
      res.status(404).json({ error: "not_found", sku });
      return;
    }
    res.status(200).json({ item: hit });
    return;
  }
  res.status(200).json({
    shop: "Demo Kiryana (mock merchant)",
    currency: "PKR",
    items: ITEMS,
  });
}
