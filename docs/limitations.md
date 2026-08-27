# WayTrace — Honest Limitations

Written Day 15, 27 Aug 2026, immediately after the held-out validation run and
before the dashboard was built. Every number here comes from a committed file,
not from memory.

Read this section before believing any headline figure in this project.

---

## 1. The dataset is small. Very small.

25 clean trips, 13 clips, 3 participants, one corridor, one camera, one evening.
23 labelled events in total — 14 on the tuning set, 9 on the held-out set.

At this size a single event moves a percentage by roughly ten points. The
held-out recall figure of 56% rests on 9 labelled events; one more hit would
make it 67%, one fewer would make it 44%. **These numbers demonstrate that the
method runs end to end and can be measured. They do not establish a rate.**

Anyone reporting a percentage from 9 events without saying so is overclaiming.

## 1b. The held-out set is harder — but only mildly

Trip categories, counted from `data/trip.csv`, not from memory:

| category | odd (tuning) | even (held-out) |
|---|---|---|
| MISSING (destination absent from the sign — the hard cases) | 3 | 5 |
| AMBIG | 5 | 3 |
| EASY | 5 | 4 |

The held-out set holds the majority of MISSING trips, so validation was not
performed on the easy cases (Rule 8). But the imbalance is 5 against 3, not the
lopsided split claimed in an earlier session summary, which said "6 of 9". The
real figure is 5 of 8. **Difficulty explains part of the drop from 85% to 62%.
It does not explain all of it, and it should not be offered as though it does.**

## 2. The U-turn detector caught nothing on the held-out set

| | tuning set (odd, 13 trips) | held-out set (even, 12 trips) |
|---|---|---|
| Hesitation | P 100%  R 86%  F1 92% | P 83%  R 71%  F1 77% |
| U-turn | P 71%  R 71%  F1 71% | **P 0%  R 0%  F1 0%** |
| Combined | P 85%  R 79%  F1 81% | P 62%  R 56%  F1 59% |

The combined held-out figure of 62% / 56% **hides this completely.** The split is
the honest presentation; the combined number alone is not.

Two readings, and both are true:

- There were **2 labelled U-turns** on the held-out set. A detector operating at
  the tuning-set rate of 71% would miss both by chance alone roughly 8% of the
  time. At n=2 you cannot distinguish "broken" from "unlucky", and claiming
  either with confidence would be dishonest.
- But both misses share **one known cause** — a U-turn immediately following a
  stop, rejected by the speed gate. This failure was written down on Day 14,
  before the held-out set was scored. So it is not random: it is a specific,
  documented failure mode that happened to be well represented in these trips.

**No threshold was changed after seeing this.** The speed gate is what took
tuning-set precision from 61% to 85%. Removing it now would be tuning against
held-out data, which would destroy the only uncontaminated evidence in the
project.

## 3. Every miss is explained — none is mysterious

Four misses on the held-out set:

| miss | cause |
|---|---|
| clip1 trip 4, 114.0 s, HESITATION | The pause was under 2 seconds. `min_seconds = 2.00`. The definition excluded it. Confirmed by watching the footage. |
| clip8 trip 12, 62.0 s, HESITATION | **One event classified wrong, not two errors.** A U-turn fired at 62.5 s, 0.5 s away. The matcher requires the type to agree, so a single real event cost one miss *and* one false positive. |
| clip11 trip 18, 29.0 s, UTURN | Speed gate — U-turn following a hesitation. Predicted Day 14. |
| clip12 trip 20, 86.0 s, UTURN | Same cause. Predicted Day 14. |

Zero unexplained misses. A predicted failure that appears on unseen data is
better evidence of understanding than an unexplained success.

## 4. The homography extrapolates beyond the tiles it was fitted to

The calibration patch is a 5×2 tile diamond measuring **58.8 cm × 154 cm**
(`homography_camC.npz`, `world_points`). Inside that patch, accuracy along the
walking axis is sub-centimetre.

But results are reported well outside it. A hotspot sits at x = 1.00 m — roughly
1.7× the calibrated width. The right-hand junction opening is at y = 1.79 m,
beyond the 1.54 m patch length. **Projective error grows with distance from the
fitted region, and this project has not measured how much.**

The correct fix is a larger calibration pattern covering the full corridor.
It was not done, and every coordinate outside 0.588 m × 1.54 m should be read as
an estimate with unquantified error.

## 5. What "blind thresholds" does and does not cover

`docs/definitions.md` was committed as `2c7b427` on **Mon 24 Aug at 23:57** —
before any labelling (25 Aug) and before any detector existed (26 Aug). The
timestamp is the evidence, not the prose.

