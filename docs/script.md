# Demo video — narration script

**VoltHacks 2026. Hard limit: 2:00. Timed read: 1:47.**
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

*Visual: dashboard, hotspot map. Scroll SLOWLY — the reveal animation catches
elements mid-fade otherwise.*

> "Every trip lands on one map. Where stops cluster, you get a hotspot. The one in
> the middle holds four hesitations and no turn-arounds — just over a metre from
> the only sign, on the approach side. Every hotspot is. People slow down
> *before* they reach the sign."

> "The cluster below has more events, but three of its five are turn-arounds, and
> my U-turn detector scored zero. So the map doesn't lead with it."

*Visual: dashboard, accuracy panel.*

> "Twelve held-out trips, never tuned on. 62% precision, 56% recall. Not the score
> I wanted. The one I got."

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

**The U-turn zero is stated, and then followed by the choice it drove** — "so the
map doesn't lead with it." The last thing a judge hears is the method, not the
failure. It cannot simply be cut: it is permanently visible on the dashboard, so
staying silent would leave a judge reading it alone while the narration talks about
something else.

**No number is spoken that is not in a committed file.** "Four hesitations, no
turn-arounds" and "three of its five are turn-arounds" both come from
`data/output/hotspots.json`. 62% / 56% come from the held-out validation.

**"Just over a metre from the only sign" — NOT "right under the sign."**
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
| "in the corridor", "not at it", one "for" | Nothing. |

**First timed read was 1:58 — two seconds under the limit, which is not a margin.**
Three trims brought it to 1:47.

---

## Filming reminders

- **Scroll the dashboard SLOWLY**, pausing after each scroll.
- **Hover content does not appear in a recording.** Narrate the legends aloud.
- **Ctrl+C the Streamlit server before starting another**, or you record old code.
- Cut source clips with `ffmpeg -ss/-to` rather than screen-recording them. All
  three opening shots are already cut, 21.000 s each, h264, in `data/web/`.
- `data/undist/` and `data/output/` are **mpeg4** and render as a black box.
  `data/web/` is the h264 folder.
