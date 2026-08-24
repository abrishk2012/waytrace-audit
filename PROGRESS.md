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

---

## How Claude must teach me — standing rules

These are not preferences. Breaking them is how I end up copying commands I do not
understand, which is how I end up unable to defend this project to a judge.

1. **Explain like I am 3.** Short sentences. Plain words. A concrete analogy for
   every new idea. If a sentence needs a second sentence to explain it, the first
   sentence was wrong.
2. **Two steps at a time. Then stop.** Give Step 1 and Step 2, then wait for me to
   say I have done them. Never a wall of ten steps.
3. **Every step in full detail.** Exact folder. Exact filename, before and after.
   Exact command to type. Exact button to click. Never "change the path" — say
   *which line, to what*. If Claude is guessing at my files, it must ask to see
   them first instead of guessing.
4. **Brutal honesty over reassurance.** If something is broken, behind, or bad,
   say so plainly with the number attached.
5. **`[LEARN THIS]`** marks the ideas I must be able to explain without notes.
6. **Remind me to commit** after every working chunk.
7. **Any update to this file comes as a downloadable file**, never as text pasted
   into chat for me to copy by hand.

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

**13 clips, not one file.** The camera stops recording after ~3 minutes and needs a
manual restart, so the 24-Aug session is 13 separate files. Each one gets its own
CFR conversion, its own undistort and its own tracking run. **Frame numbers restart
at zero in every clip** — which is exactly why `shoot_log.csv` carries a `clip#`
column on every row.

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
- **Trips 1–12 = tuning set.** Thresholds are chosen here.
- **Trips 13–21 = held-out evaluation set.** Opened once, on Day 15, and never
  tuned against. Whatever it says is what goes in the README.

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

> **ORDER IS NOT OPTIONAL TODAY. Shoot prep before velocity.**
> Shoot prep has now slipped twice — planned on Day 4, scheduled for Day 7, done
> on neither. It is the only work here that **cannot be caught up later**: the
> shoot is Saturday, and the signs are what make the hesitation real rather than
> acted. Velocity can be built any day between now and Day 12. The signs cannot.
> Velocity is the more interesting problem. That is exactly why it keeps eating
> the boring one. **Do not open a Python file until Part 1 is fully ticked.**

---

### PART 1 — SHOOT PREP (do this first, no exceptions)
- [ ] Make the wall sign — A4, thick black marker, eye height:
      `GATES A-C →` / `BAGGAGE CLAIM ←` / `EXIT ↑`
- [ ] Make the 5 destination cards (A5): `GATES A-C`, `BAGGAGE CLAIM`,
      `TOILETS`, `EXIT`, `LOUNGE`
      *`TOILETS` and `LOUNGE` are deliberately NOT on the wall sign — that is the
      missing-destination failure mode, and it is what defeats the learning effect.*
- [ ] Confirm the 2-hour slot with mum **in writing**
- [ ] Clear the floor: shoes, slippers, rug, trolley, shoe rack, **robot vacuum**
- [ ] Confirm the wooden door is open, exactly as it was for the homography
- [ ] Charge everything, check storage, test-record 30 s and play it back
- [ ] **Do not touch the camera.** camC carries the homography.

### PART 2 — THE ANSWER KEY (20 seconds, before any code)
- [ ] Walk the corridor once at normal pace. **Count tiles crossed. Count seconds.**
- [ ] Work it out by hand: `tiles × 30.8 cm ÷ 100 ÷ seconds` = m/s
- [ ] Write that number down.

*Why: the system is about to print a speed. `1.2`, `120` and `0.012` all look like
numbers. Without my own measurement I cannot tell which is real, and the failure
mode here is a silent factor of 100. Rule 18.*

### PART 3 — VELOCITY
- [ ] Apply `homography_camC.npz` to every stored footpoint → centimetres
- [ ] **Convert cm → m in ONE explicit, obvious, commented place**
- [ ] Compute speed over time per track
- [ ] Compute heading (direction of travel) per track
- [ ] Smooth the trajectories; check it kills the Day 3 crossing spikes
- [ ] **Compare the output against the answer key before moving on**

