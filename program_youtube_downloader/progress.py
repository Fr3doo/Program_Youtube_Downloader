import sys
from dataclasses import dataclass
from typing import Protocol
import logging

import colorama
from colorama import init

init(autoreset=True)

logger = logging.getLogger(__name__)


class ProgressHandler(Protocol):
    """Interface for receiving progress events from pytube."""

    def on_progress(
        self, stream, chunk, bytes_remaining
    ) -> None:  # pragma: no cover - typing
        """Handle a download progress event."""
        raise NotImplementedError


def on_download_progress(
    stream, chunk, bytes_remaining
) -> None:  # pragma: no cover - legacy
    """Backward compatible wrapper around :class:`ProgressBarHandler`."""
    ProgressBarHandler().on_progress(stream, chunk, bytes_remaining)


@dataclass
class ProgressOptions:
    """Configuration for :func:`progress_bar`."""

    size: int = 35
    sides: str = "||"
    full: str = "█"
    empty: str = " "
    prefix_start: str = "Downloading ..."
    prefix_end: str = "Download OK ..."
    color_text: str = colorama.Fore.WHITE
    color_Downloading: str = colorama.Fore.LIGHTYELLOW_EX
    color_Download_OK: str = colorama.Fore.GREEN


def progress_bar(progress: float, options: ProgressOptions | None = None) -> None:
    """Print a textual progress bar to standard output.

    Args:
        progress: Percentage of completion between 0 and 100.
        options: Display configuration. If ``None`` defaults are used.
    """
    if options is None:
        options = ProgressOptions()

    x = int(options.size * progress / 100)
    bar = (
        options.sides[0]
        + options.full * x
        + options.empty * (options.size - x)
        + options.sides[1]
    )
    sys.stdout.write(
        options.color_text
        + "\r"
        + options.prefix_start
        + options.color_Downloading
        + bar
        + f" {progress:.2f}% "
    )

    if progress == 100:
        sys.stdout.write(
            "\r"
            + options.color_text
            + options.prefix_end
            + options.color_Download_OK
            + bar
            + f" {progress:.2f}% "
        )
        print(colorama.Fore.RESET)

    sys.stdout.flush()


class ProgressBarHandler:
    """Default progress handler displaying a textual bar."""

    def __init__(self, options: ProgressOptions | None = None) -> None:
        self.options = options

    def on_progress(self, stream, chunk, bytes_remaining) -> None:
        """Compute percentage and forward it to :func:`progress_bar`."""
        total_bytes_download = getattr(stream, "filesize", None)
        if not total_bytes_download:
            logger.warning("Missing total filesize. Assuming complete")
            progress = 100.0
        else:
            bytes_downloaded = total_bytes_download - bytes_remaining
            progress = (bytes_downloaded / total_bytes_download) * 100
        progress_bar(progress, self.options)


class VerboseProgressHandler:
    """Progress handler printing only the percentage."""

    def on_progress(self, stream, chunk, bytes_remaining) -> None:
        """Display the download percentage without a bar."""
        total = stream.filesize
        downloaded = total - bytes_remaining
        percent = (downloaded / total) * 100
        print(f"{percent:.2f}%")


__all__ = [
    "ProgressHandler",
    "on_download_progress",
    "ProgressOptions",
    "progress_bar",
    "ProgressBarHandler",
    "VerboseProgressHandler",
]
