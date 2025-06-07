class DownloadError(Exception):
    """Raised when a download fails after several retries."""


class ValidationError(Exception):
    """Raised when user input validation repeatedly fails."""

