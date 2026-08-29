# Phone Import — index and labelling worksheet

Folder: [Phone Import](https://drive.google.com/drive/folders/1IvtBxOO_fYG2FRUyoK7BZYoxEdAFq68-)
`1IvtBxOO_fYG2FRUyoK7BZYoxEdAFq68-` · owner `ybelt@beltbuckledent.com`

Walked 2026-08-29. Roughly 100 to 110 files: HEIC, JPG, PNG and MOV, straight off the phone.

## The move: label clusters, not files

Labelling 100+ files one at a time is a bad job that never gets done. It does not have to be done that
way.

Two things in the raw metadata already group the footage for free:

1. **`IMG_####` sequence numbers.** iOS assigns them in order. A run like `IMG_1480` through `IMG_1492`
   is one continuous session with one camera. Runs that are far apart in number were shot far apart in
   time, whatever order they got uploaded in.
2. **Upload timestamps.** The dump went up in tight bursts, and each burst is one selection Yina made
   from the camera roll. Files uploaded in the same 5 seconds were almost certainly chosen together for
   the same reason.

Cross the two and the pile collapses into about ten shoots. **Yina writes ten labels, not a hundred.**
Everything under a label inherits the date, project and subject, and the rename becomes mechanical.

## The worksheet

Fill in the three right-hand columns. One line per cluster. That is the whole job.

| # | Files | Type | Uploaded | Capture date | Project | Subject |
|---|---|---|---|---|---|---|
| A | `IMG_1034`–`1058`, `IMG_0897`, `IMG_0898`, `IMG_9286`, `Resized_Resized_20221210_152305`, `Resized_Resized_20221210_152450` | HEIC + JPG | 21:30:41–44 | **2022-12-10** for the two `Resized_` files. Rest? | | |
| B | `IMG_0787`, `0788`, `0789`, `0840`, `0841`, `0899` | MOV, 17–66 MB | 21:31:00–31 | | | |
| C | `IMG_1480`–`1492`, `IMG_8696`–`8702`, 2 UUID `.MOV` | HEIC + JPG + MOV | 21:32:29–38 | | | |
| D | `IMG_2781`, `2809`, `2825`–`2833`, `2847`–`2857` | HEIC + JPG + MOV | 21:34:02–21:36:44 | | | |
| E | `IMG_4387`, `4462`, `4508`–`4511`, `4518`, `4519`, `4983`–`4994` | HEIC + MOV | 21:38:03–20 | | | |
| F | `IMG_5005`, `5010`–`5023` | HEIC + MOV | 21:39:08–21:41:13 | | | |
| G | `IMG_2261`–`2280`, `IMG_2438` | HEIC, 2–5 MB | 21:40:51–21:41:03 | | | |
| H | `IMG_2447`, `IMG_2480.PNG` | HEIC + PNG | 21:54:24–25 | | | |
| I | `IMG_2446`, `IMG_2479.PNG` | HEIC + PNG | 22:02:55–56 | | | |
| J | 14 UUID-named `.jpeg`, suffixed `_1_105_c` and `_4_5005_c` | JPEG | Aug 29, 00:15–00:17 | | | |

Project slugs come from `references/content-naming-convention.md`. Subject is one to three hyphenated
words.

## What the metadata already tells us

**Cluster A holds the oldest material in the dump.** `Resized_Resized_20221210_152305.JPG` and
`...152450.JPG` carry a real date in the filename: **10 December 2022**. That is the original pajama
party at the sister-in-law's apartment, the year `context/content-strategy.md` logs as mostly photos.
The double `Resized_` prefix means they were shrunk twice, probably forwarded through a messaging app,
so expect low resolution. They are still the only footage of where the Christmas story starts, which
makes them the proof for the hook already on record: "Our Christmas party somehow went from a crowded
apartment pajama party to almost 100 RSVPs."

**Cluster J is a different kind of file.** The `_1_105_c` and `_4_5005_c` suffixes are Apple Photos
export naming, not camera naming, and they arrived a day after everything else. These were exported
deliberately rather than bulk-selected. They may already be a shortlist.

**Clusters G, H and I are all in the `IMG_24xx` range** but were uploaded in three separate bursts up to
30 minutes apart. Same shooting period, three separate decisions to include them. Worth checking whether
they are one shoot split up or genuinely different subjects.

**The MOV files are where the weight is.** `IMG_0787` at 66 MB, `IMG_0841` at 66 MB, `IMG_5005` at
57 MB, `IMG_0899` at 52 MB. Together the video is the large majority of the folder by size. It is also
the material most likely to carry a story, and the most expensive to review. Label the video clusters
first.

## What I can and cannot review

Straight answer on the feasibility question, because it changes what is worth asking me to do.

**Can do, at no cost:** everything above. Filenames, types, sizes, timestamps, sequence runs, the
clustering. That is the whole index and it needed no file opened.

**Can do, expensively:** view individual images. Files come to me through the Drive connector as encoded
text, so a single 21 KB photo consumed about the same budget as several pages of writing. A 5 MB HEIC
is hundreds of times that. Reviewing 10 to 20 small images across the session is realistic. Reviewing
100+ is not, and the ones that would most repay a look are the large ones.

**Cannot do:** watch video. The MOV files cannot be transferred at that size, so nothing in the folder's
largest and most important category can be reviewed by eye here.

**So the fastest path is not for me to look.** Yina already knows what every cluster is. Ten labels from
her beats a hundred guesses from me, and it is the version that is actually accurate.

**If a cluster is genuinely unidentifiable,** name it and I will pull a small sample from it to identify
the shoot. That is the right use of the expensive channel: a handful of files chosen on purpose, not a
sweep.

## Then what

1. Yina fills in the three columns above.
2. Rename each cluster to `YYYYMMDD_project_subject_nnn.ext` per the convention.
3. File into `03 — Content Collection/Photos — Raw` and `/Video — Raw`.
4. `Phone Import` ends up empty. It is a loading dock, not a folder.

Renaming ~100 Drive files one at a time is exactly the kind of repeated manual task that belongs in
`/level-up`. Once the labels exist, the rename should be scripted, not clicked.

## Caveat on completeness

The Drive search paginator returned overlapping pages on this folder, so the file list above was
assembled across pages that repeat entries. Cluster boundaries and the observations are sound. Exact
counts are not guaranteed, and a few stragglers may sit outside the ranges listed. Verify against the
folder before treating any cluster as closed.
