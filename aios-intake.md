# AIS-OS Intake

This is the source-of-truth file for your AIOS. Fill it in by typing, voice-pasting (Wispr Flow / OS dictation), or running `/onboard` for a guided conversation. Whichever mode, this file is what `/onboard` reads to scaffold your Day-1 setup.

**Hard cap: 7 questions.** Each answerable in under 60 seconds. Don't overthink — you can edit and re-run `/onboard` any time.

---

## Q1 — Who are you, what do you sell, who do you sell it to?

Identity, offer, ICP. One paragraph each is fine.

```
**Name:** Yina Belt. **Brand name:** TBD — not chosen yet.

**What I sell:** Custom-crafted items. Specifically custom design *application* onto physical products — not reselling, not dropshipping. I design, then apply the design to the item.

**Primary product focus:** Party favors and party decor for kids' parties.

**Who I sell to:** Moms of young kids — the person planning and buying for the party.

**Explicitly out of scope:** Reselling. That's a different business.
```

---

## Q2 — Paste 1-2 things you've written recently. Don't edit them.

An email, a LinkedIn post, a DM, a doc — anything that sounds like you when you're not trying. **Paste verbatim.** Do not type these mid-conversation with Claude — chat-shaped samples are worse than no samples (voice contamination).

```
**Sample 1 — raw turns from her own ChatGPT thread, "Custom Concert Shirt" project (verbatim, unedited).**
Not written for an audience. This is how she talks when she is working a problem.

Is 14x18.43 too big for the back image

The front print is 14"x14", is that ok or should I make it larger

Is there a way to politely ask for more money? ... We didn't really talk cost ... I ended up overspending.

Here's my costs... doesn't even include time and labor.

I was thinking maybe I could offer it to someone who wants to cut it.

I don't think I was taking into consideration ... the sides of the shirt are gonna be taken up by the human body. I just don't want it to look small.

Do I need to wash the Gildan 5000 shirts first? I don't want to lol

I'm netting a hundred dollar loss on this ... but I have some inventory.

I want to ... sell. Put a video together ... and figure out how I want to sell. Transfers? Put them on blanks? Colors customizable?

I want to put pics on FB Marketplace ... but I only have the plus sized shirts I made.

Did I really design this? Some stuff I just bought ... I had inspiration, like a template.

I kind of want to mention knocking out this project ... clearing my projects because it's almost time ... Christmas tree ... teaser for the Christmas party.
```

```
**Sample 2 — a personal relationship message. WITHHELD FROM THIS REPO by request of the AIOS.**

The raw text was provided and read during intake, but it is intimate correspondence involving another
person, and this repo is pushed to GitHub. Storing it verbatim here would publish it. Yina can paste it
back in at any time if she wants it kept.

Register notes captured from it (no verbatim text):
- Long, unbroken, run-on sentences when the subject is emotional. Very different rhythm from Sample 1.
- Leads by naming the other person's experience before her own. "I hear what you're saying about what
  happens for you too."
- Repairs rather than argues. Names the shared problem, not the opponent.
- Softens with an emoji at the close rather than a hard stop.
- Zero jargon. Zero bullet points. Plain, direct, warm.
```

---

## Q3 — What are your 2-3 biggest priorities for the next 90 days?

Quarterly priorities. Not yearly aspirations. Things that, if not done by July, would make you say "I wasted Q2."

```
1. **$1,000 in sales by 2026-11-20** (90 days from 2026-08-22). Gross sales, not profit. This is the number that decides whether the business is real.
2. **Post about the brand 3x per week**, every week, for the full 90 days. That is 39 posts. Measured by posts published, not by reach or follower count.
3. **Pick the brand name.** One deliverable, one decision, done. Priorities 1 and 2 are both partially blocked until this lands, so it goes first.
```

---

## Q4 — Where does revenue actually land, and where is it tracked?

Multiple answers OK. Stripe? Skool? GoHighLevel? QuickBooks? A spreadsheet?

```
**Tracked where:** Nowhere. It's a receipts pile. No ledger, no spreadsheet, no accounting tool.

**Channel plan (deliberate, risk-based):**

| Channel | Status | What sells there | Fulfillment |
|---|---|---|---|
| Facebook Marketplace | Confirmed, in use | Finished shirts, incl. concert/fan-art designs | Local pickup only to date. Open to shipping. |
| Etsy | Possible, not started | **PNG / digital transfer files only.** Explicitly NOT finished shirts. | Digital |
| eBay | Undecided, leaning no | — | — |

**The reason for the split:** licensing risk. Concert and artist-referencing designs stay on Facebook
Marketplace only, to keep exposure contained. Etsy would carry the digital files, not the fan-art shirts.
This is a stated, intentional constraint — not an accident of where she happens to have accounts.

**Where the money actually lands:** Not yet pinned down. Depends on the platform. Local pickup to date
implies cash or a peer-to-peer app, but the specific rail was not named. **OPEN ITEM — see gap below.**

**Gap flagged during intake:** Priority 1 is "$1,000 in sales by 2026-11-20." There is currently no place
where a sale gets recorded. A number you can't count is a number you can't hit. Simplest fix on Day 2:
one sheet, five columns — date, item, channel, amount collected, cost of goods.
```

---

## Q5 — Where do you talk to customers, your team, and the outside world day-to-day?

Email (which one — Gmail / Outlook)? Slack? Teams? DMs (Skool / Discord / iMessage)? Phone?

```
[Your answer here]
```

---

## Q6 — Where do meeting recordings, notes, and important docs live?

Granola? Otter? Fireflies? Google Drive? Notion? Dropbox? A folder on your desktop you keep meaning to organize?

```
[Your answer here]
```

---

## Q7 — What's the one task that eats your week, and where do you currently track work?

The single biggest time-suck or recurring drudgery. Plus where tasks/projects live (ClickUp / Asana / Linear / Notion / a notebook).

```
[Your answer here]
```

---

When this file is filled, run `/onboard` (or re-run it) and the wizard will scaffold your Day-1 file set: `context/`, `references/voice.md`, populated `connections.md`, and a filled `CLAUDE.md`.
