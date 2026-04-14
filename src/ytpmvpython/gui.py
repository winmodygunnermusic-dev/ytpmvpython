"""Tkinter GUI for quick YTPMV pipeline setup and preview."""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from .audio_renderer import AudioRenderer
from .mod_parser import ModuleParser
from .video_renderer import VideoRenderer


class YTPMVGuiApp:
    """Simple desktop UI to validate module input and preview pipeline actions."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("ytpmvpython")
        self.root.geometry("760x500")

        self.module_path = tk.StringVar(value="")
        self.audio_source = tk.StringVar(value="vocal.wav")
        self.video_source = tk.StringVar(value="clip.mp4")

        self.parser = ModuleParser()
        self.audio_renderer = AudioRenderer()
        self.video_renderer = VideoRenderer()

        self._build_layout()

    def _build_layout(self) -> None:
        frame = ttk.Frame(self.root, padding=12)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Module file (.it/.mod/.xm/.s3m/.mptm):").grid(
            row=0, column=0, sticky="w"
        )
        module_entry = ttk.Entry(frame, textvariable=self.module_path, width=70)
        module_entry.grid(row=1, column=0, padx=(0, 8), sticky="we")
        ttk.Button(frame, text="Browse", command=self._pick_module).grid(row=1, column=1)

        ttk.Label(frame, text="Audio source:").grid(row=2, column=0, sticky="w", pady=(12, 0))
        ttk.Entry(frame, textvariable=self.audio_source, width=70).grid(
            row=3, column=0, columnspan=2, sticky="we"
        )

        ttk.Label(frame, text="Video source:").grid(row=4, column=0, sticky="w", pady=(12, 0))
        ttk.Entry(frame, textvariable=self.video_source, width=70).grid(
            row=5, column=0, columnspan=2, sticky="we"
        )

        actions = ttk.Frame(frame)
        actions.grid(row=6, column=0, columnspan=2, pady=(12, 0), sticky="w")
        ttk.Button(actions, text="Validate Module", command=self._validate_module).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(actions, text="Preview Build Plan", command=self._preview_plan).pack(
            side="left"
        )

        self.output = tk.Text(frame, height=14, wrap="word")
        self.output.grid(row=7, column=0, columnspan=2, pady=(12, 0), sticky="nsew")

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(7, weight=1)

    def _pick_module(self) -> None:
        chosen = filedialog.askopenfilename(
            title="Select module file",
            filetypes=[
                ("Tracker modules", "*.it *.mod *.xm *.s3m *.mptm"),
                ("All files", "*.*"),
            ],
        )
        if chosen:
            self.module_path.set(chosen)

    def _validate_module(self) -> None:
        path = self.module_path.get().strip()
        if not path:
            messagebox.showwarning("Missing file", "Please select a module file first.")
            return

        try:
            _ = self.parser.parse(path)
        except ValueError as exc:
            messagebox.showerror("Unsupported format", str(exc))
            return
        except FileNotFoundError as exc:
            messagebox.showerror("File not found", str(exc))
            return

        self._log(f"✔ Module format accepted: {Path(path).name}")

    def _preview_plan(self) -> None:
        path = self.module_path.get().strip()
        if not path:
            messagebox.showwarning("Missing file", "Please select a module file first.")
            return

        try:
            events = self.parser.parse(path)
        except Exception as exc:  # Surface friendly error in UI.
            messagebox.showerror("Cannot build plan", str(exc))
            return

        if not events:
            self._log("No note events parsed yet (parser backend placeholder).")
            self._log(
                "When parser backend is connected, this view will list generated audio/video segments."
            )
            return

        self._log(f"Parsed {len(events)} events from {Path(path).name}")
        for event in events[:16]:
            audio = self.audio_renderer.render_segment(
                source=self.audio_source.get(),
                start_ms=event.tick,
                duration_ms=120,
            )
            video = self.video_renderer.render_segment(
                source=self.video_source.get(),
                start_ms=event.tick,
                duration_ms=120,
            )
            self._log(
                f"tick={event.tick} note={event.note} | "
                f"audio={audio.source}@{audio.start_ms}ms | "
                f"video={video.source}@{video.start_ms}ms"
            )

    def _log(self, text: str) -> None:
        self.output.insert("end", text + "\n")
        self.output.see("end")


def run_gui() -> None:
    root = tk.Tk()
    YTPMVGuiApp(root)
    root.mainloop()
