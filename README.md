# WayTrace

**Privacy-preserving edge computer vision for wayfinding audits.**

WayTrace analyses anonymous pedestrian trajectories from fixed CCTV footage to
locate *wayfinding friction* — the places where people hesitate, backtrack, or
turn around. It reports **where** friction happens. It does not attempt to say
**why**, and it never identifies anyone.

> Status: in development. Built for VoltHacks 2026.
> This README documents the system as currently built and measured, including
> the parts that do not work yet.

---

## What it is

An **edge sensor system**, not a SaaS product. Video is processed locally on the
device attached to the camera. No footage leaves the premises; no faces, no
identities, and no re-identification across cameras. What comes out is a set of
anonymous `(x, y, time)` paths in real-world metres, and hotspots derived from them.

The unit of output is a **location on a floor plan**, not a person.

## What it deliberately does not do

- **It does not diagnose signage.** WayTrace reports that people hesitate at a
  given spot. A human decides why. Where OCR of nearby signs is available, the
  language used is *"possible signage issue associated with this hotspot"* — an
  association, never a cause.
- **It does not identify or re-identify people.** Track IDs are per-video and
  meaningless across recordings.
- **It does not store video.** Trajectories are the artefact; footage is input.

---

## Pipeline

```
CFR convert  →  undistort  →  detect (YOLO)  →  track (ByteTrack)
     →  homography  →  trajectory storage  →  smooth
     →  behavioural event detection  →  hotspot clustering  →  dashboard
```

Order matters and is fixed. Undistortion happens on the whole video before
detection, so every downstream pixel coordinate refers to the same corrected
frame. Homography is applied after tracking, so the tracker works in the space it
was trained for.

**Every video is converted to constant frame rate first** (`ffmpeg -r 15 -an`).
The source camera records at variable frame rate; every timing figure in the
system depends on this conversion having happened.

---

## Current state

| Stage | Status |
|-------|--------|
| CFR conversion | working |
| Lens undistortion | working, verified |
| Detection + tracking | working, ~83% frame coverage |
| Homography (pixels → metres) | working, verified to 3 cm |
| Trajectory storage | working |
| Smoothing | working, tuned |
| Hesitation detection | not built |
| U-turn detection | not built |
| Hotspot clustering | not built |
| Dashboard | not built |
| Signage OCR | not built, first to be cut |

### Verification so far

Homography was checked against a hand-measured walk. The system reported
**2.44 m**; the tape measure said **2.46 m**. That 3 cm agreement is the main
evidence that the pixel-to-metre conversion is correct and that no unit error
(the classic factor-of-100) is present.

Smoothing is a 5-frame moving average (one third of a second at 15 fps), applied
after conversion to metres. It was chosen over larger windows deliberately:
larger windows produce lower peak speeds but blur the *start and end* of events
in time, and the planned hesitation detector is time-bounded.

---

## Limitations

These are measured, not estimated. Each one is a real constraint on how the
current results should be read.

### 1. Accuracy varies across the floor — by a factor of four

The homography does not have a single error. It has an **error field**: the
number of centimetres covered by one pixel changes with distance from the camera.

Measured across the frame, along the walking axis:

| Image row | Distance from camera | 1 pixel covers |
|-----------|---------------------|----------------|
| y = 550 (bottom) | nearest | **0.41 cm** |
| y = 450 | | 0.52 cm |
| y = 350 | | 0.70 cm |
| y = 250 | | 0.98 cm |
| y = 150 (top) | furthest | **1.47–1.68 cm** |

**A 4.2× spread.** The same detector jitter — say a 15-pixel wobble in the
footpoint — is 6 cm near the camera and 25 cm at the far end.

The stretch is driven almost entirely by image *row*, not column: at a fixed row,
the three sampled columns differ by under 10%. This is ordinary perspective for a
camera looking along a corridor.

**Consequence:** position error, and therefore speed error, is roughly four times
larger in the far third of the frame. Events detected there carry proportionally
less confidence than events near the camera. A single RMS figure for the whole
scene would hide this entirely.

### 2. Walking happens on the less-accurate axis

