#!/usr/bin/env python3
"""Landed cost calculator for Days Like These.

Deterministic. No AI, no network. You supply vendor prices, it returns
landed cost per unit and the price floor.

Usage:
    python3 landed_cost.py project.json

See examples/ for input files. Schema documented in SKILL.md.
"""

import json
import math
import sys

DEFAULT_WASTE = 0.10
DEFAULT_MULTIPLIER = 2.5

# Below this many units, a flat multiplier stops covering labor in any
# meaningful way, because setup time does not shrink with the run.
SMALL_RUN_THRESHOLD = 6


def money(x):
    return f"${x:,.2f}"


def price_option(option, quantity, waste, multiplier):
    """Compute landed cost and price floor for one sourcing option."""
    materials = 0.0
    shipping = 0.0
    units_bought = {}
    lines = []

    for item in option.get("items", []):
        packs = item["packs"]
        pack_price = item["pack_price"]
        per_pack = item.get("units_per_pack", 1)
        ship = item.get("shipping", 0.0)

        line_materials = packs * pack_price
        materials += line_materials
        shipping += ship

        bought = packs * per_pack
        units_bought[item["label"]] = bought
        lines.append({
            "label": item["label"],
            "vendor": item.get("vendor", "—"),
            "materials": line_materials,
            "shipping": ship,
            "units": bought,
        })

    flats = 0.0
    for flat in option.get("flat_costs", []):
        flats += flat["amount"]
        lines.append({
            "label": flat["label"],
            "vendor": flat.get("vendor", "—"),
            "materials": flat["amount"],
            "shipping": 0.0,
            "units": None,
        })

    total_landed = materials + shipping + flats
    per_unit = total_landed / quantity
    per_unit_waste = per_unit * (1 + waste)
    floor_raw = per_unit_waste * multiplier
    floor = math.ceil(floor_raw)

    # Leftover stock you paid for but are not selling in this run.
    leftovers = {
        label: bought - quantity
        for label, bought in units_bought.items()
        if bought > quantity
    }

    return {
        "name": option.get("name", "unnamed"),
        "lines": lines,
        "materials": materials,
        "shipping": shipping,
        "flats": flats,
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


def report(project):
    quantity = project["quantity"]
    waste = project.get("waste_allowance", DEFAULT_WASTE)
    multiplier = project.get("multiplier", DEFAULT_MULTIPLIER)

    if quantity <= 0:
        raise ValueError("quantity must be greater than zero")
    if not project.get("options"):
        raise ValueError("project needs at least one sourcing option")

    results = [
        price_option(o, quantity, waste, multiplier)
        for o in project["options"]
    ]
    results.sort(key=lambda r: r["total_landed"])

    out = []
    out.append(f"LANDED COST — {project.get('project', 'untitled')}")
    out.append(f"{quantity} units · {int(waste * 100)}% waste allowance · {multiplier}x floor")
    out.append("")

    for rank, r in enumerate(results, 1):
        marker = "  ← cheapest" if rank == 1 else ""
        out.append(f"[{rank}] {r['name']}{marker}")
        for line in r["lines"]:
            unit_note = f" · {line['units']} units" if line["units"] else " · flat"
            ship_note = f" + {money(line['shipping'])} ship" if line["shipping"] else ""
            out.append(
                f"      {line['label']} ({line['vendor']}): "
                f"{money(line['materials'])}{ship_note}{unit_note}"
            )
        out.append(f"      materials {money(r['materials'])} · "
                   f"shipping {money(r['shipping'])} · flats {money(r['flats'])}")
        out.append(f"      total landed        {money(r['total_landed'])}")
        out.append(f"      landed per unit     {money(r['per_unit'])}")
        out.append(f"      + waste             {money(r['per_unit_waste'])}")
        out.append(f"      PRICE FLOOR         {money(r['floor'])}  "
                   f"(raw {money(r['floor_raw'])})")
        out.append(f"      at floor: {money(r['run_revenue'])} in, "
                   f"{money(r['run_margin'])} margin, "
                   f"{r['margin_pct'] * 100:.0f}% gross")
        for label, extra in r["leftovers"].items():
            out.append(f"      NOTE: {extra} leftover {label} — paid for, not in this run")
        out.append("")

    if len(results) > 1:
        best, second = results[0], results[1]
        delta = second["total_landed"] - best["total_landed"]
        out.append(f"Cheapest option saves {money(delta)} on the run "
                   f"({money(delta / quantity)} per unit) vs next best.")
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
    try:
        with open(sys.argv[1]) as f:
            project = json.load(f)
        print(report(project))
    except (ValueError, KeyError) as e:
        print(f"Input problem: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
