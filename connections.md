# Connections

Registry of every system your AIOS can reach. Filled by `/onboard` from Q4-Q7 answers; expanded over time as you wire new tools. `/audit` checks this file for domain coverage and freshness.

| # | Domain | Tool | Mechanism | Auth | Last checked |
|---|---|---|---|---|---|
| 1 | Revenue / Financials | Receipts pile (no system). Facebook Marketplace; Etsy possible for digital files | not yet connected | — | — |
| 2 | Customer interactions | Facebook Messenger DM, Instagram DM and reel replies, iMessage/text, in person | not yet connected | — | — |
| 3 | Calendar | Google Calendar (inferred from Gmail) | not yet connected | — | — |
| 4 | Communication | Gmail | not yet connected | — | — |
| 5 | Project / task tracking | None | not yet connected | — | — |
| 6 | Meeting intelligence | None. Customer conversations happen by text and verbally, nothing is captured | not yet connected | — | — |
| 7 | Knowledge / files | Canva, Google Drive, desktop folders | `mcp` (Google Drive) | OAuth, `alvinbelt@beltbuckledent.com` | 2026-08-29 |

**Mechanism options:** `mcp` (MCP server), `script` (Python/Bash hitting an API, in `scripts/`), `export` (CSV/JSON dump pipeline), `key+ref` (`.env` key + `references/{tool}-api.md` guide), `not yet connected`.

When you wire a new tool, also save `references/{tool}-api.md` capturing endpoints, auth flow, and common queries — researched-once-saved-forever.

## Notes from intake

- **Domain 1 is the weak point.** Priority 2 is "$1,000 in gross sales by 2026-11-20" and there is
  currently nowhere a sale gets recorded. This is the highest-leverage thing to wire first.
- **Domain 5 and 6 are genuinely empty**, not just unconnected. There is no task system and no capture
  of customer conversations. Do not score these as connection gaps until there is something to connect.
- **Domain 7 is split three ways** across Canva, Drive and desktop folders with no source of truth and
  no naming convention. Google Drive is the consolidation target, since Gmail is already confirmed.
- **Vendors touched so far:** Ninja Transfers, Jiffy (jiffyshirts), Gildan 5000 blanks. No preferred
  vendor selected. A landed-cost comparison across these is the standing `/level-up` candidate.

## Drive sync — 2026-08-29

Google Drive is now readable by the AIOS over MCP. Domain 7 moved from "not yet connected" to connected.
Full folder map, IDs and drift list live in `references/drive-map.md`.

**What the first walk found:**

- **Signal.** One new strategy Doc (2026-08-27) and one raw media dump, `Phone Import` (2026-08-28).
  The Doc is mirrored to `context/content-strategy.md` and it conflicts with the rest of the OS. See
  `decisions/log.md`, 2026-08-29.
- **Noise.** 10 top-level folders and 30+ subfolders built 2026-08-22, still holding zero files. The
  taxonomy exists. Nothing has been filed into it.

**Still missing, and still the same gap as intake.** Reading Drive does not close Domain 1. Revenue is
not in Drive. `08 — Business Operations/Finance` is empty. The receipts pile is still a receipts pile and
the $1,000 still has no measurement surface.

**New gap this walk exposed:** there is no file naming convention, so consolidating Canva and desktop
folders into Drive would produce a bigger unsearchable pile. Naming comes before migration.
