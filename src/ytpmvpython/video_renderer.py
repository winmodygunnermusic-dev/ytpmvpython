"""Video rendering primitives for YTPMV workflows."""

from dataclasses import dataclass


@dataclass(slots=True)
class VideoSegment:
    """Rendered video fragment metadata."""

    start_ms: int
    duration_ms: int
    source: str
    playback_rate: float = 1.0


class VideoRenderer:
    """Builds video segments from parsed events."""

    def render_segment(
        self,
        *,
        source: str,
        start_ms: int,
        duration_ms: int,
        playback_rate: float = 1.0,
    ) -> VideoSegment:
        if duration_ms <= 0:
            raise ValueError("duration_ms must be greater than zero")
        if playback_rate <= 0:
            raise ValueError("playback_rate must be greater than zero")
        return VideoSegment(
            start_ms=start_ms,
            duration_ms=duration_ms,
            source=source,
            playback_rate=playback_rate,
        )
