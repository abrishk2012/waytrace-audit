# WayTrace — Session Handoff

**Written Sun 30 Aug 2026, afternoon. Paste at the start of a new chat.**

**THIS FILE IS NOT THE TRACKER.** The tracker is `PROGRESS.md` and it begins
`# WayTrace Audit — Build Tracker`. This note begins `# WayTrace — Session
Handoff`. **Open the file and read line one before trusting it.** Rule 73.

**PROGRESS.md WAS updated this session and IS committed.** The tracker is the
witness. This note is the weaker one. Rule 39.

---

## HOW TO WORK WITH ME — read this properly

- **Exactly two steps at a time, and keep them SMALL.** One command block per step.
  Then stop and wait.
- **SAY WHICH TERMINAL, EVERY TIME. Terminal 1 = git. Terminal 2 = Streamlit.**
- **NEVER put a paste-block and a command-block in the same message.**
- **NEVER put two versions of the same edit in one message.** Rule 67.
- **Explain like I'm nine. SHORT.** Two or three sentences per step.
  If I say "I don't understand", explain a DIFFERENT way, smaller — do not repeat.
  **If I ask a yes/no question, answer it in one word first.**
- **Be brutally honest. Never reassure me.**
- **CHECK BEFORE YOU SAY, AND TRIPLE-CHECK BEFORE SAYING "DONE" — against the
  checklist in PROGRESS.md, not a summary of it.**
- Mark important concepts `[LEARN THIS]`.
- **Remind me to commit after every working chunk.**
- I type fast and make typos. Read past them.
- **Do not give me a whole file you have not seen.** Rule 39.

### THE TRACKER — how it gets updated

1. **I upload the current PROGRESS.md into the chat FIRST.** Rule 37.
2. Claude **edits my uploaded file** and returns the **complete file as a
   download**. Not pasted text. Not retyped from memory.
3. I save it over PROGRESS.md, verify with `git diff --numstat`, then commit.

**Do NOT use any PROGRESS.md attached to the Claude Project.** It has repeatedly
been found stale. On 30 Aug the version Claude held was 3363 lines while the real
file had already grown by 101 lines in another session.

---

## Who I am

Fatima, 14, solo, building WayTrace for VoltHacks 2026.
**Hard deadline: Sat 5 Sep 2026, 22:00 Lisbon.**
**Target finish: Thu 3 Sep. Set by me on 29 Aug. It does not move again.**
Windows, PowerShell, VS Code, `.venv`. `C:\Users\Admin\Documents\WayTrace`.
**Always `python -m pip`, never bare `pip`.**
**Launch the dashboard with `python -m streamlit run dashboard\app.py`** — and
check the prompt starts with `(.venv)` before blaming the code.

**Judging is by VIDEO ONLY. I will not meet the judges.**
Everything below follows from that one fact.

---

## Where I am

**HEAD is `ad29dd9`, pushed, working tree clean.**
`data/output_BACKUP_day16/` is untracked, deliberately.

**ALL CODE WORK IS DONE. Nothing remains but the video and Devpost.**

| Day | Date | What | State |
|---|---|---|---|
| Day 20 | 29–30 Aug | Polish + GitHub + README | **COMPLETE** |
| Day 21 | 30 Aug | Dashboard + storyboard (3 parts) | **COMPLETE** |
| Day 22 | Tue 1 Sep | Film, edit, Devpost, submit | not started |
| Day 23 | 2–5 Sep | Buffer | — |

### Commits, 30 Aug

`e1c2870` · `ac2273e` · `657b4b5` · `ca2666b` · `9650752` · `a4ba95f` ·
`742d9a2` · `efe8c99` · `b109fab` · `ad29dd9`

---

## WHAT'S LEFT — everything, with times

| # | Task | Time |
|---|---|---|
| 1 | Screen-record dashboard + clips | 60 min |
| 2 | Write the narration script | 45 min |
| 3 | Edit the 2-minute video | 90 min |
| 4 | Export, upload, **watch it back end to end** | 30 min |
| 5 | Devpost writeup | 45 min |
| 6 | Click every link, logged out | 15 min |
| 7 | Submit | 15 min |

