# ytpmvpython Tutorial

This tutorial walks you through building a basic YTPMV pipeline with **ytpmvpython**.

## 1) Install and set up

From the project root:

```bash
pip install -e .
```

You can now import the package in Python scripts.

---

## 2) Prepare your tracker/module file

`ModuleParser` currently accepts these file extensions:

- `.it`
- `.mod`
- `.xm`
- `.s3m`
- `.mptm`

If your song is MIDI, convert it to `.mod` (or another supported module format) with OpenMPT,
then do manual cleanup as needed.

---

## 3) Create your first script

Create `my_first_ytpmv.py`:

```python
from ytpmvpython import AudioRenderer, ModuleParser, VideoRenderer

parser = ModuleParser()
audio = AudioRenderer()
video = VideoRenderer()

events = parser.parse("song.mod")

for event in events:
    audio_segment = audio.render_segment(
        source="vocal.wav",
        start_ms=event.tick,
        duration_ms=120,
        pitch_shift=0.0,
    )
    video_segment = video.render_segment(
        source="clip.mp4",
        start_ms=event.tick,
        duration_ms=120,
        playback_rate=1.0,
    )

    print(audio_segment, video_segment)
```

Run:

```bash
python my_first_ytpmv.py
```

---

## 4) Use source sample utilities

When projects grow, managing source clip paths inline gets messy. Use `SourceLibrary`:

```python
from ytpmvpython import SourceLibrary, SourceSample

sources = SourceLibrary()
sources.add(SourceSample(name="lead_vocal", path="vocal.wav", category="vocal"))
sources.add(SourceSample(name="main_clip", path="clip.mp4", category="video"))

print(sources.names())
lead_vocal = sources.get("lead_vocal")
```

Now you can map notes/channels to reusable source entries.

---

## 5) Try the GUI (optional)

Launch:

```bash
ytpmvpython-gui
```

In the GUI you can:

1. Select a module file
2. Validate file support quickly
3. Preview event-driven build output in the log panel

---

## 6) Build your own arrangement logic

The toolkit is designed for custom decision logic. Typical next steps:

- Map pitch ranges to different source samples
- Add timing rules for stutters, reverses, and repeats
- Route percussion rows to dedicated visual cuts
- Group sections (intro/drop/breakdown) with different render rules

---

## 7) Common errors and fixes

- **`FileNotFoundError: Module file not found`**
  - Check the module path and working directory.
- **Unsupported extension error**
  - Convert the input with OpenMPT to a supported module format.
- **No events returned**
  - Current parser backend is intentionally lightweight; extend parser logic for your real module content.

---

## 8) Next improvements you can implement

- Add a real module parser backend (OpenMPT/libopenmpt bridge)
- Add FFmpeg render backends for writing final audio/video output files
- Add timeline export (JSON/CSV) to inspect generated segment plans
- Add unit tests for mapping and rendering rules

Happy building — the goal is advanced YTPMVs in less time, with more control.
