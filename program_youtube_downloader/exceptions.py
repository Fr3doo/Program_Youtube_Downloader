class PydlError(Exception):
    """Base class for all custom errors."""


class DownloadError(PydlError):
    """Raised when a download fails after several retries."""


class ValidationError(PydlError):
    """Raised when user input validation repeatedly fails."""


class PlaylistConnectionError(PydlError):
    """Raised when connecting to a playlist fails."""


class ChannelConnectionError(PydlError):
    """Raised when connecting to a channel fails."""


class StreamAccessError(PydlError):
    """Raised when accessing the streams of a video fails."""


class DirectoryCreationError(PydlError):
    """Raised when a destination directory cannot be created."""


class InvalidURLError(PydlError):
    """Raised when a provided URL does not match expected YouTube patterns."""


__all__ = [
    "PydlError",
    "DownloadError",
    "ValidationError",
    "PlaylistConnectionError",
    "ChannelConnectionError",
    "StreamAccessError",
    "DirectoryCreationError",
    "InvalidURLError",
]

