"""Example YTPMV pipeline using ytpmvpython primitives."""

from ytpmvpython import AudioRenderer, ModuleParser, SourceLibrary, SourceSample, VideoRenderer


def main() -> None:
    parser = ModuleParser()
    audio = AudioRenderer()
    video = VideoRenderer()

    sources = SourceLibrary()
    sources.add(SourceSample(name="lead_vocal", path="vocal.wav", category="vocal"))
    sources.add(SourceSample(name="main_clip", path="clip.mp4", category="video"))

    events = parser.parse("song.mod")
    for event in events:
        # Replace with your real clip selection and timing strategy.
        audio.render_segment(
            source=sources.get("lead_vocal").path,
            start_ms=event.tick,
            duration_ms=120,
        )
        video.render_segment(
            source=sources.get("main_clip").path,
            start_ms=event.tick,
            duration_ms=120,
        )


if __name__ == "__main__":
    main()
