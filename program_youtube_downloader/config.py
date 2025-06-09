from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Callable, Any
import os

from .progress import ProgressHandler


def _max_workers_from_env() -> int:
    value = os.getenv("PYDL_MAX_WORKERS")
    if value is None:
        return 1
    try:
        return int(value)
    except ValueError:
        return 1


@dataclass
class DownloadOptions:
    """Options controlling the download workflow.

    Attributes:
        save_path: Destination directory for downloaded files. If ``None``
            the current working directory is used.
        download_sound_only: When ``True`` only the audio track is kept and the
            resulting file is converted to MP3.
        choice_callback: Callback invoked to let the user choose the quality of
            a stream. It receives ``download_sound_only`` and the list of
            available streams and must return the chosen index (starting at 1).
        progress_handler: Object receiving progress events from ``pytubefix``.
            Defaults to :class:`~program_youtube_downloader.progress.ProgressBarHandler`.
        max_workers: Number of simultaneous downloads. ``1`` disables
            threading. If not provided, the value is read from the
            ``PYDL_MAX_WORKERS`` environment variable, defaulting to ``1``.
    """

    save_path: Optional[Path] = None
    download_sound_only: bool = False
    choice_callback: Optional[Callable[[bool, Any], int]] = None
    progress_handler: Optional[ProgressHandler] = None
    max_workers: int = field(default_factory=_max_workers_from_env)
