#!/usr/bin/env python3
"""Landed cost calculator for Days Like These.

Deterministic. No network calls. Prices come from the cached price book
(vendors.json), which is refreshed by the lookup procedure in SKILL.md.

Usage:
    python3 landed_cost.py project.json
    python3 landed_cost.py --check-prices     # staleness report only

See examples/ for input files. Schema documented in SKILL.md.
"""

import datetime as dt
import json
import math
import os
import sys

DEFAULT_WASTE = 0.10
DEFAULT_MULTIPLIER = 2.5
SMALL_RUN_THRESHOLD = 6

BOOK_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendors.json")


def money(x):
    return f"${x:,.2f}"


def load_book(path=BOOK_PATH):
    with open(path) as f:
        return json.load(f)


def days_old(datestr, today=None):
    today = today or dt.date.today()
    return (today - dt.date.fromisoformat(datestr)).days


def staleness_warnings(book, today=None):
    """Every dated price in the book, flagged if older than the threshold."""
    limit = book.get("staleness_warn_days", 30)
    warnings = []

    def check(entry, label, vendor_name):
        fetched = entry.get("fetched")
        if not fetched:
            warnings.append(f"{vendor_name} / {label}: NO fetch date recorded")
            return
        age = days_old(fetched, today)
        if age > limit:
            warnings.append(
                f"{vendor_name} / {label}: price is {age} days old "
                f"(fetched {fetched}, limit {limit})"
            )

    for vendor in book["vendors"].values():
        name = vendor["name"]
        for sheet in vendor.get("gang_sheets", []):
            check(sheet, sheet["sku"], name)
        for blank in vendor.get("blanks", []):
            check(blank, blank["sku"], name)
        if "individual_transfers" in vendor:
            check(vendor["individual_transfers"], "individual transfers", name)

    return warnings


def find_sku(book, sku):
    """Locate a SKU anywhere in the price book. Returns (entry, vendor_name, kind)."""
    for vendor in book["vendors"].values():
        for sheet in vendor.get("gang_sheets", []):
            if sheet["sku"] == sku:
                return sheet, vendor["name"], "gang_sheet"
        for blank in vendor.get("blanks", []):
            if blank["sku"] == sku:
                return blank, vendor["name"], "blank"
    raise KeyError(f"SKU '{sku}' not found in the price book")


def transfer_unit_price(book, vendor_key, size_label, quantity):
    """Price per individual pre-printed transfer at a given order quantity."""
    it = book["vendors"][vendor_key]["individual_transfers"]
    size = next((s for s in it["sizes"] if s["label"] == size_label), None)
    if size is None:
        available = ", ".join(s["label"] for s in it["sizes"])
        raise KeyError(f"transfer size '{size_label}' not in book. Have: {available}")

    discount = 0.0
    for tier in it["quantity_tiers"]:
        hi = tier["max"]
        if quantity >= tier["min"] and (hi is None or quantity <= hi):
            discount = tier["discount"]
            break
    return size["price_1_14"] * (1 - discount), discount


