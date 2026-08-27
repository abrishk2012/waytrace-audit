# Fills the Day 15 block in PROGRESS.md and appends rules 47 and 48.
# Surgical: it does not rebuild the file. If any pattern is missing it writes
# nothing at all, so a half-applied edit is impossible (Rules 37, 46).

$p = "C:\Users\Admin\Documents\WayTrace\PROGRESS.md"
$t = [System.IO.File]::ReadAllText($p)
$fail = $false

# ---- 1. tick the five Day 15 boxes -------------------------------------
$oldBoxes = @'
- [ ] Open the EVEN trips for the first time
- [ ] Precision, recall, F1 per behaviour
- [ ] **Include the hard cases.** 100% recall on huge obvious U-turns says nothing
      about subtle ones, and easy-test scores do not go in the README (Rule 8)
- [ ] Write the honest limitations section, including the homography paragraph
- [ ] Practise explaining every number out loud
'@

$newBoxes = @'
- [x] Open the EVEN trips for the first time — `--all` run ONCE, 27 Aug
- [x] Precision, recall, F1 per behaviour — `per_behaviour.py`, commit `083e7dc`.
      **The combined figure hid a detector scoring zero. Rule 22 earned again.**
- [x] **Include the hard cases.** Category split counted from `trip.csv`, not
      recalled: MISSING 5 even / 3 odd, AMBIG 3/5, EASY 4/5. The held-out set
      holds the majority of hard trips, so this was not an easy test (Rule 8).
      **An earlier handoff claimed "6 of 9 MISSING". The real figure is 5 of 8.**
- [x] Write the honest limitations section, including the homography paragraph —
      `docs/limitations.md`, twelve sections, commits `ecef878` and `0e33d4d`
- [x] Practise explaining every number out loud — four questions rehearsed:
      62 vs 85, the U-turn zero, why the hotspots are real, and the small-n
      objection. **Judging is video-only, so these become Day 21 narration:
      there is no follow-up question in a video, only a gap the judge fills
      themselves — and they will fill it worse than the truth.**
'@

# ---- 2. status / notes / quiz -------------------------------------------
$oldStatus = @'
**Status:**
**Notes:**
**Quiz score:      /3**

## Day 16
'@

$newStatus = @'
**Status: DONE.** All five boxes. Twelve commits, all pushed, `0f089fb` … `0e33d4d`.

### THE HELD-OUT RESULT — one run, no retuning

`validate.py` was written and committed as `b8c38a2` **before it was ever run**,
so the scoring rules are in public history with a timestamp that predates the
numbers. The ODD block reprints 11/3/2 P85 R79 unchanged as a self-check, which
is what makes the EVEN block below it trustworthy.

|                | ODD (tuning, 13 trips) | EVEN (HELD-OUT, 12 trips) | ALL (25) |
|---|---|---|---|
| Hesitation | P 100%  R 86%  F1 92% | P 83%  R 71%  F1 77% | P 92%  R 79% |
| U-turn     | P 71%   R 71%  F1 71% | **P 0%  R 0%  F1 0%** | P 56%  R 56% |
| Combined   | P 85%   R 79%  F1 81% | **P 62%  R 56%  F1 59%** | P 76%  R 70% |

**The combined 62/56 hid the U-turn zero completely.** Rule 22 — averages hide
events — cost a whole extra pass today, because the first "Day 15 done" claim
was made on the combined number alone.

### All four held-out misses explained — none unexplained

| miss | cause |
|---|---|
| clip1 t4 114.0 s HESITATION | pause under 2 s. `min_seconds=2.00` excluded it **by definition**. Confirmed by watching the footage. |
| clip8 t12 62.0 s HESITATION | **ONE event typed wrong, not two errors.** A UTURN fired at 62.5 s, 0.5 s away. The matcher demands type agreement, so one real event cost a miss AND a false positive. |
| clip11 t18 29.0 s UTURN | speed gate — U-turn following a stop. **Predicted Day 14.** |
| clip12 t20 86.0 s UTURN | same cause. **Predicted Day 14.** |

A predicted failure appearing on unseen data is stronger evidence of
understanding than an unexplained success.

### Hotspots confirmed on data they were never built from

`--all` produced 21 events, reconciling exactly with the scorer (13 odd + 8 even).
Both original hotspots survived: **(+0.50,+1.00) grew 4 → 5 events, (+1.00,+0.50)
held at 3.** Neither moved. Two new ones appeared, giving 4 total, stable across
cell sizes 0.40–0.75 m. All four on the **approach side** of a junction measured
with a tape measure, independent of any detector output.

### The plan's contingency was deliberately overridden

This block said: *"If recall is poor: Days 18 and 19 are the sacrificial days.
Cut signage or live mode and fix the detector."* Recall is 56% and U-turn is 0%,
so by that rule the detector should now be fixed.

