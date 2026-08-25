---
name: landed-cost
description: Look up current vendor prices, compute landed cost per unit, and return a price floor for a Days Like These production run. Also compares gang sheets against individual transfers. Use when quoting a job, comparing vendors, deciding whether a price is high enough, or answering "what does this actually cost me". Trigger on "landed cost", "what should I charge", "price this", "quote this", "compare vendors", "refresh prices", "check vendor prices", "is this price too low", "cost per shirt", "price floor", "gang sheet", "am I making money on this".
bike-method-phase: 1  # Phase 1 — Training wheels. Review every refreshed price.
three-ms-attribution: |
  Adapted from The Three Ms of AI™ © 2026 Nate Herk.
autonomy-level: L2  # Drafted. Lookups are automated; Yina reviews prices and picks the vendor.
kpi-bucket: less cost
kpi-metric: gross margin per unit ≥ 60%; new project to quotable number in under 5 minutes
---

# Landed Cost

Turns current vendor prices into one number you can quote from.

Two layers, deliberately separated:

- **The lookup** fetches live vendor prices into a cached price book. Automated, reviewable.
- **The math** reads the price book and computes. Pure arithmetic, no network, no AI.

**Why this exists:** the first real project netted a $100 loss because cost was never settled before
the work was quoted. Sourcing and pricing are the same problem. This closes it.

## Autonomy level: L2

The lookup drafts prices. **Yina reviews them and picks the vendor.** The arithmetic is deterministic
and never guesses. Nothing is auto-purchased and no final price is ever set by this skill.

Do not advance past L2. The failure mode that matters here is a wrong price entering a quote
silently, which is the original $100 loss with extra steps.

## Two ways to run it

### Price a project

```bash
python3 .claude/skills/landed-cost/landed_cost.py path/to/project.json
```

Copy `examples/template.json`, name the SKUs, run it. You no longer type prices for anything in the
price book.

### Refresh the price book

Say "refresh prices" or "check vendor prices". Run `--check-prices` first to see what is stale:

```bash
python3 .claude/skills/landed-cost/landed_cost.py --check-prices
```

## The lookup procedure

Run the fetcher. It is deterministic Python — it parses structured data, it does not guess.

```bash
python3 .claude/skills/landed-cost/refresh_prices.py --dry-run   # show the diff, write nothing
python3 .claude/skills/landed-cost/refresh_prices.py             # fetch and write
```

It prints **only what changed** — prices that moved, with old and new. Prices that held are noise and
are collapsed to one line. Then it writes `vendors.json` with fresh `fetched` dates.

### Where the prices come from

| Vendor | Source | What it yields |
|---|---|---|
| Ninja Transfers | Shopify `products.json` | full blank catalog, per-variant prices, stock counts |
| Jiffy | product page DOM (`data-size` / `data-amount`) | the full size ladder per style |

Both are structured data, not scraped prose. Ninja publishes a standard Shopify products endpoint.
Jiffy embeds the size/price grid in `data-` attributes on the product page.

**robots.txt is respected.** Jiffy disallows `/api`, `/cart`, `/checkout`, `/account` and similar —
none of which this touches. Product pages are permitted. Do not point the fetcher at a disallowed
path.

### It never fabricates a price

- A failed fetch leaves the existing entry **untouched, with its original date**, and reports the
  failure. Stale-and-labelled is safe. Invented is not.
- If a page is fetched but the expected structure is missing, the parser says the layout changed and
  refuses to update that SKU rather than writing a wrong number.
- Conflicting published sources are recorded and flagged, never averaged. Live example: Ninja's tier
  table says 250+ is 50% off while their cost page implies ~65%. The calculator uses the
  conservative number, producing a higher cost and a safer floor.
- Exit code is non-zero when any source had a problem, so it fails loudly.

## Size-aware pricing — the thing that bit the concert shirt

Blank cost is not flat across sizes. Live from Jiffy, Gildan G500:

| Size | S | M / L / XL | 2XL | 3XL | 4XL / 5XL |
|---|---|---|---|---|---|
| Price | $1.86 | $2.79 | $5.38 | **$7.17** | **$7.50** |

**A 5XL costs four times what a small costs.** The concert shirt was a 3X and a 5X — the two most
expensive rows. Quoting one flat price per shirt regardless of size silently destroys margin on
exactly the orders that feel like wins.

