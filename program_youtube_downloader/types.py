from typing import Protocol, Any, Callable


class ConsoleIO(Protocol):
    """Simple interface abstracting console input/output."""

    def input(self, prompt: str = "") -> str:  # pragma: no cover - typing stub
        ...

    def print(self, *args: Any, **kwargs: Any) -> None:  # pragma: no cover - typing stub
        ...


class DefaultConsoleIO:
    """Default :class:`ConsoleIO` implementation relying on built-ins."""

    def input(self, prompt: str = "") -> str:
        return input(prompt)

    def print(self, *args: Any, **kwargs: Any) -> None:
        print(*args, **kwargs)


class YouTubeVideo(Protocol):
    """Minimal interface required from pytube ``YouTube`` objects."""

    streams: Any

    @property
    def title(self) -> str:  # pragma: no cover - typing stub
        """Return the video title."""

        ...

    def register_on_progress_callback(
        self, cb: Callable[[Any, bytes, int], None]
    ) -> None:  # pragma: no cover - typing stub
        """Register a callback invoked during downloads."""

        ...


__all__ = [
    "YouTubeVideo",
    "ConsoleIO",
    "DefaultConsoleIO",
]
