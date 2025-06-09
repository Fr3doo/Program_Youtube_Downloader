"""Input validation helpers."""

from urllib.parse import urlparse, parse_qs

from .exceptions import InvalidURLError



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
    clean_url = url.strip()
    if not clean_url or " " in clean_url:
        raise InvalidURLError("URL invalide")

    parsed = urlparse(clean_url)

    if parsed.scheme not in ("http", "https"):
        raise InvalidURLError("URL invalide")

    netloc = parsed.netloc.lower()
    if netloc == "www.youtube.com":
        netloc = "youtube.com"

    if netloc not in {"youtube.com", "youtu.be"}:
        raise InvalidURLError("URL invalide")

    video_id = ""
    if netloc == "youtube.com":
        video_id = parse_qs(parsed.query).get("v", [""])[0]
    else:
        path = parsed.path.strip("/")
        if path:
            video_id = path.split("/", 1)[0]

    if not video_id:
        raise InvalidURLError("URL invalide")

    return True

