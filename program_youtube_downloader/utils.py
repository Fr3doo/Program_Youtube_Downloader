"""Miscellaneous utility helpers for console display."""

from __future__ import annotations

import os
import subprocess
import time
import logging
from urllib.parse import urlparse, parse_qs

__all__ = ["clear_screen", "program_break_time", "shorten_url"]

logger = logging.getLogger(__name__)


def clear_screen() -> None:
    """Clear the terminal screen on Windows or POSIX systems."""
    try:
        if os.name == "posix":
            subprocess.run(["clear"], check=True)
        else:
            subprocess.run(["cmd", "/c", "cls"], check=True)
    except subprocess.CalledProcessError as exc:  # pragma: no cover - failure path
        logger.warning(f"Échec de l'effacement de l'écran : {exc}")
        return


def program_break_time(memorization_time: int, message: str) -> None:
    """Display a short countdown.

    Args:
        memorization_time: Duration of the countdown in seconds.
        message: Message displayed before the countdown number.
    """
    remaining_seconds = memorization_time
    print(
        f"{message} {memorization_time} secondes ",
        end="",
        flush=True,
    )
    while remaining_seconds > 0:
        time.sleep(1)
        print(f"{remaining_seconds} ", end="", flush=True)
        remaining_seconds -= 1


def shorten_url(url: str) -> str:
    """Return video ID from ``url`` for safer logging."""
    try:
        parsed = urlparse(url.strip())
        host = parsed.netloc.lower()
        if host in {"youtu.be", "www.youtu.be"}:
            vid = parsed.path.strip("/").split("/", 1)[0]
        else:
            vid = parse_qs(parsed.query).get("v", [""])[0]
        if vid:
            return vid
    except Exception:  # pragma: no cover - defensive
        logger.debug("Failed to shorten url", exc_info=True)
    return "<url>"
