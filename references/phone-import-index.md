# Phone Import — dated index

Folder: [Phone Import](https://drive.google.com/drive/folders/1IvtBxOO_fYG2FRUyoK7BZYoxEdAFq68-)
`1IvtBxOO_fYG2FRUyoK7BZYoxEdAFq68-` · owner `ybelt@beltbuckledent.com`

**60 of roughly 110 files now carry a real capture date**, read from EXIF on 2026-08-29. Raw data in
`references/data/phone-import-exif.csv`. The reader that produced it is
`references/data/extract-exif.py`.

## Read this first: the archive is one Christmas, not four

`context/content-strategy.md` records a Christmas archive spanning four years: 2023 photos, 2024 photos
plus video, 2025 Santa's Workshop, 2026 the 90s build.

**The dated files do not show that.** The only Christmas material in this folder is
**24–25 December 2022**, seventeen frames running from 21:11 on Christmas Eve to 09:10 on Christmas
morning. There is nothing from December 2023, December 2024 or December 2025. There is nothing from
calendar 2024 at all, and nothing captured in the last eleven months: the most recent real capture in
the whole folder is **2025-09-28**.

Two possibilities, and it matters which:

1. The later Christmases are still on the phone or in iCloud and have not been uploaded. Then this is a
   half-finished import and the rest is the priority.
2. They were never shot in a usable way. Then "Christmas Story Begins", the third priority post in the
   content strategy, does not have the multi-year archive it assumes, and the post needs rethinking
   before it gets made.

Do not resolve this by guessing. It is one look at the camera roll.

## The trap: sequence numbers reset

`IMG_####` runs in order **per device**, and the counter restarted. Three devices are present:

| Device | Range in this folder | Dates |
|---|---|---|
| iPhone XR | `IMG_9286` | 2022-04 |
| iPhone 14 | `IMG_0897` → `IMG_5023` | 2022-11 → 2023-05 |
| iPhone 16 | `IMG_2261` → `IMG_2480` | 2025-09 |

So `IMG_2825` is **February 2023** and `IMG_2261` is **September 2025**. Two files thirty numbers apart
can be two and a half years apart. Sorting or grouping this folder by filename produces a wrong answer
that looks right, which is worse than no answer.

Two files even share a name at different IDs (`IMG_2826`, `IMG_2848` each appear twice). Deduplicate by
capture time, not by title.

## The real shoots

Each row is one sitting. Ranges are inferred from dated endpoints; every date shown was read from a file.

| # | Files | Captured | Device | Notes |
|---|---|---|---|---|
| 1 | `IMG_9286` | 2022-04-17 14:54 | iPhone XR | Lone survivor of the older phone |
| 2 | `IMG_0897`, `0898` | 2022-11-17 18:08 | iPhone 14 | 3520x1980, a wide crop |
| 3 | `IMG_1034`–`1036` | 2022-11-19 19:51 | iPhone 14 | |
| 4 | `IMG_1055`–`1058` | 2022-11-22 18:27 | iPhone 14 | |
| 5 | `Resized_Resized_20221210_*` ×2 | 2022-12-10 | unknown | Date from filename. 1024x1024, twice-resized, EXIF gone |
| 6 | **`IMG_1480`–`1492`** | **2022-12-24 21:11 → 2022-12-25 09:10** | iPhone 14 | **The Christmas material. Eve into morning.** |
| 7 | `IMG_8696`–`8702` | 2023-02-12 15:30–15:43 | screenshots | 1206x2208, no camera. Phone screenshots, not photos |
| 8 | `85DFFD44-…MOV` | 2023-02-13 00:14 | — | 17.7 seconds |
| 9 | `IMG_2825`–`2857` | 2023-02-18 17:07 → 2023-02-19 16:50 | iPhone 14 | Two days |
| 10 | `IMG_4462` | 2023-05-06 21:12 | iPhone 14 | |
| 11 | `IMG_4508`–`4511` | 2023-05-12 21:43 | iPhone 14 | |
| 12 | `IMG_4983`–`4994` | 2023-05-29 15:27 → 18:22 | iPhone 14 | |
| 13 | `IMG_5010`–`5023` | 2023-05-30 20:42 → 2023-05-31 15:57 | iPhone 14 | |
| 14 | `IMG_2261`–`2280` | 2025-09-19 09:24 → 13:55 | iPhone 16 | Full day, three sittings |
| 15 | `IMG_2438`–`2447` | 2025-09-26 05:41 → 15:45 | iPhone 16 | |
| 16 | `IMG_2479`, `2480` | 2025-09-28 05:17 | screenshots | 1179x2556 |

## Things worth knowing before labelling

**Cluster J was duplicates.** The UUID-named `.jpeg` files uploaded a day later are not a shortlist. Two
of them carry EXIF, and it matches files already in the folder: `31575641-…` is 2022-12-25 09:10, the
same instant as `IMG_1492`; `E5E19FA8-…` is 2023-05-30 20:42, the same instant as `IMG_5010`. Both are
**768x1024**, against 3024x4032 for the originals. They are downsized copies of footage already present
at full resolution. Delete them or ignore them; do not label them as their own shoot.

**Some files are screenshots, not footage.** `IMG_8696`–`8702` at 1206x2208 and `IMG_2479`–`2480` at
1179x2556 are phone screen captures. They may still be useful as evidence, an order confirmation or a
message, but they are not shootable material and should not be filed as photos.

**Three files have no recoverable date and no camera:** `IMG_2809.JPG` (1275x1964), `C145184A-…`
(665x1182), `EA632B82-…` (323x576). Odd sizes, stripped metadata: these were saved or forwarded from
somewhere else rather than shot. Treat provenance as unknown.

**The video is still mostly dark.** See the limit below. Only two videos were readable, and one of them,
`IMG_5016.MOV`, reports 2026-08-28 21:38 as its creation time, which is the moment it hit Drive, not the
moment it was shot. Video timestamps here are not trustworthy without a second signal.

## What blocked full coverage

The Drive connector refuses any download over **10 MB**. That is a hard stop, not a budget question.

Every video except five is over the limit, including all the large ones: `IMG_0787` and `IMG_0841` at
66 MB, `IMG_5005` at 57 MB, `IMG_0899` at 52 MB. About twenty video files cannot be reached this way at
all, and video is the majority of the folder by size and the material most likely to carry a story.

The connector also strips Drive's own `imageMediaMetadata`, so capture dates that Google already holds
have to be recovered by reading each file. That works, and it is how the table above was built, but it
is why the 10 MB ceiling bites.

**To date the video, one of these:**
- Yina reads the dates off the phone or Drive web UI and pastes them in. Fastest.
- A script with real Google Drive API credentials pulls `videoMediaMetadata.time` for the whole folder
  in one call. This is the right long-term fix and is a `/level-up` candidate.

## The worksheet

Dates are done for the images. What is left is what each shoot *is*. One line each.

| # | Captured | Project | Subject |
|---|---|---|---|
| 1 | 2022-04-17 | | |
| 2 | 2022-11-17 | | |
| 3 | 2022-11-19 | | |
| 4 | 2022-11-22 | | |
| 5 | 2022-12-10 | | |
| 6 | 2022-12-24/25 | `xmas-2022`? see note above | |
| 7 | 2023-02-12 | screenshots | |
| 8 | 2023-02-13 | | |
| 9 | 2023-02-18/19 | | |
| 10 | 2023-05-06 | | |
| 11 | 2023-05-12 | | |
| 12 | 2023-05-29 | | |
| 13 | 2023-05-30/31 | | |
| 14 | 2025-09-19 | | |
| 15 | 2025-09-26 | | |
| 16 | 2025-09-28 | screenshots | |

Project slugs and subject vocabulary: `references/content-naming-convention.md`.

Once a project is named, the rename is mechanical: the date and sequence are already known, so
`YYYYMMDD_project_subject_nnn.ext` writes itself.

## Method note

The first version of this index clustered by **upload** timestamp, on the theory that files uploaded in
the same burst were chosen together. Capture dates show that was wrong: single upload bursts mix
material years apart, because they were selections from a camera roll rather than from an event.

Upload time records when Yina was at a computer. Capture time records when the thing happened. Only one
of those is worth indexing on.