### PART 4 — U-TURN v1 (only if Parts 1–3 are done)
- [ ] Angle between "before" and "after" movement vectors
- [ ] Require a minimum travel distance either side, so jitter can't fake a reversal
- [ ] Thresholds are placeholders — real tuning is Day 12, after labels exist

**If the day runs out:** Part 4 slides to Day 10. Parts 1 and 2 do not slide.

**Status:** PARTIAL
**Notes:** Shoot prep done — wall sign and 5 destination cards made. Velocity and
the cm→m conversion done. `smooth()` moving-average (window=5) written for
`speeds.py`; unsmoothed vs smoothed still to be printed side by side. Part 4
(U-turn v1) did not happen — slides. The shoot itself slipped from Sat 22 to
Mon 24, which is where the two lost days went.
**Quiz score:  2  /3** — three concepts owed and re-taught at the start of Day 9:
tiny position errors ÷ tiny time gaps, saving a file mid-run does nothing, and
÷100 living in exactly one place.

## Day 9 — planned Sat 22 Aug, ACTUALLY SHOT Mon 24 Aug — ★ THE SHOOT ★
**Highest-risk day in the project. Everything downstream eats this footage.**

- [x] Consent on camera first — each person says their name and that they agree
- [x] 24 clean trips recorded (target was 21)
- [x] **5 full seconds between people. Never two in frame at once.**
- [x] Log each trip as it happens: trip number, destination card, clean or wasted
- [x] **DID NOT TOUCH THE CAMERA** — camC intact, homography survives
- [ ] ~~One continuous recording~~ — **not possible.** The camera stops recording
      after ~3 minutes and must be restarted by hand. Session came out as
      **13 separate clips**. Handled by taking control of the cuts: stop after
      ~4 trips, restart, never let a trip straddle a cut.

**Same day, before bed — verify it, don't assume it:**
- [x] `check_video.py` on all 13 raw clips — resolution, real frame count, duration
- [x] **Backed up to `OneDrive/waytrace_raw_backup/2026-08-24_shoot/`**, all 13
      files, sizes byte-matched against the originals
- [ ] `ffmpeg -r 15 -an` CFR conversion, then `check_video.py` again → Day 10
- [ ] Undistort one frame and eyeball it → Day 10
- [ ] Run the existing tracker over 500 frames and watch the preview → Day 10

### What was recorded

**24 clean trips across 13 clips.** Log: `data/shoot_log.csv` (+ `.xlsx`).

| Category | Card shown | Why it is hard | Count |
|---|---|---|---|
| `MISSING` | `TOILETS`, `LOUNGE` | Not on the wall sign at all. Nothing to read. | 9 |
| `AMBIG` | `EXIT`, `BAGGAGE CLAIM` | Both on the sign, both share one arrow. Answer given, answer useless. | 8 |
| `EASY` | `GATES A-C` | On the sign, own arrow, no ambiguity. **The control group.** | 7 |

**Why the 7 EASY trips exist.** Precision asks: *of everything the detector
flagged, how much was real?* That question is unanswerable unless the footage
contains walks that **should not** be flagged. All-hard footage lets a detector
flag everything, score 100%, and be worthless. Rule 13.

### How real hesitation was produced without acting
The cast lives in the house and already knows where every room is. Two mechanical
rules made the pauses genuine rather than performed:
- **Card face down**, flipped only after crossing a line ~1 m into the corridor —
  so the destination is unknown until they are already walking.
- **"Go where the *sign* sends you, not where you know it is."**

**Stated limitation for the README:** the cast are not naive to the building. This
is a wayfinding-behaviour rig, not a naturalistic study.

### Rules used on the day
- Trip ends when the walker **exits frame**. The walk back is not part of the trip.
- Reset walks are made with **one hand raised** — instantly identifiable when
  scrubbing on labelling day, and never mistaken for a real U-turn.