Calibration residuals differ by axis: approximately **0.6 cm** along one and
**2.0 cm** across the other. All measured walks are dominated by movement along
the **~2 cm axis**, by a factor of 2.5–4.5x, including a walk in the opposite
direction.

Over a typical 2.4 m walk this is under 1% of the distance travelled and does not
materially affect reported speeds — but it is the weaker of the two calibrated
axes, and it should not be described as the well-calibrated one.

### 3. Speed alone cannot separate standing from walking

During a **confirmed ten-second standstill**, the system reported a peak of
**0.49 m/s** unsmoothed and **0.38 m/s** smoothed. Measured walking speed is
**0.64 m/s**.

Standing peaks at 59–77% of walking speed. The two populations overlap, so no
single speed threshold can separate them: set it low and one real stop fragments
into several short false ones; set it high and slow walking is called hesitation.

**This is why hesitation is defined as "below X m/s *sustained for Y seconds*"**
rather than as a bare threshold. Duration does the separating, not the threshold
value.

### 4. Averages over a whole track are meaningless

One measured track covered 2.44 m in 21.9 s — an average of 0.11 m/s. That figure
describes neither the walking (0.6 m/s) nor the ten-second stop it contains. All
event detection therefore operates on per-frame speeds within time windows, never
on track averages.

### 5. Residual speed spikes are unexplained noise, not movement

Peak reported speeds of 2–3.7 m/s appear in a short corridor where nobody ran.
Five candidate explanations were tested:

| Hypothesis | Result |
|-----------|--------|
| Track-edge artefacts, removable by time-trimming | **Rejected** — worked on one track, did nothing for the other two, and no common trim value exists |
| Detection box aspect ratio anomaly | **Rejected** — spikes occur above, below and at the median aspect |
| Sudden detection box size change | **Rejected** — frame-to-frame area ratios at spikes are all 0.82–1.12x |
| Missing frames inflating the divisor | **Rejected** — all spike frames are adjacent (gap = 1) |
| Position on the floor | **Supported** — the three largest spikes, across two different tracks, occur at world y = +1.49 to +1.53 |

The supported explanation is limitation 1: the far region magnifies ordinary
detector jitter. Smoothing reduces peak speed from 3.70 to 1.40 m/s but does not
eliminate it, and **1.40 m/s should not be quoted as a walking speed** — it is a
less-wrong maximum, not a believable one.

No position-weighted correction is applied yet. Doing so requires labelled data
to validate against.

### 6. Hesitation uses an absolute speed threshold, not a per-person baseline

The test corridor is too short to establish each person's normal walking speed
before they reach the decision point. A longer approach would allow per-person
normalisation; this one does not.

### 7. Validation footage is from a small, non-naive cast

Test recordings use a small number of people walking the same corridor
repeatedly. Familiarity increases through a session: by the later trips, subjects
know the route and stop hesitating because they have **learned it**, not because
the signage improved.

Hesitation rates from later trips are therefore a **floor, not a true rate**.
Early trips carry the most weight.

### 8. Homography is bound to camera position

Lens distortion coefficients survive remounting; the homography does not. Any
movement of the camera — however small — invalidates the pixel-to-metre mapping
and requires rebuilding it from new reference points.

---

## Repository

```
src/trajectories.py   detection, tracking, trajectory export
src/speeds.py         homography application, speed, smoothing, diagnostics
data/output/          generated trajectories and annotated video
PROGRESS.md           day-by-day build log, including failed approaches
```

`PROGRESS.md` records what was tried and rejected, not only what worked. Several
entries are corrections of earlier conclusions.

---

## Notes on method

Two practices are used throughout and are worth stating:

**Every parameter is swept, never guessed.** Smoothing window and edge-trim
duration were both chosen by testing a range and looking for a plateau — a value
that stops changing the result — rather than by picking whichever number made an
unwanted figure disappear. Where no plateau exists, the parameter is treated as
the wrong tool rather than tuned harder.

**Every sweep includes a null row.** `window = 1` and `trim = 0.0` must reproduce
the unprocessed numbers exactly. If they do not, the function is broken and every
other row is meaningless.
