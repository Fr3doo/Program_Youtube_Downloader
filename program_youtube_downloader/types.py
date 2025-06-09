from typing import Protocol, Any


class YouTubeVideo(Protocol):
    """Minimal interface required from pytube ``YouTube`` objects."""

    streams: Any

    @property
    def title(self) -> str:  # pragma: no cover - typing stub
        ...

    def register_on_progress_callback(self, cb) -> None:  # pragma: no cover - typing stub
        ...


__all__ = ["YouTubeVideo"]
