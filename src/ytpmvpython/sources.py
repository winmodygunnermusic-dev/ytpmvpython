"""Source sample helpers for mapping events to media assets."""

from dataclasses import dataclass


@dataclass(slots=True)
class SourceSample:
    """Represents a named source asset that can feed audio/video renderers."""

    name: str
    path: str
    category: str = "general"


class SourceLibrary:
    """Container for reusable YTPMV source samples."""

    def __init__(self) -> None:
        self._samples: dict[str, SourceSample] = {}

    def add(self, sample: SourceSample) -> None:
        self._samples[sample.name] = sample

    def get(self, name: str) -> SourceSample:
        try:
            return self._samples[name]
        except KeyError as exc:
            raise KeyError(f"Unknown sample '{name}'") from exc

    def names(self) -> list[str]:
        return sorted(self._samples.keys())
