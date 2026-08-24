# WayTrace — Event Definitions

**Written 24 Aug 2026, BEFORE any labelling and BEFORE any detector output was
examined.** These numbers were chosen from reasoning and memory of the shoot, not
from tuning against results. The commit timestamp on this file is the evidence.

They are expected to be wrong. Day 12 tunes them against the odd-numbered trips
only. What matters is that the starting point was chosen honestly.

---

## HESITATION

> A person is hesitating when their **smoothed** speed drops **below 0.3 m/s**
> and stays below it for **at least 2 seconds**.

**Why 0.3 m/s:** normal walking is about 1.2 m/s. 0.3 is a quarter of that —
shuffling, or effectively stopped. Setting it near 1.2 would count ordinary
walking; setting it at 0 would count nothing, because no tracked point is ever
exactly still.

**Why 2 seconds:** a shorter dip is a footstep, not a pause. Confirmed against
the shoot — pauses on the night ran about 2 seconds or longer.

**Why smoothed:** unsmoothed speeds spike whenever the box bottom edge jumps as a
foot lifts (Rule 21). An unsmoothed detector fires on footsteps, not hesitation.

---

## U-TURN

> A person made a U-turn when their **direction of travel changes by more than
> 135 degrees** and they keep going the new way for **at least 1 second**.

**Why 135 degrees:** a full turn-around is 180. Turning a corner is about 90.
135 sits between them, so corners are not counted as U-turns.

**Why 1 second:** the direction has to *stay* changed. A momentary flicker is
tracker noise.

**Measured over a window, never frame to frame** (Rule 21). Two consecutive
frames are 0.067 s apart, and heading computed over that gap is dominated by
position error.

---

## DOES NOT COUNT

- **Walk-backs** — a person returning to the start point. Excluded automatically
  by the direction rule (final y greater than starting y).
- Someone standing still talking to another person.
- Someone waiting by the door, not travelling to a destination.
- Any track shorter than the fragment filter (`int(fps * 1.0)`).

---

## What these definitions deliberately do NOT claim

An event is a **behaviour**, not a mental state. The system detects that someone
slowed down or turned around. It does not detect confusion, and the wording
throughout the project reflects that:

- Say **"hesitation event"**, never "this person was confused".
- Say **"possible signage issue associated with this hotspot"**, never
  "this sign caused it".
