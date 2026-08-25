---
name: landed-cost
description: Compute landed cost per unit and the price floor for a Days Like These production run. Use when quoting a job, comparing vendors, deciding whether a price is high enough, or answering "what does this actually cost me". Trigger on "landed cost", "what should I charge", "price this", "quote this", "compare vendors", "is this price too low", "cost per shirt", "price floor", "am I making money on this".
bike-method-phase: 1  # Phase 1 — Training wheels. Run manually first.
three-ms-attribution: |
  Adapted from The Three Ms of AI™ © 2026 Nate Herk.
autonomy-level: L1  # Suggested. Yina supplies every price. Yina picks the vendor.
kpi-bucket: less cost
kpi-metric: gross margin per unit ≥ 60%; new project to quotable number in under 5 minutes
---

# Landed Cost

Turns vendor prices into one number you can quote from. Deterministic arithmetic, no AI in the
calculation, no network calls. It cannot look prices up. You supply them.

**Why this exists:** the first real project netted a $100 loss because cost was never settled before
the work was quoted. Sourcing and pricing are the same problem. This closes it.

## Autonomy level: L1

This skill computes and ranks. It does not choose a vendor, does not fetch a price, and does not set
a final price. Every number in comes from Yina. The decision stays with Yina.

Do not advance this to L2 or higher until it has been run manually on at least three real projects
and the numbers have been checked by hand at least once.

## How to run it

1. Copy `examples/template.json` to a new file for the project.
2. Fill in the real prices from the vendor sites. Every price is a live lookup — Ninja Transfers,
   Jiffy, Gildan blanks. Write down what you see, including shipping.
3. Run it:

```bash
python3 .claude/skills/landed-cost/landed_cost.py path/to/project.json
```

## The math it applies

| Step | Rule |
|---|---|
| Materials | packs × pack price, per line |
| Shipping | added whole, per line, not per unit |
| Flat costs | outsourced prints and one-offs, added whole |
| Landed per unit | total landed ÷ quantity in the run |
| Waste | +10% on landed per unit (misprints, bad presses) |
| Price floor | landed-with-waste × 2.5, rounded up to the next whole dollar |

**2.5x and 10% are the standing defaults**, set 2026-08-23. Override per project with
`multiplier` and `waste_allowance` in the JSON.

## What it flags

- **Cheapest option**, ranked, with the dollar delta against the next best.
- **Leftover stock** — when pack sizes force you to buy more units than the run needs. That money is
  spent whether or not it ships. The calculator names the number so it is not invisible.
- **Small run warning** — under 6 units, setup time does not shrink with the run, so 2.5x is thin
  cover for labor. Consider a setup fee on top of the floor.
- **Cost of goods** for the run, formatted to drop straight into the sales tracker when that exists.

## The honest limit

**2.5x does not pay you for your time. It pays for materials, shipping, and misprints, and leaves a
margin. Your labor lives inside that margin, not on top of it.** On a twelve-shirt run that is fine.
On a two-piece custom job it may still lose money per hour. That is why the small-run warning exists.

If you want labor priced explicitly, switch to `multiplier: 1.0` and add your press time as a
`flat_cost` line at your hourly rate. The skill supports it. It is more accurate and more typing.

## Input schema

```json
{
  "project": "name",
  "quantity": 12,
  "waste_allowance": 0.10,
  "multiplier": 2.5,
  "options": [
    {
      "name": "sourcing option name",
      "items": [
        {
          "label": "what it is",
          "vendor": "who sells it",
          "pack_price": 9.91,
          "units_per_pack": 2,
          "packs": 7,
          "shipping": 8.99
        }
      ],
      "flat_costs": [
        { "label": "outsourced print", "vendor": "who", "amount": 18.00 }
      ]
    }
  ]
}
```

`options` is a list so you can compare vendors in one run. One option is fine.
`units_per_pack` is 1 for anything sold singly. `flat_costs` may be omitted.

## Examples

- `examples/template.json` — blank to copy.
- `examples/two-vendor-comparison.json` — shows the comparison output. **The prices in it are
  invented.** It demonstrates the shape, not real vendor pricing.
- `examples/concert-shirt-hindsight.json` — the real numbers from the first project: $9.91 two-pack
  of Gildan blacks, $32.63 in transfers. The outsourced 5X print is set to `0.00` because that cost
  was never recorded. **Fill it in if you find the receipt** — it is the missing piece of the $100.

## What it does not do

- Look up prices. Live lookups stay manual until a vendor connection is wired.
- Track sales. That is a separate, unbuilt thing — the measurement surface for the $1,000.
- Decide a final price. It gives you the floor. The floor is not the price.

---

> *Adapted from The Three Ms of AI™. © 2026 Nate Herk. All rights reserved.*
> *The Three Ms of AI™ is a trademark of Nate Herk.*
