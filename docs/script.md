# Demo video — narration script

**VoltHacks 2026. Hard limit: 2:00. Timed read: 1:52.**
Written Sun 30 Aug. Companion to `storyboard.md`, which holds the shot list.

**Read only the quoted lines aloud.** Everything else is a stage direction.

---

## The script

**WAIT 7 SECONDS. Say nothing.**
*Visual: `shot1_opening.mp4` — undistorted, no overlay. The stop at 15.6 s, then
the stop at 24.7 s.*

> "Twice, nine seconds apart. Both within three centimetres."

**WAIT 2 SECONDS.**

> "Buildings get audited for fire safety and accessibility. Nobody audits whether
> people can find their way."

*Visual: `shot2_tracking.mp4` — boxes, ID `#1`, orange trail.*

> "This is one ceiling camera in a corridor. YOLO spots each person, ByteTrack
> keeps them tracked. A homography turns pixels into real metres."

*Visual: switch to `docs/architecture.svg`. Hold on the yellow dashed line.*

> "And then the video stops mattering. Below this line, nothing opens a clip
> again. A person has become an ID and a list of floor positions. Delete every
> video, and every number on that dashboard still reproduces."

*Visual: `shot3_events.mp4` — event markers, labelled by type.*

> "So what counts as hesitation? Slow — under thirty centimetres a second.
> Sustained — at least two seconds. And going nowhere."

> "Watch. It fires here."

**WAIT 3 SECONDS.** *Let the marker appear. Do not talk over it.*

> "The scoring counted this one as a false positive. There's no label at
> 15.6 seconds. I found it afterwards — and by then I'd already seen the
> detector's answer, so I left the score alone."

*Visual: dashboard, **"How accurate it is"** — the F1 figures. Hold still.*

> "These come from twelve trips I never tuned on. The split was written down
> before a detector existed, the scoring script was committed before it was ever
> run, and I ran it once. 62% precision, 56% recall."

*Visual: still the same panel, the amber U-turn box. Hold still.*

> "The combined number hides a zero. And I predicted that failure in writing, six
> days before I opened the held-out trips."

*Visual: scroll SLOWLY down to **"Where it happened"** — the hotspot map. One
scroll, then stop. The reveal animation catches elements mid-fade otherwise.*

> "Green dot, someone stopped. Orange triangle, someone turned around. Blue
> squares are where those bunched. The strongest one holds four stops and no
> turn-arounds — and it's a metre *short* of the sign."

*Visual: still the map.*

> "The biggest cluster isn't the finding. It's drawn because it's in the data,
> not because I trust it."

**STOP.**

---

## Why the script says what it says

**The thesis is "nobody audits wayfinding."** Chosen from ten candidates. It is the
only one that explains why the project should exist rather than what it does. It
also earns the project's name: WayTrace *audits* wayfinding.

**The false positive is stated out loud, at 15.6 s.** `data/misses_day15.txt`
line 13 scores it against the detector. The repo is public. Showing that detection
without naming it would mislead a judge who does not open the file, and contradict
one who does. It is placed in the detector section, not the opening — at 10 seconds
a judge does not yet know a detector exists, so the admission means nothing there.

**The U-turn zero is stated, and then followed by the choice it drove.** It cannot
simply be cut: it is permanently visible on the dashboard, so staying silent would
leave a judge reading it alone while the narration talks about something else.

**★ THE NARRATION MUST NOT READ THE SCREEN ALOUD. ★**
The dashboard already prints *"People got confused BEFORE they reached the sign"*
and *"The largest cluster is not the one to trust."* An earlier draft spoke almost
those exact words while they were on screen — the judge would have been reading and
hearing the same sentence, which is dull and costs seconds. **The screen states the
finding; the voice says what the screen cannot:** that the split predates the
detector, what a green dot means, and why a cluster is drawn but not trusted.

**Narrating the legends aloud also solves the hover problem.** A recording cannot
hover, so "green dot, someone stopped" has to be spoken. Rule 85.

**No number is spoken that is not in a committed file.** "Four stops, no
turn-arounds" comes from `data/output/hotspots.json`. 62% / 56% come from the
held-out validation.

**"A metre short of the sign" — NOT "right under the sign."**
The strong hotspot is **1.15 m** from `sign_A`. The hotspot *closest* to the sign
(0.65 m) is the weak one, three of whose five events are U-turns. An earlier draft
said "right under the sign" and was false. The real finding is better anyway:
**all four hotspots are on the approach side.** People slow before the sign.

---

## Cut, and why

| Cut | Cost |
|---|---|
| The upload/Analyse demo (~10 s) | Real loss. It is the clearest proof the system runs. It takes ~3 min on CPU, so it could only ever be shown with a cut, and the privacy section earns the seconds more. |
| "a stop by the door counts the same as one down the hall" | The line that made homography intuitive. |
| "Not just standing still." | Nothing — the three conditions carry it. |
| The closing 62%/56% line | Nothing — the figures moved earlier, into the accuracy panel. |

**Timings, measured by reading aloud, not estimated:**
first draft 1:58 → trimmed to 1:47 → dashboard section rewritten → **1:52.**
Estimating from word counts was wrong twice. Only a stopwatch settles it.

---

## Filming reminders

- **Page order is: counts → accuracy → map → timeline → deployment → upload.**
  The accuracy panel comes BEFORE the map. The script follows page order, so it is
  one continuous downward scroll.
- **Scroll SLOWLY**, pausing after each scroll. Mostly you hold still.
- **Hover content does not appear in a recording.** Narrate the legends aloud.
- **Ctrl+C the Streamlit server before starting another**, or you record old code.
- Cut source clips with `ffmpeg -ss/-to` rather than screen-recording them. All
  three opening shots are already cut, 21.000 s each, h264, in `data/web/`.
- `data/undist/` and `data/output/` are **mpeg4** and render as a black box.
  `data/web/` is the h264 folder.
- Dashboard footage recorded 30 Aug runs 48 s; the dashboard narration runs ~52 s.
  Hold a frame longer in the edit, or record a few seconds more.
