"""Input validation helpers."""

from urllib.parse import urlparse, parse_qs
import re

from .exceptions import InvalidURLError



def validate_youtube_url(url: str) -> bool:
    """Check whether ``url`` points to a YouTube video.

    The link must use HTTP(S), come from ``youtube.com``/``www.youtube.com`` or
    ``youtu.be`` and either contain a ``v=`` parameter or use the short
    ``youtu.be/<id>`` form. A ``list`` query parameter is also accepted when
    present.

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
    if netloc not in {"youtube.com", "www.youtube.com", "youtu.be"}:
        raise InvalidURLError("URL invalide")

    # only allow common share/query parameters
    allowed_params = {"v", "list", "t"}
    query_params = parse_qs(parsed.query, keep_blank_values=True)
    if any(k not in allowed_params for k in query_params):
        raise InvalidURLError("URL invalide")

    video_id = ""
    if netloc in {"youtube.com", "www.youtube.com"}:
        path = parsed.path
        if path.startswith("/shorts"):
            parts = path.strip("/").split("/")
            if len(parts) >= 2:
                video_id = parts[1]
            else:
                video_id = ""
        else:
            video_id = query_params.get("v", [""])[0]

        # reject playlist or channel URLs that don't specify a video ID
        if not video_id and (path.startswith("/playlist") or path.startswith("/channel")):
            raise InvalidURLError("URL invalide")
    else:
        path = parsed.path.strip("/")
        if path:
            video_id = path.split("/", 1)[0]

    if not video_id:
        raise InvalidURLError("URL invalide")

    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id):
        raise InvalidURLError("URL invalide")

    return True


__all__ = ["validate_youtube_url"]

