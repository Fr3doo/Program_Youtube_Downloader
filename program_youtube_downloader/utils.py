"""Miscellaneous utility helpers for console display."""

from __future__ import annotations

import os
import subprocess
import time
import logging

__all__ = ["clear_screen", "program_break_time"]

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
