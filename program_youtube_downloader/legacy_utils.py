"""Deprecated helper wrapper to preserve old imports.

Import :func:`clear_screen` and :func:`program_break_time` from
``program_youtube_downloader.utils`` instead.
"""

from __future__ import annotations

from .utils import clear_screen, program_break_time

__all__ = ["clear_screen", "program_break_time"]