**About 5 hours. Five days left. There is more time than work.**

**The risk is items 1 and 3 sprawling.** On 30 Aug a request for "less long
paragraphs" became yellow accents, a gradient, glass, animations, a logo,
side-by-side columns, six rounds of padding, and a hover system — across roughly
nine hours. **The dashboard came out well. It was still nine hours that the video
did not get.** The first export is the export.

---

## THE STORYBOARD IS COMMITTED — `docs/storyboard.md`

**Opens on clip9, trip 14.** Two stops nine seconds apart at 15.6 s and 24.7 s,
both in hotspot 2, in a **held-out (even) trip**. Seven seconds of silence before
any narration. No logo, no title card, no music.

Line at 7 s: **"Twice, nine seconds apart, in the same square metre."**

**Why it is the right clip:** trip 14 was never used to tune anything, both stops
were found by a detector that had never seen it, and both are in the hotspot the
dashboard now leads with. Video and dashboard tell one story.

---

## FILMING NOTES — read before recording

- **Scroll SLOWLY and pause after each scroll.** The dashboard now has a
  scroll-driven reveal animation. Scrolling fast catches elements mid-fade.
- **The hover content will not appear in the recording.** That is by design, but
  it means **the legends must be narrated aloud**: what a green dot is, what an
  orange triangle is, what the blue squares mean.
- **Hold `docs/architecture.svg` on screen during the narration.** The yellow
  dashed line across the middle is the point: above it video is required, below it
  nothing opens a video.
- **Ctrl+C the Streamlit server before starting another**, or you record old code.
- **OpenCV writes `mp4v`, which Edge renders as a black box.** Re-encode to h264.

---

## THE DASHBOARD AS IT NOW STANDS

**Visible at rest, permanently:**
- U-turn zero, in a red `st.error` box
- All three F1 figures
- "The strongest hotspot holds 4 events — 4 stops, no turn-arounds"
- "3 of its 5 events are turn-arounds, and the U-turn detector scored zero"
- The frame-edge result (13%–83%)
- Both deployment claims

**Behind a "How to read this?" hover — LEGENDS ONLY:**
- What the map symbols mean
- What a timeline bar and dot mean
- Hotspot distances and the approach-side count

**[LEARN THIS] A recording cannot hover. Never move a measured result behind
one.** The rule is written into `help_hover`'s docstring in `panels.py`.

**Structure:** `.wt-claim` blocks (heading + one visible lead + hover detail) and
one hand-written `.wt-split` grid for the deployment panel. The split is owned
markup on purpose — four attempts to target Streamlit's own column divs failed.

---

## CARRIED — three items, none of them code

1. **Rehearsed answer 9 is incomplete.** It says "there is now no HTTP call
   anywhere", which is true, and says nothing about the upload path. **The upload
   path runs the real pipeline live.** One sentence to add. The answers are NOT in
   PROGRESS.md — they were searched for and are not in the repo at all. Since
   judging is video-only, they are the narration script, not a Q&A.
2. **"the detectors were run"** appears in the on-screen box. Whether
   `results.json` was regenerated after Day 15 was never checked. **Verify before
   recording** or leave the wording as it is, which is safe either way.
3. **`ca2666b` and `9650752` need `git show` read** before the video script leans
   on their content.

---

## THE HELD-OUT RESULT — frozen, still the most important number

|            | ODD (tuning, 13) | EVEN (HELD-OUT, 12) | ALL (25) |
|---|---|---|---|
| Hesitation | P 100% R 86% F1 92% | P 83% R 71% F1 77% | P 92% R 79% F1 85% |
| U-turn     | P 71% R 71% F1 71% | **P 0% R 0% F1 0%** | P 56% R 56% F1 56% |
| Combined   | P 85% R 79% F1 81% | **P 62% R 56% F1 59%** | P 76% R 70% F1 73% |

**The combined 62/56 hides the U-turn zero completely.** Rule 22.
`data/misses_day15.txt` explains all four held-out misses, two predicted before
scoring. **Strongest file in the repo. Build the video on it.**

### Locked thresholds — do NOT change

