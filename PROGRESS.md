# WayTrace Audit — Build Tracker

**Hackathon:** VoltHacks 2026 (Devpost)
**Hard deadline:** Sat 5 Sep 2026, 17:00 EDT = **22:00 Lisbon time**
**Target finish:** Day 22 (Tue 1 Sep) — SUBMIT. Days 2–5 Sep are four buffer days.
**Re-planned again:** Wed 26 Aug (Day 12), resolving the 12-blocks-into-11-days
collision. Signage OCR cut; live sensor mode cut to a post-submission addition.
**Re-planned:** Wed 19 Aug, after lens calibration overran by two days.
**Builder:** solo, 14, learning Python

---

## How to use this file

At the end of every working day:

1. Tick the boxes you actually completed. Do not tick things that "nearly" work.
2. Fill in **Status**: `DONE` / `PARTIAL` / `BLOCKED` / `SKIPPED`.
3. Write one line in **Notes** about what broke or what you learned.
4. Record your **Quiz score** (Claude asks you 3–5 questions each night).
5. Paste this day's block back to Claude at the start of the next session.

**How the tracker gets updated — Claude does it, not me.**
I do not hand-edit this file. At the end of every working day, and any time
this file needs changing:

- I upload the current `PROGRESS.md` into the chat FIRST. Claude's own copy is
  routinely stale — on Day 15 and again on Day 16 the project-folder copy was
  a Day 8 version, 1300 lines with rules stopping at 22, while git held 2371
  lines to rule 50. **Rebuilding from a held copy silently deletes over a
  thousand lines of real work.** Rule 37, Rule 46.
- Claude then produces the **complete updated file as a download** in the chat.
  Not pasted text for me to copy. Not a patch script I have to run. A file.
- I save it over `PROGRESS.md`, then verify with `git diff --stat` and
  `Select-String -SimpleMatch` before committing.

Rule: if a quiz score is below 3/5, we re-teach before moving forward. Understanding is not optional — you have to defend this project.

**Commit rule: commit after every working chunk, not once at the end of the day.**
Many small commits per day. Each one is a save point you can go back to.

---

## The one-sentence version (memorise this)

> WayTrace analyses anonymous passenger trajectories from fixed-camera footage to find wayfinding-friction hotspots, then audits the signage around those locations.

## The five words that keep you honest

- Say **"hesitation event"**, never "this person was confused".
- Say **"possible signage issue associated with this hotspot"**, never "this sign caused it".

---

## Decisions locked in on Day 1

- **UI = Streamlit.** FastAPI + Next.js dropped. Solo, 23 days, beginner Python —
  those buy zero judging points over a clean Streamlit dashboard.
- **Processing separated from display.** Pipeline writes `results.json` + an
  annotated MP4; the dashboard reads them. A slow CPU can never break the demo.
- **Homography added (Day 5).** Thresholds become "0.3 m/s for 2 s", not
  "3 px/frame". Physical, camera-independent, defensible. ~20 lines of code.
- **Backtracking is optional.** Two behaviours validated properly beat three
  half-working. If Day 13 fails, mark SKIPPED without regret.
- **Hardware framing.** VoltHacks is a hardware/IoT hackathon; WayTrace is pure
  software. Fix = a camera is a sensor. Live webcam mode (Day 18) + CPU-only
  edge inference, footage never leaves the building. Hardware story and privacy
  story from one feature.
- **Judging is async video-only.** No live Q&A expected. That makes the demo
  video carry 100% of the score — so the footage has to be right.

---

## Decision locked in on Day 4 — Intel AI Global Impact Festival: NOT entering 2026

