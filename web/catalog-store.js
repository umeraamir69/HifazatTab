/**
 * Shared catalog source for the live agent + owner dashboard.
 *
 * Priority (highest first):
 *   1. Connected merchant API snapshot (localStorage hifazat_api_catalog)
 *   2. Local dashboard edits overlay (hifazat_local_edits)
 *   3. Bundled demo shop_catalog.json
 *
 * Tools stay the same — only the data source changes.
 */
(function (root) {
  "use strict";
  var KEY_API = "hifazat_api_catalog";
  var KEY_EDITS = "hifazat_local_edits";
  var KEY_CONN = "hifazat_connector";
  var KEY_SOURCE = "hifazat_source"; // "demo" | "api" | "edited"

  function read(key) {
    try {
      var raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : null;
    } catch (e) {
      return null;
    }
  }

  function write(key, val) {
    localStorage.setItem(key, JSON.stringify(val));
  }

  function clear(key) {
    localStorage.removeItem(key);
  }

  function deepClone(o) {
    return JSON.parse(JSON.stringify(o));
  }

  function applyEdits(base, edits) {
    if (!edits || !edits.catalog) return base;
    var out = deepClone(base);
    out.catalog = out.catalog || {};
    Object.keys(edits.catalog).forEach(function (k) {
      var e = edits.catalog[k];
      if (e === null) {
        delete out.catalog[k];
        if (out.aliases) delete out.aliases[k];
        return;
      }
      out.catalog[k] = Object.assign({}, out.catalog[k] || {}, e);
      if (!out.aliases) out.aliases = {};
      if (!out.aliases[k]) {
        out.aliases[k] = [k, k.replace(/_/g, " ")];
      }
    });
    return out;
  }

  function stats(data) {
    var cat = (data && data.catalog) || {};
    var keys = Object.keys(cat);
    var low = 0, sumStock = 0, value = 0;
    keys.forEach(function (k) {
      var s = Number(cat[k].stock) || 0;
      var p = Number(cat[k].price) || 0;
      if (s <= 20) low++;
      sumStock += s;
      value += p * s;
    });
    var cats = {};
    keys.forEach(function (k) {
      var c = cat[k].category || "general";
      cats[c] = (cats[c] || 0) + 1;
    });
    return {
      skus: keys.length,
      lowStock: low,
      units: sumStock,
      inventoryValuePkr: value,
      categories: cats,
    };
  }

  /**
   * Resolve active catalog. Pass bundled demo as fallback.
   */
  function resolve(demoData) {
    var source = localStorage.getItem(KEY_SOURCE) || "demo";
    var base = demoData || { catalog: {}, aliases: {} };
    if (source === "api") {
      var api = read(KEY_API);
      if (api && api.catalog) base = api;
    }
    var edits = read(KEY_EDITS);
    var merged = applyEdits(base, edits);
    var hasEdits = !!(edits && edits.catalog && Object.keys(edits.catalog).length);
    return {
      data: merged,
      source: source,
      hasEdits: hasEdits,
      connector: read(KEY_CONN),
      stats: stats(merged),
    };
  }

  function setSource(src) {
    localStorage.setItem(KEY_SOURCE, src);
  }

  function saveApiCatalog(payload, connector) {
    write(KEY_API, {
      catalog: payload.catalog,
      aliases: payload.aliases || {},
      syncedAt: new Date().toISOString(),
      source: payload.source || null,
      count: payload.count || Object.keys(payload.catalog || {}).length,
    });
    if (connector) write(KEY_CONN, connector);
    setSource("api");
  }

  function saveEdit(sku, patch) {
    var edits = read(KEY_EDITS) || { catalog: {} };
    edits.catalog = edits.catalog || {};
    if (patch === null) {
      edits.catalog[sku] = null;
    } else {
      edits.catalog[sku] = Object.assign({}, edits.catalog[sku] || {}, patch);
    }
    edits.updatedAt = new Date().toISOString();
    write(KEY_EDITS, edits);
  }

  function clearEdits() {
    clear(KEY_EDITS);
  }

  function clearApi() {
    clear(KEY_API);
    setSource("demo");
  }

  function exportCsv(data) {
    var cat = (data && data.catalog) || {};
    var lines = ["item,price_pkr,stock,category"];
    Object.keys(cat).sort().forEach(function (k) {
      var r = cat[k];
      lines.push([k, r.price, r.stock, r.category || ""].join(","));
    });
    return lines.join("\n");
  }

  root.HifazatStore = {
    KEY_API: KEY_API,
    KEY_EDITS: KEY_EDITS,
    KEY_CONN: KEY_CONN,
    resolve: resolve,
    setSource: setSource,
    saveApiCatalog: saveApiCatalog,
    saveEdit: saveEdit,
    clearEdits: clearEdits,
    clearApi: clearApi,
    exportCsv: exportCsv,
    stats: stats,
    readConnector: function () { return read(KEY_CONN); },
    readApi: function () { return read(KEY_API); },
    readEdits: function () { return read(KEY_EDITS); },
  };
})(typeof window !== "undefined" ? window : globalThis);
