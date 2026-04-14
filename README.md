# ytpmvpython

A Python toolkit for creating YTPMVs on Windows 8.1, 10, and 11.

I built this because I wanted a faster workflow than manually pitching audio and placing clips in Vegas. The goal is to automate the repetitive parts of YTPMV production while keeping full creative control in code.

## What it includes

This project is a library of utilities with three main parts:

1. **Module file parser** for tracker/module formats like `.IT`, `.MOD`, `.XM`, `.S3M`, `.MPTM`, and more via conversion workflows  
   **Includes source-sample helpers for YTPMV multi-parser workflows.**
2. **Audio renderer**
3. **Video renderer**

## Workflow

To make a YTPMV, you write a Python program that:

1. Parses a module file (`.mod` or another supported tracker format)
2. Iterates through each note/event
3. Generates audio and video segments based on your own rules

Any module or MIDI file can be converted to `.mod` with OpenMPT (usually with some manual cleanup/fixing).

## Quick start

```bash
pip install -e .
python examples/basic_pipeline.py
```

### Minimal code example

```python
from ytpmvpython import ModuleParser, AudioRenderer, VideoRenderer

parser = ModuleParser()
audio = AudioRenderer()
video = VideoRenderer()

for event in parser.parse("song.mod"):
    audio.render_segment(source="vocal.wav", start_ms=event.tick, duration_ms=120)
    video.render_segment(source="clip.mp4", start_ms=event.tick, duration_ms=120)
```

## Multi-parser and source sample utilities

The toolkit includes a small source-sample registry so you can define reusable source clips
for vocals, drums, bass, stabs, and visual layers, then map note events to those assets
programmatically.

## GUI (optional)

A basic desktop GUI is included for fast iteration:

```bash
ytpmvpython-gui
```

Use it to select module files, validate supported formats, and preview event-driven build output.

## Project direction

There are a few example videos, and the long-term goal is to enable very advanced YTPMVs in under an hour.