- Robot vacuum left in the far corner: unreachable behind a table, and **never once
  detected as a person in prior runs**. Measured, not assumed (Rule 11). Logged at
  the top of the sheet so future-me does not lose an hour to a white blob.

### Verification results — all 13 clips
Every clip: **frames claimed = frames actually read.** No truncation, no
corruption, nothing died mid-recording. **No reshoot needed.**

WhatsApp transfer did **not** degrade the footage — 1024×576 survived intact.

**★ OPEN QUESTION — five clips are 1280×720, not 1024×576 ★**

| Resolution | Clips | Clean trips affected |
|---|---|---|
| 1024×576 (correct) | 1, 3, 4, 7, 8, 10, 12, 13 | 19 |
| **1280×720 (wrong)** | **2, 5, 6, 9, 11** | **6, 8, 9, 14, 17** |

Calibration and homography were both built at 1024×576. Pixel coordinates from a
1280×720 frame mean different real-world positions — every speed from those clips
would be silently, plausibly wrong.

Both are 16:9, so it may be a pure rescale and fully recoverable. **Test, do not
assume:** pull frame 200 from one clip of each resolution, scale the 1280 one down
to 1024×576, and compare the door edge and tile lines.
- Same place → pure scale → resize and keep all 24 trips.
- Different → different field of view → those 5 clips are dead, and the dataset
  drops to **19 trips (6 MISSING / 7 AMBIG / 6 EASY)**. Thinner, but still valid.

**Status:** DONE — shoot complete, verified, backed up, committed
**Notes:** Highest-risk day in the project and it landed. Finished at ~04:30, which
is why the quiz was postponed rather than taken saturated (Rule 7).
**Quiz score:  POSTPONED to Day 10  /3**

---

# ★ RE-PLAN — Mon 25 Aug — two days behind, new target 1 Sep ★

The shoot slipped from Sat 22 to Mon 24. **Two days lost.** The original plan is
no longer a calendar, it is a list of work. Below is the real one.

**New target: SUBMIT Mon 1 Sep.** The Devpost deadline is still Sat 5 Sep, 22:00
Lisbon. Finishing on 1 Sep turns 2–4 Sep into real buffer instead of panic. This
is deliberate: **the buffer has already been spent once (Days 5–6). This rebuilds it.**

## Hours needed per day

Honest estimate of the work left, in hours:

| Work left | Hours |
|---|---|
| Resolution question + CFR convert 13 clips + undistort | 3 |
| Track all 13 clips, watch every output | 3 |
| Finish smoothing (unsmoothed vs smoothed side by side) | 2 |
| Hesitation detector v1 | 3 |
| U-turn detector v1 | 3 |
| Labelling, blind, 24 trips | 5 |
| Tuning on the tuning set only | 4 |
| Event log + hotspot clustering | 5 |
| Metrics on the held-out set | 2 |
| Streamlit dashboard — **never written a line of it** | 8 |
| README, limitations, responsible-AI section | 3 |
| Demo video — script, record, edit, export | 6 |
| Things breaking (they will) | 8 |
| **TOTAL** | **≈ 55 h** |

**8 days from Tue 25 Aug to Mon 1 Sep. 55 ÷ 8 ≈ 7 hours a day, every day, no days off.**

If only 4–5 hours a day are realistic, that is fine — but then something must be
cut **now, in writing**, not discovered on 31 Aug:
- **Cut first: signage OCR (Day 18).** Already the first cut. Do it now.
- **Cut second: OpenVINO.** Keep plain live webcam mode — it is the entire
  "this is a sensor, not software" story for a hardware hackathon.
- **Never cut: metrics.** Precision and recall are the spine. A project with two
  detectors and honest numbers beats a project with five features and no evidence.

## The new day map

