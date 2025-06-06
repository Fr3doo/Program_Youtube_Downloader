from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Callable, Any

from .progress import ProgressHandler, ProgressBarHandler


@dataclass
class DownloadOptions:
    """Configuration for downloading YouTube content."""

    save_path: Optional[Path] = None
    download_sound_only: bool = False
    choice_callback: Optional[Callable[[bool, Any], int]] = None
    progress_handler: Optional[ProgressHandler] = None
