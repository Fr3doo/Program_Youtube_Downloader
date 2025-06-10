import pytest

from program_youtube_downloader.validators import validate_youtube_url
from program_youtube_downloader.exceptions import InvalidURLError


VALID_ID = "dQw4w9WgXcQ"


def test_validate_youtube_url_valid() -> None:
    assert (
        validate_youtube_url(f"https://www.youtube.com/watch?v={VALID_ID}") is True
    )
    assert validate_youtube_url(f"https://youtube.com/watch?v={VALID_ID}") is True
    assert validate_youtube_url(f"https://youtu.be/{VALID_ID}") is True
    assert (
        validate_youtube_url(
            f"https://www.youtube.com/watch?v={VALID_ID}&list=123"
        )
        is True
    )
    assert validate_youtube_url(f"https://youtu.be/{VALID_ID}?list=xyz") is True
    assert (
        validate_youtube_url(f"https://YouTube.com/watch?v={VALID_ID}&t=5") is True
    )
    assert validate_youtube_url(f"https://youtu.be/{VALID_ID}/") is True


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
        validate_youtube_url(
            f"https://www.youtube.com/watch?v={VALID_ID} extra"
        )
    with pytest.raises(InvalidURLError):
        validate_youtube_url(f"https://youtu.be/{VALID_ID} extra")


def test_validate_youtube_url_bad_length() -> None:
    with pytest.raises(InvalidURLError):
        validate_youtube_url("https://www.youtube.com/watch?v=shortid")
    with pytest.raises(InvalidURLError):
        validate_youtube_url("https://youtu.be/too_long_id12")


def test_validate_youtube_url_bad_chars() -> None:
    bad = "dQw4w9WgXcQ!"
    with pytest.raises(InvalidURLError):
        validate_youtube_url(f"https://www.youtube.com/watch?v={bad}")
    with pytest.raises(InvalidURLError):
        validate_youtube_url(f"https://youtu.be/{bad}")


def test_validate_youtube_url_invalid_domain() -> None:
    with pytest.raises(InvalidURLError):
        validate_youtube_url(f"https://m.youtube.com/watch?v={VALID_ID}")
    with pytest.raises(InvalidURLError):
        validate_youtube_url(f"https://youtube.co/watch?v={VALID_ID}")
    with pytest.raises(InvalidURLError):
        validate_youtube_url(f"https://youtu.be.com/watch?v={VALID_ID}")


def test_validate_youtube_url_space_handling() -> None:
    assert (
        validate_youtube_url(
            f"  https://www.youtube.com/watch?v={VALID_ID}  "
        )
        is True
    )
    with pytest.raises(InvalidURLError):
        validate_youtube_url(f"https://www.youtube.com/watch?v=dQw4w9 WgXcQ")
