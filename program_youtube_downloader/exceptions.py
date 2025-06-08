class DownloadError(Exception):
    """Raised when a download fails after several retries."""


class ValidationError(Exception):
    """Raised when user input validation repeatedly fails."""


class PlaylistConnectionError(Exception):
    """Raised when connecting to a playlist fails."""


class ChannelConnectionError(Exception):
    """Raised when connecting to a channel fails."""


class StreamAccessError(Exception):
    """Raised when accessing the streams of a video fails."""


class DirectoryCreationError(Exception):
    """Raised when a destination directory cannot be created."""


class InvalidURLError(Exception):
    """Raised when a provided URL does not match expected YouTube patterns."""

