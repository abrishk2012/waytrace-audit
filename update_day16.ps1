# update_day16.ps1 - surgical edit of PROGRESS.md. Writes NOTHING unless every
# pattern matches. Run from anywhere; paths are absolute.

$ErrorActionPreference = "Stop"
$path = "C:\Users\Admin\Documents\WayTrace\PROGRESS.md"
$text = [System.IO.File]::ReadAllText($path)
$text = $text.Replace("`r`n", "`n")   # normalise; restored on write
$abort = $false

function Swap([string]$old, [string]$new, [string]$label) {
    if (-not $script:text.Contains($old)) {
        Write-Host "FAIL: $label" -ForegroundColor Red
        $script:abort = $true
        return
    }
    $script:text = $script:text.Replace($old, $new)
    Write-Host "ok:   $label" -ForegroundColor Green
}

# ---- 1. Day 16 checklist boxes ----
$old16 = @"
- [ ] Upload / select video
- [ ] Analyse button + progress indicator
- [ ] Show the processed video
"@
$new16 = @"
- [x] Upload / select video
- [x] Analyse button + progress indicator
- [x] Show the processed video
"@
Swap $old16 $new16 "Day 16 checklist boxes"

# ---- 2. Day 16 status / notes / quiz ----
$oldStatus = @"
**Status:**
**Notes:**
**Quiz score:      /3**

## Day 17
"@
$newStatus = @"
**Status:** COMPLETE. All three boxes. Streamlit dashboard runs; both sources
show the same things.

**Notes:**

DAY 16 RAN A DAY EARLY (Thu 27 Aug), Day 15 having finished on schedule.

THE DASHBOARD (``dashboard/app.py``, 5618 bytes)
- Radio: recorded clip (13 pre-computed) or upload.
- Recorded path: selector reads ``trips_examined`` from ``results.json``, plays the
  h264 copy from ``data/web/``.
- Upload path: file written to ``data/uploads``, Analyse runs undistort -> track ->
  ``analyse_one`` as subprocesses, each failure surfaced in the UI with its last
  five output lines. Progress bar driven by the tracker's own ``Frame N`` prints -
  no change to ``trajectories.py``.
- Tracked video re-encoded to h264 and shown above the events table, so the
  upload path displays what the recorded path displays.

TIMING - MEASURED, NOT GUESSED (Rule 43)
``cuda False``: yolo11m runs on CPU. clip2, 324 frames, 177.85 s = **0.549 s per
frame, 8x slower than realtime**. All 13 clips = 20,157 frames = **~3 h 04 m**.
Largest, clip1 at 2691 frames, is ~25 min. Consequence: a full re-run is a
three-hour wall-clock cost and must be planned, not discovered on Day 21.
This killed the live-Analyse-in-the-demo design. The button is real and stays,
but the demo shows pre-computed results; the "~8x video length on CPU" figure is
printed next to the button as a spec, not an apology.

