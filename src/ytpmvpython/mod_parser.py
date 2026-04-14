"""Module parsing helpers.

This module intentionally provides a clean interface and a lightweight parser
placeholder. It can be extended with real tracker/module readers.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class NoteEvent:
    """Represents one musical event from a song timeline."""

    tick: int
    note: str
    instrument: int | None = None
    velocity: int | None = None


class ModuleParser:
    """Parser interface for module files like IT/MOD/XM and converted MIDI data."""

    SUPPORTED_EXTENSIONS = {".it", ".mod", ".xm", ".s3m", ".mptm"}

    def parse(self, module_path: str | Path) -> list[NoteEvent]:
        """Parse a module file and return note events.

        Current behavior is intentionally minimal to provide project structure.
        """
        path = Path(module_path)
        if not path.exists():
            raise FileNotFoundError(f"Module file not found: {path}")
        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported format '{path.suffix}'. "
                f"Supported: {', '.join(sorted(self.SUPPORTED_EXTENSIONS))}."
            )

        # Placeholder implementation. Real parser integration can be added here.
        return []