**It will not be.** That contingency was written before the odd/even discipline
existed. Fixing a detector in response to held-out numbers destroys the only
uncontaminated evidence in the project — the thing no other entry will have.
The numbers are reported as they stand. **This override is recorded here as a
deliberate decision, not a quietly skipped step.**

### Other work landed today

- `even_trips()` added to `odd_only.py` — membership stays in ONE file.
  Verified odd 13 + even 12 = all 25.
- `tune.py` refactored to take `trips_fn`; **every sweep row reprinted
  identically**, proving the refactor moved plumbing and not maths.
- `hotspots.py` sanity check now **PASSES or FAILS out loud** instead of printing
  the condition and leaving the reader to check by eye. Rule 26.
- `.gitignore` had a missing newline gluing `.DS_Store` to `data/*.png`, so
  **neither rule worked**. Fixed. Results, hotspots and heatmaps now tracked —
  they are small, and they are the evidence.
- `signs.json` was missing the sign's top line, **GATE A-C ->**, present
  throughout the shoot. Same board, same position, nothing re-measured, no
  distance changed. It makes the audit claim STRONGER: the sign lists three
  destinations and TOILETS and LOUNGE are on none of them. A signage **gap**,
  not a sparse sign.
- `show_origin.py` draws the calibration corners on a real frame. The tile
  diamond sits on the actual tiles — confirmed by eye.
- U-turn timing offset found: `find_uturns` stamps frame `i` but compares heading
  at `i` vs `i + hold`, so the marker lands ~1 s **before** the visible pivot.
  Systematic, inside the ±3 s tolerance, affects no score. **Reported, not fixed
  —** changing detector behaviour after seeing held-out results is the exact
  thing this project is built to avoid.

**Notes:** Started with three hours of admin that turned out to be necessary.
The project-folder copy of this file was a **Day 8 version** — 1300 lines, rules
stopping at 22, the word "odd" appearing zero times — while claiming to be
current at `35ee54d`. Separately, commit `0f089fb` carried the message
"Re-date Day 13-21 headers", changed 43 lines, and changed **no dates at all**.
Both caught by checking rather than reading. Rules 47 and 48 below.

**Quiz score: 3/3 (multiple choice — easier than cold recall, Rule 13).**
Q1 why a second `--all` run is contamination even with no changes; Q2 why
`min_seconds` must not drop to 1.5 after seeing the miss; Q3 which command
exposed `0f089fb` and what it had really changed.

## Day 16
'@

# ---- 3. rules 47 and 48 -------------------------------------------------
$rules = @'

47. **A commit message is a claim; the diff is the evidence.** Commit `0f089fb`
    was titled "Re-date Day 13-21 headers", changed 43 lines, and changed no
    dates at all — it was the Day 12–14 housekeeping: three checkboxes ticked,
    the 8/9 quiz recorded, Day 19 expanded, rule 46 added. All of it correct,
    all of it filed under a label describing something else, which made real
    work findable only by accident. Second occurrence in four days — the
    `MAX_GAP` whitespace replace on Day 14 also shipped a message for a change
    that had not happened. `git status` before `git add` catches the wrong
    *files*. Only `git show <hash> --stat` catches a commit whose *message*
    outran its content. Verify the number first, then put it in the message:
    "7 insertions, 7 deletions" is a claim you can be held to.

48. **A `}` alone on a line ends the command.** An `if { }` / `else { }` pasted
    into the console across several lines dies with "the term 'else' is not
    recognized" — and the write that lived inside the `else` never happens while
    every line before it reports success. Keep `} else {` on one line. In a
    `.ps1` file the same code runs fine, which is why this only bites when
    pasting. Sibling of Rule 17: the failure is loud in the wrong place and
    silent in the right one.

49. **A conditional is not a check.** `hotspots.py` printed "SANITY CHECK PASSES
    if every hotspot is on the approach side" — the same sentence whether it
    passed or failed, leaving a human to verify by eye. A check that cannot fail
    out loud is documentation, not a check. It now prints PASSED or FAILED and
    names the offending hotspot. Rule 26's sibling.

50. **When a plan's contingency meets a rule made later, record the override.**
    Day 15's block said to fix the detector if recall was poor. Recall was poor.
    Fixing it would have contaminated the held-out evidence — a discipline
    adopted after that contingency was written. Overriding an old plan is often
    correct; doing it silently is how a project loses track of what it decided
    and why.
'@

foreach ($x in @(@($oldBoxes, $newBoxes), @($oldStatus, $newStatus))) {
  if ($t.Contains($x[0])) { $t = $t.Replace($x[0], $x[1]); Write-Host "ok" }
  else { Write-Host "PATTERN NOT FOUND"; $fail = $true }
}

if ($fail) {
  Write-Host "ABORTED - nothing written to disk"
} else {
  $t = $t.TrimEnd() + "`r`n" + $rules
  [System.IO.File]::WriteAllText($p, $t, (New-Object System.Text.UTF8Encoding $false))
  Write-Host "Written, no BOM"
}
