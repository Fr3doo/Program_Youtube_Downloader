from program_youtube_downloader import cli_utils


def test_ask_numeric_value_retries(monkeypatch):
    inputs = iter(["foo", "5", "2"])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))
    value = cli_utils.ask_numeric_value(1, 3)
    assert value == 2


def test_ask_youtube_url_normalizes_channel(monkeypatch):
    inputs = iter(["https://www.youtube.com/@MyChannel"])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))
    url = cli_utils.ask_youtube_url()
    assert url == "https://www.youtube.com/c/MyChannel"


def test_ask_youtube_url_invalid_prefix(monkeypatch):
    inputs = iter([
        "http://example.com/video",
        "https://www.youtube.com/watch?v=ok",
    ])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))
    url = cli_utils.ask_youtube_url()
    assert url == "https://www.youtube.com/watch?v=ok"


def test_ask_youtube_url_invalid_then_valid(monkeypatch):
    inputs = iter([
        "invalid",
        "https://www.youtube.com/watch?v=good",
    ])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))
    url = cli_utils.ask_youtube_url()
    assert url == "https://www.youtube.com/watch?v=good"
