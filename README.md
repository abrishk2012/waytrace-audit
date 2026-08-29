# WayTrace

**Privacy-preserving edge computer vision for wayfinding audits.**

WayTrace analyses anonymous pedestrian trajectories from fixed CCTV footage to
locate *wayfinding friction* — the places where people hesitate, backtrack, or
turn around. It reports **where** friction happens. It does not attempt to say
**why**, and it never identifies anyone.

> Status: built and validated. Made for VoltHacks 2026.
> This README documents the system as measured, including the parts that do not
> work. The U-turn detector scored **zero** on held-out data; that number is in
> the status table and in Validation, not buried.

---

## What it is

An **edge sensor system**, not a SaaS product. Video is processed locally on the
device attached to the camera. No footage leaves the premises; no faces, no
identities, and no re-identification across cameras. What comes out is a set of
anonymous `(x, y, time)` paths in real-world metres, and hotspots derived from them.

The unit of output is a **location on a floor plan**, not a person.

## Why this matters — SDG 11

**UN Sustainable Development Goal 11.2** asks for *"access to safe, affordable,
accessible and sustainable transport systems for all, with special attention to the
needs of those in vulnerable situations — women, children, persons with disabilities
and older persons."*

Wayfinding is part of accessibility. A station or terminal can be step-free,
ramped and compliant, and still be unusable if a person cannot work out which way
to go. Getting lost is not distributed evenly. It falls hardest on:

- **older people**, who are navigating under time pressure with less confidence in
  backtracking,
- **disabled people**, for whom a wrong turn is not a minor cost but a long
  detour, a missed connection, or physical pain,
- **non-native speakers and non-readers**, who cannot fall back on text when the
  symbols are ambiguous,
- **first-time and infrequent travellers**, who have no memory of the building to
  fall back on.

Everyone else absorbs bad signage invisibly. These groups pay for it.

**The measurement problem this addresses.** Signage is normally audited by asking
people, or by an expert walking the space and giving an opinion. Both are
after-the-fact and both are subjective. Neither tells an operator *which* sign, at
*which* junction, is failing. WayTrace measures the behaviour instead: it reports
that people slowed, stopped or turned around at a specific point on a floor plan,
in metres, from footage the building already records.

That turns an opinion into a location an operator can act on — and it does it
without identifying anybody, which is what makes it deployable in a public space
at all.

**Scope, stated honestly.** This is validated on 25 walks through one corridor
junction. It is evidence that the measurement works, not evidence about airports.
The claim is about the method, not the scale.

## What it deliberately does not do

- **It does not diagnose signage.** WayTrace reports that people hesitate at a
  given spot. A human decides why. The wording used is *"possible signage issue
  associated with this hotspot"* — an association, never a cause.
- **It does not read signs.** OCR was cut on Day 12, deliberately, to protect
  the validation work. The signage audit is hardcoded for this one junction from
  `data/signs.json`. Automating it is the obvious next step, not a hidden one.
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
| Hesitation detection | working, held-out F1 77% |
| U-turn detection | working, held-out F1 0% — see Validation |
| Hotspot clustering | working, 4 hotspots, stable 0.40–0.75 m |
| Dashboard | working, local Streamlit |
| Signage OCR | cut on Day 12, deliberately |

### Verification so far

Homography was checked against a hand-measured walk. The system reported
**2.44 m**; the tape measure said **2.46 m**. That 3 cm agreement is the main
evidence that the pixel-to-metre conversion is correct and that no unit error
(the classic factor-of-100) is present.

Smoothing is a 5-frame moving average (one third of a second at 15 fps), applied
after conversion to metres. It was chosen over larger windows deliberately:
larger windows produce lower peak speeds but blur the *start and end* of events
in time, and the hesitation detector is time-bounded.

### Held-out validation

Trips were split odd/even **before any detector code was written**. Odd trips
were used for tuning; even trips were never looked at until scoring. `validate.py`
was committed before it was run. The test was run once and the result kept.

|            | Odd (tuning, 13) | **Even (held-out, 12)** | All (25) |
|------------|------------------|-------------------------|----------|
| Hesitation | P 100% R 86% F1 92% | P 83% R 71% F1 77% | P 92% R 79% F1 85% |
| U-turn     | P 71% R 71% F1 71% | **P 0% R 0% F1 0%** | P 56% R 56% F1 56% |
| Combined   | P 85% R 79% F1 81% | **P 62% R 56% F1 59%** | P 76% R 70% F1 73% |

Source: `data/validation_day15.txt` and `data/per_behaviour_day15.txt`.

**Read the U-turn row, not the combined row.** The combined 62/56 hides a
detector that scored zero. Only 2 U-turns fell in the held-out set and both were
missed for the same reason: the speed gate ignores turns made from a standstill.
Two events is far too small a sample to call the detector broken — and far too
small to call it working.