Price a run by its real size mix:

```json
{ "sku": "gildan_5000", "sizes": { "3XL": 1, "5XL": 1 }, "shipping": 8.99 }
```

The report shows the per-size breakdown on the line, so you can see where the cost actually sits.

## The math it applies

| Step | Rule |
|---|---|
| Materials | packs × price, per line, from the book or entered manually |
| Shipping | added whole, per line, not per unit |
| Flat costs | outsourced prints and one-offs, added whole |
| Landed per unit | total landed ÷ quantity in the run |
| Waste | +10% on landed per unit (misprints, bad presses) |
| Price floor | landed-with-waste × 2.5, rounded up to the next whole dollar |

**2.5x and 10% are the standing defaults**, set 2026-08-23. Override per project with `multiplier`
and `waste_allowance`.

## What it flags

- **Every price's provenance.** Each line prints where its number came from and when it was fetched.
- **Stale prices**, loudly, at the top of the report. Older than 30 days triggers it.
- **Cheapest option**, ranked, with the dollar delta against the next best.
- **Transfer routes** — gang sheet versus individual transfers for the same design, ranked by cost
  per design. This is usually the largest single saving available.
- **Leftover stock** when pack sizes force over-buying. That money is spent whether or not it ships.
- **Small run warning** under 6 units, where 2.5x is thin cover for setup labor.
- **Cost of goods** for the run, formatted for the sales tracker.

## Gang sheets are the lever

Add a `design` block to any project and the report compares routes:

```json
"design": { "width_in": 5, "height_in": 5, "count": 12 }
```

For twelve 5"×5" designs: a $35.00 gang sheet holds 16 of them at **$2.92 per design**, against
**$4.00** each buying individual 5×5 transfers. The gap widens fast with volume.

For context, the concert shirt used **$32.63 in transfers for two shirts**. A $35.00 gang sheet costs
about the same and fits roughly thirty small designs.

Fit is computed by **conservative grid packing** — straight rows and columns, best of both
orientations. Ninja's own nesting tool will often fit more, so the real cost is usually a little
lower than quoted here. The calculator errs toward overestimating cost, never under.

## The honest limit

**2.5x does not pay you for your time. It pays for materials, shipping, and misprints, and leaves a
margin. Your labor lives inside that margin, not on top of it.** On a twelve-shirt run that is fine.
On a two-piece custom job it may still lose money per hour. Hence the small-run warning.

To price labor explicitly, set `multiplier: 1.0` and add press time as a `flat_costs` line at your
hourly rate. More accurate, more typing.

## Input schema

Line items take four forms:

```json
{ "sku": "gildan_5000", "sizes": { "3XL": 1, "5XL": 1 }, "shipping": 8.99 }
{ "sku": "gang_22x24", "packs": 1 }
{ "transfer_size": "5x5", "quantity": 12 }
{ "label": "custom thing", "vendor": "who", "pack_price": 9.91,
  "units_per_pack": 2, "packs": 7, "shipping": 8.99 }
```

The last form is the escape hatch for anything not in the price book. `options` is a list so you can compare
vendors in one run; one option is fine. `flat_costs` may be omitted.

## Examples

- `examples/template.json` — blank to copy, shows all three item forms.
- `examples/gang-sheet-vs-individual.json` — the routes comparison on a real 12-tee run.
- `examples/concert-shirt-hindsight.json` — the first project, priced two ways: the flat 2-pack price
  that was actually used, against the real 3XL/5XL size cost. The outsourced 5X print is still `0.00`
  because that cost was never recorded; **fill it in if you find the receipt.** The design size is an
  assumption — correct it and the counterfactual sharpens.
- `examples/two-vendor-comparison.json` — manual-entry shape demo. **Its prices are invented.**

## What it does not do

- Buy anything, or set a final price. It gives you the floor. The floor is not the price.
- Price a blank style that is not yet in `refresh_prices.py`. Add its catalog number and URL to
  `JIFFY_PRODUCTS` and re-run the fetcher.
- Track sales. That is a separate, unbuilt thing — the measurement surface for the $1,000.

---

> *Adapted from The Three Ms of AI™. © 2026 Nate Herk. All rights reserved.*
> *The Three Ms of AI™ is a trademark of Nate Herk.*
