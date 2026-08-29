# Content naming convention

Started 2026-08-29, in response to the `Phone Import` dump. Applies to every photo, video and audio file
that enters Drive from here forward, and retroactively to the back catalog as it gets labelled.

**Why this exists.** `context/priorities.md` records that the posting cadence is not blocked on making
new things. It is blocked on editing and publishing what already exists. A hundred files called
`IMG_2847` is not an archive, it is a pile. You cannot pull "the Santa's Workshop build footage" out of
a pile, so the footage may as well not exist.

The convention is the cheapest thing that turns the pile into an archive.

## The format

```
YYYYMMDD_project_subject_nnn.ext
```

Four fields, one underscore between each, hyphens inside a field. All lowercase except the extension.

| Field | What it is | Rules |
|---|---|---|
| `YYYYMMDD` | The date the shot was **captured**, not uploaded | 8 digits, no separators. Sorts correctly by default. |
| `project` | Which build or event it belongs to | From the project list below. Add new ones to that list, never invent one inline. |
| `subject` | What it actually shows | One to three words, hyphenated. Plain description, not a caption. |
| `nnn` | Sequence within that project and date | 3 digits, `001` up. Keeps burst shots together and stable. |

### Examples

```
20251214_xmas-2025_workshop-build_014.MOV
20251220_xmas-2025_table-setup_003.HEIC
20261025_aidens-fifth_favor-assembly_001.HEIC
20260810_concert-shirt_press-close_007.JPG
20221210_xmas-2023_pajama-party_002.JPG
```

Read left to right you get: when, what build, what it shows. That is enough to find footage without
opening it.

## Project list

Keep this list short and add to it deliberately. One project equals one build or event, not one topic.

| Slug | What it covers | Side |
|---|---|---|
| `xmas-2022` | 24–25 Dec 2022. The only Christmas footage actually in Drive. Eve into morning. | Brand |
| `xmas-2023` | Claimed in the content strategy. **Not found in Drive.** | Brand |
| `xmas-2024` | Photos plus some video. Crafting and behind-the-scenes. | Brand |
| `xmas-2025` | Santa's Workshop theme and party. The strongest archive year. | Brand |
| `xmas-2026` | The nostalgic 90s build, in progress. The tentpole. | Brand |
| `aidens-fifth` | Aiden's fifth birthday. Edition 001, Level Five. | Both |
| `concert-shirt` | The adult concert shirt project. | Shop |
| `birthday-shirts` | Custom kids' birthday shirts. | Shop |
| `craft-general` | Untied crafting footage. B-roll and process. | Brand |
| `house` | House projects. | Brand |
| `halloween-2026` | Costume making. | Brand |
| `thanksgiving-2026` | Thanksgiving at home. | Brand |
| `studio` | Workspace, tools, materials, setup. Not tied to one build. | Both |
| `unsorted` | Only until it is labelled. Never the final answer. | — |

**Side** records whether an asset belongs to the brand's story, the shop's proof, or both. Days Like
These is the umbrella and the shop lives inside it, so a lot of footage is legitimately both. Recording
it means you can find shop proof without scrubbing the whole archive.

## Subject vocabulary

Use plain, repeatable words. Consistency beats precision, because consistency is searchable.

- **Process:** `build`, `assembly`, `press`, `cutting`, `weeding`, `packing`, `prep`
- **Result:** `finished`, `flatlay`, `worn`, `installed`, `table-setup`, `reveal`
- **Context:** `workspace`, `supplies`, `before`, `after`, `guests`, `detail`
- **Person-led:** `talking`, `hands`, `wide`

Combine as needed: `favor-assembly`, `press-close`, `table-setup`, `workshop-build`.

**Note tied to the production comfort boundary** in `context/content-strategy.md`: close-up hand footage
is not a default when nails are not done. Tagging shots `hands` makes that constraint checkable at a
glance instead of a surprise in the edit.

## Rules

1. **Capture date, not upload date.** Upload date is an accident of when the phone was near a computer.
   Proven on the Phone Import dump: single upload bursts there mix material years apart. Read the real
   date from EXIF.
2. **Never sort or group by `IMG_####`.** The counter resets with a new phone. In Phone Import,
   `IMG_2825` is February 2023 and `IMG_2261` is September 2025, because they came off different
   devices. Filename order looks like chronological order and is not.
3. **Never rename to a name you cannot reconstruct.** Every rename gets recorded in the index against
   its original filename. Nothing becomes unfindable mid-migration.
4. **Do not encode status in the name.** Raw, in production, approved and published are *folders*, and
   Drive already has them at `03`, `04` and `05`. A file that gets edited keeps its identity; only its
   location changes.
5. **Do not encode platform in the name.** One asset can go to more than one place. Platform belongs to
   the published export, not the master.
6. **Keep bursts together.** Twelve frames of the same moment share a subject and differ only in `nnn`.
7. **`unsorted` is a queue, not a category.** Anything still called `unsorted` after it has been looked
   at once is a bug.
8. **New project slugs go in the table above before they go on a file.** That is what stops this from
   drifting back into a pile.

## Where files live

The taxonomy already exists in Drive and is empty. Naming and filing are the same job.

| Stage | Drive location |
|---|---|
| Raw off the phone, named | `03 — Content Collection/Photos — Raw`, `/Video — Raw` |
| Being edited | `04 — Content Production/In Production` |
| Finished master | `04 — Content Production/Final Masters` |
| Sized for a platform | `05 — Publishing/Platform-Ready` |
| Posted | `05 — Publishing/Published` |

`Phone Import` is not a stage. It is the loading dock. It should end up empty.

## Rollout

1. Label the back catalog by cluster, not by file. See `references/phone-import-index.md`.
2. Rename and file the labelled clusters.
3. Apply the convention at capture from here forward. Renaming on the phone at the moment of shooting is
   cheaper than any batch job later.
