from urllib.parse import urlparse


def validate_youtube_url(url: str) -> bool:
    """Return True if ``url`` appears to be a valid YouTube URL."""
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

