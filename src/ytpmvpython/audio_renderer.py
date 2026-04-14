"""Audio rendering primitives for YTPMV workflows."""

from dataclasses import dataclass


@dataclass(slots=True)
class AudioSegment:
    """Rendered audio fragment metadata."""

    start_ms: int
    duration_ms: int
    source: str
    pitch_shift: float = 0.0


class AudioRenderer:
    """Builds audio segments from parsed events."""

    def render_segment(
        self,
        *,
        source: str,
        start_ms: int,
        duration_ms: int,
        pitch_shift: float = 0.0,
    ) -> AudioSegment:
        if duration_ms <= 0:
            raise ValueError("duration_ms must be greater than zero")
        return AudioSegment(
            start_ms=start_ms,
            duration_ms=duration_ms,
            source=source,
            pitch_shift=pitch_shift,
        )
