# WayTrace — Labelling Tracker

**Rule: count walks from the video FIRST. Open the shoot log only after the
clip's rows are written.** The log is a check, never a source. This is what
found abrish's unlogged second walk in clip3.

**`category` stays blank on every row until all 13 clips are done.**

---

## Progress

| Clip | Walks seen | Trips | Excluded | Events | Status |
|---|---|---|---|---|---|
| clip1 | 5 | 5 | 0 | 8 | DONE |
| clip2 | 1 | 1 | 0 | 0 | DONE |
| clip3 | 4 | 1 | 3 | 0 | DONE |
| clip4 | | | | | |
| clip5 | | | | | |
| clip6 | | | | | |
| clip7 | | | | | |
| clip8 | | | | | |
| clip9 | | | | | |
| clip10 | | | | | |
| clip11 | | | | | |
| clip12 | | | | | |
| clip13 | | | | | |

**Trips numbered so far: 1–7.** Next trip number: **8**.
**Events so far: E1–E8.** Next event id: **E9**.

---

## The three passes

**Pass 1 — watch whole clip, write nothing.** Calibrating on what a normal walk
looks like in this clip. Lighting and distance shift between clips.

**Pass 2 — boundaries only.** Start second and end second, whole numbers. Person
code. Nothing about events.

**Pass 3 — events only.** Hesitations and U-turns, one decimal place.

Then write the rows. Then open the shoot log and compare.

---

## Is it a trip?

- One person in frame, alone
- Enters bottom, ends nearer the top — **final y < starting y**
- Start and end both visible, not cut off by the clip edges
- Never leaves frame mid-walk

A walk-back (hands up, returning to start) is **not** a trip. No number, but a
note on the trip it follows.

**Excluded is not unrecorded.** A walk that fails the test still gets a row with
`valid = EXCLUDE`, a blank trip number, and an `exclude_reason`.

Common exclude reasons seen so far:
- `left frame into side room, ID would split`
- `logged wasted on shoot night`
- `not in shoot log at all`

---

## trips row — paste order

```
trip	clip	valid	exclude_reason	person	start_sec	end_sec	others_in_frame	occluded	clean_entry	boundary_sure	category	notes
```

- `person`: P1 fatima, P2 zarlish, P3 abrish
- `boundary_sure`: SURE / MAYBE — could you see the exact second?
- `category`: **always blank**

## events row — paste order

```
event_id	trip	event_type	start_sec	end_sec	confidence	notes	boundary_note
```

- `event_type`: HESITATION / UTURN
- `end_sec`: one decimal. **UTURN is always start + 1**
- `confidence`: SURE / MAYBE — *did it happen*, nothing else
- `boundary_note`: `end by convention` on every UTURN
- Zero events is a result, not a gap. Leave the tab untouched.

---

## Wording

Never "they were confused" or "they got lost" — a camera cannot see a mental
state. Write "appeared to hesitate", "stopped facing the sign", "turned back".

**Never delete an event because you know why it happened.** Stopping to read a
sign IS the friction this system detects.

---

## Commit after every clip

```
git add data/trip.csv data/event.csv
git commit -m "labels: clipN, trips X-Y"
git push
```

Check the byte count moved before committing. A file that didn't change is an
export that didn't overwrite.
