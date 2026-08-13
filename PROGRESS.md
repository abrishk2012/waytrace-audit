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
- [ ] YOLO + ByteTrack running over the whole video
- [ ] Each person keeps the same ID number across frames
- [ ] Count how often IDs wrongly switch

**Status:**
**Notes:**
**Quiz score:      /5**

## Day 3 — Sat 15 Aug — Trajectories
- [ ] Store position history per track ID (footpoint, not box centre)
- [ ] Draw coloured trails behind each person
- [ ] Save an annotated output video to `data/output/`

**Status:**
**Notes:**
**Quiz score:      /5**

## Day 4 — Sun 16 Aug — FOOTAGE DECISION DAY ⚠️
This is the day that decides how strong the final project is.
- [ ] Decide the final judge-facing footage (staged recording vs public dataset)
- [ ] If staging: plan the corridor, the sign, the walkers
- [ ] If dataset: confirm the licence in writing

**DECIDED ON DAY 1 — staging my own footage.** Carry these constraints in:
- Cast: me, mum, sister (10). Only 3 people.
- **Not a problem: 3 people x 6–8 trips each = 20+ anonymous journeys.**
  The tracker has no memory — each re-entry is a brand-new ID. Real airport
  cameras aggregate over time too, not all at once.
- **Learning effect is the real risk.** By trip 3 they know the route and stop
  hesitating. Fix: 4–5 different paper destinations (`GATES A–C`, `BAGGAGE CLAIM`,
  `TOILETS`, `EXIT`, `LOUNGE`), a different one called out each trip. Vary the
  start direction too. Residual effect goes in the limitations section, stated plainly.
- **Record at 1080p.** Day 1 proved 360x288 is near YOLO's limit. More pixels per
  person = better detection, costs nothing.
- Phone must not move at all. Books/shelf/tripod.
- Everyone on camera consents first. Raw video deleted after processing; only
  anonymous trajectories kept.
- **Book the 2-hour slot with mum now**, not on Day 4.
- Day 1 showed occlusion breaks detection → position the camera so walkers don't
  line up behind each other.

**Status:**
**Notes:**
**Quiz score:      /5**

## Day 5 — Mon 17 Aug — Homography (pixels → metres)
- [ ] Click 4 floor points, supply their real-world distances
- [ ] `cv2.findHomography` maps image coords to floor coords
- [ ] Speeds now reported in m/s instead of pixels/frame

**Status:**
**Notes:**
**Quiz score:      /5**

## Day 6 — Tue 18 Aug — Smoothing + velocity
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
- [ ] Low speed sustained for a minimum duration
- [ ] Compare against that person's own normal walking speed
- [ ] Ignore people who are simply stationary the whole time

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

**Status:**
**Notes:**
**Quiz score:      /5**

## Day 19 — Mon 31 Aug — Ground truth labelling
- [ ] Watch the evaluation clip and log every real event by timestamp
- [ ] Do this BEFORE looking at what the system found

**Status:**
**Notes:**
**Quiz score:      /5**

## Day 20 — Tue 1 Sep — Validation metrics
- [ ] Compute precision, recall, F1 per behaviour
- [ ] Write an honest limitations section
- [ ] Learn to explain these numbers out loud

**Status:**
**Notes:**
**Quiz score:      /5**

## Day 21 — Wed 2 Sep — Polish + GitHub + README
- [ ] `.gitignore` (no `.venv`, no big videos, no model weights)
- [ ] README with pitch, architecture, definitions, privacy, metrics, limitations
- [ ] Architecture diagram

**Status:**
**Notes:**
**Quiz score:      /5**

## Day 22 — Thu 3 Sep — Demo video
- [ ] Storyboard the first 10 seconds FIRST
- [ ] Record real system output only — zero fake numbers
- [ ] Edit, export, upload

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
| Tracking / track ID | |
| Trajectory | |
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
| Confidence threshold | The model scores every guess 0–1; anything below the cutoff is binned. Too high → real people missed. Too low → shadows and legs become "people", which become fake trajectories, fake events, and a poisoned hotspot. Currently 0.25. |
| Occlusion | One person blocking another from the camera. Detection merges them into one box; the tracker will swap their IDs. Seen on Day 1 in the 0.89 box. |

Fill these in yourself as you learn them. If a box is empty on Day 20, that's a problem.

---

## Things I am NOT allowed to say

- ❌ "WayTrace detects confused passengers"
- ❌ "This sign caused the confusion"
- ❌ Any statistic I did not measure
- ❌ "It's basically YOLO" (it isn't — YOLO is the input layer)
