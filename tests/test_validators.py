import pytest

from program_youtube_downloader.validators import validate_youtube_url
from program_youtube_downloader.exceptions import InvalidURLError


def test_validate_youtube_url_valid() -> None:
    assert validate_youtube_url("https://www.youtube.com/watch?v=ok") is True
    assert validate_youtube_url("https://youtube.com/watch?v=ok") is True
    assert validate_youtube_url("https://youtu.be/abc") is True
    assert validate_youtube_url("https://www.youtube.com/watch?v=ok&list=123") is True
    assert validate_youtube_url("https://youtu.be/abc?list=xyz") is True
    assert validate_youtube_url("https://YouTube.com/watch?v=ok&t=5") is True
    assert validate_youtube_url("https://youtu.be/abc/") is True


def test_validate_youtube_url_invalid() -> None:
    with pytest.raises(InvalidURLError):
        validate_youtube_url("http://example.com")
    with pytest.raises(InvalidURLError):
        validate_youtube_url("notaurl")
    with pytest.raises(InvalidURLError):
        validate_youtube_url("ftp://youtu.be/id")
    with pytest.raises(InvalidURLError):
        validate_youtube_url("https://www.youtube.com/watch?list=only")
    with pytest.raises(InvalidURLError):
        validate_youtube_url("https://youtu.be/")
    with pytest.raises(InvalidURLError):
        validate_youtube_url("https://www.youtube.com/playlist?list=abc")
    with pytest.raises(InvalidURLError):
        validate_youtube_url("https://www.youtube.com/watch?v=")
    with pytest.raises(InvalidURLError):
        validate_youtube_url("https://www.youtu.be/watch?v=ok")


def test_validate_youtube_url_rejects_extra_chars() -> None:
    with pytest.raises(InvalidURLError):
        validate_youtube_url("https://www.youtube.com/watch?v=ok extra")
    with pytest.raises(InvalidURLError):
        validate_youtube_url("https://youtu.be/abc extra")