| Date | Day | Work |
|---|---|---|
| Tue 25 Aug | 10 | Resolution question → CFR convert all 13 → undistort → track all 13 |
| Wed 26 Aug | 11 | Finish smoothing → hesitation detector v1 → U-turn v1 |
| Thu 27 Aug | 12 | ★ LABELLING, BLIND — write definitions and the split rule first ★ |
| Fri 28 Aug | 13 | Tune both detectors **on the tuning set only** + event log |
| Sat 29 Aug | 14 | Hotspot engine + heatmap |
| Sun 30 Aug | 15 | ★ VALIDATION METRICS on the held-out set ★ |
| Mon 31 Aug | 16 | Streamlit dashboard, both halves |
| Mon 1 Sep | 17 | README + demo video + **SUBMIT** |
| 2–4 Sep | — | Buffer. Live webcam mode only if everything else is done. |

**Two risks that will actually bite, named in advance:**
1. **The demo video.** Async judging means the video *is* the score, and it sits
   on the last day when I am most tired. Storyboard it on 30 Aug, not on 1 Sep.
2. **Labelling is boring and it comes before the fun part.** Rule 19 says the
   interesting task eats the boring one. It goes first in the day, not last.

---

## Day 10 — Tue 25 Aug — Footage into the pipeline  *(was Sun 23)*

**Do this before any detector work. Every downstream number depends on it.**

### PART 1 — Settle the resolution question (10 minutes, blocking)
- [ ] Pull frame 200 from clip1 (1024×576) and clip2 (1280×720)
- [ ] Scale the 1280 frame down to 1024×576
- [ ] Compare door edge and tile lines. Same → rescale and keep 24 trips.
      Different → drop clips 2, 5, 6, 9, 11 and run with 19 trips.
- [ ] **Write the answer in this file either way.**

### PART 2 — Convert and undistort
- [ ] `ffmpeg -r 15 -an` on all 13 clips → `data/interim/..._cfr.mp4`
- [ ] `check_video.py` on every converted clip — confirm a true 15.0 fps
- [ ] Undistort every clip with `calibration_ezviz.npz` (k1 = −0.41)
- [ ] Eyeball one undistorted frame before trusting all 13

### PART 3 — Track
- [ ] Run the tracker over all 13 undistorted clips
- [ ] **Watch every output.** Looking for: mid-walk ID switches, footpoints that
      leave the feet, trail spikes, and any fake track in the vacuum corner
- [ ] `MIN_TRACK_LENGTH = int(fps * 1.0)` — never a hardcoded number (Rule 17)

**Status:**
**Notes:**
**Quiz score:      /3** — includes the three postponed from Day 9

---

## OLD Day 10 — Hesitation detector v1  *(now Day 11, Wed 26 Aug)*
- [ ] **Absolute speed threshold** — speed below X m/s sustained for Y seconds.
      NOT a per-person baseline: 2.7 m of approach is too short to establish one.
      See Day 4. This limitation is stated plainly in the README.
- [ ] **CHECK THE UNITS.** Homography is centimetres. Thresholds are m/s.
- [ ] Ignore people who are simply stationary for their whole track
- [ ] Sanity-check X against a normal walking pace measured from the real footage
- [ ] Thresholds are placeholders — tuning is Day 12

**Status:**
**Notes:**
**Quiz score:      /3**

## OLD Day 11 — ★ GROUND TRUTH LABELLING (BLIND) ★  *(now Day 12, Thu 27 Aug)*
**Do this before looking at any detector output.**

- [ ] **Write the definitions FIRST, before watching anything.** What exactly counts
      as a hesitation? A U-turn? How many seconds? How many degrees? Day 2 proved
      that me and the filter were counting different things.
- [ ] Watch every clip and log every real event by timestamp + clip number
- [ ] Hand-raised walks are **reset walks, not trips.** Never labelled.
- [ ] Do not open the detector output today. Not once.

### ★ THE SPLIT RULE — written 24 Aug, BEFORE any labelling or tuning ★

**Chronological splitting is banned.** Trips 20–24 are all `EASY` and were all shot
last, so trips 1–12 / 13–24 would give a tuning set with almost no easy walks and a
held-out set with almost nothing else. Both halves would be broken, in opposite
directions.

**The rule instead:**

