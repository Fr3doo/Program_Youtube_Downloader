from urllib.parse import urlparse


def validate_youtube_url(url: str) -> bool:
    """Check whether ``url`` is a valid YouTube address.

    Args:
        url: URL provided by the user.

    Returns:
        ``True`` if the URL looks like a YouTube link, ``False`` otherwise.
    """
    if not url:
        return False
    url = url.strip()

    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return False
    host = parsed.netloc.lower()
    if host == "youtu.be":
        return True
    if host.endswith("youtube.com"):
        return True
    return False

