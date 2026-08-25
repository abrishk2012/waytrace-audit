# WayTrace Audit — Build Tracker

**Hackathon:** VoltHacks 2026 (Devpost)
**Hard deadline:** Sat 5 Sep 2026, 17:00 EDT = **22:00 Lisbon time**
**Target finish:** Day 22 (Fri 4 Sep) — SUBMIT. Day 23 (Sat 5 Sep) is buffer only.
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
- [x] Real-world units via homography
- [ ] U-turn detection
- [ ] Hesitation detection
- [ ] Hotspot clustering
- [ ] Precision / recall numbers from hand-labelled ground truth
- [ ] Polished dashboard
- [ ] Demo video

## SHOULD HAVE — cuttable, in this order

- [ ] Signage OCR + arrow direction (Day 18 — cut first)
- [ ] Live webcam "sensor mode" + OpenVINO (Day 19 — cut second)

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

## Day 9 — Sat 22 Aug — ★ THE SHOOT ★
**Highest-risk day in the project. Everything downstream eats this footage.**

- [ ] Consent on camera first — each person says their name and that they agree
- [ ] One continuous recording for the whole session
- [ ] 21 trips (~7 each), roughly two-thirds using the missing destinations
      (`TOILETS`, `LOUNGE` — deliberately absent from the wall sign)
- [ ] **5 full seconds between people. Never two in frame at once.**
- [ ] Log each trip on paper as it happens: trip number, destination card, clean or wasted
- [ ] **DO NOT TOUCH THE CAMERA**

**Same day, before bed — verify it, don't assume it:**
- [ ] `check_video.py` on the raw file — resolution, real frame count, duration
- [ ] `ffmpeg -r 15 -an` CFR conversion, then `check_video.py` again
- [ ] Undistort one frame and eyeball it
- [ ] Run the existing tracker over 500 frames and watch the preview
- [ ] **Back the raw file up to a second location before touching anything**

If the footage is unusable, that is discovered tonight, not on Day 15.
Sun 23 Aug is the reshoot slot if needed — hesitation work slides.

**Status: DONE** (ran Sun 24 Aug, not 22 Aug)
**Notes:** 13 clips, 25 numbered trips logged, 7 wasted takes. Every trip shot
alone with 5+ s between people and a hands-up walk-back to close each take —
exactly as planned on this day. That protocol is why the trip boundaries are
reliable, and it is also a stated limitation: the tracker never had to handle
two people at once, so ByteTrack's performance here overstates what it would do
on real airport footage. Say so in the README rather than waiting to be asked.
Backed up to OneDrive, verified by file count AND byte total (Rule 23).
**5 clips were 1280x720 instead of 1024x576** — would have silently broken the
homography on 3 of the 9 MISSING trips. Proved it was a pure 1.25x rescale with
the same field of view, then scaled down to match the calibration.
**Quiz score: n/a — shoot day**

## Day 10 — Sun 23 Aug — Hesitation detector v1  *(or RESHOOT)*
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

## Day 11 — Mon 25 Aug — ★ GROUND TRUTH LABELLING (BLIND) ★
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
Never regenerate this file.** Rule 37. **Still outstanding — Day 12 job one.**

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

## Day 12 — Wed 26 Aug — Hesitation + U-turn detectors, then tune **on ODD trips only**
**Re-scoped: detectors slid from Day 10. Labelling is COMPLETE — Day 11 done.**

- [ ] **BLOCKING FIRST:** `smooth()` verification in `speeds.py` — print
      unsmoothed vs smoothed side by side. Wobbles under ~20 cm must die; the
      real 1.6 m y-swing in ID 1 must survive. Outstanding since Day 8. Without
      it the hesitation detector fires on footsteps (Rule 21).
- [ ] **BLOCKING SECOND:** printed-vs-saved track count mismatch. clip1 prints
      10 IDs and saves 13; clip13 prints 11 and saves 16; clip12 prints 3 and
      saves 7. Same gap on every clip. Either the JSON holds short fragments the
      printout filters out, or the count measures something else. If fragments,
      the detector will invent events from 1-second scraps of people.
- [ ] **BLOCKING THIRD:** restore the four sections deleted from PROGRESS.md,
      by hand from `2c7b427`. Never regenerate the file (Rule 37).
- [ ] Hesitation detector v1 — test against trip 18's squared-off U-turn
- [ ] U-turn detector v1
- [ ] Tune U-turn thresholds against ODD trips only
- [ ] Tune hesitation thresholds against ODD trips only
- [ ] Kill false positives from tracker jitter
- [ ] **One variable at a time.** Every trustworthy number in this file came from that.
- [ ] **Do not open EVEN trips.** Touching them turns the Day 15 metrics into fiction.

**Status:**
**Notes:**
**Quiz score:      /3**

## Day 13 — Wed 26 Aug — Event log
- [ ] Event schema: type, track ID, timestamp, x, y (metres), confidence
- [ ] Every detected event written to `results.json`
- [ ] Events drawn on the output video as they fire
- [ ] Processing stays separated from display — the Day 1 decision that makes the
      demo immune to a slow CPU

