# WayTrace Audit — Build Tracker

**Hackathon:** VoltHacks 2026 (Devpost)
**Hard deadline:** Sat 5 Sep 2026, 17:00 EDT = **22:00 Lisbon time**
**Target finish:** Day 22 (Thu 3 Sep). Days 23–24 are buffer only.
**Builder:** solo, 14, learning Python

---

## How to use this file

At the end of every working day:

1. Tick the boxes you actually completed. Do not tick things that "nearly" work.
2. Fill in **Status**: `DONE` / `PARTIAL` / `BLOCKED` / `SKIPPED`.
3. Write one line in **Notes** about what broke or what you learned.
4. Record your **Quiz score** (Claude asks you 3–5 questions each night).
5. Paste this day's block back to Claude at the start of the next session.

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

- [ ] Person detection
- [ ] Anonymous tracking IDs
- [ ] Trajectories drawn on video
- [ ] Real-world units via homography
- [ ] U-turn detection
- [ ] Hesitation detection
- [ ] Hotspot clustering
- [ ] Precision / recall numbers from hand-labelled ground truth
- [ ] Polished dashboard
- [ ] Demo video

## SHOULD HAVE

- [ ] Backtracking detection
- [ ] Signage OCR + arrow direction
- [ ] Live webcam "sensor mode"

## NICE TO HAVE

- [ ] Automatic sign detection
- [ ] Before/after signage experiment
- [ ] OpenVINO edge optimisation

---

## Camera configurations

| Name | What it is | Status |
|---|---|---|
| camA | Original wall mount, before tilting | superseded |
| camB | Tilted on mount to fix the arch ID switch | superseded |
| camC | Remounted after coming off the wall for lens calibration | **current** |

**File naming:** `date_location_cameraSetup_take`. Calibration videos omit the
camera letter, because lens calibration doesn't care where the camera is.

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
- [ ] Record 30 s of the **empty room on camC** — the homography calibration frame
      needs clean, unobstructed tile corners.
- [ ] Clear the floor completely: shoes, slippers, rug, trolley, shoe rack. The rug
      especially — it covers the tiles.
- [ ] Make the signs (see below).
- [ ] Fragment filter must become `int(fps * 1.0)`, not hardcoded 25. At 15 fps,
      25 frames = 1.7 s, and with a 2.7 m corridor that would silently discard
      real tracks.

### The signs
One wall sign at the fork, A4, thick black marker, eye height:

```
GATES A-C        →
BAGGAGE CLAIM    ←
EXIT             ↑
```

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
- [ ] Homography (moved to next session)

**Status:** PARTIAL — undistortion DONE, homography still to do

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

## Day 5 (carried) — Homography (pixels → metres)
- [ ] Record 30 s of the empty room on **camC**, floor completely clear
- [ ] Undistort the frame FIRST — homography on a distorted frame maps a bent world
- [ ] Click 4 floor points, supply their real-world distances (tiles = 29.4 x 30.8 cm)
- [ ] `cv2.findHomography` maps image coords to floor coords
- [ ] Speeds now reported in m/s instead of pixels/frame
- [ ] **Accuracy check:** build the homography from centre tiles, then ask it to
      measure a tile near the frame edge. If it says 29 cm, distortion is handled.
      If it says 38 cm, it isn't. Measured, not assumed — goes in limitations either way.

**Status:**
**Notes:**
**Quiz score:      /5**

## Day 6 (carried) — Smoothing + velocity
- [ ] Smooth noisy trajectories
- [ ] Compute speed over time per track
- [ ] Compute heading (direction of travel) per track

**Status:**
**Notes:**
**Quiz score:      /5**

## Day 7 — Wed 19 Aug — U-turn detector v1
- [ ] Angle between "before" and "after" movement vectors
- [ ] Flag reversals above threshold
- [ ] Require minimum travel distance either side

**Status:**
**Notes:**
**Quiz score:      /5**

# WEEK 2 — Make the computer understand behaviour

## Day 8 — Thu 20 Aug — U-turn tuning
- [ ] Hand-label real U-turns in the test clip
- [ ] Tune thresholds against those labels
- [ ] Kill false positives from tracker jitter

**Status:**
**Notes:**
**Quiz score:      /5**

## Day 9 — Fri 21 Aug — Hesitation detector
- [ ] **Absolute speed threshold** — speed below X m/s sustained for Y seconds.
      NOT a per-person baseline: the corridor is 2.7 m, too short to establish one.
      See Day 4. This limitation gets stated plainly in the README.
- [ ] Ignore people who are simply stationary the whole time
- [ ] Sanity-check X and Y against a normal walking pace measured from the footage

**Status:**
**Notes:**
**Quiz score:      /5**

## Day 10 — Sat 22 Aug — Hesitation tuning + event schema
- [ ] Tune against hand labels
- [ ] Define the event record: type, track ID, timestamp, x, y, confidence

**Status:**
**Notes:**
**Quiz score:      /5**

## Day 11 — Sun 23 Aug — Event log
- [ ] Every detected event written to `results.json`
- [ ] Events also drawn on the output video as they happen

**Status:**
**Notes:**
**Quiz score:      /5**

