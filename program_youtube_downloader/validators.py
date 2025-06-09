import re

from .exceptions import InvalidURLError


_VIDEO_RE = re.compile(
    r"^https?://(?:www\.)?"
    r"(?:(?:[\w-]+\.)?youtube\.com/watch\?(?:[^\s]*\bv=[\w-]+)(?:[^\s]*\blist=[\w-]+)?"
    r"|youtu\.be/[\w-]+(?:\?list=[\w-]+)?)$",
    re.IGNORECASE,
)


def validate_youtube_url(url: str) -> bool:
    """Check whether ``url`` points to a YouTube video.

    The link must use HTTP(S) and either contain a ``v=`` parameter or use the
    short ``youtu.be/<id>`` form. A ``list`` query parameter is also accepted
    when present.

    Args:
        url: URL provided by the user.

    Returns:
        ``True`` if the URL looks like a YouTube link.

    Raises:
        InvalidURLError: If the URL does not look like a YouTube link.
    """
    if not url or not _VIDEO_RE.match(url.strip()):
        raise InvalidURLError("URL invalide")

    return True

