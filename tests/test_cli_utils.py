import pytest

from program_youtube_downloader import cli_utils
from program_youtube_downloader.exceptions import ValidationError


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


def test_demander_save_file_path_existing(tmp_path, monkeypatch):
    inputs = iter([str(tmp_path)])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))
    p = cli_utils.demander_save_file_path()
    assert p == tmp_path.resolve()


def test_demander_save_file_path_create(tmp_path, monkeypatch):
    new_dir = tmp_path / "newdir"
    inputs = iter([str(new_dir), "y"])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))
    p = cli_utils.demander_save_file_path()
    assert p == new_dir.resolve()
    assert new_dir.exists()


def test_demander_save_file_path_retry(monkeypatch, tmp_path):
    missing = tmp_path / "missing"
    existing = tmp_path / "exists"
    existing.mkdir()
    inputs = iter([str(missing), "n", str(existing)])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))
    p = cli_utils.demander_save_file_path()
    assert p == existing.resolve()


def test_demander_youtube_link_file(monkeypatch, tmp_path):
    links_file = tmp_path / "links.txt"
    links_file.write_text(
        "https://www.youtube.com/watch?v=ok\ninvalid\nhttps://youtu.be/abc\n"
    )
    inputs = iter([str(links_file)])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))
    links = cli_utils.demander_youtube_link_file()
    assert links == [
        "https://www.youtube.com/watch?v=ok",
        "https://youtu.be/abc",
    ]


def test_ask_numeric_value_validation_error(monkeypatch):
    inputs = iter(["x", "y", "z"])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))
    with pytest.raises(ValidationError):
        cli_utils.ask_numeric_value(1, 2)


def test_ask_youtube_url_validation_error(monkeypatch):
    inputs = iter(["bad", "nope", "still"])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))
    with pytest.raises(ValidationError):
        cli_utils.ask_youtube_url()