THE EVIDENCE WAS NOT IN GIT
``.gitignore`` line 18, ``data/output/*``, was hiding all 13 ``_traj.json`` files - the
0.17 MB of text every result in this project is computed from. ``results.json``,
``hotspots.json`` and the heatmaps were tracked; **the inputs to them were not**. The
repo held the conclusions and none of the evidence, and the evidence existed in
exactly one untracked folder on one laptop. Fixed with ``!data/output/*_traj.json``;
13 files committed as ``2ed4fce``.

DETERMINISM CONFIRMED (a free result)
Re-running the tracker on clip2 returned MD5 ``F5541AE670F7A963EC93676A29ACD763``,
byte-identical to before. Same video in, same file out. Anyone who clones the
repo and runs it gets these numbers, not numbers that wobble.

THE BROWSER WOULD NOT PLAY THE PROCESSED VIDEOS
OpenCV writes ``FMP4`` (mpeg4 Simple Profile). Edge draws a full player, shows
``0:00``, and silently refuses to decode - **no error anywhere**. Confirmed by
dragging the file into the browser, not deduced from the fourcc. All 13
re-encoded to h264/avc1/yuv420p into ``data/web/`` in ~19 s each; the boxes were
already burned into the pixels, so YOLO was not re-run. ``data/web`` is 79.3 MB and
stays out of git - regenerate with the ffmpeg loop.

``analyse_one.py`` - AND WHY ``build_events.py`` WAS NOT TOUCHED
``build_events.py`` filters tracks against ``trip.csv`` before any detector runs. An
uploaded video has no trips, so it would be skipped and return zero events with
no error. Rather than add a branch to the file that guards the held-out
evidence, uploads got their own script. **``build_events.py`` diff is unchanged
since Day 15 and stays that way to submission.**
- All eight thresholds passed **explicitly**, because the function defaults
  (``max_speed=0.25``, ``min_seconds=1.5``, ``max_gap=1.0``, ``min_speed=0.15``) are NOT
  the locked values (0.30 / 2.00 / 0.00 / 0.20). Silence would have run different
  maths and produced plausible, unvalidated events. **Rule 51.**
- EQUIVALENCE TESTED: clip10 gives 4 events identical to ``results.json`` in type,
  second and position to 3 dp; clip6 gives 0 in both. The upload path gets the
  same maths the 25 labelled trips got.

UPLOAD IS RESTRICTED TO THIS CAMERA - stated on screen
A checkbox offering "undistort or not" was considered and **rejected**: it hands
the project's hardest judgement call to someone who cannot make it, and judging
is video-only so there is no chance to explain the tick. The homography maps
this camera's pixels to metres on this floor. Another camera means real
detections at meaningless coordinates, printed confidently. Recalibration is a
~20 min deployment step, and saying so is stronger than pretending the limit is
not there.

P AND R ARE NOT SHOWN FOR UPLOADS, and the dashboard says why
They are measured against hand-made labels. Uploaded footage has none. The
62% / 56% figures stay attributed to the 25 labelled trips.

TWO FILES WERE SILENTLY CLOBBERED TODAY, BOTH RECOVERED FROM GIT
- Morning: the working copy of PROGRESS.md was the **Day 14** version - 1300
  lines, rules stopping at 22, dated 8/26 23:07 - while git held 2371 lines to
  rule 50. ``docs/limitations.md`` and ``update_day15.ps1`` were absent from disk
  entirely. All three restored. The handoff warned about exactly this and it was
  still true. **Rule 46, confirmed a second time.**
- Midnight: ``analyse_one.py`` was overwritten with a copy of the dashboard (133
  insertions, 87 deletions). It printed Streamlit warnings and wrote nothing.
  Recovered by ``git restore`` **only because it had been committed 40 minutes
  earlier**. This is the small-commits discipline paying out in real time.

KNOWN GAP, CARRIED TO DAY 17
The app's chain is upload -> undistort -> track. The real pipeline is raw -> CFR
-> undistort -> track. **The app skips CFR.** Raw footage is 1280x720 at variable
frame rate; cfr and undist are both 1024x576, so the app cannot tell them apart
by dimensions and cannot detect a pre-undistorted file. Uploading from
``data/undist`` double-undistorts (visible bowing on the right-hand doorframe);
uploading raw would break every frames-to-seconds calculation, all of which
assume exactly 15 fps. Right now only ``data/cfr`` files are correct input.

**Quiz score:  2 /3**
Q1 (why no P/R on uploads) and Q3 (why upload is camera-restricted) correct
first time. Q2 (why all eight thresholds are passed explicitly) needed three
explanations before it landed. Recorded as 2/3, not 3/3.

## Day 17
"@
Swap $oldStatus $newStatus "Day 16 status / notes / quiz"

# ---- 3. append Rule 51 ----
$anchor = "50. **When a plan's contingency meets a rule made later, record the override.**"
if (-not $text.Contains($anchor)) {
    Write-Host "FAIL: rule 50 anchor" -ForegroundColor Red
    $abort = $true
} else {
    Write-Host "ok:   rule 50 anchor found" -ForegroundColor Green
}

$rule51 = @"

51. **A default is a value you did not choose.** ``find_hesitations`` defaults to
    ``max_speed=0.25``; the locked value is 0.30. Calling it without naming every
    argument runs maths that was never validated, produces events that look
    entirely reasonable, and raises nothing. Pass every threshold explicitly,
    every time.
52. **Same filename, different folder, same output path.** ``trajectories.py`` names
    its output from ``basename`` only, so ``raw/clip2.mp4``, ``cfr/clip2.mp4`` and
    ``undist/clip2.mp4`` all write to ``clip2_traj.json``. A timing test on the wrong
    copy would have silently overwritten a file every Day 15 number depends on.
53. **A player that draws controls has not necessarily decoded anything.** Edge
    showed a full video player, ``0:00``, and an empty scrub bar for a codec it
    could not read. Absence of an error is not evidence of playback - drag the
    file into the browser and press play.
"@

if (-not $abort) {
    $text = $text.TrimEnd() + $rule51 + "`n"
    Write-Host "ok:   rules 51-53 appended" -ForegroundColor Green
}

# ---- write, or not ----
if ($abort) {
    Write-Host ""
    Write-Host "ABORTED. Nothing written." -ForegroundColor Red
} else {
    $text = $text.Replace("`n", "`r`n")   # restore Windows line endings
    $enc = New-Object System.Text.UTF8Encoding $false
    [System.IO.File]::WriteAllText($path, $text, $enc)
    Write-Host ""
    Write-Host "WRITTEN. Now verify with git diff --stat before committing." -ForegroundColor Cyan
}