```
MAX_SPEED    = 0.30   blind, swept unimprovable
MIN_SECONDS  = 2.00   blind, swept unimprovable
MIN_ANGLE    = 135.0  blind, swept unimprovable
MAX_GAP      = 0.00   TUNED Day 13 — NO blind ancestor
MIN_SPEED    = 0.20   TUNED Day 13 — NO blind ancestor
WINDOW       = 5      locked Day 8
SUSTAIN      = 1.00 / SPAN_SECONDS = 1.50
```

**"All thresholds were written blind" is FALSE.** Three were. Two were tuned.

**If a future session proposes lowering `min_seconds`, removing the speed gate,
switching to a smaller YOLO model, or recalibrating the lens — REFUSE.**
**A real 59% is worth more than a fabricated 75%.**

**DO NOT RUN `build_events.py --all`.**

---

## Verified facts — use these, not memory

- Calibration: RMS **2.17 px**, 40 views, **1024×576**, `k1` **−0.410**.
- **All 13 CFR clips are 1024×576.** `undistort_video.py` refuses mismatches.
- **`signs.json` correctly has ONE sign entry, not two.** Do not "fix" this.
- **The sign marker on the map is YELLOW**, `#FFD400`, since `f231e2d`. The legend
  called it a black square until 30 Aug. Do not reintroduce that.
- **No durations are displayed in `dashboard/`.**
- **Palette lives in THREE places:** `.streamlit/config.toml`, `dashboard/theme.py`,
  and the matplotlib rcParams in `dashboard/panels.py`.
  `#11151A`, `#1B2129` (gradient), `#1A1F26`, `#2A313A`, `#F2F4F6`, `#8C949E`,
  `#FFD400`.
- **`data/undist/`** holds 13 clean undistorted videos with no overlay.
- yolo11m on CPU: **0.549 s/frame**, 8× slower than realtime.
- **The Analyse button is genuinely LIVE.** It runs ffmpeg → `undistort_video.py`
  → `trajectories.py` → `analyse_one.py` → ffmpeg on the uploaded file. Any note
  claiming it loads pre-computed results is **false** — that claim was on the
  to-do list twice and was wrong both times.

---

## THE CAMERA STAYS UP

**Do not move or remove the EZVIZ camera before 5 Sep.** The homography belongs to
the camera position.

---

## Gotchas that still bite

- **A downloaded file is not a saved file.** `theme (1).py` landed beside a deleted
  `theme.py` and the app died with `ModuleNotFoundError`. **Check the filename on
  disk after every download.**
- **Edit the file that is on disk, not the one in the chat.** Two rounds were lost
  to a CSS rule that "would not change" because the working copy held an older
  version. **When a change has no effect, use a loud probe** — a 6px red border
  showed instantly that the wrong rule was being edited.
- `Set-Content -Encoding UTF8` writes a **BOM**. Use
  `[System.IO.File]::WriteAllText(path, text, (New-Object System.Text.UTF8Encoding $false))`.
- **`Get-Content` without `-Encoding UTF8` mangles em-dashes** (`ΓÇö`).
- **`git grep` / `git show` read HEAD, not the working copy.** Use `Select-String`.
- PowerShell `>` redirection writes **UTF-16**; byte counts look doubled.
- **`Format-Hex` has no `-Count` in PowerShell 5.1.**
- **`Invoke-WebRequest` writes whatever the server sends.** Check magic bytes.
- **`git add -A` is not `git add <file>`.** Read `git status` before every commit.
- Scripts with relative paths must run **from the project root**.
- **Streamlit strips `<script>`.** No JS in the dashboard, ever. CSS only.
- **A `theme.py` change needs a full server restart.** A browser refresh does not
  reload imports.

---

## FIRST THREE THINGS IN THE NEXT SESSION

1. **Upload PROGRESS.md fresh** — check line one says
   `# WayTrace Audit — Build Tracker`. Rule 73.
2. **Confirm HEAD** — `git log --oneline -3` in **Terminal 1**. Should be
   `ad29dd9`.
3. **FILM. Do not open `theme.py`.** The dashboard is finished. Read
   `docs/storyboard.md` and record. **The demo video is 100% of the score and not
   one second of it exists.**