**25 trips is a small dataset.** One event moves a percentage by roughly ten
points, so these are not performance figures. What was controllable was honesty:
split before coding, scoring script committed before it ran, one scoring run,
worse number kept.

**Not every threshold was written blind, and it would be easy to imply that it
was.** Three of the five — `MAX_SPEED`, `MIN_SECONDS`, `MIN_ANGLE` — were written
into `docs/definitions.md` before the detector existed, then swept and found
unimprovable. The other two, `MAX_GAP` and `MIN_SPEED`, were **tuned on Day 13
against the odd trips** and have no blind ancestor. Tuning happened on the tuning
half only, but they are tuned values and are labelled as such.

`data/misses_day15.txt` explains all four held-out misses individually, two of
them predicted in writing before scoring.

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

**This is why hesitation is defined as "below 0.30 m/s *sustained for 2.00
seconds*"** — both written into `docs/definitions.md` before the detector
existed, both later swept and found unimprovable — rather than as a bare
threshold. Duration does the separating, not the threshold value.

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

No position-weighted correction is applied. Labelled data now exists — 25 trips
— so the original blocker is gone; the reason it remains unbuilt is time, and
building it after seeing the held-out result would mean tuning against the test
set. It stays out.

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

## Responsible AI

**What is collected.** Video of one corridor junction, from one fixed camera, in a
private building. Thirteen clips, twelve usable. Three participants, all of whom
consented to public release of the footage.

**What is discarded — and this is structural, not a promise.** The analysis never
opens a video. The detector and the clustering read a file of numbered tracks:
positions in metres, frame numbers, box sizes. Every clip could be deleted and every
number in this repository would still reproduce. Video is an input to tracking, not
to analysis.

**Where it runs.** A local Streamlit server on the machine holding the footage. No
`requests`, no `urllib`, no HTTP call anywhere in the codebase. Nothing leaves the
machine.

**Faces.** All three participants consented to public release. I built face blurring
from the saved track boxes anyway and verified zero uncovered frames — every frame
inside any track's lifetime has a rectangle over the head slice. I do not apply it to
the demo footage, because consent exists here. The tool is in the repo because a real
deployment wouldn't have consent from anyone walking through an airport.
See `src/blur_heads.py`.

**Where the system is biased, stated plainly.** Detection is YOLO, and YOLO's
performance varies with body size, clothing and lighting. A wheelchair user's
silhouette is not what it was trained on. Neither is a person pushing a luggage
trolley, or a child. The behaviour detectors sit on top of detection, so anyone the
detector sees less reliably is also measured less reliably — and those are
disproportionately the people the system exists to help. I have not measured this,
because my cast was three adults. I am stating it rather than implying it isn't there.

**What this system must never be.** It counts behaviours at a location. It does not
identify anyone, and it should not be extended to. The output that matters is
"four people hesitated near this sign", not "this person hesitated".

---

## Repository

```
src/                  33 scripts. The pipeline proper:
  undistort_video.py    lens correction
  track_people.py       YOLO + ByteTrack
  build_homography.py   pixels -> metres
  speeds.py             speed, smoothing, diagnostics
  build_events.py       hesitation + U-turn detection
  hotspots.py           spatial clustering
  validate.py           held-out scoring (committed before first run)
  analyse_one.py        single-video path used by the dashboard
                      The rest are calibration helpers, one-off
                      diagnostics and sweep tools, kept because
                      PROGRESS.md refers to them.

dashboard/app.py      local Streamlit server
dashboard/panels.py   result panels, all numbers parsed from files
dashboard/pipeline_ui.py  pipeline stage display

data/output/          trajectories, results.json, hotspots.json
data/*_day15.txt      validation, per-behaviour and miss analysis
docs/definitions.md   thresholds, written before the detector existed
docs/limitations.md   measured constraints
PROGRESS.md           day-by-day build log, including failed approaches
```

`PROGRESS.md` records what was tried and rejected, not only what worked. Several
entries are corrections of earlier conclusions.

---

## Notes on method

Three practices are used throughout and are worth stating:

**Every parameter is swept, never guessed.** Smoothing window and edge-trim
duration were both chosen by testing a range and looking for a plateau — a value
that stops changing the result — rather than by picking whichever number made an
unwanted figure disappear. Where no plateau exists, the parameter is treated as
the wrong tool rather than tuned harder.

**Every sweep includes a null row.** `window = 1` and `trim = 0.0` must reproduce
the unprocessed numbers exactly. If they do not, the function is broken and every
other row is meaningless.

**The tuning half and the test half were separated before any detector code was
written.** Odd trips tuned, even trips held out. Every threshold sweep, every
hotspot cell-size check and every parameter decision on this project was made
against odd trips only. The even trips were scored once, on Day 15.