def designs_per_sheet(sheet, design_w, design_h):
    """Conservative grid packing. Their nesting tool may fit more; this errs high on cost."""
    def grid(sw, sh, dw, dh):
        return int(sw // dw) * int(sh // dh)
    # Try the design both ways round; take the better fit.
    a = grid(sheet["width_in"], sheet["height_in"], design_w, design_h)
    b = grid(sheet["width_in"], sheet["height_in"], design_h, design_w)
    return max(a, b)


def transfer_route_analysis(book, design, count):
    """Compare gang sheets against individual transfers for the same design need."""
    dw, dh = design["width_in"], design["height_in"]
    routes = []

    ninja = book["vendors"]["ninja_transfers"]
    for sheet in ninja.get("gang_sheets", []):
        per = designs_per_sheet(sheet, dw, dh)
        if per < 1:
            continue
        sheets = math.ceil(count / per)
        total = sheets * sheet["price"]
        routes.append({
            "label": f"{sheet['label']} x{sheets}",
            "total": total,
            "per_design": total / count,
            "note": f"fits {per} per sheet at {dw}\"x{dh}\" (conservative grid packing)",
            "confidence": sheet.get("confidence", "ok"),
        })

    it = ninja.get("individual_transfers", {})
    for size in it.get("sizes", []):
        if size["width_in"] >= dw and size["height_in"] >= dh:
            unit, disc = transfer_unit_price(book, "ninja_transfers", size["label"], count)
            total = unit * count
            routes.append({
                "label": f"Individual {size['label']} transfers x{count}",
                "total": total,
                "per_design": unit,
                "note": f"{int(disc * 100)}% quantity discount applied",
                "confidence": "ok",
            })

    routes.sort(key=lambda r: r["total"])
    return routes


def resolve_item(item, book):
    """Normalize one line item into materials/shipping/units, from book or manual entry."""
    shipping = item.get("shipping", 0.0)

    if "sku" in item:
        entry, vendor_name, kind = find_sku(book, item["sku"])
        packs = item.get("packs", 1)
        if kind == "gang_sheet":
            return {
                "label": entry["label"],
                "vendor": vendor_name,
                "materials": packs * entry["price"],
                "shipping": shipping,
                "units": None,
                "source": f"book · fetched {entry['fetched']}",
            }
        return {
            "label": entry["label"],
            "vendor": vendor_name,
            "materials": packs * entry["pack_price"],
            "shipping": shipping,
            "units": packs * entry.get("units_per_pack", 1),
            "source": f"book · fetched {entry['fetched']}",
        }

    if "transfer_size" in item:
        qty = item["quantity"]
        unit, disc = transfer_unit_price(
            book, item.get("vendor_key", "ninja_transfers"), item["transfer_size"], qty
        )
        return {
            "label": f"{item['transfer_size']} individual transfers",
            "vendor": book["vendors"][item.get("vendor_key", "ninja_transfers")]["name"],
            "materials": unit * qty,
            "shipping": shipping,
            "units": qty,
            "source": f"book · {int(disc * 100)}% qty discount",
        }

    packs = item["packs"]
    return {
        "label": item["label"],
        "vendor": item.get("vendor", "—"),
        "materials": packs * item["pack_price"],
        "shipping": shipping,
        "units": packs * item.get("units_per_pack", 1),
        "source": "manual entry",
    }


def price_option(option, quantity, waste, multiplier, book):
    lines = [resolve_item(i, book) for i in option.get("items", [])]

    for flat in option.get("flat_costs", []):
        lines.append({
            "label": flat["label"],
            "vendor": flat.get("vendor", "—"),
            "materials": flat["amount"],
            "shipping": 0.0,
            "units": None,
            "source": "manual entry",
        })

    materials = sum(l["materials"] for l in lines)
    shipping = sum(l["shipping"] for l in lines)
    total_landed = materials + shipping

    per_unit = total_landed / quantity
    per_unit_waste = per_unit * (1 + waste)
    floor_raw = per_unit_waste * multiplier
    floor = math.ceil(floor_raw)

    leftovers = {
        l["label"]: l["units"] - quantity
        for l in lines
        if l["units"] is not None and l["units"] > quantity
    }

    return {
        "name": option.get("name", "unnamed"),
        "lines": lines,
        "materials": materials,
        "shipping": shipping,
        "total_landed": total_landed,
        "per_unit": per_unit,
        "per_unit_waste": per_unit_waste,
        "floor_raw": floor_raw,
        "floor": floor,
        "run_revenue": floor * quantity,
        "run_margin": (floor * quantity) - total_landed,
        "margin_pct": 1 - (per_unit_waste / floor) if floor else 0.0,
        "leftovers": leftovers,
    }


def report(project, book):
    quantity = project["quantity"]
    waste = project.get("waste_allowance", DEFAULT_WASTE)
    multiplier = project.get("multiplier", DEFAULT_MULTIPLIER)

    if quantity <= 0:
        raise ValueError("quantity must be greater than zero")
    if not project.get("options"):
        raise ValueError("project needs at least one sourcing option")

    results = sorted(
        (price_option(o, quantity, waste, multiplier, book)
         for o in project["options"]),
        key=lambda r: r["total_landed"],
    )

    out = []
    out.append(f"LANDED COST — {project.get('project', 'untitled')}")
    out.append(f"{quantity} units · {int(waste * 100)}% waste allowance · {multiplier}x floor")
    out.append(f"price book refreshed {book.get('refreshed', 'unknown')}")
    out.append("")

    stale = staleness_warnings(book)
    if stale:
        out.append("!! STALE PRICES — re-run the lookup before quoting:")
        for w in stale:
            out.append(f"   {w}")
        out.append("")

    for rank, r in enumerate(results, 1):
        marker = "  ← cheapest" if rank == 1 else ""
        out.append(f"[{rank}] {r['name']}{marker}")
        for line in r["lines"]:
            unit_note = f" · {line['units']} units" if line["units"] else " · flat"
            ship_note = f" + {money(line['shipping'])} ship" if line["shipping"] else ""
            out.append(f"      {line['label']} ({line['vendor']}): "
                       f"{money(line['materials'])}{ship_note}{unit_note}")
            out.append(f"        └ {line['source']}")
        out.append(f"      materials {money(r['materials'])} · shipping {money(r['shipping'])}")
        out.append(f"      total landed        {money(r['total_landed'])}")
        out.append(f"      landed per unit     {money(r['per_unit'])}")
        out.append(f"      + waste             {money(r['per_unit_waste'])}")
        out.append(f"      PRICE FLOOR         {money(r['floor'])}  (raw {money(r['floor_raw'])})")
        out.append(f"      at floor: {money(r['run_revenue'])} in, "
                   f"{money(r['run_margin'])} margin, {r['margin_pct'] * 100:.0f}% gross")
        for label, extra in r["leftovers"].items():
            out.append(f"      NOTE: {extra} leftover {label} — paid for, not in this run")
        out.append("")

    if len(results) > 1:
        best, second = results[0], results[1]
        delta = second["total_landed"] - best["total_landed"]
        out.append(f"Cheapest option saves {money(delta)} on the run "
                   f"({money(delta / quantity)} per unit) vs next best.")
        out.append("")

    design = project.get("design")
    if design:
        count = design.get("count", quantity)
        out.append(f"TRANSFER ROUTES for {design['width_in']}\"x{design['height_in']}\" "
                   f"x{count} designs:")
        for route in transfer_route_analysis(book, design, count):
            flag = "  [low confidence]" if route["confidence"] == "low" else ""
            out.append(f"   {money(route['total']):>10}  "
                       f"({money(route['per_design'])}/design)  {route['label']}{flag}")
            out.append(f"               {route['note']}")
        out.append("")

    if quantity < SMALL_RUN_THRESHOLD:
        out.append(f"SMALL RUN WARNING: {quantity} units. Setup time does not shrink "
                   f"with the run, so a {multiplier}x multiplier is thin cover for your "
                   f"labor here. Consider a setup fee on top of the floor.")
        out.append("")

    best = results[0]
    out.append("For the sales tracker:")
    out.append(f"  cost of goods (this run): {money(best['total_landed'])}")
    out.append(f"  minimum price per unit:   {money(best['floor'])}")
    out.append("")
    out.append("The floor is the floor. It is not the price. Charge above it.")

    return "\n".join(out)


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 1

    book = load_book()

    if sys.argv[1] == "--check-prices":
        stale = staleness_warnings(book)
        print(f"Price book refreshed {book.get('refreshed', 'unknown')}")
        if stale:
            print("STALE:")
            for w in stale:
                print(f"  {w}")
            return 1
        print("All prices within the freshness limit.")
        return 0

    try:
        with open(sys.argv[1]) as f:
            project = json.load(f)
        print(report(project, book))
    except (ValueError, KeyError) as e:
        print(f"Input problem: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
