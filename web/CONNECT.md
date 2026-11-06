# Connect your shop API

HifazatTab’s **tools stay fixed**. You only change where price/stock/category come from.

## Sources (priority)

1. **Connected API** — dashboard → Connect API → Fetch & activate  
2. **Local edits** — dashboard inventory row Save (browser overlay)  
3. **Demo catalog** — bundled `shop_catalog.json` (~219 SKUs)

## Quick test (no backend)

1. Open `/dashboard.html` → **Connect API**  
2. Click **Fill mock merchant**  
3. **Fetch & activate**  
4. Ask the live agent: `olive oil 500ml details`

Mock endpoint: `GET /api/mock-merchant`  
Proxy: `POST /api/catalog-proxy`

## Your API contract

Return JSON with an items array (path configurable):

```json
{
  "items": [
    {
      "sku": "atta_20kg",
      "price_pkr": 2850,
      "quantity": 40,
      "aisle": "staples",
      "name": "Atta 20kg"
    }
  ]
}
```

Map any field names in the dashboard (`sku` / `price` / `stock` / `category`).

Auth: optional header + value (e.g. `Authorization: Bearer …`).  
Demo stores the secret in **localStorage** — for production put keys in Vercel env / a vault and call the proxy from a trusted path.

## Agent tools (unchanged)

| Tool | Arg |
|------|-----|
| `lookup_price` | item key |
| `check_stock` | item key |
| `item_details` | item key |
| `list_category` | category |
| `list_low_stock` | threshold |
| `loan_eligibility` | monthly income PKR |
