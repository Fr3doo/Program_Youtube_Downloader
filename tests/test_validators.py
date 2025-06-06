from program_youtube_downloader.validators import validate_youtube_url


def test_validate_youtube_url_valid() -> None:
    assert validate_youtube_url("https://www.youtube.com/watch?v=ok")
    assert validate_youtube_url("https://youtube.com/watch?v=ok")
    assert validate_youtube_url("https://youtu.be/abc")


def test_validate_youtube_url_invalid() -> None:
    assert not validate_youtube_url("http://example.com")
    assert not validate_youtube_url("notaurl")
    assert not validate_youtube_url("ftp://youtu.be/id")