That file defines three parameters, and all three survived Day 13's sweeps
unimprovable:

- `max_speed = 0.30 m/s`
- `min_seconds = 2.00 s`
- `min_angle = 135°`

**Two further parameters have no blind ancestor.** `max_gap = 0.00` and
`min_speed = 0.20` were introduced during Day 13 tuning, on the odd trips only,
to remove false positives. They are tuned parameters and should be described as
such. Saying "all thresholds were written blind" would be false.

## 6. The held-out set was protected, but not unseen

What can be claimed: `build_events.py` processes odd trips only and writes
`results_odd.json`; `--all` was run exactly once, on Day 15, after the scoring
script was already committed. `odd_only.py` is the single source of trip
membership. No threshold was ever selected against an even trip.

What cannot be claimed: that even trips were never seen at all. During Days
12–13, `summarise.py` printed per-trip event counts across every clip, so
detector output for even trips was displayed on screen. **Both facts belong in
any description of the methodology. The second one does not get softened.**

## 7. Event timing is reliable; duration and U-turn timing are not

Event start times land within about 0.3 s of the labelled time. End times
over-run — the detector holds an event open past the point a human would close
it, so **durations should not be quoted.**

Separately, `find_uturns` stamps an event at frame `i` while comparing heading at
`i` against `i + hold` (`speeds.py:136`). The marker therefore lands roughly one
second **before** the visible pivot. This is systematic, is well inside the ±3 s
matching tolerance, and affects no score — but an annotated video will look
slightly early, and that is why.

This offset was found by watching footage on Day 15 and was **not** corrected,
because changing detector behaviour after seeing held-out results is exactly the
thing this project is structured to avoid.

## 8. The setting is a home corridor, not an airport

Filming took place in a domestic entrance hall. The signage was made for the
shoot. The corridor is roughly 2 m of usable width, not a 40 m concourse.

The wayfinding *mechanism* under test — people slow down and turn around near a
decision point when their destination is not signposted — is not specific to
airports. But **no claim is made that these hotspot positions, distances or
rates transfer to a real terminal.** They are a demonstration that the
measurement works, on a corridor small enough for one person to calibrate by
hand.

## 9. One person at a time

Trips were filmed individually, 4 to 5 seconds apart (the gap was intended to be 5 s; some trips came out at 4 s). The tracker has never
been tested with two people in frame simultaneously. Occlusion, identity
switching and crowd behaviour are all unaddressed. In a real terminal these are
the dominant engineering problems, and this system has not met them.

## 10. Hotspot 4 barely qualifies

Hotspots require **2 or more events in a 0.5 m cell**. Hotspots 1 and 2 hold 5
and 4 events and survived the tuning-set → full-set transition, growing rather
than moving. Hotspot 4 holds exactly 2 and clears the threshold by nothing.

Cell size sensitivity: the count is 4 hotspots across cell sizes 0.40–0.75 m,
falling to 3 at both 0.30 m and 1.00 m. Stable across a roughly 2× range, not
across all values. Report hotspots 1 and 2 with confidence; report 3 and 4 as
secondary.

One hotspot also sits below the camera's field of view — real, inside the
calibrated corridor, but the floor there is off the bottom edge of every frame.
It is drawn at the lowest visible row and labelled accordingly.

## 11. What the system does not claim

From `docs/definitions.md`, written before any result existed:

> An event is a **behaviour**, not a mental state. The system detects that
> someone slowed down or turned around. It does not detect confusion.

Accordingly: "hesitation event", never "this person was confused". And
"possible signage issue associated with this hotspot", never "this sign caused
it".

## 12. Participants were not told what was being measured

The three participants were given a destination — "walk to the toilets" — and
nothing about hesitation, U-turns or what the system detects. Their behaviour
was therefore not shaped by knowing the research question.

This is a strength of the protocol, but it is recorded here because it is the
kind of thing that should be stated rather than assumed.

---

## Summary for a judge in one paragraph

WayTrace detects hesitations and U-turns in corridor footage and locates them on
the floor in real-world metres. On a held-out set of 12 trips never used for
tuning, hesitation detection scored 83% precision and 71% recall; U-turn
detection scored zero on two labelled events, for a documented reason predicted
before validation. Combined, 62% precision and 56% recall — down from 85% / 79%
on the tuning set, as expected, since the held-out trips are the harder ones.
All four misses are explained. Two friction hotspots found on half the data were
confirmed on the other half, both on the approach side of the junction and both
within 1.21 m of the only sign, which lists three destinations and not the one
these people wanted. The dataset is 25 trips in a home corridor and the numbers
should be read as a demonstration that the measurement works, not as a
performance figure.
