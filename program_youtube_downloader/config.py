from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Callable, Any

from .progress import on_download_progress


@dataclass
class DownloadOptions:
    """Configuration for downloading YouTube content."""

    save_path: Optional[Path] = None
    download_sound_only: bool = False
    choice_callback: Optional[Callable[[bool, Any], int]] = None
    progress_callback: Optional[Callable[[Any, Any, int], None]] = on_download_progress