**Status:**
**Notes:**
**Quiz score:      /3**

## Day 14 — Thu 27 Aug — Hotspot engine
- [ ] Cluster event coordinates (DBSCAN or grid density)
- [ ] Output hotspot centre, event count, type breakdown
- [ ] Heatmap overlay on a still frame
- [ ] Sanity check: does the biggest hotspot land at the fork? If it lands somewhere
      nobody stopped, something upstream is wrong

**Status:**
**Notes:**
**Quiz score:      /3**

## Day 15 — Fri 28 Aug — ★ VALIDATION METRICS (held-out set) ★
**Moved before the dashboard. If the numbers are bad, there is still time.**

- [ ] Open the EVEN trips for the first time
- [ ] Precision, recall, F1 per behaviour
- [ ] **Include the hard cases.** 100% recall on huge obvious U-turns says nothing
      about subtle ones, and easy-test scores do not go in the README (Rule 8)
- [ ] Write the honest limitations section, including the homography paragraph
- [ ] Practise explaining every number out loud

**If recall is poor:** Days 18 and 19 are the sacrificial days. Cut signage or
live mode and fix the detector. Metrics are MUST HAVE; those two are not.

**Status:**
**Notes:**
**Quiz score:      /3**

## Day 16 — Sat 29 Aug — Dashboard part 1 (Streamlit)
- [ ] Upload / select video
- [ ] Analyse button + progress indicator
- [ ] Show the processed video

**Status:**
**Notes:**
**Quiz score:      /3**

## Day 17 — Sun 30 Aug — Dashboard part 2
- [ ] Event counts, hotspot map, event timeline
- [ ] Precision/recall shown in the UI, not hidden in the README
- [ ] Privacy-by-design statement visible on screen
- [ ] **"Not SaaS" stated explicitly** — a dashboard makes people assume cloud.
      On-premises, self-hosted, footage never leaves the building.

**Status:**
**Notes:**
**Quiz score:      /3**

## Day 18 — Mon 31 Aug — Signage MVP  *(CUTTABLE — SHOULD HAVE)*
- [ ] User draws a box around a sign; OCR reads the text
- [ ] Arrow direction, basic
- [ ] Associate a sign with the nearest hotspot
- [ ] Generate a conservatively worded audit finding —
      *"possible signage issue associated with this hotspot"*, never *"this sign caused it"*

**Cut this whole day if Day 15 metrics need rescuing.**

**Status:**
**Notes:**
**Quiz score:      /3**

## Day 19 — Tue 1 Sep — Live sensor mode  *(CUTTABLE — SHOULD HAVE)*
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

## Day 20 — Wed 2 Sep — Polish + GitHub + README
- [ ] `.gitignore` verified (no `.venv`, no videos, no `*.pt`) — `git status` first
- [ ] README: pitch, architecture, definitions, privacy, metrics, limitations
- [ ] **Homography limitation paragraph** (Day 5) + `floor_points.jpg` as evidence
- [ ] Architecture diagram
- [ ] **SDG 11 framing** — accessible transport; wayfinding difficulty falls hardest
      on elderly, disabled and non-native speakers
- [ ] **Responsible-AI section:** what is collected, what is discarded, who consented,
      and where the system is biased (YOLO detection varies with body size, clothing
      and lighting; a wheelchair user's silhouette is not what it was trained on)
- [ ] The commit history is the evidence of original work. Do not squash it.

**Status:**
**Notes:**
**Quiz score:      /3**

## Day 21 — Thu 3 Sep — Demo video
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

## Day 22 — Fri 4 Sep — ★ SUBMIT ★
- [ ] Description, screenshots, tech list, GitHub link, video link
- [ ] **Click every link yourself, logged out**
- [ ] SUBMIT TODAY. Do not wait for Day 23.

**Status:**
**Notes:**

## Day 23 — Sat 5 Sep — BUFFER ONLY
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
23. **A copy is not a backup until the count AND the byte total match.** "Copy
    complete" is a message, not evidence.
24. **Calibration is measured in pixels, so resolution is part of the
    calibration.** 5 clips came off the camera at 1280x720 against a 1024x576
    calibration. Same lens, same view, silently wrong maths.
25. **Prefer the command that is harmless when unnecessary.** `Get-ChildItem`,
    `Select-String`, `git status` cost nothing and cannot break a run.
26. **A loud failure is a cheap failure.** `Cannot find path` took five seconds
    to read and saved an evening. The expensive failures are the silent ones.
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
37. **Never regenerate a long file — edit it in place.** Rewriting PROGRESS.md
    from an older copy deleted ~90 lines with no error and no visible gap.
    Anything not consciously carried across is gone, and the result reads as
    complete afterwards. Scoped edits to one section at a time, then `git diff`
    before committing.
38. **A missed observation is invisible; an invented one is not.** Tired
    labelling does not produce obviously wrong events — it produces trips that
    look clean because nothing was noticed. Flag the session, not the row: the row
    gives no sign that there is anything to check.
