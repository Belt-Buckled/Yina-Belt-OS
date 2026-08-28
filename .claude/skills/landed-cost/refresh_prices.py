#!/usr/bin/env python3
"""Refresh the landed-cost price book from live vendor sources.

Deterministic fetch and parse. No AI. Never fabricates a price: if a source
fails, the existing entry is left untouched with its original fetch date and
the failure is reported.

Sources:
  Ninja Transfers — Shopify products.json (structured, public)
  Jiffy           — product page DOM, size/price grid in data- attributes
                    (robots.txt permits product pages; /api and /cart are not touched)

Usage:
    python3 refresh_prices.py            # fetch, show diff, write
    python3 refresh_prices.py --dry-run  # fetch, show diff, write nothing
"""

import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK_PATH = os.path.join(HERE, "vendors.json")

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
TIMEOUT = 30

JIFFY_PRODUCTS = {
    "gildan_5000": {
        "url": "https://www.jiffy.com/gildan-G500.html",
        "label": "Gildan G500 / 5000 heavy cotton tee",
        "catalog": "G500",
    },
}

NINJA_PRODUCTS_JSON = "https://ninjatransfers.com/products.json?limit=250"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read().decode("utf-8", errors="replace")


def parse_jiffy_sizes(html):
    """Extract the size -> price ladder from a Jiffy product page."""
    rows = re.findall(
        r'data-active-color="([^"]+)"\s+data-size="([^"]+)"\s+'
        r'data-variant-id="(\d+)"[^>]*data-amount="([\d.]+)"',
        html,
    )
    sizes, color = {}, None
    for c, size, _vid, amount in rows:
        color = color or c
        sizes[size] = float(amount)
    return sizes, color


def parse_jiffy_colors(html):
    """Extract the color -> starting price list."""
    pairs = re.findall(
        r'data-composition-name="([^"]+)"\s*>\s*<!--\s*\$?([\d.]+)\s*-->', html
    )
    return {c: float(p) for c, p in pairs}


def refresh_jiffy(book, today, problems):
    vendor = book["vendors"]["jiffy"]
    changes = []

    for sku, cfg in JIFFY_PRODUCTS.items():
        try:
            html = fetch(cfg["url"])
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
            problems.append(f"Jiffy {sku}: fetch failed ({e}). Kept the existing price.")
            continue

        sizes, color = parse_jiffy_sizes(html)
        colors = parse_jiffy_colors(html)

        if not sizes:
            problems.append(
                f"Jiffy {sku}: page fetched but no size grid found. The page layout "
                f"probably changed. Kept the existing price — DO NOT trust this SKU "
                f"until the parser is fixed."
            )
            continue

        existing = next((b for b in vendor.get("blanks", []) if b["sku"] == sku), None)
        old_sizes = (existing or {}).get("sizes", {})

        for size, price in sorted(sizes.items()):
            old = old_sizes.get(size)
            if old is None:
                changes.append(f"  NEW  jiffy/{sku} {size}: ${price:.2f}")
            elif abs(old - price) > 0.001:
                arrow = "UP" if price > old else "DOWN"
                changes.append(f"  {arrow:<4} jiffy/{sku} {size}: ${old:.2f} -> ${price:.2f}")

        entry = {
            "sku": sku,
            "label": cfg["label"],
            "catalog": cfg["catalog"],
            "priced_color": color,
            "sizes": sizes,
            "colors_available": len(colors),
            "color_base_price": min(colors.values()) if colors else None,
            "source": cfg["url"],
            "fetched": today,
        }
        vendor["blanks"] = [b for b in vendor.get("blanks", []) if b["sku"] != sku]
        vendor["blanks"].append(entry)

    vendor["auto_refreshable"] = True
    vendor["fetched"] = today
    return changes


def refresh_ninja(book, today, problems):
    vendor = book["vendors"]["ninja_transfers"]
    changes = []

    try:
        data = json.loads(fetch(NINJA_PRODUCTS_JSON))
    except (urllib.error.URLError, urllib.error.HTTPError, OSError, ValueError) as e:
        problems.append(f"Ninja: products.json fetch failed ({e}). Kept existing prices.")
        return changes

    products = data.get("products", [])
    if not products:
        problems.append("Ninja: products.json returned no products. Kept existing prices.")
        return changes

    blanks = []
    for p in products:
        title = p.get("title", "")
        variants = [v for v in p.get("variants", []) if v.get("price")]
        if not variants:
            continue
        prices = [float(v["price"]) for v in variants]
        blanks.append({
            "handle": p.get("handle"),
            "label": title,
            "price_min": min(prices),
            "price_max": max(prices),
            "variants": len(variants),
            "in_stock": sum(1 for v in p.get("variants", []) if v.get("available")),
        })

    old = {b["handle"]: b for b in vendor.get("blank_catalog", [])}
    for b in blanks:
        prev = old.get(b["handle"])
        if prev is None:
            continue
        if abs(prev.get("price_min", 0) - b["price_min"]) > 0.001:
            arrow = "UP" if b["price_min"] > prev["price_min"] else "DOWN"
            changes.append(
                f"  {arrow:<4} ninja/{b['handle']}: "
                f"${prev['price_min']:.2f} -> ${b['price_min']:.2f}"
            )

    if not old and blanks:
        changes.append(f"  NEW  ninja blank catalog: {len(blanks)} products indexed")

    vendor["blank_catalog"] = sorted(blanks, key=lambda b: b["price_min"])
    vendor["blank_catalog_fetched"] = today
    vendor["fetched"] = today
    vendor.setdefault("notes", "")
    return changes


def main():
    dry = "--dry-run" in sys.argv
    today = dt.date.today().isoformat()

    with open(BOOK_PATH) as f:
        book = json.load(f)

    problems = []
    changes = []
    changes += refresh_jiffy(book, today, problems)
    changes += refresh_ninja(book, today, problems)

    print(f"PRICE REFRESH — {today}")
    print()

    if changes:
        print("Changed:")
        for c in changes:
            print(c)
    else:
        print("No price changes. (Signal: nothing moved.)")
    print()

    if problems:
        print("PROBLEMS — these prices were NOT updated and keep their old dates:")
        for p in problems:
            print(f"  {p}")
        print()

    if dry:
        print("--dry-run: nothing written.")
        return 1 if problems else 0

    book["refreshed"] = today
    with open(BOOK_PATH, "w") as f:
        json.dump(book, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Wrote {BOOK_PATH}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