## Day 12 — Mon 24 Aug — Hotspot engine
- [ ] Cluster event coordinates (DBSCAN or grid density)
- [ ] Output hotspot centre, event count, type breakdown
- [ ] Heatmap overlay on a still frame

**Status:**
**Notes:**
**Quiz score:      /5**

## Day 13 — Tue 25 Aug — Backtracking (cut this if behind)
- [ ] Simple revisit-with-opposite-heading detector
- [ ] If it isn't working by end of day, mark SKIPPED and move on

**Status:**
**Notes:**
**Quiz score:      /5**

## Day 14 — Wed 26 Aug — Signage MVP part 1
- [ ] User draws a box around a sign
- [ ] OCR reads the sign text
- [ ] Store sign position + text

**Status:**
**Notes:**
**Quiz score:      /5**

# WEEK 3 — Make it a product

## Day 15 — Thu 27 Aug — Signage MVP part 2
- [ ] Arrow direction (basic)
- [ ] Associate sign with nearest hotspot
- [ ] Generate a conservatively worded audit finding

**Status:**
**Notes:**
**Quiz score:      /5**

## Day 16 — Fri 28 Aug — Dashboard part 1 (Streamlit)
- [ ] Upload / select video
- [ ] Analyse button + progress indicator
- [ ] Show processed video

**Status:**
**Notes:**
**Quiz score:      /5**

## Day 17 — Sat 29 Aug — Dashboard part 2
- [ ] Event counts, hotspot map, event timeline
- [ ] Signage audit panel
- [ ] Privacy-by-design statement visible in the UI

**Status:**
**Notes:**
**Quiz score:      /5**

## Day 18 — Sun 30 Aug — Live sensor mode (hardware angle)
- [ ] Same pipeline running on a live webcam feed
- [ ] Record a short clip of a real U-turn being detected live
- [ ] **OpenVINO conversion** — measure ms/frame before and after against the
      622 ms yolo11m baseline. Real Intel technology, real measured number, and
      it answers the "medium model is heavy" objection.

**Status:**
**Notes:**
**Quiz score:      /5**

## Day 19 — Mon 31 Aug — Ground truth labelling
- [ ] Watch the evaluation clip and log every real event by timestamp
- [ ] Do this BEFORE looking at what the system found
- [ ] **Define what counts as an event before counting anything** (Day 2 lesson)

**Status:**
**Notes:**
**Quiz score:      /5**

## Day 20 — Tue 1 Sep — Validation metrics
- [ ] Compute precision, recall, F1 per behaviour
- [ ] **Include hard cases, not just obvious ones.** 100% recall on huge obvious
      U-turns says nothing about the subtle ones. Easy-test scores don't go in
      the README.
- [ ] Write an honest limitations section
- [ ] Learn to explain these numbers out loud

**Status:**
**Notes:**
**Quiz score:      /5**

## Day 21 — Wed 2 Sep — Polish + GitHub + README
- [ ] `.gitignore` (no `.venv`, no big videos, no model weights)
- [ ] README with pitch, architecture, definitions, privacy, metrics, limitations
- [ ] Architecture diagram
- [ ] **SDG 11 framing paragraph** (sustainable cities / accessible transport;
      wayfinding difficulty falls hardest on elderly, disabled and non-native
      speakers). Useful for VoltHacks, essential for Intel 2027.
- [ ] **Responsible-AI section:** what's collected, what's discarded, who consented,
      and where the system is biased (YOLO detection varies with body size, clothing,
      lighting; a wheelchair user's silhouette is not what it was trained on).

**Status:**
**Notes:**
**Quiz score:      /5**

## Day 22 — Thu 3 Sep — Demo video
- [ ] Storyboard the first 10 seconds FIRST
- [ ] Record real system output only — zero fake numbers
- [ ] **Blur faces** in every frame shown — proves the privacy claim instead of
      asserting it, and my sister is 10
- [ ] Edit, export, upload

Structure (2 min, landscape):
1. 0–10 s — the problem, shown not told. No logo, no title card.
2. 10–40 s — raw footage → same footage with boxes, IDs, trails.
3. 40–70 s — an event firing live on screen.
4. 70–100 s — the dashboard: hotspot map, signage finding in careful wording.
5. 100–120 s — precision and recall, and one honest limitation. **Don't skip this.**

**Status:**
**Notes:**
**Quiz score:      /5**

## Day 23 — Fri 4 Sep — Devpost submission
- [ ] Project description, screenshots, tech list, GitHub link, video link
- [ ] Click every link yourself
- [ ] SUBMIT (do not wait for Day 24)

**Status:**
**Notes:**

## Day 24 — Sat 5 Sep — BUFFER ONLY
- [ ] Fix anything broken. Deadline 22:00 Lisbon.

**Status:**
**Notes:**

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
| Homography | |
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
| Variable frame rate (VFR) | The camera doesn't space frames evenly — it drops or adds them depending on light and motion. Deadly here because trajectories store `frame_number` and never a timestamp, so **frame numbers are the clock**. Uneven spacing = every speed silently wrong, worst during fast movement. Fixed with `ffmpeg -r 15`. |
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
