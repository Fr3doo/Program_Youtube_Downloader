from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Callable, Any, TypeVar
import os

from .progress import ProgressHandler

T = TypeVar("T")


def _option_from_env(name: str, converter: Callable[[str], T], default: T) -> T:
    """Return ``name`` converted by ``converter`` or ``default`` on error."""
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return converter(value)
    except Exception:
        return default


def _max_workers_from_env() -> int:
    """Return ``PYDL_MAX_WORKERS`` as an integer or fallback to ``1``."""
    return _option_from_env("PYDL_MAX_WORKERS", int, 1)


def _output_dir_from_env() -> Optional[Path]:
    """Return ``PYDL_OUTPUT_DIR`` as a ``Path`` or ``None``."""
    return _option_from_env(
        "PYDL_OUTPUT_DIR",
        lambda p: Path(p).expanduser().resolve(),
        None,
    )


def _audio_only_from_env() -> bool:
    """Return ``PYDL_AUDIO_ONLY`` as a boolean."""
    return _option_from_env(
        "PYDL_AUDIO_ONLY",
        lambda v: v.strip().lower() in {"1", "true", "yes", "on"},
        False,
    )


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

    save_path: Optional[Path] = field(default_factory=_output_dir_from_env)
    download_sound_only: bool = field(default_factory=_audio_only_from_env)
    choice_callback: Optional[Callable[[bool, Any], int]] = None
    progress_handler: Optional[ProgressHandler] = None
    max_workers: int = field(default_factory=_max_workers_from_env)


__all__ = ["DownloadOptions"]
