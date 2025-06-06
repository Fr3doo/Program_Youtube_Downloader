import sys
from typing import Protocol

import colorama
from colorama import init

init(autoreset=True)


class ProgressHandler(Protocol):
    """Interface for receiving progress events from pytube."""

    def on_progress(self, stream, chunk, bytes_remaining) -> None:  # pragma: no cover - typing
        """Handle a download progress event."""
        raise NotImplementedError


def on_download_progress(stream, chunk, bytes_remaining) -> None:  # pragma: no cover - legacy
    """Backward compatible wrapper around :class:`ProgressBarHandler`."""
    ProgressBarHandler().on_progress(stream, chunk, bytes_remaining)


def progress_bar(
    progress: float,
    size: int = 35,
    sides: str = "||",
    full: str = "█",
    empty: str = " ",
    prefix_start: str = "Downloading ...",
    prefix_end: str = "Download OK ...",
    color_text: str = colorama.Fore.WHITE,
    color_Downloading: str = colorama.Fore.LIGHTYELLOW_EX,
    color_Download_OK: str = colorama.Fore.GREEN,
) -> None:
    """Print a textual progress bar to standard output."""
    x = int(size * progress / 100)
    bar = sides[0] + full * x + empty * (size - x) + sides[1]
    sys.stdout.write(color_text + "\r" + prefix_start + color_Downloading + bar + f" {progress:.2f}% ")

    if progress == 100:
        sys.stdout.write("\r" + color_text + prefix_end + color_Download_OK + bar + f" {progress:.2f}% ")
        print(colorama.Fore.RESET)

    sys.stdout.flush()


class ProgressBarHandler:
    """Default progress handler displaying a textual bar."""

    def on_progress(self, stream, chunk, bytes_remaining) -> None:
        total_bytes_download = stream.filesize
        bytes_downloaded = stream.filesize - bytes_remaining
        progress = (bytes_downloaded / total_bytes_download) * 100
        progress_bar(progress)