> Number the trips **within each category** (`MISSING`, `AMBIG`, `EASY`).
> **Odd → tuning set. Even → held-out set.**

That gives roughly **12 tuning / 12 held out**, and both halves contain all three
categories.

**This rule is fixed. It was written down before any labels existed and before any
detector output was seen.** Changing a split after seeing results is how metrics
become fiction — and the whole point of this project is that its numbers are real.

**Status:**
**Notes:**
**Quiz score:      /3**

## Day 12 — Tue 25 Aug — Tune both detectors **on the tuning set only**
- [ ] Tune U-turn thresholds against trips 1–12
- [ ] Tune hesitation thresholds against trips 1–12
- [ ] Kill false positives from tracker jitter
- [ ] **One variable at a time.** Every trustworthy number in this file came from that.
- [ ] **Do not open the held-out (even-numbered) trips.** Touching them turns the
      metrics into fiction.

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

- [ ] Open the held-out (even-numbered) trips for the first time
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
| Velocity | How fast **and** in which direction. Speed on its own is just the how-fast part. Comes from footpoints in centimetres, divided by the time gap — and the time gap is tiny, which is why small errors explode (Rule 21). |
| Heading | |
| Angle between vectors | |
| Smoothing | Replacing each point with the average of it and its neighbours (window = 5), so tracker jitter stops looking like real movement. Kills wobbles under ~20 cm. **Must not flatten real movement** — the test is that the genuine 1.6 m y-swing on ID 1 survives. |
| Homography | The recipe that turns a pixel into a spot on the floor. Built by clicking 4 points whose real-world distances I already know. Belongs to **one camera in one position** — scrap it on any remount. Mine covers 154 x 58.8 cm and is accurate to **0.6 cm along the walking axis**. |
| Extrapolation | Asking the model about ground **outside** the region it was taught. It answers just as confidently either way. My across-axis error tripled (0.6 → 2.0 cm) the moment I tested outside the 2-tile-wide strip. |
| Undistortion crop (`alpha`) | `cv2.undistort` straightens the picture by pulling edge pixels inward, so the frame narrows. `getOptimalNewCameraMatrix(alpha=1)` zooms back out to keep everything. **Chose the default crop** — the recovered pixels are the extreme edges, where the distortion model is least trustworthy, and changing it would invalidate the homography. |
| Hesitation event | |
| U-turn event | |
| Backtracking | |
| Clustering / DBSCAN | |
| OCR | |
| Precision | Of everything the detector flagged, how much was actually real. Needs footage that should *not* be flagged, or it cannot be measured — which is why the 7 `EASY` trips exist. |
| Recall | Of everything that actually happened, how much the detector found. Needs hand-made ground-truth labels, which is what labelling day produces. |
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
20. **Ctrl+S, then run. Never save during a run.** Python reads the file **once**,
    at launch, and works from its own copy. Editing after that is editing a recipe
    for a meal already cooking.
21. **A short time gap magnifies a small position error into a huge speed.**
    Distance ÷ 0.067 s. A 25 cm foot wobble becomes 3.7 m/s. Small mistake, tiny
    divider, enormous lie.
22. **Averages hide events.** A trip that stops dead for two seconds and then
    hurries can average out to a perfectly normal walking speed. The average is the
    thing that erases exactly what WayTrace is looking for.
23. **Never split data after seeing results.** The split rule goes in this file in
    writing, before labelling. A split chosen after the fact isn't a measurement,
    it's a decoration.
24. **A dataset made only of hard cases cannot catch a detector lying.** The 7
    `EASY` trips exist so that flagging everything scores badly instead of perfectly.
25. **Excel's default filename will end up in the repo if you let it.** `Book 3.csv`
    was committed and pushed before anyone noticed. Name the file at Save As time,
    and read what `git status` actually lists before typing `git add .`.
26. **Verify the copy, not the copy command.** A backup is backed up when the file
    count and byte sizes match at the destination — and, in the cloud, when the sync
    icon is a green tick and not a blue arrow.