- Global nomination window is 1 Jul – 30 Aug 2026, but that is when **countries**
  pass their picks up to Intel. Country-level selection happens *upstream* of it
  (Poland's national deadline was 1 July — the same day the global window opened).
- Portugal's route runs through the entrepreneurship ecosystem, not school offices.
  The 2025 Portuguese winner (CropVision, Colégio Novo da Maia) came via a school
  startup incubator and Junior Achievement Portugal — a network built over a year+,
  not something to plug into in 16 days.
- 30 Aug also falls on Day 18 — **three days before precision/recall exist (Day 20)**.
  Entering would mean submitting the version of WayTrace without its evidence.
- **Plan: enter 2027** with a finished, validated system. Still in the 13–17 bracket.
- **Sept/Oct action:** look up Junior Achievement Portugal and find the real door.
- Build the Intel-facing parts into WayTrace anyway — they improve VoltHacks too:
  OpenVINO (Day 18), SDG 11 framing in the README, responsible-AI section (Day 21).

---

## MUST HAVE (never sacrifice these)

- [x] Person detection
- [x] Anonymous tracking IDs
- [x] Trajectories drawn on video
- [x] Real-world units via homography
- [x] U-turn detection — v1 Day 12, untuned
- [x] Hesitation detection — v1 Day 12, untuned
- [x] Hotspot clustering — Day 14, grid density not DBSCAN. 2 hotspots, count stable across a 3x range of cell size
- [ ] Precision / recall numbers from hand-labelled ground truth
- [ ] Polished dashboard
- [ ] Demo video

## SHOULD HAVE — cuttable, in this order

- ~~Signage OCR + arrow direction (Day 18)~~ — **CUT on Day 12, 26 Aug.**
  Twelve blocks of work against eleven calendar days. Sign wording is hardcoded
  instead: the corridor signs are fixed and their text is already known, so the
  signage audit survives and only the *reading* of it is manual. OCR automates a
  fact already in hand; it does not earn a day.
- ~~Live webcam "sensor mode" + OpenVINO (Day 19)~~ — **CUT on Day 12, 26 Aug**,
  to bring the finish date to 1 Sep. Becomes a post-submission addition on the
  2–5 Sep buffer, re-submitted via Devpost edit if the buffer is genuinely free.

## CUT on 19 Aug

- ~~Backtracking detection~~ — flagged optional on Day 1. Two behaviours validated
  properly beat three half-working.
- ~~Automatic sign detection~~
- ~~Before/after signage experiment~~

---

## Camera configurations

| Name | What it is | Status |
|---|---|---|
| camA | Original wall mount, before tilting | superseded |
| camB | Tilted on mount to fix the arch ID switch | superseded |
| camC | Remounted after coming off the wall for lens calibration | **current** |

**File naming:** `date_location_cameraSetup_take`. Calibration videos omit the
camera letter, because lens calibration doesn't care where the camera is.

**Location word is `flat`, always.** `hall` was used once by mistake on Day 5.
Two words for one place is how you lose a file.

**camC is now load-bearing.** The homography is built for this exact mount.
Knock it and the homography is scrap — recording, clicking and testing all
have to be redone.

---

# WEEK 1 — Make the computer see people

## Day 1 — Thu 13 Aug — Video conversion + first detection
- [x] Convert `test_people.avi` to MP4 with FFmpeg
- [x] Watch the MP4 and describe what's in it
- [x] Confirm OpenCV can read it frame by frame
- [x] Run YOLO on a single frame, see boxes around people

**Status:** DONE

**Notes:**
- FFmpeg conversion worked (`-crf 18`, H.264). Kept the AVI.
- Video specs: 360x288, 25 FPS, 179.2 s, 4480 frames. OpenCV read 4480/4480 — clean.
- **Judged the terrace footage UNSUITABLE for the final demo.** No stopping, no
  destination, no decision point, no signage. Test rig only — never shown to judges.
- First YOLO run (`yolo11n.pt`, `imgsz=960`, `conf=0.25`, `classes=[0]`) on frame 2000:
  **7 people found**, confidences 0.73–0.90.
- Two failure modes spotted by eye:
  1. **Occlusion** — one box (0.89) swallowed a person standing behind another.
     Expect ID switches here on Day 2.
  2. **Duplicate box** — a second, low-confidence (0.40) box latched onto one
     person's legs. Lowest confidence in the frame = the model signalling doubt.
- Speed: ~383 ms/frame on CPU → ~30 min to process this 3-min clip.
  Frame-skipping will be needed on Day 3.
- `yolo11n.pt` downloaded to project root → **must go in `.gitignore` on Day 21.**
- Lesson learned: VS Code's file tree can disagree with what's on disk.
  `Get-ChildItem` is the ground truth.

**Quiz score: 1.5/5 → retaught, re-tested, PASSED**
- Q1 (the frame loop) — missed. Re-taught, then answered correctly.
- Q2 (`conf` threshold) — half. Knew high = misses real people; didn't have
  low = invents fake people → fake trajectories → fake events → poisoned hotspot.
- Q3 (why footpoint not box centre) — correct.
- Follow-up lesson: a silent infinite loop is worse than a crash. Loud bugs are a
  gift; quiet wrong numbers are the dangerous kind. This is why Day 19 ground-truth
  labelling exists.

## Day 2 — Fri 14 Aug — Tracking
- [x] YOLO + ByteTrack running over the whole video
- [x] Each person keeps the same ID number across frames
- [x] Count how often IDs wrongly switch

**Status:** DONE

**Notes:**
- `model()` → `model.track(persist=True, tracker="bytetrack.yaml")`. `persist=True`
  is the load-bearing word: without it the tracker wipes memory every frame and
  everyone gets a new number forever. No persistence → no trajectories → no WayTrace.
- `lap` auto-installed by Ultralytics on first tracking run (ByteTrack needs it).
- **First run was on the wrong 500 frames.** Frames 0–500 are nearly empty (0–2
  people). Re-ran from frame 1800. Lesson: a clean-looking number from the wrong
  slice of data means nothing. Applies directly to Day 20 metrics.
- Results on frames 1800–2300 (500 frames, 20 s):
  - 43 unique IDs created, but only **5–8 alive at any moment**
  - Average people visible per frame: **5.78** (cross-checks against the
    "IDs alive right now" readings — two independent numbers agreeing)
  - After a 25-frame minimum filter: **19 real tracks, 24 fragments discarded**
  - Longest tracks: ID 40 = 303 frames (12.1 s), ID 26 = 289 frames (11.6 s)
- **ID switches counted by eye: ~15 wrongly-created IDs** in 20 s. Caveat recorded
  honestly: the preview video draws ALL boxes with no 25-frame filter, so that
  count mixes genuine switches with fragments. Me and the filter were counting
  different things. → **Define what counts as an event BEFORE counting, on Day 19.**
- **Main finding: crossings are where tracking breaks.** Predicted from the Day 1
  still image (occlusion), confirmed on video on Day 2. Directly shapes the shoot:
  position the camera so walkers don't line up behind each other.
- ~19 real tracks for ~8–10 actual people → roughly half are the same person
  counted twice. **Deliberately NOT fixing this.** 360x288 + crowding is near
  worst-case; my own footage is 1080p with 3 people. Tuning ByteTrack for footage
  no judge will ever see is wasted time. Measured, recorded, revisit after Sunday.
- Discipline rule adopted: **change one thing, measure, then change the next.**
  Resisted raising `conf` at the same time as adding the filter, so the improvement
  is attributable.
- `annotate_tracking.py` writes `data/output/tracked_preview.mp4` with per-ID
  colours and footpoint dots. Colour change mid-walk = ID switch, visible by eye.

**Quiz score: 1/3 → retaught, re-tested 2/2, PASSED**
- Q1 (`persist=True`) — missed, re-taught.
- Q2 (why fragments are dangerous) — missed, re-taught. A 1-frame track has a
  position but no movement → reads as "never moved" → fake hesitation event →
  fake coordinate → poisoned hotspot. Junk doesn't stay junk-shaped; it comes out
  the far end looking like a finding.
- Q3 (colour change) — partial. Knew the ID changed, not why it matters.
- **Re-test passed both.** Best insight of the day, my own words:
  *"you need another frame to compare what moved and what stayed."*
  Movement is not a property of a frame — it's a property of the GAP between two
  frames. One frame is a photograph and nothing in a photograph ever moves.
  Speed, heading and velocity don't exist until there are two positions and a
  time between them. Foundation for Day 6 (velocity) and Day 7 (U-turn angles).
- Note on pacing: 1/3 came at the end of a long second session. Retention drops
  when saturated. Break before re-testing rather than pushing through.

## Day 3 — Sat 15 Aug — Trajectories
- [x] Store position history per track ID (footpoint, not box centre)
- [x] Draw coloured trails behind each person
- [x] Save an annotated output video to `data/output/`

**Status:** DONE (finished early, on Day 2 evening)

**Notes:**
- The one line the whole project rests on:
  `trajectories[track_id].append((foot_x, foot_y, frame_number))`
  A dict of track ID → ordered list of (x, y, frame). Everything downstream —
  speed, heading, U-turns, hesitation, hotspots — reads from this structure and
  never touches the video again.
- Storing `frame_number` in each point is what makes *time* available. Two
  consecutive points are 1/25 s apart; that's what turns a distance into a speed.
- **Cross-check passed:** point counts today matched frame counts from Day 2
  exactly (ID 40 = 303 both times, ID 26 = 289 both times). Confirms one point
  stored per frame per track, nothing dropped or doubled.
- **Bug found and fixed: ghost trails.** The draw loop iterated over every track
  that had EVER existed, so people who left the frame at frame 200 still had
  trails painted at frame 500. Floor filled with trails attached to nobody.
  Fix = read `points[-1][2]` (last seen frame) and `continue` if it's more than
  5 frames stale. 5 rather than 0 so a one-frame tracker dropout doesn't flicker.
- **Bug found and fixed: indentation.** Pasted the new loop at column 0, which
  pulled it out of the `while`. Would not have crashed — would have silently
  written a 1-frame video. Reminder that Python indentation decides which loop
  code belongs to, and that the dangerous bugs are the ones that don't crash.
- **Remaining artefact, deliberately NOT fixed today: trail spikes at crossings.**
  When two people overlap, YOLO's box stretches or clips and the BOTTOM EDGE
  moves. Footpoint = bottom edge, so the trajectory records a jump the person
  never made. Downstream that reads as a huge one-frame speed AND a sudden
  heading change — exactly the pattern the Day 7 U-turn detector looks for.
  **Detection noise becomes fake behaviour.** This is why Day 6 (smoothing) comes
  BEFORE Day 7 (U-turns). Needs velocity defined first to say what "impossibly
  fast" means, so fixing it now would be guessing.
- Same root cause — occlusion at crossings — has now produced three different
  symptoms across three days: merged boxes (Day 1), ID switches (Day 2),
  footpoint spikes (Day 3).

**Quiz score: n/a — day finished early, quiz folded into Day 2**

## Day 4 — Sun 16 Aug — FOOTAGE DECISION DAY
- [x] Decide the final judge-facing footage (staged recording vs public dataset)
- [x] If staging: plan the corridor, the sign, the walkers
- [x] If dataset: confirm the licence in writing — n/a, staging

**DECIDED ON DAY 1 — staging my own footage.** Carry these constraints in:
- Cast: me, mum, sister (10). Only 3 people.
- **Not a problem: 3 people x 6–8 trips each = 20+ anonymous journeys.**
  The tracker has no memory — each re-entry is a brand-new ID. Real airport
  cameras aggregate over time too, not all at once.
- **Learning effect is the real risk.** By trip 3 they know the route and stop
  hesitating. Fix: 4–5 different paper destinations (`GATES A–C`, `BAGGAGE CLAIM`,
  `TOILETS`, `EXIT`, `LOUNGE`), a different one called out each trip. Vary the
  start direction too. Residual effect goes in the limitations section, stated plainly.
- Everyone on camera consents first. Raw video deleted after processing; only
  anonymous trajectories kept.
- Day 1 showed occlusion breaks detection → position the camera so walkers don't
  line up behind each other.

**LOCATION CONFIRMED (Day 2 evening) — the flat.** Mum has agreed to the 2-hour slot.
- Layout: front door → entrance hall → arch → corridor → dining area, with doors
  opening off both sides. Real approach walk AND a real fork. Good enough.
- **Floor is regular square tiles** → free homography grid.
- Clear the shoes, bags and rug out of shot. Judges see this footage — tidy reads
  as "controlled experiment", clutter reads as "filmed in a hurry".

**Status:** DONE

**Notes:**

### Camera changed: phone → wall-mounted EZVIZ CCTV
Phone wouldn't mount safely. This turned out **better**, not worse:
- The camera physically cannot move mid-shoot — biggest shoot risk eliminated.
- Already mounted high → less occlusion, which Days 1–3 proved is the main enemy.
- **The hardware framing stops being a metaphor.** WayTrace now runs on an actual
  fixed wall sensor, not a phone pretending to be one. Say exactly that in the demo.

### Measurements
- **Tiles: 29.4 x 30.8 cm.** Measured 5 tiles across (1.47 m / 1.54 m) and divided
  by 5. Not square — that's fine, homography doesn't need squares, it needs the truth.
- **Why 5 and not 1:** the tape error (~1 cm) stays the same size whatever you
  measure, so spreading it over 150 cm instead of 30 cuts the per-tile error
  five-fold (3% → 0.6%). It caught a real mistake — the eyeball guess said 30x31,
  a 2% error that would have propagated into every speed the system ever reports.
- **Approach distance: 9 tiles ≈ 2.7 m.** That is the ceiling. No camera position
  in the flat gets more. Tested the arch entry (+1 tile) and the front door (9 total).

### CONSEQUENCE — hesitation spec changed (affects Day 9)
2.7 m is under 2 seconds of walking. There is not enough normal walking to
establish a person's own baseline before the decision point.
- **Day 9 changes from** "compare against that person's own normal walking speed"
  **to** an absolute speed threshold (speed < X m/s sustained for Y s), with X and
  Y tuned against hand labels on Day 10.
- **This is a downgrade and it gets stated plainly in limitations:**
  > "Hesitation is detected against a fixed speed threshold rather than a
  > per-person baseline, because the capture space (2.7 m of approach) is too
  > short to establish an individual walking baseline. In a real deployment with
  > longer approach corridors, a per-person baseline would be preferred."
- **U-turn detection is unaffected.** A heading reversal is the angle between the
  before and after vectors — it needs no baseline at all. The headline behaviour,
  and the most visually obvious one in a demo, is untouched.

### CCTV records VARIABLE frame rate — every import must be converted
- Camera reports ~15.14 fps with tbr 15.17. Two different numbers describing what
  should be one rate = variable frame rate.
- **Why this is dangerous:** trajectories store `(x, y, frame_number)` and never a
  timestamp. **Frame numbers ARE the project's clock.** Speed = distance ÷ time, and
  the time comes from counting frames. If frames aren't evenly spaced, every speed
  is wrong — and worst during fast motion, because that's when cameras drop frames.
  It would not crash. It would hand back reasonable-looking numbers that are ~10% off.
- **Fix, on every single import:**
  `ffmpeg -i in.mp4 -r 15 -an -c:v libx264 -crf 18 -pix_fmt yuv420p out_cfr.mp4`
  Confirmed 15.0 exactly afterwards with `check_video.py`. `-an` strips audio —
  smaller files, and voices in a privacy-focused project are a liability.
- Resolution confirmed **1024x576**, read from the file itself rather than trusting
  the app's settings screen.

### MODEL CHANGED: yolo11n → yolo11m, imgsz 960 → 640
Measured on one frame, one variable at a time:

| model | best conf | boxes | speed |
|---|---|---|---|
| yolo11n | 0.45 | 2 (split) | 172 ms |
| yolo11s | 0.63 | 2 (split) | 253 ms |
| **yolo11m** | **0.85** | **1 (clean)** | 622 ms |

- **imgsz=1280 produced ZERO detections.** Bigger input is not better — YOLO was
  trained near 640, so a much larger input no longer matches the patterns it learned.
  960 gave 0.38; 640 gave 0.45. Tested, not assumed.
- 622 ms is acceptable **because of the Day 1 decision** to separate processing from
  display. ~19 min for a 2-min clip, run offline while doing something else.
- **The honest tradeoff, to say out loud:** medium is a heavier model, which slightly
  weakens the cheap-edge-sensor story. Answer: WayTrace runs offline on CPU, no cloud,
  no GPU, footage never leaves the building. Accuracy over speed was deliberate —
  a missed detection is a missed event, and this is an audit tool, not a real-time
  system. OpenVINO (Day 18) answers the speed side.
- Updated in `track_people.py`, `trajectories.py`, `annotate_tracking.py`.
  `.gitignore` already covers it via `*.pt`.

### Silent bug: START_FRAME = 1800
Left over from the terrace clip (4480 frames). The route test has 296. The seek
failed → first `cap.read()` returned False → loop broke immediately → **257-byte
file, no crash**, and it printed "Saved to". Caught by running `check_video.py` on
the output.
- Same family as Day 3's indentation bug and Day 2's wrong-500-frames run:
  **a setting that was correct for one video is silently wrong for the next.**
  Hardcoded numbers don't announce that they've expired.
- Second tell: identical timings to three decimal places (317.7 ms twice) meant the
  code never re-ran at all. Real re-runs vary by milliseconds.

### FIXED: ID switch at the arch → camB
- Symptom: box flickers off, then a **new track ID** appears — while still fully
  visible. So it was a **detection** failure, not a tracker failure: no box → nothing
  for ByteTrack to match → track declared dead → reappears as a stranger.
- `conf` 0.25 → 0.15 did **not** help. That ruled out "weak detection" — YOLO wasn't
  finding me at all there, and a threshold can only rescue a detection that exists.
  Restored to 0.25.
- **Fixed by tilting the camera on its mount.** Never touched the tracker. Fixed
  detection and the tracker fixed itself — the chain was always detection → tracking.
- Why it mattered: a journey split across two IDs contains no complete trajectory,
  so U-turns and hesitation inside it become **invisible**.

### PARTLY FIXED: footpoint offset → now a fisheye problem (Day 5)
- Original cause: camera was tilted, so an upright person appeared diagonal, and
  YOLO's axis-aligned box put its bottom edge at the lowest foot rather than the
  centre. Footpoint landed beside the walker on empty floor. **Systematic, not
  noise** — same direction every frame, survives smoothing, becomes a real offset
  in metres after homography. YOLO has no rotated-box option.
- After tilting the camera the dot sits under the feet **near frame centre**, and
  drifts toward the **edges** — barrel distortion from the CCTV's wide lens.
- **This is the same error that will corrupt homography**, since homography assumes
  straight world lines stay straight in the image. Undistortion therefore belongs
  with homography on Day 5, not as a separate task.
- Rejected a StackOverflow MATLAB snippet: wrong language, **guesses** the distortion
  (`k = 1.5`) instead of measuring it, and has a bug (reuses `k` as a loop counter).
  Correct approach: `cv2.calibrateCamera` on a chessboard, then `cv2.undistort`.
- **Shoot decision: keep the walking path near frame centre**, where distortion is
  mildest. Free accuracy.

### Still to do before the real shoot
- [x] Record 30 s of the **empty room on camC** — done Day 5.
- [ ] Clear the floor completely: shoes, slippers, rug, trolley, shoe rack. The rug
      especially — it covers the tiles. **The robot vacuum too** — it's in the
      bottom-left of the camC frame.
- [ ] Make the signs (see below).
- [ ] Fragment filter must become `int(fps * 1.0)`, not hardcoded 25. At 15 fps,
      25 frames = 1.7 s, and with a 2.7 m corridor that would silently discard
      real tracks.

### The signs
One wall sign at the fork, A4, thick black marker, eye height:

```
GATES A-C        →
BAGGAGE CLAIM    ←
EXIT             ←
```

*Arrow corrected Day 16: `EXIT` points LEFT, the same way as `BAGGAGE
CLAIM`, not up. `data/signs.json` recorded it correctly as `EXIT <-` when the
physical sign was measured on Day 14; this planning block had it wrong and
nobody had compared the two. The measured file was right, the plan was not.*

Five A5 destination cards: `GATES A-C`, `BAGGAGE CLAIM`, `TOILETS`, `EXIT`, `LOUNGE`.

**`TOILETS` and `LOUNGE` are deliberately NOT on the wall sign.** That's the
missing-destination failure mode — the walker reads a perfectly legible sign and
still can't resolve it. Real hesitation, not acted hesitation.

The destinations are fake, which is the point: nobody knows which real door is
"GATES B" unless the sign says so. That's what defeats the learning effect.

### Shoot protocol
1. Consent on camera first — each person says their name and that they agree.
2. **One continuous recording** for the whole session. Don't stop between trips —
   consistent timestamps, and each re-entry naturally becomes a new track ID.
3. Per trip: walker waits out of frame → show them a destination card → say **"go"**
   out loud → they walk at normal pace, read the sign, decide, exit.
4. **Wait 5 full seconds between people. Never two in frame at once.** Occlusion is
   what broke Days 1, 2 and 3.
5. Never tell them which door is which. The sign is the only source of truth.
6. Don't let them perform confusion — fake hesitation poisons Day 19 ground truth.
7. Target 21 trips (~7 each), roughly two-thirds using the missing destinations.
   Stop at 21 or 2 hours, whichever first.
8. A trip is not clean if two people overlapped, someone left the shot, or the
   camera was knocked. Note the wasted ones and redo them.
9. **The wooden door stays open.** The homography was built with it open, because
   that is how the room will look on shoot day.
10. **Do not touch the camera.** camC carries the homography.

**Quiz score: 2/3 — PASSED**
- Q1 (why variable frame rate breaks things) — got it in my own words: uneven frames
  → wrong counting → less accurate results. Missing piece re-taught: **frame numbers
  ARE the clock**, because trajectories store `frame_number` and never a timestamp.
- Q2 (25-frame filter at 15 fps) and Q3 (why 5 tiles ÷ 5) — not attempted, taught
  directly instead.
- Process note: asked for must-know points to be flagged explicitly rather than
  buried in prose. Adopted going forward.

## Day 5/6 — Mon 17 – Tue 18 Aug — Lens calibration (undistortion)

- [x] Print/display a chessboard pattern and measure the square size
- [x] Record a calibration video through the actual camera at 1024x576
- [x] `cv2.calibrateCamera` → camera matrix `K` and distortion coefficients `dist`
- [x] Verify undistortion **visually**, not just by RMS
- [x] Remount the camera → **camC**

**Status:** DONE

**Notes:**

### The board
- No printer, so the chessboard was displayed **on an iPad screen**. A screen is
  perfectly flat, which is better than a taped-down printout that curls.
- Pattern: **10 x 7 squares = 9 x 6 INNER corners.** `CHESSBOARD = (9, 6)`.
  `findChessboardCorners` counts corners, not squares. Get this wrong and every
  frame silently fails with no error.
- Square size measured on the glass: **5 squares = 9.7 cm → 19.4 mm**. Cross-checked
  against a single-square measurement of 1.9 cm. Two independent measurements
  agreeing is what makes a number trustworthy.
- Never calculate square size from screen resolution — Photos scales the image, so
  file pixels tell you nothing about millimetres on the glass. Measure the glass.
- iPad setup that matters: Auto-Lock **Never**, Auto-Brightness **OFF**, brightness
  ~50% not max (max blooms into the black squares), no pinch-zoom, wipe the screen.
- Room lights ON — if the EZVIZ switches to infrared, an iPad screen becomes a
  featureless grey rectangle.

### The recording
- **`findChessboardCorners` is all-or-nothing.** It needs every one of the 54 inner
  corners visible in a single frame. One square clipped by the frame edge and it
  returns False — no partial credit, no error message, just a silent skip.
- First attempt failed on exactly this: the board was hanging off the frame edge in
  8 of 9 shots. Right positions, board not fully inside.
- Coverage needed: all 9 positions (centre, 4 edges, 4 corners), each with the whole
  board inside, mixed flat and tilted 30–45° in assorted directions.
- **Why tilt matters:** flat-on, a big board far away and a small board close up look
  identical, so focal length and distortion trade off against each other and the fit
  drifts. A tilt makes the near edge measurably bigger than the far edge, and that
  difference is what pins the numbers down.
- Final video: `2026-08-18_flat_calib.mp4`, 1024x576, ~9 minutes, 8340 frames.
- **No `ffmpeg -r 15` needed on a calibration video.** It reads independent still
  frames and never measures time, so VFR is harmless here. CFR conversion is only
  for footage where frame numbers act as the clock.

### Screenshots are NOT camera files
- 36 WhatsApp photos were rejected: 1170 px wide with varying heights (647, 643, 649).
- `K` holds the principal point — where the lens axis hits the sensor. Crop the image
  and that point moves. Crop each image differently and it's trying to fit one lens
  to 36 slightly different cameras. Wouldn't crash. Would produce confident numbers
  describing a camera that doesn't exist.
- **Rule: calibration input must come off the camera at the exact resolution the
  footage will use.** Same principle as measuring the tiles instead of eyeballing them.

### Tuning the view selection — three runs, one variable at a time

| views | how they were chosen | RMS |
|---|---|---|
| 1338 | everything that passed | 2.23 px |
| 40 | first 40 that passed (all from minute 1) | 1.32 px |
| 40 | spread evenly across all 9 minutes | **2.17 px** |

- Blurry frames were passing corner detection. Added a sharpness gate using
  `cv2.Laplacian(gray, cv2.CV_64F).var()`. Threshold was **measured, not guessed**:
  printed the sharpness value into each check-image filename, looked at the 4 bad
  ones, found the worst was 342, set `BLUR_MIN = 360`.
- **`kept < MAX_VIEWS` was silently a "take the beginning" filter.** It stopped at
  the first 40 qualifying frames — all from the opening minute, where the board
  barely moved. Fixed by collecting every view first, then `np.linspace` to sample
  40 evenly across the whole video.
- **The 2.17 is the honest number.** Low error on easy, near-identical views is a
  flattering lie — the same mistake as Day 2's frames 0–500. Real footage has people
  everywhere in the frame, so the hard-test score is the one that matches reality.

### Results — `calibration_ezviz.npz`
- **k1 = -0.41.** Negative = barrel distortion, exactly as predicted on Day 4.
  Stable at ≈ -0.41 across all four runs with different frame sets — that stability
  is what makes it believable.
- Principal point moved between runs (442 to 537), which says that part of the fit
  is still loose. Recorded honestly rather than hidden.
- **Verified visually, which is the test that actually counts:** `undistort_check.jpg`
  and `fisheye_before_after.jpg` both show bent lines becoming straight.
- **Undistortion crops the frame slightly.** Straightening a barrel-bent image pulls
  edge pixels inward and leaves blank wedges, so `cv2.undistort` crops them off.
  Expected, not a bug. May cost a few frames at the start of each approach walk.
  Decide later: accept the crop, or `getOptimalNewCameraMatrix(alpha=1)` to keep the
  full field with black wedges.

### BUG: `check_video.py` had a hardcoded video path
- Line 2 read `video_path = "data/output/tracked_preview.mp4"`. It ignored the
  filename typed on the command line entirely.
- **Reported "300 frames" for four different videos in a row.** Never crashed. The
  number was plausible. Every verification that night was reporting on a Day 2 file.
- Worse than a wrong answer: it sent the whole diagnosis down a false path. We built
  a theory that the EZVIZ header was unreliable. That theory was wrong. **Wrong input
  in, wrong conclusion out — even when the reasoning on top of it is sound.**
- Fixed: reads `sys.argv[1]`, prints which file it's checking, and warns when the
  header count disagrees with the real count.
- After the fix, camC calib clip verified: **1024x576, 15.0 fps, 466 frames, 31.1 s**,
  header and real count in agreement.
- Same family as `START_FRAME` (Day 4) and the indentation bug (Day 3).

### Camera remounted → camC
- `K` and `dist` describe the **camera as an object** — focal length, and how the
  glass bends light. Carry it anywhere, point it anywhere, same numbers. **They
  survive remounting. Never redo them.**
- Homography describes the **camera's relationship to one specific floor**. Nudge
  the mount and every pixel maps to the wrong floor spot. **Scrap on any remount.**

### Process notes
- **Twice in one session an edit "didn't work" because the file was never saved.**
  Tell: a number identical to 4 decimal places after an edit means the edit didn't
  land. That's Rule 4 pointing at the editor, not the code.
- **Stale output in a check folder.** `calib_check/` still held images from the
  1338-view run while displaying 40 new ones. Inspecting yesterday's results and
  drawing today's conclusions. Clear output folders before re-running.
- Python goes in `.py` files; PowerShell goes in the terminal. Pasting one into the
  other produces confusing parser errors.

**Quiz score: 1/3 → retaught, re-tested 2/2, PASSED**
- Q1 (the `check_video.py` hardcoded path) — **correct**, including the important
  half: bad input sent the whole diagnosis to the wrong place.
- Q2 (what `K` and `dist` are) — not known, taught directly.
- Q3 (why the worse RMS is more trustworthy) — not known, taught directly.
- Re-test 2/2: what survives a knock to the mount, and why 100% recall on obvious
  U-turns doesn't belong in the README.
- **Process failure on my side: RMS was used for hours before it was ever defined.**
  Terms get explained the first time they appear, not retroactively.

## Day 5 (carried) — Wed 19 Aug — Homography (pixels → cm)
- [x] Record 30 s of the empty room on **camC**
- [x] Undistort the frame FIRST — homography on a distorted frame maps a bent world
- [x] Click 4 floor points, supply their real-world distances
- [x] `cv2.findHomography` maps image coords to floor coords
- [x] **Accuracy check on tiles OUTSIDE the calibrated region**

**Status:** DONE

**Notes:**

### The empty-room clip
- `2026-08-19_flat_camC_empty.mp4` — 1024x576, 503 frames, 33.6 s.
- `check_video.py` reported header count and real count **in agreement** this time.
  That does not retire the EZVIZ rule. Unreliable is not the same as always-wrong,
  and unreliable is still unusable. Read-until-false stays everywhere.
- **No `ffmpeg -r 15` needed.** One still frame is extracted and no time is ever
  measured, so VFR is harmless. Same reasoning as the calibration video.
- `grab_frame.py` pulls frame 200 by **reading forward and counting** — no
  `cap.set()` seek anywhere. Seeking is what silently broke `START_FRAME` on Day 4.

### Undistort BEFORE clicking — non-negotiable
- `undistort_frame.py` applies `K` and `dist` from `calibration_ezviz.npz` to
  `floor_raw.jpg` → `floor_undistorted.jpg`.
- Verified by eye on the actual floor, not by a number: the door frames on both
  edges of the raw frame **bow outward like a barrel**, and are straight afterwards.
  Black wedges at the corners, exactly as expected from Day 6.
- Homography assumes a straight line in the world stays straight in the picture.
  Feed it a bent world and every centimetre it reports is wrong — silently.
- **RMS 2.17 px was the homework. Bent door frames on the real floor are the exam.**

### The calibration region is 5 x 2 tiles, not 4 x 4 — and why
- Wanted a square-ish block. Couldn't have one. Two things ate the corners:
  1. The wooden door is **open in shot and must stay open** — walkers use it.
  2. The nearest row of tiles runs off the **bottom edge of the frame**, so its
     corner does not exist in the image at all.
- **A corner you cannot see is a corner you must not click.** A guessed click looks
  identical to a measured one in the output — four numbers, no error message, and a
  bent floor forever. Rule 1 in its purest form.
- Settled on **5 tiles along x 2 tiles across = 154.0 x 58.8 cm**.
- Considered shrinking further to 2 x 5 in the other orientation and rejected it:
  two corners nearly touching gives the maths almost nothing in that direction.
- **The calibration frame must show the room exactly as it will be during the shoot.**
  Closing the door for a tidier block would have mapped a floor that won't exist on
  shoot day. Same family as Rule 5 — correct for one situation, silently wrong for
  the next.

### The floor is laid DIAGONALLY
- Tiles run at an angle to the frame, so a tile-aligned block looks like a **diamond**
  on screen. Lost time thinking the corners were being marked wrongly. They weren't.
- Homography does not need a screen-aligned rectangle. Same lesson as the
  29.4 x 30.8 tiles on Day 4: **it doesn't need neat, it needs true.**

### Pixel cross-check before trusting the clicks
Clicked corners, in order: **left, bottom, right, top**
`(399,431)  (473,536)  (755,374)  (668,306)`

- Short edges ≈ **128** and **111** px. Long edges ≈ **325** and **295** px.
- Long ÷ short ≈ **2.5**, and 5 ÷ 2 = **2.5**.
- **Two independent numbers agreeing** — same check that validated the Day 2 track
  counts and the chessboard square size. This is how a number earns trust.

### Real-world coordinates handed to `findHomography`
| click | corner | world (cm) |
|---|---|---|
| 1 | left | (0, 0) |
| 2 | bottom | (58.8, 0) |
| 3 | right | (58.8, 154.0) |
| 4 | top | (0, 154.0) |

x = across (2 tiles x 29.4 cm). y = **along the walking direction** (5 tiles x 30.8 cm).
Order matters absolutely: `findHomography` pairs them **by position in the list**.
Wrong order maps the floor to a bow-tie, without complaining.

### THE ACCURACY TEST — measured, not assumed
Round-tripping the 4 clicked corners returned them exactly (0.0, 58.8, 154.0…).
**That test cannot fail** — it is homework with the answers attached. The real test
is floor the system was never taught.

| clicked point | true value | homography said | error |
|---|---|---|---|
| 1 tile *before* zero, along | -30.8 cm | **-30.2 cm** | **0.6 cm (~2%)** |
| 4 tiles up, along | 123.2 cm | **123.8 cm** | **0.6 cm (~0.5%)** |
| 1 tile left of zero, across | -29.4 cm | **-31.4 cm** | **2.0 cm (~7%)** |

- **Along-axis strong, across-axis weak — exactly what a 5x2 strip predicts.**
  The maths is worst precisely where it was given least. It **failed honestly**
  rather than failing quietly, which is the behaviour you want from a measurement.
- The along-axis is the walking direction — the one every speed is made of.
- Error includes mouse-click precision, so the true error is smaller than shown.
- Had distortion still been uncorrected, a tile outside the taught region would have
  come back as ~38 cm or ~25 cm instead of 30.8. It came back within 6 mm.

### LIMITATION (goes in the README verbatim)
> Homography was built from a 5 x 2 tile region (154 x 58.8 cm), the largest area of
> floor with four unobstructed tile corners visible. Measured error on tiles outside
> that region: **0.6 cm along the walking axis and 2.0 cm across it.** The lateral
> axis is less reliable because the calibration strip is narrow — the open floor
> available was limited by a doorway that must remain open during recording.
> Speeds are computed predominantly along the corridor axis, which is the
> well-calibrated direction.

### Units — `homography_camC.npz` is in CENTIMETRES
Centimetres went in, so centimetres come out. The maths has no idea what a
centimetre is; whatever unit goes in is the unit that comes out.
**Day 9 thresholds are in m/s. Divide by 100, or every speed is 100x wrong —
silently, and it will look almost plausible.**

### `pick_points.py` drew dots it never saved
Red dots existed only inside the popup window; the file on disk stayed clean, leaving
no record of where the clicks landed. Added `draw_points.py` → `floor_points.jpg`,
numbered dots plus a green outline of the strip.
- Four numbers in a terminal look correct no matter where they landed. Drawing them
  back onto the picture is the only way to **see** that they're right.
- Doubles as the README evidence on Day 21.

### Stray file `c` in `data/raw`
A 3.9 MB file with no extension, created at 03:11, that `git status` offered to commit.
- `.gitignore` blocks `*.mp4`. It does not block a file with no name-shape at all.
  **`.gitignore` matches patterns, not intentions.** This is exactly why `git status`
  runs before `git add .`, every single time.
- **`check_video.py` identified it: 15.0 fps exactly.** The camera records 14.97;
  only `ffmpeg -r 15` produces 15.000. **A number told us which tool made the file.**
- It was the queued CFR conversion with a mangled output name. Renamed, not deleted.

### New scripts this session
`grab_frame.py`, `undistort_frame.py`, `pick_points.py`, `build_homography.py`,
`test_homography.py`, `draw_points.py`, `test_one_point.py`

### Naming inconsistency found and fixed
`hall` and `flat` both used for the same location. Standardising on **`flat`**.
Two words for one place is how a file gets lost.

**Quiz score:      /3**


---

# RE-PLAN — Wed 19 Aug

Lens calibration took two days instead of one, so the original schedule is dead.
16 working days remain (Thu 20 Aug – Fri 4 Sep) plus one buffer day.

**Four things changed, and the reasons matter more than the dates.**

### 1. THE SHOOT WAS NEVER ON THE SCHEDULE
The protocol, the signs, the cast, the camera and the consent plan were all
planned on Day 4 — and no day was ever allocated to **actually recording it**.
Every remaining task downstream (tuning, ground truth, metrics, dashboard, demo)
consumes that footage. It is now **Day 9, Sat 22 Aug**, and it is the single
highest-risk item left.

**Shoot earlier if the family can.** Two reasons:
- **camC carries the homography.** Every day the camera sits on that wall is
  another day it can be knocked. A knock before the shoot costs a full rebuild:
  re-record, re-click, re-test.
- **All footage recorded before camC is homography-orphaned.** The route test was
  camB. Those pixels cannot be converted to centimetres by `homography_camC.npz`.
  Until the shoot happens, every detector can only be developed in pixels.

### 2. GROUND TRUTH LABELLING MOVED FROM DAY 19 TO DAY 11
The old plan tuned the detectors on Days 8 and 10, then labelled ground truth on
Day 19. **That is backwards, and the old Day 19 entry said so in its own words:**
*"Do this BEFORE looking at what the system found."* It was scheduled after
eleven days of looking at what the system found.

Labels written after watching the system output are contaminated — you end up
agreeing with the machine instead of judging it. Labels come first, blind.

### 3. TUNING SET AND EVALUATION SET ARE NOW SPLIT
Tuning thresholds on the same trips used to compute precision and recall would
inflate both. That is Rule 8 wearing a lab coat.
- **ODD trip numbers = tuning set.** Thresholds are chosen here.
- **EVEN trip numbers = held-out evaluation set.** Opened once, on Day 15, and
  never tuned against. Whatever it says is what goes in the README.

**Changed from chronological to odd/even on Day 11, BEFORE labelling began.**
A 1–12 / 13–21 split would have been contaminated by the shoot order: clip13
alone holds trips 21–25 and every one of them is the same difficulty category.
The held-out set would have been all-easy and the metrics meaningless — Rule 8
again. Odd/even guarantees both sets contain hard and easy trips.
The rule was fixed in writing before the first label was typed. That ordering
is the point; a split chosen after seeing results is not a split.

### 4. VALIDATION MOVED BEFORE THE DASHBOARD
If recall comes back at 20%, that needs to be known while there is still time to
fix detectors — not after two days of UI work built on top of it. Metrics are
MUST HAVE; the dashboard is MUST HAVE; the dashboard displays the metrics.
Measure first.

### What got cut
- **Backtracking — CUT.** Was already flagged optional on Day 1. Two behaviours
  validated properly beat three half-working.
- **Signage OCR — one day, not two.** Demoted to a cuttable day.
- **Automatic sign detection, before/after experiment — CUT.** Nice-to-haves that
  were never going to happen in 16 days.

---

## Day 7 — Wed 19 Aug (eve) — Pipeline running on camC footage
- [x] Record a dev walk clip on camC
- [x] CFR convert + undistort the whole video
- [x] Decide and lock the pipeline order
- [x] Tracking working on real camC footage
- [x] Resolve the fisheye `alpha` question
- [ ] ~~Velocity~~ → moved to Day 8
- [ ] ~~Shoot prep~~ → moved to Day 8

**Status:** PARTIAL — the plumbing landed, the maths did not

**Notes:**

### All pre-camC footage is homography-orphaned
The route test was **camB**. `homography_camC.npz` cannot convert those pixels to
centimetres — a homography belongs to one camera in one position. Recorded a 53 s
dev walk on camC so the pipeline has something real to chew on before Saturday.

### Pipeline order — DECIDED AND LOCKED
**CFR convert → undistort the whole video → track → homography → smooth.**
Undistorting the video first means every footpoint YOLO produces is already
straight, so the homography applies directly with no per-point correction step.
It also produces the video the judges will actually see.

### Fisheye `alpha` question — raised, tested, dropped
One room entrance falls outside the undistorted frame. Considered
`getOptimalNewCameraMatrix(alpha=1)` to recover the full field of view.
**Rejected after watching the dev walk: nobody walks there.** Two reasons:
- Changing alpha **moves every pixel**, so the 4 clicked corners land somewhere
  new and `homography_camC.npz` becomes wrong. Full rebuild: re-click, re-build,
  re-test.
- `alpha=1` hands back the extreme edge pixels — exactly where the distortion
  model is weakest (principal point wandered 442 → 537 between calibration runs,
  and across-axis error is already 2 cm). **Buying floor area with accuracy.**
One line in limitations instead. **LOCKED — do not reopen after the shoot.**

### `START_FRAME` killed a run for the SECOND time
`START_FRAME = 1800` and `MAX_FRAMES = 500` were still sitting in
`trajectories.py` from the terrace clip. This video has 793 frames. The seek
landed past the end → first `cap.read()` returned False → loop broke instantly.
- **257-byte output. Printed "Saved to". Exited clean. Zero tracks.**
  Byte-for-byte the same failure as Day 4.
- Two tells: finished in seconds when it should take 8 minutes, and
  `Tracks with 25+ points:` printed with **nothing after it**.
- **The fix was deletion, not adjustment.** Removed `START_FRAME` and the
  `cap.set(CAP_PROP_POS_FRAMES, ...)` seek entirely. Read forward and count —
  the only thing this camera is honest about.
- **A hardcoded frame number has no correct value. Only "correct until the next
  file."** Rule 5, third occurrence — and the second time this exact variable did it.

### Fragment filter finally parameterised
`25` → `MIN_TRACK_LENGTH = int(fps * 1.0)` = **15 at 15 fps**.
The hardcoded 25 also appeared **twice more** in the summary block at the bottom,
which is why the first edit looked like it hadn't worked. Confirmed by the output
reading `Tracks with 15+ points:`.

### Tracking result — `devwalk_undist.mp4`, 793 frames, 15.0 fps
Three tracks survived the filter: **329, 151, 177 points** = 657 of 793 frames,
**~83% detection coverage**. Watched the output end to end:
- No mid-walk ID switches
- Footpoint stayed under the feet, including at distance
- No trail spikes

**First clean end-to-end run on my own camera.**

### ffmpeg duplicated one frame
792 frames in, 793 out, log said `dup=1`. The camera ran fractionally slow and
ffmpeg filled the gap to hit a true 15.0. **That is the VFR problem being
corrected in front of me.** Harmless at 1 in 793 — but worth seeing.

### New scripts
`undistort_video.py`

### Carried to Day 8
Velocity, the cm→m conversion, the signs, and the ground-truth walk measurement.

**Quiz score:      /3**

## Day 8 — Thu 20 Aug — SHOOT PREP FIRST, then velocity

### PART 1 — SHOOT PREP
- [x] Wall sign made — A4, thick marker, eye height at the fork
- [x] 5 destination cards made (A5)
- [x] 2-hour slot confirmed with mum **in writing**
- [x] Floor cleared: shoes, slippers, rug, trolley, shoe rack, robot vacuum
- [x] Wooden door confirmed open, as per homography
- [x] Storage checked, 30 s test recorded and played back
- [x] Camera not touched

### PART 2 — THE ANSWER KEY
- [x] Walked the corridor: **8 tiles, 3.85 s**
- [x] By hand: 8 x 30.8 / 100 / 3.85 = **0.64 m/s**, distance **2.46 m**

### PART 3 — VELOCITY
- [x] Trajectories saved to JSON (they were never saved before)
- [x] Homography applied -> metres
- [x] cm -> m conversion in ONE place
- [x] Per-frame speed working
- [x] Compared against the answer key — **passed**
- [ ] Smoothing — NOT DONE, moved to Day 10

### PART 4 — U-TURN v1
- [ ] SLIDES TO DAY 10 (permitted by the day's own plan)

**Status:** PARTIAL — Parts 1–3 done, smoothing and U-turn slid to Day 10

**Notes:**

### Shoot prep finally closed
Slipped on Day 4 and Day 7. Done now, two days before the shoot. Rule 19 held
once it was written into the day's order instead of left to willpower.

### Sign design changed — BAGGAGE CLAIM and EXIT now share a left arrow
Checked first that the left side has **two doors**. Without a second decision at
the end of the arrow there would be no pause, and a pause the camera can't see
is not an event. A confusion mechanism only counts if it ends in "...and therefore
they stop walking."
- Before/after signage experiment stayed CUT. 21 trips split across two sign
  states is ~10 each, and the cast would have learned the route by trip 22.
  **One shoot, one sign state.**

### WayTrace does not diagnose signs — corrected
WayTrace outputs **where**, never **why**. OCR (Day 18) reads what is nearby.
A human joins them. Wording stays *"possible signage issue associated with this
hotspot."* Two cheap deterministic sign checks noted for Day 18 (shared arrow,
missing destination) — Day 18 only, and it is still first to be cut.

### THE TRAJECTORY DATA WAS NEVER BEING SAVED
Day 7 printed 329/151/177 points to the terminal and wrote only a video. The
actual `(x, y, frame)` lists existed nowhere. Every look at the numbers meant an
8-minute tracker re-run — impossible to iterate on.
- Fixed: `trajectories.py` now writes `data/output/devwalk_trajectories.json`.
  **11,155 bytes, 3 tracks.** Cross-check: 657 points x ~17 chars = ~11,000. Two
  independent numbers agreeing.
- Saves **all** tracks, unfiltered. Filtering is a decision and belongs downstream
  where it can be changed.
- Unit written into the file as a comment: **PIXELS**.

### The edit was saved but the run used the old file
Ran the script, then saved during the 8-minute run. Python had already loaded the
old version at launch. Output was correct — but the two new print lines never
appeared, which is what caught it.
- **The print you expected and didn't get is as much a signal as an error.**
- Order is now: **Ctrl+S -> then run.** Never overlap.

### Homography verified against the answer key — 3 cm
ID 1 walked dx=+2.25 m, dy=+0.93 m -> **2.44 m**. Hand measurement: **2.46 m**.
No factor of 100 anywhere. Rule 18 paid for itself.

### The walk is mostly on the WEAK axis — README claim now in doubt
`y` was assumed to be the walking direction. The walk is 2.25 m in **x** and only
0.93 m in y. x is the across-axis — **2.0 cm error, not 0.6 cm.**
The README limitation currently claims *"speeds are computed predominantly along
the corridor axis, which is the well-calibrated direction."* **That may be false.**
Under 1% error over 2.4 m so not urgent — **re-check on real shoot footage and
correct the paragraph before Day 20.**
Found by accident during a units check, not by looking for it.

### The average speed is a number that describes nothing
ID 1: 2.44 m in 21.9 s = 0.11 m/s. Real distance, real time, meaningless answer —
it averages a walk with a 10-second standstill and matches neither.
**This is why hesitation is "below X m/s sustained for Y seconds", never an average.**
An average over a whole track hides the exact thing being detected.

### Per-second dump of ID 1 — a hesitation, visible in raw numbers
- t=4.3–7.3 s: walking, ~0.6 m/s (matches the answer key)
- t=7.3–17.3 s: **stopped.** Ten seconds, x stuck between 0.71 and 1.07
- t=18.3–25.3 s: moving again, 1.6 m swing in y
Watched the video to check the last part: **that was real movement, confirmed.**
Small +/-15 cm wobbles are foot-lift noise — the footpoint is the box bottom edge,
so lifting a foot moves it.

### max = 3.70 m/s on a 2.7 m hallway
Nobody ran. ~25 cm of footpoint wobble / 0.067 s = 3.7 m/s.
**Short time gaps magnify small errors into huge speeds.** The Day 3 spike
problem, measured instead of asserted.
- **Smoothing now has a measured spec, not a guess: remove wobbles under ~20 cm,
  preserve the real 1.6 m swing.** If smoothing flattens that swing it is too strong.

### Indentation bug — Day 3, again
Three blocks in `speeds.py` sat indented inside `for` loops they didn't belong to
and ran three times each. Output looked identical because each pass overwrote the
last with the same value. Harmless here; in a list-building step it would have
produced three copies and still looked plausible.
- Fixed, re-ran, **every number identical**. A refactor that changes a number is
  a bug, not an improvement.

### New file this session
`src/speeds.py`

### Commits this session
- Save trajectories to JSON
- speeds.py: pixel->metre in one place, per-frame speed, verified
- Tidy speeds.py: imports to top, indentation fixed, output unchanged

**Quiz score: POSTPONED to Day 9.**
Honest reason recorded: the explanations were being copy-pasted without being
read, at ~1am, at the end of a long session. Flagged by me, not caught by a test.
Rule 7 — retention drops when saturated. Re-teach happens tomorrow, fresh, in
short chunks. Three ideas owed: (1) why a small position error becomes a huge
speed, (2) why the run used the old file, (3) why the /100 lives in one place.
**Nothing in the shoot depends on this. The shoot needs signs, a clear floor and
an untouched camera — all done.**

## Day 9 — Sun 23 Aug (shot) / Mon 24 Aug (verified) — ★ THE SHOOT ★
**Highest-risk day in the project. Everything downstream eats this footage.**
**Slipped ~2 days from plan. Shoot happened Sun 23 Aug evening; verification and
CFR conversion ran Mon 24 Aug.**

- [x] Consent on camera first
- [x] ~~One continuous recording~~ — **13 separate clips instead.** See notes.
- [x] 25 trips logged, **all 25 clean** (target was 21), plus 8 wasted takes
- [x] **5 full seconds between people. Never two in frame at once.**
- [x] Log each trip as it happens — `data/shoot_log.csv`
- [x] **CAMERA NOT TOUCHED** — homography and calibration both survive

**Verification — Mon 24 Aug:**
- [x] `check_video.py` on all 13 raw clips
- [x] **Backed up** to `OneDrive\waytrace_raw_backup\` — verified by count and
      byte total, not by the copy finishing without an error
- [x] `ffmpeg` CFR conversion of all 13 → `data/cfr/`, then `check_video.py` again
- [ ] Undistort one frame and eyeball it — **carried to Day 10**
- [ ] Tracker over 500 frames — **carried to Day 10**

**Status:** DONE (footage secured and CFR-converted; two eyeball checks carried)

**Notes:**

### Trip counts — better than planned
25 trips logged, all 25 clean, 8 wasted takes. Category split:
- **MISSING** (destination not on the sign — `TOILETS`, `LOUNGE`): 9
- **AMBIG** (`EXIT` / `BAGGAGE CLAIM` sharing one left arrow): 8
- **EASY** (`GATES A-C`, unambiguous right arrow): 8

*(Corrected on Day 11: an earlier note said 24 clean / 7 wasted / 7 EASY. The log
holds 25 numbered clean trips with no gaps and 8 wasted takes. Every clip was
reconciled against the log after labelling.)*

### FIVE CLIPS WERE THE WRONG RESOLUTION — caught by verification, not by luck
Clips **2, 5, 6, 9, 11** recorded at **1280x720**. The other eight are 1024x576.
The 720p clips are all short (21–55 s) and high-bitrate (1763 vs 660 kb/s, tbr
29.42 vs 15.17); the 576p ones are long. Two different ways of pulling video off
the same camera, **interleaved through the evening** — clip4 is timestamped
20:32:06 and clip5 20:34:38, so this is not two sessions.

**Why this was nearly fatal and completely silent.** `calibration_ezviz.npz` and
the homography are both measured **in pixels at 1024x576**. K says the lens axis
sits at pixel (512, 288); the homography says pixel (640, 400) is a specific spot
on the floor. Feed a 1280x720 frame to either and every number is wrong — and
**nothing errors.** It would have produced confident, wrong centimetres.

**What it would have cost.** Those five clips hold trips 6, 8, 9, 14, 18 —
**three of them MISSING**, out of only 9 MISSING trips in the whole dataset. A
third of the most valuable category. Worse, trips 6/8/14/18 are all **even**, so
under the odd/even split the loss would have landed almost entirely on one half
and quietly unbalanced tuning against held-out.

**The diagnosis took five minutes because the shoot log existed.** Clip → trip →
category was a lookup, not an investigation. This is the argument for logging on
paper *during* the shoot.

### It was a pure rescale, so the calibration survives
Compared one frame from clip4 (576p) against one from clip5 (720p). Three
landmarks — robot vacuum edge 180→225 px, top of painting 140→175, wall sign
810→1012 — all exactly **1.25x**, and `1280/1024 = 1.25`. No new room visible at
the edges; the barrel arc on the left curves identically in both. **Same lens,
same mount, same field of view, bigger picture.**

Fix = scale the video **down** to match the calibration, never adjust the
calibration to match the video.

### One command for all 13, no special cases
`ffmpeg -vf scale=1024:576 -r 15 -an`, run over every clip. `scale=1024:576` on a
clip already at 1024x576 does nothing, so there is **no branch, no list of which
clips are special, and no chance of missing one in three days.** Same instinct as
the /100 living in exactly one place.

### The frame counts confirm the conversion rather than just surviving it
Eleven clips gained exactly **one** frame; clips 6 and 9 gained none. Those two
were the only clips whose original FPS was *above* 15 (15.0010 and 15.0009) —
everything else was slightly below and needed one duplicate frame to stretch to a
true 15.0. The pattern matches the cause, which is what separates "it worked"
from "it didn't complain".
A duplicated frame is one 0.067 s blip where the walker appears frozen. Hesitation
is *sustained* slowness over seconds, so it cannot fake an event. The payoff:
**frame 150 is now exactly 10.000 s on every clip.**

### Stray file caught in `data/cfr`
The single-clip conversion test wrote `clip5.mp4` alongside the full-length names,
leaving 14 files where there should be 13. Deleted. A second copy of one clip
under a different name is how a trip gets labelled twice. Rule 10.

### `git mv` on a file already renamed in Explorer
`fatal: bad source`. Explorer renames the file; git is never told, so it sees a
deletion and a stranger. Fixed with `git add -A data/`, which matched them at
**100% similarity** and recorded a proper rename. **Renaming in the file manager
does half the job.**

### The shoot protocol is also a stated limitation
Every trip was shot alone, with 5+ seconds between people and a hands-up walk-back
to close each take. That protocol is why the trip boundaries are reliable — and it
means **the tracker never had to handle two people at once.** ByteTrack's
performance here overstates what it would do on real airport footage. Say so in
the README rather than waiting to be asked. Rule 32.

### Commits this session
- Rename shoot log to shoot_log.csv/.xlsx
- CFR convert all 13 shoot clips to 1024x576 @ 15fps

### Re-teach delivered (owed from Day 8)
All three explained fresh: (1) short time gaps magnify small position errors,
(2) Python reads the file once at launch, (3) why /100 lives in one place.
**Quiz deliberately NOT taken immediately after** — answering right after reading
the answers proves nothing. Rule 13.

**Quiz score: not taken — deferred cold, then overtaken by Days 10–11.**

## Day 10 — Mon 24 Aug — Hesitation detector v1  *(or RESHOOT)*
**Planned for Sun 23 Aug as the reshoot slot; ran Mon 24 Aug alongside the tail
of Day 9's verification.**
- [ ] **Absolute speed threshold** — speed below X m/s sustained for Y seconds.
      NOT a per-person baseline: 2.7 m of approach is too short to establish one.
      See Day 4. This limitation is stated plainly in the README.
- [ ] **CHECK THE UNITS.** Homography is centimetres. Thresholds are m/s.
- [ ] Ignore people who are simply stationary for their whole track
- [ ] Sanity-check X against a normal walking pace measured from the real footage
- [ ] Thresholds are placeholders — tuning is Day 12

**Status: PARTIAL — detector NOT built. Day displaced by data-integrity work.**
**Notes:** All 13 clips CFR-converted (`data/cfr/`) and undistorted
(`data/undist/`), every frame count exact. Three scripts had hardcoded paths —
`check_video.py`, `undistort_video.py`, `trajectories.py` — all now read
`sys.argv` and print the paths they use (Rule 5). Tracker validated on clip1;
ByteTrack holds IDs well, no tuning needed. Direction rule fixed. Competition
research done. `docs/definitions.md` written blind. Quiz 3/3 cold.
The hesitation detector itself slides to Day 12.
**Quiz score: 3/3 cold**

## Day 11 — Tue 25 Aug — ★ GROUND TRUTH LABELLING (BLIND) ★
**Moved forward from Day 19. Do this before looking at any detector output.**

- [x] **Write the definitions FIRST, before watching anything.** `docs/definitions.md`,
      committed `2c7b427`. Hesitation = smoothed speed below 0.3 m/s for 2 s.
      U-turn = direction change over 135 degrees, sustained 1 s.
- [x] **Split the log: ODD trips = tuning set, EVEN trips = held out**
- [x] Labelling infrastructure built — two linked tables, dropdowns, zone rule
- [x] **clip1 labelled: 5 trips, 8 events**
- [x] clips 2–13 labelled: **all 25 trips, 23 events, 10 excluded walks**
- [x] Do not open the detector output today. Not once. — held

**Status: DONE — all 13 clips, all 25 trips labelled.**
**Ran 25 Aug 09:00 through 26 Aug 00:20. Clips 7–13 were labelled after 20:00
and carry a fatigue flag — see below.**

### What actually happened

**Three files the notes claimed existed did not exist.**
`data/labels.csv` — HANDOFF said "I've created it with the header row". It was
never created. `docs/definitions.md` — HANDOFF said it was written. It was, but
it was sitting in `Downloads/`, outside the repo, untracked and uncommitted; the
whole value of that file is its commit timestamp proving the thresholds were
chosen blind, and that evidence did not exist until tonight. `docs/` itself did
not exist. All three found in under a minute with `Get-ChildItem`.
**The handoff was written at the end of a 12-hour day and recorded intentions as
completed work.** It was not carelessness and it will happen again. From now on:
verify before building on any claim in PROGRESS.md or HANDOFF.md. Rule 27.

**The labels are two tables, not one.**
The original single `labels.csv` header could not represent a trip with zero
events — such a trip writes no rows, and a missing row is indistinguishable from
an unlabelled one. Split into `trips` (one row per trip, all 25, always) and
`events` (one row per event, joined by the `trip` column). Rule 28.

**`shoot_log.csv` is not a CSV.** It is an .xlsx wearing a .csv name — which is
why Notepad rendered it as binary garbage. It also has a stray note above the
header row, so any reader takes row 1 as the column names. Both must be fixed
before anything parses it. Rule 30.

**Autofill invented twenty people.** Dragging `person` down from P1/P2/P3
produced P6 through P23 — twenty humans who do not exist — plus confident
`occluded=NO`, `clean_entry=YES`, `boundary_sure=SURE` on nineteen trips that
had not been watched. No error, no warning, visually identical to real work.
Cleared. Rule 29.

### Labelling protocol (fixed before labelling, applies to all 25 trips)

- Watch the **plain CFR** video, never the annotated output. Two passes minimum:
  one with nothing written down, to calibrate on what a normal walk looks like,
  then one for boundaries only. Judging boundaries and behaviour together makes
  a slow start stretch the start time, which then stretches the event.
- **Trip boundaries in whole seconds; event boundaries to one decimal.** Half a
  second on a trip changes nothing; half a second on a 2 s hesitation is 25%.
- **`category` is filled LAST**, from the shoot log, after every clip is
  labelled. Knowing a trip was MISSING makes you expect a hesitation and
  expecting one makes you see one. Claude has read the difficulty column and
  is withholding it until labelling is complete.
- **`confidence` = SURE / MAYBE.** Borderline events marked SURE make the
  detector look bad unfairly; borderline events omitted do the same. Day 15
  headline metrics are computed on SURE only, MAYBE reported separately.
- **U-turn convention:** a human cannot see turn duration reliably, so
  `start_sec` = the frame the turn is visible and `end_sec` = start + 1.
  Fixed duration, not measured. All U-turns default to MAYBE.
- **`zone`:** NEAR = bottom third of frame, MID = middle, FAR = top. A rough
  human sanity check only — hotspot positions come from the homography in cm.
  Note the geometry: the top third covers far more real floor than the bottom,
  so FAR will collect more events for reasons that are not behavioural.
- **An event is not deleted because you know why it happened.** Trip 4's stop
  was "the person checking the arrows" — that is a mental state, unavailable to
  a camera, and stopping to read a sign is precisely the friction this system
  exists to detect. It stays in. Explanations go in `notes`, worded as
  "appeared to". Rule 31.
- **Excluded is not unrecorded.** Walk-backs get no trip number but do get a
  line in the notes of the trip they follow, because the tracker will see them
  and assign IDs to them.

### clip1 results — 5 trips, 8 events

| trip | person | start | end | events |
|---|---|---|---|---|
| 1 | P1 | 3 | 13 | E1 hesitation 7–10 SURE |
| 2 | P2 | 49 | 53 | none |
| 3 | P3 | 75 | 81 | none |
| 4 | P1 | 111 | 120 | E2 hesitation 114–116 MAYBE |
| 5 | P3 | 138 | 168 | E3 hes 142–144, E4/E5/E6 U-turns 146/148/150, E7 hes 153–155, E8 U-turn 159 |

Trip 5 is one continuous 30-second walk — three to seven times longer than any
other trip in the clip, and it holds 6 of the 8 events.
Trips 2 and 3 produced nothing, and that is a result, not a gap: a detector that
fires on every trip cannot be distinguished from a working one without trips
where the correct answer is silence.

E2 is exactly 2.0 s — sitting on the threshold, hence MAYBE. If several events
land on exactly 2.0 across the dataset, that says the threshold needs moving,
which is what Day 12 is for.

### Final counts

**13 clips · 25 trips · 23 events · 10 excluded walks recorded**
14 hesitations, 9 U-turns. `data/trip.csv` 3417 bytes, `data/event.csv` 1420.
Ten commits, last `5c6bbcb`, all pushed.

| Clip | Walks | Trips | Excluded | Events | Log agreed? |
|---|---|---|---|---|---|
| clip1 | 5 | 5 | 0 | 8 | yes |
| clip2 | 1 | 1 | 0 | 0 | yes |
| clip3 | 4 | 1 | 3 | 0 | **NO — abrish walked twice, logged once** |
| clip4 | 3 | 0 | 3 | 0 | yes — all three wasted |
| clip5 | 1 | 1 | 0 | 0 | yes |
| clip6 | 1 | 1 | 0 | 0 | yes |
| clip7 | 3 | 1 | 2 | 0 | yes |
| clip8 | 4 | 3 | 1 | 6 | yes |
| clip9 | 1 | 1 | 0 | 1 | yes |
| clip10 | 3 | 3 | 0 | 3 | yes |
| clip11 | 1 | 1 | 0 | 2 | yes |
| clip12 | 2 | 2 | 0 | 2 | yes |
| clip13 | 6 | 5 | 1 | 1 | yes |
| **Total** | **35** | **25** | **10** | **23** | 12 of 13 |

### The result the labels produced

`category` was filled LAST, from the shoot log, after every clip was watched.

| Category | Trips | Events |
|---|---|---|
| MISSING | 9 | **14** |
| AMBIG | 8 | 7 |
| EASY | 8 | **2** |

Trips whose destination is absent from the sign produce roughly seven times the
behavioural events of unambiguous ones. **This is the core hypothesis, and it
came out of labels written without knowing which trip was which.** That ordering
is the entire evidential value. No label is touched from here.

### Split as labelled

- **Tuning (odd, 13 trips):** 3 MISSING, 5 AMBIG, 5 EASY — 14 events
- **Held out (even, 12 trips):** 6 MISSING, 3 AMBIG, 3 EASY — 9 events

The held-out set is **harder** than the tuning set — it carries 6 of the 9
MISSING trips. Rule 8 warns that easy test data flatters a score; here the bias
runs the other way, so Day 15 will understate. Leave it, and state it in the
README. A judge will respect an unbalanced split fixed in advance more than a
tidy one chosen afterwards.

### Schema repair before labelling could continue

Labelling the remaining 20 trips into the morning's schema would have meant
labelling them twice.

- **`confidence` was answering two questions at once.** By convention every
  U-turn got `end_sec = start_sec + 1` and was marked MAYBE — but that MAYBE was
  about the invented end second, not about whether the turn happened. Day 15
  computes headline metrics on SURE only, so the SURE set would have held **zero
  U-turns**, and precision and recall cannot be computed on an empty set. U-turn
  detection is a MUST HAVE. Fixed by splitting the two doubts: `confidence` now
  means *did this event happen*, and boundary doubt lives in a new
  `boundary_note` column. Rule 33.
- **The dropdowns were warnings, not guards.** `UTRURN` was typed into four
  cells inside the dropdown's own range. Sheets validation defaults to "show a
  warning" and lets bad values through. Set to **Reject the input**, extended to
  row 200, then **tested with a deliberately wrong value** — a guard that has not
  been watched to fail is a guess. Rule 34.
- **Six invisible trailing spaces in the headers** (`person `, `start_sec `,
  `others_in_frame `, `clean_entry `, `boundary_sure `, `category `).
  `df['person']` would have raised KeyError on Day 15 and been blamed on
  something else. Found by byte count, not by reading.
- **`zone` deleted.** Nothing in the pipeline reads it — Day 14 clusters on
  centimetre coordinates from the homography, Day 15 matches on trip and time.
  Re-checked against the video, **2 of 5 values were wrong**, and two more could
  only be described as "between" the thirds. A field the machine can compute from
  the `y` coordinate should never be filled by a human. Rule 35.
- **Twenty pre-guessed trip rows deleted.** Rows 6–25 held trip numbers and clip
  assignments for clips not yet watched. Since ODD/EVEN is keyed to trip number,
  a shifted count would have migrated trips between tuning and held-out
  mid-labelling. Numbers are now assigned at labelling time, in clip order then by
  `start_sec` — deterministic, no discretion.

### Three findings

**1. The shoot log undercounts the footage.** clip3 holds four walks on video;
the log records three. abrish walked twice in a row and was logged once. Found
only because walks were counted from the video *before* the log was opened. The
log is a check, never a source — labelling from it would have made the two
incapable of disagreeing. Rule 13 in a new setting.

**2. The squared-off U-turn — clip11, trip 18, 0:29.** The walker reverses by
going forward, stepping sideways, then walking back: **two 90° turns, not one
pivot.** A human sees an obvious reversal. The instantaneous direction change may
never exceed 135°, so the detector as defined may be blind to it. Likely fix:
compare heading across a window (3 s ago vs now) rather than frame to frame.
Ground truth records what a human sees, not what the detector can catch — that is
the point of labelling blind, and this is what it bought.

**3. Seven of the 14 hesitations are exactly 2.0 seconds.** E2, E3, E7, E10,
E11, E17, E23. The definition says ≥2 s, and the protocol said event boundaries
to one decimal place — every value written is a whole second. **The definition
anchored the boundaries.** The labels stand, but half the hesitations sit exactly
on the threshold, so small threshold changes will swing Day 12 metrics hard.
Report sensitivity across a range, never a single number.

### Excluded walks — 10 recorded, none deleted

| Clip | Reason |
|---|---|
| clip3 ×1 | Left frame into a side room — the tracker would split the ID |
| clip3 ×2 | Logged wasted on the night |
| clip4 ×3 | Logged wasted on the night |
| clip7 ×2 | Stopped before the far end, broke character while still in frame |
| clip8 ×1 | Logged wasted on the night |
| clip13 ×1 | Checking the robot vacuum during setup — not a walk |

**clip4's first excluded walk is the hard case.** It contains a 7-second
hesitation, a U-turn, a 2-second stop and a second U-turn — the richest behaviour
outside clip1's trip 5 — and it was binned as a wasted take on the night. The
reason for wasting was not recorded. **It was not reinstated.** A judgement made
live, with information the footage does not contain, stands. Overturning it after
seeing it was full of the events I wanted is choosing data because I like what is
in it. Written down here so it can be revisited honestly if Day 15 recall is
thin, rather than edited quietly. Rule 36.

### Things that are deliberately not events

- **45° course correction** — clip9, trip 14, 0:18. Under 135°.
- **90° turn at the sign** — clip7 trip 10; clip10 trip 17. A direction choice,
  not a reversal. Worth noting for the signage audit.
- **1-second stops** — clip7 excluded walk 0:27–0:28; clip11 trip 18 0:20–0:21.
  Under the 2 s threshold. Recorded in notes only.

### PROGRESS.md had ~90 lines silently deleted

`git diff` before committing showed the working copy was missing, against
`2c7b427`: **Day 9's entire notes section** (the 720p catastrophe, the 1.25×
rescale proof with three landmarks, the one-ffmpeg-command reasoning, the
frame-count pattern, the stray `clip5.mp4`, the `git mv` lesson), the risk
register row for resolution mismatch, two vocabulary entries (Resolution vs
calibration; Field of view vs rescale), and the full text of rules 23–26 replaced
by one-line stubs.

**Cause: a previous session regenerated the whole file from an older copy** and
pasted new sections back in. Anything not consciously carried across vanished. No
error, and the file still reads as complete and well-written.

All of it survives in `2c7b427`. **Restore by hand, one section at a time.
Never regenerate this file.** Rule 37.
**DONE — restored in `880e979`.** Verified on Day 12 by diffing the working file
against `2c7b427`: 424 insertions, 43 deletions, and all 43 deletions confirmed
intentional replacements (the old chronological 1–12/13–21 split, the superseded
"24 clean" count, empty day templates, two tightened rules). The Day 11 handoff
said this was still outstanding; it was two commits stale.

### Fatigue flag

Clips 1–6 were labelled during the day; clips 7–13 between 20:00 and 00:20. In
the last hour: a clip was labelled under the wrong clip number (caught by a length
mismatch), a person was written down as the wrong person (caught by the log), a
stop was logged as `2:16–2:16` (zero seconds), a mental state was written into a
note, and two commits were skipped. All caught, none reached the file — but
roughly six near-misses in one hour against roughly zero in the first three.

**Clips 2, 4, 5 and 6 produced zero events between them.** Zero is a legitimate
result — a detector that fires on every trip cannot be distinguished from a
working one without trips where the correct answer is silence. But a *missed*
event is invisible: it looks exactly like a clean trip. Re-check the late clips
before Day 15 trusts them. Rule 38.

**Quiz score: 3/3 (multiple choice — easier than cold recall, Rule 13)**

## Day 12 — Wed 26 Aug — Hesitation + U-turn detectors v1  ✅ COMPLETE
**Re-scoped: detectors slid from Day 10. Labelling is COMPLETE — Day 11 done.**

- [x] **BLOCKING FIRST — `smooth()` VERIFIED.** `window=1` reproduces the
      unsmoothed numbers exactly (3.70 m/s max, 1.74 m y-swing), so the function
      is correct. `window=5` cuts the spurious spike to 1.40 m/s while the real
      1.6 m y-swing survives at 1.72 m. Wobble dies, real movement lives — the
      Day 8 requirement, met. The test *and its expected answer* had been written
      on Day 8 before the answer was known (Rule 18), so verification took five
      minutes against the day budgeted for it.
- [x] **BLOCKING SECOND — track-count mismatch SOLVED.** Neither number lied.
      The printout filters short tracks; the JSON keeps them.
      clip1: 13 saved = 10 real + 3 fragments.
      clip2: 3 saved = 2 real + 1 fragment.
      clip13: 16 saved = 11 printed + 5 fragments, and the 11 decompose exactly
      as 5 trips + 5 walk-backs + 1 excluded robot-vacuum walk.
      Threshold measured, not guessed (Rule 11): shortest real track 37 points,
      longest fragment 4 points — a cliff, not a judgement call.
      `drop_fragments()` in `speeds.py` now implements `int(fps * 1.0)`, which
      `docs/definitions.md` had specified but no code had ever applied.
- [x] **BLOCKING THIRD — PROGRESS.md restore.** Already done in `880e979`; see
      the damage section above. The handoff was two commits stale.
- [x] **Trip direction confirmed against real data.** Every trip runs y-rising,
      every walk-back y-falling, on clip1, clip2 and clip13 independently, and
      every labelled trip start matches a rising track to within ~1 s. The
      excluded robot-vacuum walk in clip13 runs y-falling and is therefore
      dropped by the direction rule automatically, exactly as `definitions.md`
      predicted. `docs/definitions.md` was right all along — the Day 11 handoff
      transcribed it backwards as `<`. **Nothing was changed.**
- [x] **Hesitation detector v1** — `src/detect.py`, thresholds straight from
      `definitions.md` (0.3 m/s, 2.0 s), untuned.
- [x] **U-turn detector v1** — window heading, ±1.5 s either side, per
      `definitions.md`'s "measured over a window, never frame to frame".
- [x] **The squared-off reversal is caught.** Trip 18 / E20, the case whose own
      label says *"instantaneous angle may never exceed 135"*: detected at
      **28.1 s, 138.8°** against a labelled 29 s. A frame-to-frame detector is
      blind to this shape. The window design decision is vindicated with evidence.
- [x] Tune U-turn thresholds against ODD trips only → **done Day 13**
- [x] Tune hesitation thresholds against ODD trips only → **done Day 13**
- [x] Kill false positives from tracker jitter → **done Day 13**, 7 → 2
- [x] **One variable at a time.** Every trustworthy number in this file came from that.
- [x] **Do not open EVEN trips** for tuning. See the contamination note below.

**Status: DONE.** All five assigned jobs complete. Five commits, all pushed:
`b1ae34c`, `26157a5`, `9f72adb`, `c2c0f17`, plus the PROGRESS commit.

**Notes:**

### Detector v1 vs ground truth — clip1 and clip11, untuned

| Trip | Category | Labelled | Detected | Result |
|---|---|---|---|---|
| 1 | AMBIG | E1 hes 7–10 | 6.9–11.1 | HIT, start 0.1 s off |
| 2 | MISSING | none | none | correct reject |
| 3 | AMBIG | none | none | correct reject |
| 4 | EASY | E2 hes 114–116, **MAYBE** | none | MISS |
| 5 | MISSING | E3 hes 142–144 | 142.3–147.0 | HIT, start 0.3 s off |
| 5 | MISSING | E7 hes 153–155 | 153.1–156.3 | HIT, start 0.1 s off |
| 5 | MISSING | E4/E5/E6/E8 uturns 146/148/150/159 | 147.3/149.4/153.1/157.9 | **4 for 4** |
| 18 | MISSING | E19 hes 13–18 | 13.3–18.3 | HIT |
| 18 | MISSING | E20 uturn 29 (squared-off) | 28.1, 138.8° | **HIT** |

**4 of 5 hesitations, 5 of 5 U-turns, correct rejects on four clean trips** —
from thresholds chosen blind before the code existed.

**The single miss is the single `MAYBE` in the whole event file.** E2 is the only
event labelled with doubt in all 23, and it is the only one the detector missed.
Human uncertainty and machine failure landed on the same event independently.

### Three known false positives, all diagnosed, none fixed today

1. **Ends run long, starts are exact.** Starts land within 0.3 s; ends overshoot
   by ~3 s. `max_gap=1.0` holds an event open across the U-turns that follow it —
   the person is turning, so they are slow, so the hesitation never closes.
   **Event timing is trustworthy; event duration is not yet.**
2. **A stationary person has no heading.** Two false U-turns fired at 13.9 s and
   15.0 s on trip 18, *inside* a labelled hesitation. Someone standing still and
   shifting weight has no meaningful direction, so `heading()` returns noise, and
   noise clears 135° easily. This is a design flaw, not a threshold: the fix is a
   speed gate, not a bigger angle. Day 13.
3. **1-second pauses inflate.** The 20–21 s pause on trip 18, excluded from the
   labels as under threshold, was detected as a 3.7 s hesitation. Same `max_gap`
   cause as (1).

### CONTAMINATION NOTE — read before Day 15

Running a detector over a whole clip prints every trip in it, and clips mix odd
and even. **Detector output has therefore been seen for even trips 2 and 4.** No
threshold was moved on the basis of it and no tuning has occurred, but the fact is
recorded here rather than quietly dropped, and it goes in the README. The honest
framing: the held-out set protects against *tuning* contamination, and tuning has
not happened; but "never observed" is now false and must not be claimed.

### Definitions live elsewhere

Event definitions are in **`docs/definitions.md`**, committed blind in `2c7b427`
before labelling began — not in this file. The Day 11 handoff implied they were
here and cost ~15 minutes of searching.

### Threshold evidence for Day 13 — NOT acted on today

A confirmed standstill peaks at **0.38 m/s** smoothed, above the 0.3 m/s in
`definitions.md`, and measured walking is **0.64 m/s** against the 1.2 m/s the
definitions assumed. Both roughly half, because the corridor is a hallway and not
a concourse. Recording this on Day 12 rather than acting on it is the point:
`definitions.md` says the numbers are "expected to be wrong", and this is the
evidence — not a licence to edit a threshold minutes after seeing a number.

**Quiz score: 8/9 (89%)** — one combined cold quiz covering Days 12, 13 and 14,
taken 26 Aug at the end of the session. Nine questions: smooth()'s null test,
the 13-vs-5 track breakdown, why walk-backs are false positives by construction,
why a stationary person has no heading, what max_gap was for and why it reversed,
what caught the half-applied threshold, what the odd/even guard actually restored,
why the junction had to be measured from the building, and which trips the old
direction rule decided on noise. **8 correct. The missed question was not
recorded at the time — note it here if it comes back to mind.**

## Day 13 — Wed 26 Aug — Tune on ODD trips only, then event log
> **✅ SCHEDULE CONFLICT RESOLVED on Day 12, 26 Aug.**
> Both cuttable features cut: signage OCR *and* live sensor mode. Eleven blocks
> of work now map onto real calendar days, finishing **Tue 1 Sep** with **four
> buffer days** (2–5 Sep) before the real deadline of Sat 5 Sep, 22:00 Lisbon.
> Calibration overran by two days and the shoot overran by two days; a third
> overrun is the pattern, not a surprise, and the buffer is what absorbs it.
>
> | Day | Date | Work |
> |---|---|---|
> | 12 | Wed 26 Aug | Detectors v1 ✅ |
> | 13 | Thu 27 Aug | Tune on ODD only + event log |
> | 14 | Fri 28 Aug | Hotspot engine |
> | 15 | Sat 29 Aug | ★ Validation on EVEN |
> | 16–17 | Sun 30 – Mon 31 Aug | Dashboard |
> | 20 | Mon 31 Aug | Polish, README, GitHub |
> | 21–22 | Tue 1 Sep | Demo video + SUBMIT |
> | — | 2–5 Sep | Buffer. Live sensor mode returns here if free. |

- [x] **Speed gate on the U-turn detector.** `min_speed`, gating on speed before
      the angle is even computed. A stationary person has no heading (Rule 41).
- [x] **`max_gap` sensitivity swept** on real shoot data, not the dev walk.
- [x] Tune hesitation thresholds against **ODD trips only**
- [x] Tune U-turn thresholds against **ODD trips only**
- [x] **Do not open EVEN trips** — now enforced in code, not by memory. See below.
- [x] Event schema: type, trip, track ID, timestamps, x, y (metres), confidence,
      and `angle_deg` on U-turns.
- [x] Every detected event written to `results_odd.json`
- [x] Events drawn on the output video as they fire — `annotate_events.py`
- [x] Processing stays separated from display — `annotate_events.py`, `hotspots.py`
      and `heatmap.py` all read JSON and re-run nothing.

**Status: DONE.** Everything above complete, plus a detector flaw found and fixed
that was not on the list. Commits `c741020` … `df6edfc`.

**Notes:**

### The scoring harness — `tune.py`, ODD trips only, by construction

`odd_only.py` filters `data/trip.csv` to odd trip numbers before anything runs,
and `trip_for_track()` decides membership in ONE place that every tool calls.
Match tolerance 3 s, because tracks begin 0.1–1.8 s after the labelled start on
every clip measured (YOLO needs the person properly in frame).

**BASELINE, thresholds untouched from `definitions.md`:**
**11 hits, 3 misses, 7 false positives** on 14 labelled odd-trip events.
Precision 61%, recall 79%. Committed as `de4412f` **before** any tuning, so the
starting point is in git and cannot be quietly improved afterwards.

### Five sweeps, one variable at a time, every baseline row reproducing 11/3/7

| Threshold | Range swept | Result |
|---|---|---|
| `max_speed` | 0.25 – 0.40 | **unimprovable.** 0.30 already optimal |
| `min_seconds` | 1.5 – 3.0 | **unimprovable.** 2.0 already optimal |
| `min_angle` | 120 – 165 | **unimprovable.** 135 already optimal |
| `max_gap` | 0.0 – 2.0 | **0.0 beats 1.0**: 7 false → 4, zero hits lost |
| `min_speed` | 0.05 – 0.25 | **0.20 beats 0.15**: 7 false → 5, zero hits lost |

Three of five thresholds, written blind on Day 11 from reasoning alone, could not
be improved by a sweep. That is worth stating in the README exactly as it is: not
"we guessed well" but "we tested six values either side and the original was best".

**Combination test — the two changes are independent and stack:**

| Config | hits | miss | false | P | R |
|---|---|---|---|---|---|
| baseline | 11 | 3 | 7 | 61% | 79% |
| `max_gap=0` | 11 | 3 | 4 | 73% | 79% |
| `min_speed=0.20` | 11 | 3 | 5 | 69% | 79% |
| **both** | **11** | **3** | **2** | **85%** | **79%** |

**Precision 61% → 85%, recall unchanged. Five false positives removed, not one
hit sacrificed.** No trade was made; noise was removed.

`max_gap` deserves a note. It was invented on Day 8 to stop one long stop
fragmenting into several — on the DEV WALK. On real shoot trips it does the
opposite: it holds an event open across the slow moments around it, and each
glued-on piece becomes a false event. **A parameter that helps on one dataset can
hurt on another, and only a sweep on the real data will say which.**

### The U-turn detector: what was tried, and what it cost

Three versions were built and measured on ODD trips 5 and 18.

1. **Angle + speed gate at 0.15** — trip 5: 4 of 4 U-turns, exact. Trip 18's
   squared-off reversal: MISSED.
2. **Speed gate at 0.05** — recovers trip 18's turn, but adds **2 false positives
   inside a labelled hesitation**. The real turn sits at 0.07 m/s and the noise at
   0.02–0.03; a 4 cm/s margin is inside the measurement error and would be tuning
   to one event on one trip.
3. **Net reversal over a 2 s window** (a definition change, not a threshold move)
   — WORSE on both. Trip 5: 7 detections against 4 labelled, because turns 2 s
   apart get straddled by a 2 s window. Trip 18: found a turn at 20.5 s, which is
   not the labelled 29 s, so it missed the real one and invented a new one.

**Version 1 kept, `min_speed` tuned to 0.20.** Precision over recall: a false
hotspot sends an airport to fix a working sign, and a judge who sees a marker on
someone standing still stops trusting every other marker.

**The squared-off reversal (trip 18 / E20) is a documented MISS.** It was
predicted on Day 11, in the label's own note, before the detector existed. A
detector that caught it by clearing 135° by 3.8° is not a detector you can defend
when asked why the threshold is 135.

**Second U-turn miss:** E22 on trip 20, a proper pivot at 86 s, missed for the
same reason — the person is turning right after stopping, so the speed gate
rejects it. **The gate buys precision and costs U-turns that follow a hesitation.**
That is a sentence a judge can check against the footage.

### FLAW FOUND AND FIXED — the trip direction rule decided U-turn trips on noise

`definitions.md` says a trip is `final y > starting y`. But **a trip containing a
U-turn ends roughly where it began**, so its net displacement is noise and the
sign of that noise decides whether the trip is kept or thrown away.

Measured: clip11 ID 1 (trip 18) passed at **+0.01 m**. clip12 ID 19 (trip 20)
was rejected at **−0.12 m**. Both are real trips. **The most valuable trips in the
dataset — the ones with reversals — were passing or failing a coin flip.**

Fix: judge by **START position**, not net displacement. A trip starts at the near
end (y ≈ −1); a walk-back starts at the far end (y ≈ +2). Unambiguous, and it
recovered trip 20 plus two others. Trip 20's labelled hesitation E21 (81–85 s)
was then detected at 79.9 s, so the recovery is confirmed against ground truth
rather than against a trip count.

I first diagnosed clip12 ID 19 as an ID switch on a single number. It was not.
Checking every track's net displacement showed eight tracks under 1 m, and the
one used all day for the squared-off analysis was among them at 0.01 m. **Rule 9,
committed by me: wrong input, wrong conclusion.**

### ODD/EVEN GUARD — the honest fix, not the comfortable one

The Day 12 note said even trips 2 and 4 had been seen. The real position was
worse: `build_events.py` processed all 13 clips and `summarise.py` printed
per-trip counts, so **detector output had been displayed for every even trip.**
No threshold was ever selected against them — `tune.py` reads odd only, by
construction — but "never observed" had stopped being true.

Two options were available: accept and document, or restore the guarantee.
The guarantee was restored, because the first sharp question a judge asks about
methodology is exactly this one, and an answer with a hedge in it is worth much
less than one with code behind it.

`build_events.py` now processes ODD trips only and writes `results_odd.json`.
`--all` writes `results.json` and **is for Day 15, once**. The contaminated
`results.json` was deleted. Verified by test, not assumption:

```
scope: ODD_TRIPS_ONLY
trips with events: [1, 5, 13, 17, 21]
any even? []
```

**What can now be claimed:** the held-out trips were not processed after Day 13,
and the guard is in the code with a commit date. **What cannot:** that they were
never seen at all, during Days 12–13. Both go in the README.

### Two float32 leaks and a whitespace near-miss

`results.json` came out at **402 bytes** twice — `json` refuses numpy's float32,
and `round()` on a float32 returns a float32. Fixed at the ONE point data leaves
the maths and enters the file (`to_json_safe`), not at each point of use. Same
principle as the single unit-conversion point.

Worse: a commit message claimed both tuned thresholds were applied. **Only one
was.** A PowerShell replace missed on whitespace (`MAX_GAP      = 1.0`, six
spaces, pattern had five) and `results.json` was rebuilt with half the tuning.
**Caught only because the thresholds block is written INTO the output file** —
`summarise.py` printed `"max_gap": 1.0` when the commit said 0.0. Without that,
a wrong number goes into Day 15 with nothing to catch it.

**Quiz score: covered by the combined 8/9 quiz logged under Day 12.**

## Day 14 — Wed 26 Aug — Hotspot engine
- [x] Cluster event coordinates — grid density, not DBSCAN
- [x] Output hotspot centre, event count, type breakdown
- [x] Heatmap overlay on a still frame
- [x] Sanity check: does the biggest hotspot land at the fork?
- [x] **BONUS — the signage audit**, which had been cut from the schedule on
      Day 12 and turned out to be measurable in twenty minutes.

**Status: DONE.** Commits `2bcb327` … `b266b24`.

**Notes:**

### Grid clustering, not DBSCAN

The corridor is 3 m long and the whole tuning set is 13 events. A grid has ONE
parameter; DBSCAN has two. Easier to explain to a judge and easier to sweep.
`CELL_M = 0.5`, `MIN_EVENTS = 2`.

**Two hotspots on the ODD set:**

| # | position | events | breakdown | trips |
|---|---|---|---|---|
| 1 | (+0.50, +1.00) | 4 | 1 hesitation, 3 U-turns | 5, 17 |
| 2 | (+1.00, +0.50) | 3 | 3 hesitations, 0 U-turns | 1, 13, 21 |

Hotspot 2 is three hesitations from **three separate trips** inside one 0.5 m
square. Not one slow person — a location producing the same behaviour repeatedly.
The two hotspots also have different characters: one is reversals, one is pauses.

### CELL_M sensitivity — the honest framing

| cell | hotspots | events clustered |
|---|---|---|
| 0.30 m | 2 | 4/13 |
| 0.40 m | 2 | 5/13 |
| 0.50 m | 2 | 7/13 |
| 0.60 m | 3 | 8/13 |
| 0.75 m | 3 | 9/13 |
| 1.00 m | 3 | 11/13 |

**The hotspot COUNT is stable at 2–3 across a 3× range of cell size.** It never
collapses to 1 or explodes. So the number of friction locations is a property of
the data, not of the grid. What moves between runs is which events fall inside a
boundary, which is what happens when a cluster sits near a cell edge with only
13 events. 0.5 m chosen as the largest cell still giving the conservative answer.

**Say this before a judge says it:** 13 events over 13 trips demonstrates that
the method works. It is not a statistically strong result.

### The signage audit — measured, not OCR'd

Sign position found by clicking the FLOOR at the base of the wall the sign is
mounted on, in an undistorted frame, through the homography. **Never the sign
itself:** the homography maps the floor plane, so a point up a wall is placed as
if lying flat — the same reason trajectories use the box bottom, not the centre.

**Five clicks along the sign wall agreed on y to within 1 cm** (1.64–1.65 m).
One click is a number; five that agree is a measurement. `sign_A` at
(+0.60, +1.645), saved to `data/signs.json` with its text and its omissions.

| hotspot | distance to sign_A |
|---|---|
| 1 — U-turn dominated | **0.65 m** |
| 2 — hesitation dominated | **1.21 m** |

**Both hotspots fall within 1.21 m of the only sign.** And the pattern is
readable: U-turns cluster nearer the sign (people read it and turn back),
hesitations further away (people stop at reading distance and think).

The sign says `BAGGAGE CLAIM ←` and `EXIT ←`. **TOILETS and LOUNGE are absent**,
omitted deliberately at shoot time. Trips categorised MISSING are exactly those
whose destination is not on this sign.

Wording discipline holds: *"possible signage issue associated with this hotspot"*,
never *"this sign caused it"*. The system measures distance, not causation.

### PIPELINE SANITY CHECK — passed

The junction is not one fork. **There are three openings**, so the decision is a
zone, not a point. All three measured by clicking the floor at each mouth:
left (−0.54, +1.05), middle (+0.06, +1.69), right (+1.21, +1.79); centre
(+0.24, +1.51). **Measured from the building, independent of any detector
output** — that independence is the whole value of the check.

| hotspot | distance to junction | side |
|---|---|---|
| 1 | 0.57 m | **approach side** |
| 2 | 1.26 m | **approach side** |

**Both hotspots are in front of the junction, neither beyond it.** Nobody stops
after choosing; they stop while deciding. Every stage upstream — detection,
tracking, homography, both detectors, clustering — is placing events somewhere
physically sensible. If the biggest hotspot had landed in an empty stretch of
corridor, every number in this file would have looked fine and been wrong.

**The story, in one line for the demo:** three ways to go, one sign naming two
destinations, two of the four destinations absent, and friction concentrated in
front of the junction where the choice is made.

### The heatmap, and four hours lost to a text bug

`heatmap.py` draws hotspots, sign and junction openings on a still frame.
Geometry was correct on the FIRST attempt — circles land on the tiles people
walked on, the sign marker lands where the five measurement clicks were.

The text ghosted, and it took eleven patches, two broken files and four wrong
diagnoses from me to fix. Wrong theories, in order: mismatched coordinates,
antialiasing, the image viewer, PNG scaling. **The answer came from one test that
could only have one outcome** — `text_test.py`, three sizes, one `putText` each,
nothing else on the image. Clean at every size. So the fault was the two-pass
outline in `label()`: a thick non-antialiased black stroke with a thin
antialiased fill inside it reads as doubled letters at small sizes.

Fix: ONE `putText` on an optional dark plate (32,32,32), plates on the panel and
caption where the background is busy photography, `box=False` on saturated
backgrounds. Rewritten clean rather than patched a twelfth time.

**Also fixed:** the fill loop and the outline loop each computed their own
position and radius, so shrinking the circles moved only the fill, and the
frame-edge shift was applied twice. `circle_pos()` is now the single source.

Hotspot 2 sits **below the camera's field of view** — real, inside the calibrated
area, but the floor there is off the bottom edge of every frame from this camera
position. It is drawn at the lowest visible row and labelled "below frame edge".
That is a field-of-view fact worth stating in the README, not a drawing bug.

### BOM in ten source files

Every file written with `Set-Content -Encoding UTF8` on Windows PowerShell 5
carries `239 187 191` at the start. Python's source loader tolerates it;
`json.load` does not, and `ast.parse` does not. It made `signs.json` unreadable
and produced a `SyntaxError` that looked like file damage.

All ten stripped. Verified harmless by rerunning the whole pipeline: baseline
still 11/3/7, hotspots still 2 at the same coordinates and the same sign
distances. **Bulk edits are verified by re-running against a number you already
trust, never by inspection.**

From here: `[System.IO.File]::WriteAllText(path, text, (New-Object
System.Text.UTF8Encoding $false))`.

**Quiz score: covered by the combined 8/9 quiz logged under Day 12.**

## Day 15 — Thu 27 Aug — ★ VALIDATION METRICS (held-out set) ★
**Moved before the dashboard. If the numbers are bad, there is still time.**

- [x] Open the EVEN trips for the first time â€” `--all` run ONCE, 27 Aug
- [x] Precision, recall, F1 per behaviour â€” `per_behaviour.py`, commit `083e7dc`.
      **The combined figure hid a detector scoring zero. Rule 22 earned again.**
- [x] **Include the hard cases.** Category split counted from `trip.csv`, not
      recalled: MISSING 5 even / 3 odd, AMBIG 3/5, EASY 4/5. The held-out set
      holds the majority of hard trips, so this was not an easy test (Rule 8).
      **An earlier handoff claimed "6 of 9 MISSING". The real figure is 5 of 8.**
- [x] Write the honest limitations section, including the homography paragraph â€”
      `docs/limitations.md`, twelve sections, commits `ecef878` and `0e33d4d`
- [x] Practise explaining every number out loud â€” four questions rehearsed:
      62 vs 85, the U-turn zero, why the hotspots are real, and the small-n
      objection. **Judging is video-only, so these become Day 21 narration:
      there is no follow-up question in a video, only a gap the judge fills
      themselves â€” and they will fill it worse than the truth.**

**If recall is poor:** Days 18 and 19 are the sacrificial days. Cut signage or
live mode and fix the detector. Metrics are MUST HAVE; those two are not.

**Status: DONE.** All five boxes. Twelve commits, all pushed, `0f089fb` â€¦ `0e33d4d`.

### THE HELD-OUT RESULT â€” one run, no retuning

`validate.py` was written and committed as `b8c38a2` **before it was ever run**,
so the scoring rules are in public history with a timestamp that predates the
numbers. The ODD block reprints 11/3/2 P85 R79 unchanged as a self-check, which
is what makes the EVEN block below it trustworthy.

|                | ODD (tuning, 13 trips) | EVEN (HELD-OUT, 12 trips) | ALL (25) |
|---|---|---|---|
| Hesitation | P 100%  R 86%  F1 92% | P 83%  R 71%  F1 77% | P 92%  R 79% |
| U-turn     | P 71%   R 71%  F1 71% | **P 0%  R 0%  F1 0%** | P 56%  R 56% |
| Combined   | P 85%   R 79%  F1 81% | **P 62%  R 56%  F1 59%** | P 76%  R 70% |

**The combined 62/56 hid the U-turn zero completely.** Rule 22 â€” averages hide
events â€” cost a whole extra pass today, because the first "Day 15 done" claim
was made on the combined number alone.

### All four held-out misses explained â€” none unexplained

| miss | cause |
|---|---|
| clip1 t4 114.0 s HESITATION | pause under 2 s. `min_seconds=2.00` excluded it **by definition**. Confirmed by watching the footage. |
| clip8 t12 62.0 s HESITATION | **ONE event typed wrong, not two errors.** A UTURN fired at 62.5 s, 0.5 s away. The matcher demands type agreement, so one real event cost a miss AND a false positive. |
| clip11 t18 29.0 s UTURN | speed gate â€” U-turn following a stop. **Predicted Day 14.** |
| clip12 t20 86.0 s UTURN | same cause. **Predicted Day 14.** |

A predicted failure appearing on unseen data is stronger evidence of
understanding than an unexplained success.

### Hotspots confirmed on data they were never built from

`--all` produced 21 events, reconciling exactly with the scorer (13 odd + 8 even).
Both original hotspots survived: **(+0.50,+1.00) grew 4 â†’ 5 events, (+1.00,+0.50)
held at 3.** Neither moved. Two new ones appeared, giving 4 total, stable across
cell sizes 0.40â€“0.75 m. All four on the **approach side** of a junction measured
with a tape measure, independent of any detector output.

### The plan's contingency was deliberately overridden

This block said: *"If recall is poor: Days 18 and 19 are the sacrificial days.
Cut signage or live mode and fix the detector."* Recall is 56% and U-turn is 0%,
so by that rule the detector should now be fixed.

**It will not be.** That contingency was written before the odd/even discipline
existed. Fixing a detector in response to held-out numbers destroys the only
uncontaminated evidence in the project â€” the thing no other entry will have.
The numbers are reported as they stand. **This override is recorded here as a
deliberate decision, not a quietly skipped step.**

### Other work landed today

- `even_trips()` added to `odd_only.py` â€” membership stays in ONE file.
  Verified odd 13 + even 12 = all 25.
- `tune.py` refactored to take `trips_fn`; **every sweep row reprinted
  identically**, proving the refactor moved plumbing and not maths.
- `hotspots.py` sanity check now **PASSES or FAILS out loud** instead of printing
  the condition and leaving the reader to check by eye. Rule 26.
- `.gitignore` had a missing newline gluing `.DS_Store` to `data/*.png`, so
  **neither rule worked**. Fixed. Results, hotspots and heatmaps now tracked â€”
  they are small, and they are the evidence.
- `signs.json` was missing the sign's top line, **GATE A-C ->**, present
  throughout the shoot. Same board, same position, nothing re-measured, no
  distance changed. It makes the audit claim STRONGER: the sign lists three
  destinations and TOILETS and LOUNGE are on none of them. A signage **gap**,
  not a sparse sign.
- `show_origin.py` draws the calibration corners on a real frame. The tile
  diamond sits on the actual tiles â€” confirmed by eye.
- U-turn timing offset found: `find_uturns` stamps frame `i` but compares heading
  at `i` vs `i + hold`, so the marker lands ~1 s **before** the visible pivot.
  Systematic, inside the Â±3 s tolerance, affects no score. **Reported, not fixed
  â€”** changing detector behaviour after seeing held-out results is the exact
  thing this project is built to avoid.

**Notes:** Started with three hours of admin that turned out to be necessary.
The project-folder copy of this file was a **Day 8 version** â€” 1300 lines, rules
stopping at 22, the word "odd" appearing zero times â€” while claiming to be
current at `35ee54d`. Separately, commit `0f089fb` carried the message
"Re-date Day 13-21 headers", changed 43 lines, and changed **no dates at all**.
Both caught by checking rather than reading. Rules 47 and 48 below.

**Quiz score: 3/3 (multiple choice â€” easier than cold recall, Rule 13).**
Q1 why a second `--all` run is contamination even with no changes; Q2 why
`min_seconds` must not drop to 1.5 after seeing the miss; Q3 which command
exposed `0f089fb` and what it had really changed.

## Day 16 — Fri 28 Aug — Dashboard part 1 (Streamlit)
- [x] Upload / select video
- [x] Analyse button + progress indicator
- [x] Show the processed video

**Status:** COMPLETE. All three boxes, plus the CFR gap and the double-
undistortion both found AND closed the same day - nothing was carried to
Day 17. Streamlit dashboard runs; both sources show the same things and the
upload path now runs all four real pipeline stages.

**Notes:**

DAY 16 RAN A DAY EARLY (Thu 27 Aug), Day 15 having finished on schedule.

THE DASHBOARD (`dashboard/app.py`, 5618 bytes)
- Radio: recorded clip (13 pre-computed) or upload.
- Recorded path: selector reads `trips_examined` from `results.json`, plays the
  h264 copy from `data/web/`.
- Upload path: file written to `data/uploads`, Analyse runs undistort -> track ->
  `analyse_one` as subprocesses, each failure surfaced in the UI with its last
  five output lines. Progress bar driven by the tracker's own `Frame N` prints -
  no change to `trajectories.py`.
- Tracked video re-encoded to h264 and shown above the events table, so the
  upload path displays what the recorded path displays.

TIMING - MEASURED, NOT GUESSED (Rule 43)
`cuda False`: yolo11m runs on CPU. clip2, 324 frames, 177.85 s = **0.549 s per
frame, 8x slower than realtime**. All 13 clips = 20,157 frames = **~3 h 04 m**.
Largest, clip1 at 2691 frames, is ~25 min. Consequence: a full re-run is a
three-hour wall-clock cost and must be planned, not discovered on Day 21.
This killed the live-Analyse-in-the-demo design. The button is real and stays,
but the demo shows pre-computed results; the "~8x video length on CPU" figure is
printed next to the button as a spec, not an apology.

THE EVIDENCE WAS NOT IN GIT
`.gitignore` line 18, `data/output/*`, was hiding all 13 `_traj.json` files - the
0.17 MB of text every result in this project is computed from. `results.json`,
`hotspots.json` and the heatmaps were tracked; **the inputs to them were not**. The
repo held the conclusions and none of the evidence, and the evidence existed in
exactly one untracked folder on one laptop. Fixed with `!data/output/*_traj.json`;
13 files committed as `2ed4fce`.

DETERMINISM CONFIRMED (a free result)
Re-running the tracker on clip2 returned MD5 `F5541AE670F7A963EC93676A29ACD763`,
byte-identical to before. Same video in, same file out. Anyone who clones the
repo and runs it gets these numbers, not numbers that wobble.

THE BROWSER WOULD NOT PLAY THE PROCESSED VIDEOS
OpenCV writes `FMP4` (mpeg4 Simple Profile). Edge draws a full player, shows
`0:00`, and silently refuses to decode - **no error anywhere**. Confirmed by
dragging the file into the browser, not deduced from the fourcc. All 13
re-encoded to h264/avc1/yuv420p into `data/web/` in ~19 s each; the boxes were
already burned into the pixels, so YOLO was not re-run. `data/web` is 79.3 MB and
stays out of git - regenerate with the ffmpeg loop.

`analyse_one.py` - AND WHY `build_events.py` WAS NOT TOUCHED
`build_events.py` filters tracks against `trip.csv` before any detector runs. An
uploaded video has no trips, so it would be skipped and return zero events with
no error. Rather than add a branch to the file that guards the held-out
evidence, uploads got their own script. **`build_events.py` diff is unchanged
since Day 15 and stays that way to submission.**
- All eight thresholds passed **explicitly**, because the function defaults
  (`max_speed=0.25`, `min_seconds=1.5`, `max_gap=1.0`, `min_speed=0.15`) are NOT
  the locked values (0.30 / 2.00 / 0.00 / 0.20). Silence would have run different
  maths and produced plausible, unvalidated events. **Rule 51.**
- EQUIVALENCE TESTED: clip10 gives 4 events identical to `results.json` in type,
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
  rule 50. `docs/limitations.md` and `update_day15.ps1` were absent from disk
  entirely. All three restored. The handoff warned about exactly this and it was
  still true. **Rule 46, confirmed a second time.**
- Midnight: `analyse_one.py` was overwritten with a copy of the dashboard (133
  insertions, 87 deletions). It printed Streamlit warnings and wrote nothing.
  Recovered by `git restore` **only because it had been committed 40 minutes
  earlier**. This is the small-commits discipline paying out in real time.

THE CFR GAP - FOUND AND CLOSED THE SAME DAY (nothing carried forward)
First state: the app's chain was upload -> undistort -> track, while the real
pipeline is raw -> CFR -> undistort -> track. **The app skipped CFR.**

Why it mattered: trajectories store `frame_number` and never a timestamp, so
frame numbers ARE the clock. Footage that is not exactly 15 fps makes every
speed silently wrong. Day 9 established this; the dashboard had quietly
reintroduced it.

**Fixed:** the app now runs the Day 9 command as its first stage -
`ffmpeg -vf scale=1024:576 -r 15 -an -c:v libx264 -crf 18 -pix_fmt yuv420p` -
and hands the CFR output to the undistorter. Verified end to end on raw clip6:
all four stage files landed in `data/scratch` with a clean timeline (CFR
4:43:12, undistorted 4:43:28, tracked 4:49:10, analysed 4:49:13).

CFR conversion is **safe to repeat**, which is what makes always running it
correct rather than risky: Day 9 already proved `scale=1024:576` on a 1024x576
file does nothing, and `-r 15` on a 15 fps file does nothing.

THE ASYMMETRIC BOWING - DIAGNOSED, NOT DISMISSED
The dashboard's tracked video came out visibly bent, worse on one side, while
`undistort_check.jpg` from calibration day is symmetric and fine.

Cause: **the principal point is off centre.** `K` gives `cx = 537.70`,
`cy = 278.44`; the frame centre is 512, 288. The lens centre sits 25.7 px right
and 9.6 px up from the middle, and undistortion pushes pixels outward from THAT
point. One pass hides it. **Two passes double it** - and uploading from
`data/undist` ran it twice. Confirmed by extracting frame 150 from a
single-pass and a double-pass copy of clip6 and comparing: once straight, twice
bent.

`rms = 2.17` px over 40 views. Under 1.0 is good; 2.17 is mediocre. Belongs in
limitations.md and is not currently there.

**Every frame the Day 15 numbers were computed on had exactly one pass. The
results stand.**

WHY THERE IS NO "UNDISTORT?" CHECKBOX
Considered and rejected twice. It hands the project's hardest judgement call to
someone who cannot make it, and judging is video-only, so a wrong tick gets no
correction. Detection was attempted instead and **failed honestly**: raw
footage is a MIX of 1024x576 and 1280x720 (Day 9: five clips were 720p), so
dimensions cannot separate raw from cfr from undist. Corner-brightness
detection was measured and rejected - cfr `[185,104,9,177]` vs undist
`[187,42,15,16]` invert on some corners and depend on scene content, so it
would work on clip6 and misjudge clip3. **Nothing in the file says which it
is.** So it is stated on screen as a requirement, not detected.

STAGE CHECKPOINTS AND A PROGRESS BAR THAT MOVES
Five named stages - Convert, Undistort, Track, Detect, Encode - tick from
upcoming to running to done as the pipeline advances, driven by real subprocess
completion, not a timer.

The bar itself sat dead then jumped. Not buffering: `trajectories.py` printed
`Frame N` every **100** frames, and clip6 is 352 frames, so the bar received
exactly three updates in three minutes. Changed to every 10.

**The change was proved cosmetic rather than asserted to be.** It is a print
inside an `if`, a 1-line diff - and re-running clip2 afterwards returned MD5
`F5541AE670F7A963EC93676A29ACD763`, byte-identical to the morning's run. The
determinism check from earlier in the day became the tool that verified a later
change to the same file.

**Quiz score:  2 /3**
Q1 (why no P/R on uploads) and Q3 (why upload is camera-restricted) correct
first time. Q2 (why all eight thresholds are passed explicitly) needed three
explanations before it landed. Recorded as 2/3, not 3/3.

## Day 17 — Sat 29 Aug — Dashboard part 2
- [x] Event counts, hotspot map, event timeline
- [x] Precision/recall shown in the UI, not hidden in the README
- [x] Privacy-by-design statement visible on screen
- [x] **"Not SaaS" stated explicitly** — a dashboard makes people assume cloud.
      On-premises, self-hosted, footage never leaves the building.

**Status:** COMPLETE. All four boxes, six deliverables, verified on BOTH source
paths. The verification caught a real break in the upload path that would
otherwise have shipped. 8 commits, `8fac9b0` through the import fix.

**Notes:**

DAY 17 RAN OVERNIGHT from the end of Day 16, starting ~01:00 Sat 29 Aug.

THE PIPELINE UI (`dashboard/pipeline_ui.py`, new file, `8fac9b0`)
The five text stages became circular nodes on a segmented rail. Stage data is a
list of dicts, so stages can be added or reordered without touching the drawing
code. Hover and keyboard tooltips, `aria-label` on every node, state carried by
glyph as well as colour. Wired into `app.py` as `ece67e9`.

Three failures on the way, each MEASURED rather than reasoned about:
- **The nodes were ovals.** Two CSS guesses failed. DevTools gave the real
  number: `22.667 x 18.667` - genuinely wider than tall, not the pulse halo as
  theorised. Fixed by pinning `min-` and `max-` on both axes from one `--d`
  variable, so nothing - not flex, not the glyph, not `line-height` - can
  stretch it.
- **Dark mode filled the hollow nodes white.** `prefers-color-scheme` reads the
  OPERATING SYSTEM, not Streamlit; Streamlit was dark while Windows was light.
  Second attempt used `var(--background-color)`, which Streamlit does not
  publish here - confirmed by test, not assumed. Third attempt removed the need
  for a background entirely: upcoming nodes are transparent rings.
- **The rail showed through the transparent nodes.** Predicted before the change
  and confirmed on screen. One bar behind everything became one segment per gap.

TWO STAGE-STATE BUGS THE OLD TEXT RENDERER HID
`draw_stages(steps, 1, 2)` drew Undistort as NOT STARTED while Track ran, and
Convert never showed as running at all. Both invisible as text; both obvious as
circles. **A cosmetic upgrade exposed two logic errors that had shipped.**

ONE BAR, NOT TWO
The rail and Streamlit's `st.progress` sat stacked showing the same run. Two
bars disagreeing reads as a bug. The `st.progress` bar was deleted and the rail
now creeps within a stage from the tracker's `Frame N` prints, so one bar does
both jobs: which stage, and how far through it.

THE PANELS (`dashboard/panels.py`, new file)
Five functions, all read-only. **Every number on screen is parsed from a
committed file. Nothing is typed in.** The handoff note's copy of the
per-behaviour figures had to be treated as a weaker witness than
`per_behaviour_day15.txt` itself - Rule 39 - and the parser was checked against
all nine triples before it rendered anything.

SCOPE IS STATED ON EVERY PANEL
21 events comes from all 25 trips. 62/56 comes from the 12 EVEN trips only. Side
by side and unlabelled, a judge reads the second as describing the first. Each
panel now names its own scope on screen. The U-turn zero gets its own red box
rather than hiding inside the combined 59% - Rule 22.

`st.metric` DREW AN UP ARROW ON THE 0% U-TURN FIGURE
`delta_color="off"` greys the colour but keeps the arrow. On the one number that
most needs reading as bad, the UI drew an upward arrow. Removed; P and R moved
into a caption underneath.

THE HOTSPOT MAP - DRAWN AS WHAT IT IS
Hotspot coordinates are grid cell centres at `cell_m = 0.5`, not event positions.
Drawn as **squares at their true size**, not dots: a dot would claim a precision
the method does not have. The 21 individual events are plotted underneath, so the
cluster is visibly made of real detections. Event type carried by SHAPE as well
as colour, because colour alone fails on a compressed demo video. Sign and the
three junction openings plotted from `signs.json` - tape measure, not detector.
Rotated 90 degrees AT THE DRAWING LAYER ONLY so the plot matches the camera view;
no stored coordinate is altered. Orientation confirmed against the footage by eye,
because the data alone could not settle it.

HOTSPOT 5 VERIFIED AGAINST THE EVENTS
Counting dots on a screenshot suggested 4 events in a cell claiming 5. Querying
`results.json` returned five - 2 hesitations, 3 U-turns, matching the JSON's own
breakdown. **The map was right and the eyeball was wrong.** Rule 43 again.

clip4 IS ABSENT FROM `results.json` - AND THAT IS CORRECT
`results.json` covers 12 clips, not 13. All three clip4 rows are `EXCLUDE`,
"logged wasted on shoot night", with no trip numbers. `build_events.py` skipped
them correctly. **But clip4's notes record four events including TWO U-TURNS** -
exactly the behaviour the detector is weakest on. The exclusion was logged at
shoot time, before any labelling, and un-excluding it now would be choosing data
after seeing the result. Say it before a judge asks it.

A CAPTION THAT DID NOT MATCH ITS OWN PICTURE
The timeline's first caption claimed "events bunch in the middle of a walk".
The plot showed events at 15-20% and at 85%. **Withdrawn.** Replaced with a
measured claim: every event falls between **12.9% and 83.3%** of its walk, zero
in the first or last tenth. That is stronger AND true - a tracker losing people
at the frame edge would produce fake events exactly there, and none appear. Both
bounds are computed at render time.

THE TIMELINE IS PER-TRIP, NOT A SHARED CLOCK
`start_sec` is a time within its own clip and twelve clips overlap in range. One
axis would put clip1's 60 s beside clip8's 60 s as though they were the same
moment. Each trip is normalised to its own start and end from `trip.csv`.

THE PRIVACY CLAIMS WERE CHECKED BEFORE THEY WERE WRITTEN
- Searching `src/*.py` and `dashboard/*.py` for `requests`, `urllib`, `http`,
  `socket` returns **only** the local file picker and a folder on this disk.
- `build_events.py` and `hotspots.py` contain no `cv2`, no `VideoCapture`, no
  `.mp4`. They read JSON and write JSON.
- A trajectory file holds tracks keyed `"1"`, `"2"`, `"4"` - integers - each a
  list of five-number rows. No faces, no crops, no names.

First draft said "no faces, no crops, no names" directly above a video player
showing a recognisable person. Both statements true; together they read as a
contradiction. Rewritten to separate input from what is stored, which is the
stronger claim anyway: **delete every clip and every figure on the page still
reproduces.**

THE CHECK THAT CAUGHT THE FALSE COMPLETION
Before claiming the day done, the UPLOAD path was run end to end. It threw
`NameError: draw_stages is not defined` - the `from pipeline_ui` import had been
dropped from `app.py` while the panels import line was rewritten. The recorded
path never calls it, so the dashboard looked perfect. **The same class of miss as
Day 16.** Fixed, then both paths re-verified: all five sections render and the
video plays.

STILL OPEN AFTER TODAY
- `signs.json` `text` still says `GATE A-C`; the sheet says `GATES A-C`.
- "4 of the 4 hotspots" reads awkwardly in the map's finding line.
- `heatmap.py` dead `if False:` block; `to_json_safe` duplication;
  `odd_trips()` fieldname stripping; `odd_only.py` main block mid-file.
- README still says `Hotspot clustering | not built`. **Badly stale.**

**Quiz score: 3/3 (multiple choice - easier than cold recall, Rule 13).**

## Day 18 — ~~Mon 31 Aug~~ — Signage MVP — **CUT on Day 12, 26 Aug**
- [ ] User draws a box around a sign; OCR reads the text
- [ ] Arrow direction, basic
- [ ] Associate a sign with the nearest hotspot
- [ ] Generate a conservatively worded audit finding —
      *"possible signage issue associated with this hotspot"*, never *"this sign caused it"*

**Cut this whole day if Day 15 metrics need rescuing.**

**Status:** CUT on Day 12, 26 Aug. Not attempted.
**Notes:** OCR was never built. The signage audit landed on Day 14 by a different route — sign_A measured from the building, five clicks agreeing to 1 cm, sign text hardcoded because the corridor signs are fixed and already known. Measured, not read. The four boxes above describe OCR and stay unticked.
**Quiz score:      /3**

## Day 19 — ~~Tue 1 Sep~~ — Live sensor mode — **CUT from the plan, NOT abandoned**

> **Cut on Day 12 to make the 1 Sep target, and it should COME BACK.**
> VoltHacks is a hardware/IoT hackathon and the whole framing is "real camera,
> real data, not a simulation". A live webcam mode is the strongest form of that
> argument — the difference between showing a video of results and showing the
> system running. Estimated 4–5 hours.
>
> **Plan: first job on the buffer (2 Sep), if 1 Sep lands clean and nothing is
> broken.** Devpost allows edits until the deadline, so it can be added to an
> already-submitted entry. It is cut from the plan through 1 Sep only so that it
> cannot threaten the submission — a future session reading "CUT" should not
> treat it as dead.
- [ ] Same pipeline on a live webcam feed
- [ ] Record a short clip of a real U-turn detected live
- [ ] **OpenVINO conversion** — measure ms/frame before and after against the
      622 ms yolo11m baseline. Real Intel tech, real measured number, and it
      answers the "medium model is heavy" objection directly.

This is the hardware/IoT framing for VoltHacks, and the groundwork for Intel 2027.
Valuable — but not worth a broken detector. Cut it before cutting metrics.

**Status:**
**Notes:**
**Quiz score:      /3**

## Day 20 — ~~Sun 30 Aug~~ **worked Sat 29 Aug, a day early** — Polish + GitHub + README
- [ ] `.gitignore` verified (no `.venv`, no videos, no `*.pt`) — `git status` first
- [x] README: pitch, architecture, definitions, privacy, metrics, limitations
- [x] **Homography limitation paragraph** (Day 5) — in `docs/limitations.md` §4 and
      the new §4b. `floor_points.jpg` NOT added as evidence.
- [ ] Architecture diagram
- [ ] **SDG 11 framing** — accessible transport; wayfinding difficulty falls hardest
      on elderly, disabled and non-native speakers
- [ ] **Responsible-AI section:** what is collected, what is discarded, who consented,
      and where the system is biased (YOLO detection varies with body size, clothing
      and lighting; a wheelchair user's silhouette is not what it was trained on)
- [x] The commit history is the evidence of original work. Do not squash it.

**Status: PARTIAL — 3.5 of 7 boxes. 12 commits, `ff5a7c4` → `f231e2d`, all pushed.**
Four boxes remain: `.gitignore` verification, architecture diagram, SDG 11 framing,
Responsible-AI section. **Do not mark this day complete until they are done.**
**A second session ran late the same night — see "Day 20 (part 2)" below. It did NOT
close any of the four boxes.**

**A DAY-NUMBERING ERROR HAPPENED AND IS RECORDED SO IT DOES NOT RECUR.** This work
was called "Day 18" for most of the session, by me and by Claude, until PROGRESS.md
was opened. **Day 18 is the CUT signage MVP. Day 19 is CUT live sensor mode.** The
polish/README day is Day 20. Claude accepted the label without checking the file —
the exact failure the rest of the day was spent catching in other files. Rule 64.

**Notes:**

**The day's shape.** Day 20's list was estimated at 3.5–4.5 h and the documentation
half took about 50 minutes, because most of the work turned out to be already done
or unnecessary. The hours saved went into an unplanned dashboard theme.

**README — 5 commits.** Was badly stale: five rows reading `not built` for stages
that were built, no held-out numbers anywhere, and a Repository section listing 2
source files out of 33.
- `d0edca8` status table — the four built stages, and **the U-turn 0% stated in the
  summary row** rather than only in the detail. A number in the summary cannot be
  called hidden.
- `c2d5053` new held-out validation section — the full odd/even/all table, the
  U-turn zero explained, the 25-trip caveat.
- `78955ed` Repository section — grouped, real, points at `docs/`.
- `9466aed` a closing code fence that had been swallowed onto the end of a line.
  Caught because the diff showed **5 deletions where 4 were expected.**
- `462755d` corrections: threshold provenance, OCR status, two stale limitation
  claims.

**I WROTE A FALSE CLAIM INTO THE README AND CAUGHT IT ONE COMMIT LATER.** The
validation section as first committed said *"thresholds written before the detector
existed"*. That is true of three thresholds and **false of `MAX_GAP` and
`MIN_SPEED`**, which were tuned on Day 13. It went into the one section whose whole
job is honesty. Fixed in `462755d`, which now names the 3-blind / 2-tuned split
explicitly. **The correction is stronger than the original claim would have been.**

**`limitations.md` — 1 commit, `ee7de3b`, +50 lines.**
- **New §1c, clip 4.** `results.json` covers 12 clips, not 13. Clip 4's three rows
  are EXCLUDE, logged wasted on shoot night before labelling existed. Its notes
  record two U-turns — the detector's weakest behaviour. Un-excluding after seeing
  0% would be choosing data by result. Stated in the file so it is not discovered.
- **New §4b, lens calibration.** Read from `calibration_ezviz.npz`, not from notes:
  **RMS 2.17 px, 40 views, 1024×576, fx 651.2 / fy 653.9, principal point
  (537.7, 278.4), k1 −0.410.** The principal point is **+25.7 px off centre in x**,
  2.5% of frame width. Through the README's per-row scale, 2.17 px is ~0.9 cm near
  the camera and ~3.2–3.6 cm far. **No combined error figure is quoted** — the two
  errors are measured differently and do not add, and inventing a total would be a
  made-up number.
- **Summary corrected.** It still said *"the only sign, which lists three
  destinations"* — the pre-Day-16 wording. `signs.json` says THREE SEPARATE A5
  SHEETS. The corrected version is also the stronger claim: *three chances to be
  signposted, three misses.*

**`signs.json` — 1 commit, `da99752`.** `GATE A-C` → `GATES A-C`, matching the sheet
and every note in the same file. `git grep` confirmed no code reads the string.

**THE HANDOFF'S TO-DO LIST WAS WRONG THREE TIMES OUT OF FOUR.**
1. *"`signs.json` needs a second entry for the GATE A-C sign."* **WRONG, and acting
   on it would have broken the output.** The file's own `text_note` explains why one
   entry is correct: three identical coordinates would make `nearest_sign` arbitrary,
   and `hotspots.py` uses a strict `dist < best_d`, so sheets two and three could
   never win and would vanish from the output.
2. *"`heatmap.py` has a dead `if False:` block."* **Does not exist.** The only
   `False` matches are `box=False` keyword arguments in live drawing calls.
3. *"`odd_trips()` doesn't strip CSV fieldnames the way `all_trips()` does."* True
   but **inert** — proved by asserting `odd_trips() == the odd half of all_trips()`.
   Both return 13 trips, IDENTICAL. Nothing to fix, and no risk taken to find out.
4. *"`to_json_safe` lives in `build_events.py`; other scripts convert ad hoc."*
   True. **Deliberately not refactored** — see below.

**`to_json_safe` was documented, not deduplicated — `a421cf5`.** Both copies are
`return float(v)`. The obvious tidy is to import one from the other. **Refused:**
`build_events.py` produced the validated `results.json` on Day 15 and is frozen. A
duplicated 8-line helper costs nothing; a modified `build_events.py` costs the
credibility of the only uncontaminated result in the project. A comment in
`analyse_one.py` now says so, which reads better to a judge than a clean import.

**A RESOLUTION GUARD, FOUND BY CHECKING SOMETHING THAT TURNED OUT FINE — `f966b81`.**
`calibration_ezviz.npz` is calibrated at **1024×576**. `frame_720.png` exists and
the raw camera is 1280×720, so the question was whether `undistort_video.py` ever
applies a 1024-wide K to a 1280-wide frame. **All 13 CFR clips are 1024×576,
checked with ffprobe. No mismatch. Results are fine.**

But the script had no size check at all. `cv2.undistort` does not validate, so a
1280×720 file would have produced a plausible video with **every metre coordinate
wrong by 25%**, printed "Done", and never raised anything. Rule 5 in its purest
form. The script now refuses, and **the refusal was tested, not just the success**:
a 1280×720 file was generated with ffmpeg, fed in, refused, and `Get-ChildItem`
confirmed **no output file was created before the refusal.** Rule 65.

**DASHBOARD THEME — UNPLANNED, 3 commits, ~90 min.** Not on any checklist. Taken on
because the dashboard is recorded for the video, and re-theming after filming means
filming twice.

Direction: **the dashboard is built from the visual language of airport signage,
because signage is what the system audits.** Charcoal `#11151A`, signage yellow
`#FFD400`, one typeface at strict weights (Archivo — sign systems use one family and
a hierarchy, not a decorative pairing). High contrast is not taste: judging is by
video, and compression destroys pale colours on white.
- `a3887ad` `.streamlit/config.toml` + `dashboard/theme.py` + transparent matplotlib.
  **Three places share one palette and must stay in step.** Metric tiles became sign
  panels: soft corners, hairline edge, a yellow rule along the top the way a
  destination band sits above the text on an overhead sign.
- `f231e2d` **the sign marker was `#24292f` — invisible on charcoal.** The legend
  swatch was blank. The sign is the most important object on the map, since the whole
  finding is *people got confused before reaching the sign*. Now yellow, which is
  also semantically right: yellow is the destination colour, so the map now says
  *here is the sign, and here is where people failed to find it* in the palette.
- `f231e2d` also: the clip selector sits BELOW the charts and changes only which
  video plays. A judge who changes it and sees the map not move would read that as
  broken. One caption now says the figures are the finding across all 25 trips.
  Rule 54 applies to interface behaviour, not just to data.

**Hotspot confidence — `db4f935`.** The map treated all four hotspots alike.
Real counts, read from `hotspots.json`:

| hotspot | events | hesitations | U-turns | from sign |
|---|---|---|---|---|
| 1 | 5 | 2 | **3** | 0.65 m |
| 2 | 4 | **4** | 0 | 1.15 m |
| 3 | 3 | 3 | 0 | 1.21 m |
| 4 | 2 | 0 | **2** | 1.65 m |

**THE BIGGEST HOTSPOT IS MOSTLY U-TURNS, AND THE U-TURN DETECTOR SCORED ZERO.**
The panel currently leads with hotspot 1 — five events, three of them U-turns. A
judge who reads the accuracy panel and then the map can connect those two facts, and
nothing on the page connects them first. **Hotspot 2 is four hesitations and zero
U-turns: it rests entirely on the detector that scored 77% on trips it had never
seen.** That is the sentence to lead with. **NOT YET CHANGED — carried to Day 21.**

The confidence threshold was first written as "3 or more events", which would have
called three hotspots confident while `docs/limitations.md` says *report hotspots 1
and 2 with confidence; report 3 and 4 as secondary.* **The dashboard would have
contradicted the limitations file.** Set to 4, and the caption now gives the real
reason — they grew rather than moved when the second half of the trips was added —
instead of an arbitrary count.

**No durations are displayed anywhere.** Checked, because `limitations.md` §7 says
durations must not be quoted. Zero matches in `dashboard/`. A check that finds
nothing is still worth running: it converts hoping into knowing.

**A FILE WAS CORRUPTED AND RECOVERED.** A message containing two versions of the
same edit — one retracted mid-message — was pasted as one block, colliding two
f-strings onto one line and deleting the line between them. `git checkout HEAD --
dashboard/panels.py` restored it because it had been committed. **Same lesson as
Rule 63, second occurrence, different cause.** New Rule 67.

**Quiz score:      /3**

## Day 20 (part 2) — Sat 29 Aug, late — Face blur: built, verified, NOT applied

**HEAD `2f5bbd2`, pushed. 3 commits: `073a94c`, `50025db`, `2f5bbd2`.**
**None of the four outstanding Day 20 boxes were touched. They are all still open.**

**The outcome, and the sentence that goes in the Responsible-AI section:**

> *I built face blurring from the saved track boxes and verified zero uncovered
> frames. I don't apply it to the demo footage because all three participants
> consented to public release — but the tool is in the repo, because a real
> deployment wouldn't have consent from anyone walking through an airport.*

**That is a stronger answer than a blurred video.** It says the deployment case was
thought about, not just the footage that happened to be to hand. It becomes rehearsed
answer 12.

**`src/blur_heads.py` — `50025db`, tightened in `2f5bbd2`.** Reads
`data/output/*_traj.json`, blurs the head slice of each person box, writes
`data/web/<clip>_traj_blur.mp4`. Two modes: `--check <frame>` writes a PNG with yellow
rectangles drawn so alignment can be eyeballed before any video is made; `--run`
processes the clip. **The verification number is `UNCOVERED FRAMES INSIDE A TRACK: 0`**
— every frame inside any track's lifetime has a rectangle. That is a claim that can be
said out loud, unlike "I looked at it and it seemed fine".

**THE FIX THAT COST NOTHING BECAUSE OF A DECISION MADE ON DAY 3.**
`trajectories.py` line 68 saves `(foot_x, foot_y, frame_number, box_w, box_h)` —
pixels in the undistorted frame, `foot_x` the box CENTRE, `foot_y` the BOTTOM.
`box_w` and `box_h` had never been used by anything, for two weeks. **Because they
were saved, blurring was arithmetic on a file. Without them it would have meant
re-running YOLO over 13 clips at 0.549 s/frame — hours of compute.** Data saved
cheaply is data you can use later; data thrown away is gone.

**Measured facts, all from the data rather than from estimates:**
- Detection gaps are mostly **empty corridor**, not missed people. Clip 10: 9 gaps,
  5 of them longer than 20 frames, and only **5 frames** lost to short gaps. Clip 1: 9.
- Box shape across all **6626** boxes: median height/width **2.41**, 25th 1.97,
  75th 2.73, 95th 3.38, max **12.11** (a broken box, not a person).
- Holes inside a track are filled: **≤8 frames by interpolation**, longer ones by the
  **union of both endpoint boxes**, because guessing a path across 24 frames is not
  something that can be verified.
- JSON `frame_number` starts at **1**; video frame index starts at **0**.
- **`data/undist/` holds 13 clean undistorted videos with no overlay** — the escape
  route if the trajectory overlay ever needs redrawing from the JSON.

**KNOWN UNFIXED COSMETIC ISSUE.** When a person raises an arm, the YOLO box grows
taller **and wider**, so the blur moves up and sideways off the face. Capping the
height alone did not fix it, because the width grew too. **Not fixed, and it does not
matter, because the blur is not applied to the demo footage.** If it is ever needed
for a real deployment, the fix is to stop deriving head position from the box at all.

**FOUR MISTAKES CLAUDE MADE, RECORDED SO THEY DO NOT RECUR:**
1. **A number was used as evidence without being broken down.** "930 unblurred
   frames" was computed from one subtraction and used to argue the whole task should
   be abandoned. One follow-up question collapsed it to ~5 frames of real exposure
   plus an empty corridor. **Rule 39 pointed at Claude.** New Rule 69.
2. **A bug was "fixed" using the same measurement that caused it.** The raised-arm
   problem is caused by box height changing; the proposed fix derived head position
   from box height. The rectangle came out with its bottom above its top, so
   `pixelate` skipped it and **the blur vanished entirely**. New Rule 70.
3. **A placeholder was put inside a command block** and PowerShell tried to run
   `<PASTE_ONE_FILENAME_HERE>`. Same family as Rule 67.
4. **Stale output was judged as if it were new.** `--check` writes a PNG; it does not
   rewrite the video. Two edits were assessed against a video from before them. New
   Rule 68.

**`git add -A` STAGED ~70 FILES FROM `data/output_BACKUP_day16/`**, a folder that is
deliberately untracked — all 13 traj JSONs, the whole `calib_check/` directory, every
diagnostic JPG. Caught by reading `git status` before committing, and unwound with
`git reset`. **Rule 15, and the reason the workflow says `git status` FIRST.** New
Rule 71.

**TIME COST, STATED HONESTLY.** The blur was *correct* — zero uncovered frames — on
its first run. Seven further rounds went on how it looked: pixel size, softness, edge
fade, width, the ID box being covered, the raised arm. **Over an hour, on a cosmetic
property of a tool that was then deliberately not used.** Meanwhile the four scored
Day 20 boxes stayed at zero and the demo video is Monday. **Rule 19 in its purest
form: the interesting task ate the boring one, and the boring one is the scored one.**

**Quiz score:      /3**

## Day 21 — Mon 31 Aug — Demo video
- [ ] Storyboard the first 10 seconds FIRST
- [ ] Real system output only — zero fake numbers
- [ ] **Blur faces in every frame shown.** Proves the privacy claim instead of
      asserting it, and my sister is 10
- [ ] Edit, export, upload, **watch it back once end to end**

Structure (2 min, landscape):
1. 0–10 s — the problem, shown not told. No logo, no title card.
2. 10–40 s — raw footage → same footage with boxes, IDs, trails.
3. 40–70 s — an event firing live on screen.
4. 70–100 s — dashboard: hotspot map, signage finding in careful wording.
5. 100–120 s — precision and recall, and one honest limitation. **Do not skip this.**

**Status:**
**Notes:**

## Day 22 — Tue 1 Sep — ★ SUBMIT ★
- [ ] Description, screenshots, tech list, GitHub link, video link
- [ ] **Click every link yourself, logged out**
- [ ] SUBMIT TODAY. Do not wait for Day 23.

**Status:**
**Notes:**

## Day 23 — Wed 2 Sep – Fri 5 Sep — BUFFER ONLY (four days)
- [ ] Fix anything broken. **Deadline 22:00 Lisbon.**
- [ ] If the submission is already in, this day is for sleeping.

**Status:**
**Notes:**

---

## Risk register — what actually kills this project

| Risk | Day it bites | What it costs | Mitigation |
|---|---|---|---|
| **Camera knocked before the shoot** | any day before 9 | Re-record empty room, re-click, re-test homography — half a day | Shoot as early as the family allows. Don't touch the wall. |
| **Shoot day cancelled** | 9 | Everything downstream stalls | Confirm the slot in writing on Day 7. Sun 23 is the fallback. |
| **Footage unusable, found late** | 15 | Fatal — no time to reshoot | Full verification on the night of the shoot, not later |
| **Poor precision/recall** | 15 | Weak README, weak demo | Metrics moved before dashboard; Days 18–19 are sacrificial |
| **Unit error (cm vs m)** | 10 | Every speed 100x wrong, silently | One explicit conversion point, written down on Day 7 |
| ~~**Resolution mismatch vs calibration**~~ **— HAPPENED, Day 9** | would have bitten 15 | 5 clips (3 MISSING) producing silently wrong cm | Caught by `check_video.py` on every clip on shoot night. Fixed by scaling 720p→576p. **The risk register did not predict this one.** |
| **Contaminated ground truth** | 15 | Metrics become fiction | Labels blind on Day 11; held-out set untouched until Day 15 |
| **Overrun like Days 5–6** | any | Buffer already spent once | Days 18 and 19 are the release valve. Cut, don't extend. |

**The buffer has already been used once.** Days 5–6 consumed it. What is left is
Days 18 and 19 — and they are not spare time, they are two SHOULD-HAVE features
that can be dropped. There is no third cut after that.

---

## Vocabulary I must be able to explain without notes

| Term | My own words |
|---|---|
| Object detection | Finding *where* something is in a picture and drawing a box round it. YOLO does this for people. Day 1: 7 people, confidences 0.73–0.90. |
| Tracking / track ID | Detection finds people but forgets instantly. Tracking matches this frame's boxes against last frame's and keeps the same anonymous number on the same person. `persist=True` is what turns the memory on. The number is just a number — no face, no name. |
| Trajectory | The list of footpoints one track ID leaves behind, in order. Join the dots and you get the path that person walked. |
| Footpoint | The bottom-centre of the box — roughly where the feet are. We use it because feet touch the floor, and the floor is the surface we map. The box centre floats in mid-air and shifts when someone moves an arm. |
| Velocity | |
| Heading | |
| Angle between vectors | |
| Smoothing | |
| Homography | The recipe that turns a pixel into a spot on the floor. Built by clicking 4 points whose real-world distances I already know. Belongs to **one camera in one position** — scrap it on any remount. Mine covers 154 x 58.8 cm and is accurate to **0.6 cm along the walking axis**. |
| Extrapolation | Asking the model about ground **outside** the region it was taught. It answers just as confidently either way. My across-axis error tripled (0.6 → 2.0 cm) the moment I tested outside the 2-tile-wide strip. |
| Undistortion crop (`alpha`) | `cv2.undistort` straightens the picture by pulling edge pixels inward, so the frame narrows. `getOptimalNewCameraMatrix(alpha=1)` zooms back out to keep everything. **Chose the default crop** — the recovered pixels are the extreme edges, where the distortion model is least trustworthy, and changing it would invalidate the homography. |
| Hesitation event | |
| U-turn event | |
| Backtracking | |
| Clustering / DBSCAN | |
| OCR | |
| Precision | |
| Recall | |
| F1 score | |
| Privacy by design | |
| Confidence threshold | The model scores every guess 0–1; anything below the cutoff is binned. Too high → real people missed. Too low → shadows and legs become "people", which become fake trajectories, fake events, and a poisoned hotspot. Currently 0.25. Day 4: lowering it to 0.15 did NOT recover a lost detection — a threshold can only rescue a detection that exists. |
| Occlusion | One person blocking another from the camera. Detection merges them into one box; the tracker will swap their IDs. Seen on Day 1 in the 0.89 box. |
| ID switch | The tracker loses someone and re-registers them as a stranger with a new number. Visible as a colour change mid-walk. Dangerous because WayTrace measures per person over time — if a U-turn is split across two IDs, neither ID contains the reversal and the event becomes invisible. |
| Fragment track | A track only a few frames long — noise, a shadow, half a person. Has a position but no movement, so it reads as "never moved" and can become a fake hesitation event. Filter must be `int(fps * 1.0)`, not a hardcoded 25. |
| Variable frame rate (VFR) | The camera doesn't space frames evenly — it drops or adds them depending on light and motion. Deadly here because trajectories store `frame_number` and never a timestamp, so **frame numbers are the clock**. Uneven spacing = every speed silently wrong, worst during fast movement. Fixed with `ffmpeg -r 15`. Day 9: all 13 clips converted; eleven gained one duplicate frame, the two already above 15 fps gained none. Frame 150 is now exactly 10.000 s on every clip. |
| Resolution vs calibration | K, the distortion coefficients and the homography are all **numbers of pixels**. They only mean anything at the frame size they were measured at (1024x576). A 1280x720 frame puts the principal point and every homography source point in the wrong place, and **produces plausible wrong centimetres with no error**. Day 9: 5 clips were 720p. Fixed by scaling the video down, not by touching the calibration. |
| Field of view vs rescale | Two ways a frame can be a different size. **Rescale** = same room, more pixels — landmarks all move by one constant factor, calibration survives a resize. **Different FOV** = more or less room visible at the edges — a different optical view, needing its own calibration. Told apart by measuring landmark positions in both: mine were all exactly 1.25x, and 1280/1024 = 1.25. |
| Barrel distortion / fisheye | Wide CCTV lenses bend straight lines outward, worst at the frame edges. Breaks the footpoint and will break homography, because homography assumes straight world lines stay straight in the image. Fixed by measuring the distortion with `cv2.calibrateCamera` on a known grid — never by guessing a constant. Mine: **k1 = -0.41**, negative = barrel. |
| `imgsz` | The size YOLO resizes the frame to before looking at it. Not "bigger is better": trained near 640, so 1280 gave **zero** detections on my footage while 640 gave the best result. |
| Systematic vs random error | Random error scatters both ways and partly cancels out under smoothing. Systematic error leans the same way every single time, so it survives smoothing and becomes a real offset in metres. The tilted-camera footpoint was systematic — that's why it mattered. |
| Camera matrix `K` | Describes the camera **as an object**: focal length, and where the lens axis hits the sensor (the principal point). Nothing to do with where the camera is pointing. Survives remounting. |
| Distortion coefficients `dist` | How the glass bends light. Five numbers; the first (k1) is the big one. Negative = barrel. Also a property of the camera as an object — survives remounting. |
| RMS reprojection error | The mark on the calibration's homework. Take the fitted lens model, work backwards to predict where each chessboard corner *should* appear, compare to where it actually was, average all the gaps. Measured in pixels. Lower is better — but **a low score on easy, near-identical views is a flattering lie.** |
| Inner corners | What `findChessboardCorners` counts — the points where 4 squares meet, not the squares. A 10x7-square board has 9x6 inner corners. It's all-or-nothing: one corner clipped by the frame edge and the whole frame is silently rejected. |

Fill these in yourself as you learn them. If a box is empty on Day 20, that's a problem.

---

## Things I am NOT allowed to say

- "WayTrace detects confused passengers"
- "This sign caused the confusion"
- Any statistic I did not measure
- "It's basically YOLO" (it isn't — YOLO is the input layer)

---

## UNRESOLVED — must be closed before Day 15

**1. RESOLVED — 25 clean trips, not 24.** The shoot log holds 25 numbered clean
trips, 1–25, no gaps, plus **8** wasted takes (HANDOFF said 7). The "24" has no
supporting evidence and is discarded. Confirmed independently: 25 trips were
labelled from video, and every clip's walk count was reconciled against the log
afterwards. Clip4 did contain zero numbered trips, exactly as predicted.

**1b. NEW — the shoot log undercounts the footage.** clip3 holds four walks on
video; the log records three. abrish walked twice in a row and was logged once.
Every other clip reconciled exactly. The log is a check, never a source.

**2. Printed vs saved track counts disagree on every clip.** See Day 12.

**3. CLOSED, UNANSWERABLE — `data/New Text Document.xlsx`** was deleted without
being identified. It was untracked, so git never held a copy. The question can no
longer be answered — deleting an unknown destroys the evidence along with the
problem.

**4. `shoot_log.csv` is an .xlsx — CONFIRMED by evidence.** First two bytes are
`PK`, which is a zip, which is what an Office file is (Rule 30, proven rather
than inferred). The stray robot-vacuum note is still in row 1, so any parser
reads that sentence as the column names. **Still needs fixing.**

**5. Clips 2, 4, 5 and 6 produced zero events**, and clips 7–13 were labelled
after 20:00. Zero is a legitimate result, but a missed event is invisible — it
looks exactly like a clean trip. Re-check the late clips before Day 15.

---

## Rules I've learned the hard way

1. **Verify output, don't trust the absence of an error.** Day 3's indentation bug
   and Day 4's `START_FRAME` bug both printed success and wrote nothing usable.
2. **`Get-ChildItem` is the ground truth.** VS Code's file tree lies. File size in
   bytes tells you whether something real got written (257 vs 3,738,272).
3. **Change one thing, measure, then change the next.** Every model comparison in
   this file is trustworthy only because of this.
4. **Identical numbers to three decimal places mean the code never re-ran** — or the
   file was never saved. Check Ctrl+S before blaming the logic.
5. **A setting correct for one video is silently wrong for the next.** Hardcoded
   frame numbers, thresholds, filters and **file paths** all expire without telling you.
6. **Fix the upstream problem.** The arch ID switch was a detection failure, not a
   tracker failure. Fixing detection fixed the tracker for free.
7. **Retention drops when saturated.** Break before re-testing rather than pushing
   through — Day 2's 1/3 came at the end of a long second session.
8. **A good score on easy data means nothing.** Frames 0–500 of the terrace were
   empty. 40 calibration views from one minute were near-identical. Both gave clean
   numbers about nothing. Always ask: *was this test hard enough to fail?*
9. **Wrong input in, wrong conclusion out.** When `check_video.py` reported on the
   wrong file, the reasoning built on top of it was sound and still wrong. Verify
   the tool before trusting the theory.
10. **Clear output folders before re-running.** Stale results sitting next to fresh
    ones is how you inspect yesterday's work and draw today's conclusions.
11. **Measure thresholds, don't guess them.** `BLUR_MIN` was set by printing the
    sharpness of every kept frame, finding the worst bad one (342), and setting the
    gate just above it. Same discipline as measuring 5 tiles instead of eyeballing one.
12. **Commit after every working chunk.** Many small commits per day, not one at the
    end. Six days of work once sat uncommitted on one laptop.
13. **A test the system cannot fail proves nothing.** Round-tripping the 4 clicked
    homography corners returned them perfectly — they *were* the input. The number
    that meant something came from a corner outside the taught region.
14. **A point you cannot see is a point you must not click.** A guessed coordinate is
    indistinguishable from a measured one once it's in the array. Shrink the region
    instead — a smaller honest measurement beats a bigger invented one.
15. **`.gitignore` matches patterns, not intentions.** A 3.9 MB file called `c` walked
    straight past `*.mp4`. This is why `git status` runs before `git add .`, always.
16. **Units are a silent failure mode.** The maths has no idea what a centimetre is.
    Whatever unit goes in comes out. Write the unit down next to the file that holds it.
17. **A hardcoded frame number has no correct value — only "correct until the next
    file."** `START_FRAME` silently killed a run on Day 4 and again on Day 7, both
    times producing a 257-byte file that printed "Saved to". The fix was deleting
    it, not adjusting it. Read forward and count.
18. **Make the answer key before you take the test.** A speed of `1.2`, `120` and
    `0.012` all look like numbers. Measuring the real thing by hand first is the
    only way to catch a wrong answer that looks reasonable.
19. **The interesting task will always eat the boring one.** Shoot prep slipped
    twice because velocity was more fun to work on. When one task has a hard
    external deadline and the other doesn't, the deadline one goes first —
    written into the day's order, not left to willpower.
20. **Ctrl+S, then run. Never save during a run.** Python reads the file once, at
    launch. An 8-minute script gives you 8 minutes to save an edit that run will
    never see. The tell was a print that didn't appear — **an expected line missing
    is as much a signal as an error message.**
21. **Short time gaps magnify small errors.** 25 cm of footpoint wobble over
    1/15 s reads as 3.70 m/s. The same 25 cm over a second reads as 0.25 and
    nobody notices. Speed = distance / time, and dividing by a small number makes
    things big. This is what smoothing exists to fix.
22. **An average over a whole track hides the thing you are detecting.** ID 1
    averaged 0.11 m/s: a real walk plus a real 10-second stop, producing a number
    that describes neither. Events are "below X for Y seconds", never an average.
23. **A copy is not a backup until the count and the byte total match.**
    `Copy-Item` finishing silently proves nothing — same trap as the 257-byte file
    that printed "Saved to". 13 files and 143,138,488 bytes on both sides is the
    proof. (And OneDrive is *sync*, not backup: delete the source and the cloud
    obediently deletes too. It protects against the laptop dying, not against me.
    Never edit raw footage in place — always write to a new folder.)
24. **Calibration is measured in pixels, so resolution is part of the
    calibration.** Change the frame size and K, the distortion model and the
    homography are all silently wrong, with no error anywhere. 5 clips came off the
    camera at 1280x720 against a 1024x576 calibration. When footage and calibration
    disagree, **scale the footage to fit the calibration** — never adjust the
    calibration to fit the footage.
25. **Prefer the command that is harmless when it's unnecessary.** Running
    `scale=1024:576` over all 13 clips is safe because it's a no-op on the eight
    that already match. One command with no exceptions beats a correct list of
    exceptions, because the list is what gets forgotten. Same reasoning as one
    conversion point for /100. `Get-ChildItem`, `Select-String` and `git status`
    are the same shape: they cost nothing and cannot break a run.
26. **A loud failure is a cheap failure.** A wrong script path errored 13 times in
    a row and cost ten seconds. The hardcoded path in `check_video.py` said nothing
    and cost four wrong conclusions. Ranked by danger: silent wrong answer >
    silent no-op > loud crash.
27. **My own notes are a suspect witness.** HANDOFF.md claimed two files existed
    that did not. Written tired, at the end of a long day, recording intentions
    as completed work. Verify with the filesystem before building on any
    written claim — including my own from yesterday.
28. **One row = one thing.** Trips and events are different kinds of object and
    belong in different tables, joined by a shared id. Cramming both into one
    table means a trip with zero events has nowhere to exist, and a missing row
    is indistinguishable from an unlabelled one.
29. **Autofill manufactures confident-looking data out of nothing.** Dragging a
    column down invented twenty people and nineteen unwatched observations, with
    no error and no visual difference from real work. A filled cell is not
    evidence that anyone checked. Rule 1, in a spreadsheet.
30. **A file extension is a promise, not a fact.** `shoot_log.csv` is an .xlsx.
    Nothing verifies the name against the bytes. `file`, or the first two bytes
    (`PK` = a zip = an Office file), tell the truth.
31. **Never delete an event because you know why it happened.** Knowing the
    person was reading a sign is a mental state, unavailable to the camera, and
    filtering on it turns ground truth into a record of my memory of the shoot.
    Worse: stopping to read a sign IS the friction the system detects.
32. **Data easier than reality gives a score better than reality.** One person
    at a time with 5-second gaps made trip boundaries labellable — the right
    call — and also means the tracker never handled an occlusion. Name the
    limitation in the README before a judge names it for me.
33. **One column cannot answer two questions.** "Did this happen?" and "are the
    exact seconds right?" are different doubts. Stored together, the stricter one
    swallows the looser one — every U-turn was marked MAYBE because its end second
    was invented, and a SURE-only filter would have left zero U-turns to measure
    on Day 15. Split the doubts into separate columns, never the labels.
34. **A guard that has not been watched to fail is a guess.** The dropdown held
    the right values and still accepted `UTRURN` four times, because Sheets
    validation defaults to warning rather than rejecting. Typing a valid value to
    "test" it proves nothing. The only informative test is the one that should be
    refused. Rule 13, wearing a spreadsheet.
35. **Never hand-label what the machine already measures.** `zone` was a human
    reading thirds of a frame while the homography already produced the `y`
    coordinate in centimetres. 2 of 5 re-checked values were wrong and two more
    were "between" the thirds. The test: does the field come from *observing*
    something only a human can judge, or from *measuring* something already in the
    data? Watching → human. Measuring → machine.
36. **Never reinstate excluded data after seeing what is in it.** A take binned
    live, with information the footage does not contain, stays binned — even when
    it turns out to hold the richest behaviour in the dataset. Record what was
    lost and why; do not quietly edit the decision once the contents are known.
37. **Never rebuild a file from a copy you have not verified is the current
    one.** Length is not the risk; provenance is. PROGRESS.md was rebuilt from a
    Day 8 snapshot that a previous session could see, and ~90 lines written since
    then quietly stopped existing — no error, and the result read as complete.
    Check the source is current, edit in place where possible, and `git diff`
    before every commit. A stale copy that silently refreshes to your last commit
    is more dangerous than one that obviously looks old.
38. **A missed observation is invisible; an invented one is not.** Tired
    labelling does not produce obviously wrong events — it produces trips that
    look clean because nothing was noticed. Flag the session, not the row: the row
    gives no sign that there is anything to check.

39. **A summary is a weaker witness than the thing it summarises.** On Day 12
    the handoff was wrong four times — the path to `speeds.py`, the identity of
    the last commit, whether the PROGRESS restore was outstanding, and the sign
    in the trip rule — and the committed file was right every time. The handoff
    was written at 00:30 from memory; each file was written carefully, at the
    time, doing one job. Rule 27 extended: not just "verify with the filesystem",
    but **the artefact outranks any note about the artefact**, including one
    written yesterday, including one written by me.

40. **A walk-back is not a trip.** Every trip in the dataset is followed by the
    person returning to the start. That return contains a genuine, sustained 180°
    turn the U-turn detector fires on *correctly*, with no matching ground-truth
    row — a false positive by construction, not by bug. Half of every clip is
    walk-backs. Direction filtering happens BEFORE detection, never after.

41. **A stationary object has no direction.** Heading is computed from
    displacement, so when displacement is noise, heading is noise, and noise
    clears any angle threshold you like. Two false U-turns fired inside a
    labelled *hesitation* on trip 18. The fix is a speed gate, not a bigger
    angle: some quantities are undefined rather than merely uncertain, and no
    threshold on an undefined quantity is meaningful.

42. **One file, one tool.** An open editor holds a snapshot of a file taken when
    it opened. Edit that file from anywhere else and the editor's copy goes stale
    silently — and "Save" then overwrites the real work with no warning about what
    it contains. Twice on Day 14: `build_events.py` nearly lost its float32 fix,
    and `heatmap.py` sat in an editor showing ONE EMPTY LINE with unsaved changes
    while the real 3.7 kB file ran fine on disk. If a script is editing a file,
    close it in the editor first.

43. **When code and output disagree, test — do not theorise.** The heatmap text
    ghosting cost eleven patches, two broken files and four confident wrong
    diagnoses. What settled it was a ten-second test with exactly one possible
    answer: draw the same text at three sizes with a single call and nothing else
    on the image. Build the test that can only come out one way, and build it
    FIRST, not after the fourth theory.

44. **A test script must never write to the real output path.** `hotspots_test.py`
    wrote to `hotspots_odd.json`, so a throwaway 0.75 m experiment silently
    replaced the saved 0.5 m result. A test that overwrites the thing it is
    testing is not a test.

45. **A parameter tuned on one dataset can be actively harmful on another.**
    `max_gap` was invented on Day 8 to stop a long stop fragmenting, and it worked
    on the dev walk. On real shoot trips it does the reverse, gluing events to the
    slow moments around them: 7 false positives at 1.0, 4 at 0.0, with no hits
    lost either way. Sweep every inherited parameter against the real data.

46. **No copy of a file is authoritative unless git says so.** On 26 Aug the
    project-folder copy of this file was observably in TWO different states at
    once — one session read it at commit `58be847`, the same folder reported by
    the user as a Day 8 version with rules stopping at 22 and no mention of the
    odd/even split. Neither is the arbiter. **The working tree and GitHub are.**
    Any session offering to edit this file must diff its copy against the real
    one first and list every line it removes. Rule 37's sibling: 37 says never
    rebuild from an unverified copy; 46 says you cannot verify a copy by looking
    at it, only by diffing it against git.

47. **A commit message is a claim; the diff is the evidence.** Commit `0f089fb`
    was titled "Re-date Day 13-21 headers", changed 43 lines, and changed no
    dates at all â€” it was the Day 12â€“14 housekeeping: three checkboxes ticked,
    the 8/9 quiz recorded, Day 19 expanded, rule 46 added. All of it correct,
    all of it filed under a label describing something else, which made real
    work findable only by accident. Second occurrence in four days â€” the
    `MAX_GAP` whitespace replace on Day 14 also shipped a message for a change
    that had not happened. `git status` before `git add` catches the wrong
    *files*. Only `git show <hash> --stat` catches a commit whose *message*
    outran its content. Verify the number first, then put it in the message:
    "7 insertions, 7 deletions" is a claim you can be held to.

48. **A `}` alone on a line ends the command.** An `if { }` / `else { }` pasted
    into the console across several lines dies with "the term 'else' is not
    recognized" â€” and the write that lived inside the `else` never happens while
    every line before it reports success. Keep `} else {` on one line. In a
    `.ps1` file the same code runs fine, which is why this only bites when
    pasting. Sibling of Rule 17: the failure is loud in the wrong place and
    silent in the right one.

49. **A conditional is not a check.** `hotspots.py` printed "SANITY CHECK PASSES
    if every hotspot is on the approach side" â€” the same sentence whether it
    passed or failed, leaving a human to verify by eye. A check that cannot fail
    out loud is documentation, not a check. It now prints PASSED or FAILED and
    names the offending hotspot. Rule 26's sibling.

50. **When a plan's contingency meets a rule made later, record the override.**
    Day 15's block said to fix the detector if recall was poor. Recall was poor.
    Fixing it would have contaminated the held-out evidence â€” a discipline
    adopted after that contingency was written. Overriding an old plan is often
    correct; doing it silently is how a project loses track of what it decided
    and why.
51. **A default is a value you did not choose.** `find_hesitations` defaults to
    `max_speed=0.25`; the locked value is 0.30. Calling it without naming every
    argument runs maths that was never validated, produces events that look
    entirely reasonable, and raises nothing. Pass every threshold explicitly,
    every time.
52. **Same filename, different folder, same output path.** `trajectories.py` names
    its output from `basename` only, so `raw/clip2.mp4`, `cfr/clip2.mp4` and
    `undist/clip2.mp4` all write to `clip2_traj.json`. A timing test on the wrong
    copy would have silently overwritten a file every Day 15 number depends on.
53. **A player that draws controls has not necessarily decoded anything.** Edge
    showed a full video player, `0:00`, and an empty scrub bar for a codec it
    could not read. Absence of an error is not evidence of playback - drag the
    file into the browser and press play.

54. **When you cannot detect it, say it - do not offer a checkbox.** Nothing in an
    mp4 records whether it has already been undistorted. Dimensions do not
    separate raw from cfr from undist; corner brightness inverts by scene. A tick
    box would have moved the judgement onto a judge who cannot make it, in a
    video-only submission where a wrong tick is never corrected. State the
    requirement on screen instead.
55. **A verification built for one purpose is reusable for the next.** The MD5
    determinism check on clip2 was run to answer "does this pipeline reproduce?".
    Hours later the same fingerprint proved that changing a print frequency in
    `trajectories.py` had altered nothing. Cheap checks compound.
56. **A dead progress bar is usually a quiet source, not a broken display.** The
    bar was correct; `trajectories.py` only spoke every 100 frames and the clip
    was 352 frames long. Three updates in three minutes looks identical to
    broken. Count the updates before rewriting the display.

57. **A browser refresh reruns the script, not its imports.** Editing
    `panels.py` and pressing refresh changed nothing three separate times on
    Day 17: Streamlit keeps an imported module in memory. The fix that "did not
    work" had worked. **Restart the server after editing an imported file.**

58. **Auto-indent puts a pasted function inside the one above it.** Twice on
    Day 17 a new top-level `def` landed with 4 or 8 leading spaces, nesting it
    inside `hotspot_map` and throwing `IndentationError` on its own docstring.
    Verify with `("[" + ($_ -replace ' ', '·') + "]")` - the eye cannot count
    leading spaces, and "press Backspace once" was wrong when the answer was
    eight.

59. **A caption is a claim; check it against its own picture.** "Events bunch in
    the middle of a walk" was written above a plot showing events at 15% and at
    85%. A judge checks the sentence against the image in front of them, and a
    caption that fails makes every other number suspect.

60. **The path you did not open is the path that is broken.** A missing import
    threw only on the upload branch, because the recorded branch never calls
    that function. The dashboard looked complete. **Exercise every path before
    claiming a day done** - this is the second day running that this check
    caught a false completion.

61. **A truncated paste is a syntax error, not a missing file.** 155 lines
    arrived where 178 were sent, ending mid-expression. Python reported an
    unclosed bracket, which sends you hunting one character instead of counting
    lines. **Check the line count after any long paste.**

62. **The editor's copy and the disk's copy can disagree, and the editor wins on
    save.** After fixing indentation from PowerShell, VS Code refused to save
    with "the content of the file is newer" and offered Overwrite - which would
    have restored the broken version. Close the tab rather than overwrite.

63. **Delete-and-append is not replace.** "Add this at the end of the file" was
    read as select-all-and-paste and wiped four working functions out of
    `panels.py`. They came back from `git checkout HEAD -- <path>` because they
    had been committed twenty minutes earlier. **This is what committing after
    every working chunk is for.**

64. **A to-do item is a claim about a file, and claims decay. Open the file
    before doing the work.** Three of Day 20's four tidy jobs were wrong: the
    `heatmap.py` dead block did not exist, the `odd_trips()` fieldname difference
    was provably inert, and **the `signs.json` "missing second sign entry" would
    have broken `nearest_sign` if acted on** — the file itself explains why one
    entry is correct. The same failure hit the day number: this was called
    "Day 18" for hours because nobody opened PROGRESS.md, where Day 18 is the cut
    signage MVP. **A note about a file is weaker evidence than the file.**

65. **A guard proven not to fire is not proven.** The new resolution check in
    `undistort_video.py` passed a 1024×576 clip and ran to 2691 frames — which
    demonstrates nothing about the rejection path. Only feeding it a deliberately
    wrong 1280×720 file proved it refuses, and only `Get-ChildItem` proved it
    refuses **before** writing an output file. Test the rejection, not just the
    acceptance. Rule 49's sibling, and Rule 60's.

66. **`Measure-Object -Line` skips blank lines. It is not `wc -l`.** A predicted
    diff size was wrong by a factor of two because one count came from PowerShell
    and the other from `wc`. Comparing two different counters produces a fake
    discrepancy, and a fake discrepancy wastes the attention a real one needs.
    Related: **`git grep` and `git show` read the COMMITTED file, not the disk.**
    Searching for an uncommitted edit with `git grep` returns nothing and looks
    like the edit failed. Use `Select-String` for the working copy.

67. **Two versions of one edit in a single message become one corrupted paste.**
    A message that gave an edit, retracted it mid-message, then gave a simpler
    one was pasted as a single block. Two f-strings collided on one line and the
    line between them was deleted. **One instruction per message, and never a
    retraction in the same message as the thing it retracts.** Recovered by
    `git checkout HEAD -- <path>`. Rule 63's cause was ambiguous wording; this
    one's cause was ambiguous quantity.

68. **A "check" mode does not rewrite the output.** `blur_heads.py --check` writes a
    PNG; only `--run` remakes the video. Two edits in a row were judged against a
    video made before either of them, and both were reported as "nothing changed".
    **After editing, re-run the thing that produces the artefact, then look.**
    Rule 43's sibling: measure, but measure the current thing.

69. **A number is not evidence until it is broken down.** 930 frames "with no
    detection" in clip 10 looked catastrophic and was used to argue for abandoning
    face blur entirely. Grouping the gaps by length took one command and showed 5 of
    9 gaps were longer than 20 frames — an empty corridor between walks — and only
    **5 frames** were real short-gap exposure. **A single aggregate can be as
    misleading as an average.** Rule 22's sibling, and the reason to ask "made of
    what?" before acting on any total.

70. **Do not fix a bug using the same measurement that caused it.** The blur jumped to
    a raised hand because the YOLO box grows taller when an arm goes up. The proposed
    fix computed head position as `y2 - box_height * 0.95` — still box height. The
    rectangle came out inverted, `pixelate` skipped it, and **the blur disappeared
    from the whole video**. Identify which quantity is unreliable, then use a
    different one.

71. **`git add -A` is not `git add <file>`.** One `-A` staged ~70 files from
    `data/output_BACKUP_day16/`, a folder kept untracked on purpose. Nothing was lost
    because `git status` was read before committing and `git reset` unwound it.
    **Stage named files; if `-A` is used, read the full status output before the
    commit, not after.** Reinforces Rule 15.

72. **A tool that is built and not used can still be the point.** Face blur was built,
    verified at zero uncovered frames, and then deliberately not applied, because all
    three participants consented to public release. **The honest statement — "the tool
    is in the repo because a real deployment wouldn't have consent from anyone walking
    through an airport" — is worth more than the filter would have been.** Building
    something to understand the problem and then declining to use it is a defensible
    engineering outcome, not wasted work. Sibling of the `to_json_safe` non-refactor
    and the `signs.json` non-fix.
