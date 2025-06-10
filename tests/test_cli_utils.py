import logging
import pytest
from pathlib import Path

from program_youtube_downloader import cli_utils


class DummyConsole:
    def __init__(self, inputs):
        self._iter = iter(inputs)

    def input(self, *args, **kwargs):
        return next(self._iter)

    def print(self, *args, **kwargs):
        pass
from program_youtube_downloader.exceptions import (
    ValidationError,
    DirectoryCreationError,
)

VALID_ID = "dQw4w9WgXcQ"


def test_ask_numeric_value_retries():
    console = DummyConsole(["foo", "5", "2"])
    value = cli_utils.ask_numeric_value(1, 3, console=console)
    assert value == 2


def test_ask_youtube_url_normalizes_channel():
    console = DummyConsole([
        "https://www.youtube.com/@MyChannel",
        f"https://www.youtube.com/watch?v={VALID_ID}",
    ])
    url = cli_utils.ask_youtube_url(console=console)
    assert url == f"https://www.youtube.com/watch?v={VALID_ID}"


def test_ask_youtube_url_invalid_prefix():
    console = DummyConsole([
        "http://example.com/video",
        f"https://www.youtube.com/watch?v={VALID_ID}",
    ])
    url = cli_utils.ask_youtube_url(console=console)
    assert url == f"https://www.youtube.com/watch?v={VALID_ID}"


def test_ask_youtube_url_invalid_then_valid():
    console = DummyConsole([
        "invalid",
        f"https://www.youtube.com/watch?v={VALID_ID}",
    ])
    url = cli_utils.ask_youtube_url(console=console)
    assert url == f"https://www.youtube.com/watch?v={VALID_ID}"


def test_ask_save_file_path_existing(tmp_path):
    console = DummyConsole([str(tmp_path)])
    p = cli_utils.ask_save_file_path(console=console)
    assert p == tmp_path.resolve()


def test_ask_save_file_path_create(tmp_path):
    new_dir = tmp_path / "newdir"
    console = DummyConsole([str(new_dir), "y"])
    p = cli_utils.ask_save_file_path(console=console)
    assert p == new_dir.resolve()
    assert new_dir.exists()


def test_ask_save_file_path_retry(tmp_path):
    missing = tmp_path / "missing"
    existing = tmp_path / "exists"
    existing.mkdir()
    console = DummyConsole([str(missing), "n", str(existing)])
    p = cli_utils.ask_save_file_path(console=console)
    assert p == existing.resolve()


def test_ask_save_file_path_mkdir_failure(tmp_path, caplog, monkeypatch):
    new_dir = tmp_path / "newdir"
    console = DummyConsole([str(new_dir), "y", str(tmp_path)])

    def fail_once(self, *a, **k):
        fail_once.calls += 1
        raise OSError("boom")

    fail_once.calls = 0
    monkeypatch.setattr(Path, "mkdir", fail_once)

    with caplog.at_level(logging.ERROR):
        result = cli_utils.ask_save_file_path(console=console)
    assert result == tmp_path.resolve()
    assert "Échec de la création du dossier" in caplog.text
    assert "boom" in caplog.text


def test_ask_save_file_path_dircreation_error(tmp_path, monkeypatch):
    missing = tmp_path / "missing"
    console = DummyConsole([str(missing), "y", str(missing), "y"])

    def always_fail(self, *a, **k):
        raise OSError()

    monkeypatch.setattr(Path, "mkdir", always_fail)

    with pytest.raises(DirectoryCreationError):
        cli_utils.ask_save_file_path(max_attempts=2, console=console)


def test_ask_save_file_path_missing_after_creation(tmp_path, monkeypatch):
    missing = tmp_path / "missing"
    console = DummyConsole([str(missing), "y", str(missing), "y"])

    def fake_mkdir(self, *a, **k):
        pass

    orig_exists = Path.exists

    def fake_exists(self):
        if self == missing:
            return False
        return orig_exists(self)

    monkeypatch.setattr(Path, "mkdir", fake_mkdir)
    monkeypatch.setattr(Path, "exists", fake_exists)

    with pytest.raises(DirectoryCreationError):
        cli_utils.ask_save_file_path(max_attempts=2, console=console)


def test_ask_youtube_link_file(tmp_path):
    links_file = tmp_path / "links.txt"
    links_file.write_text(
        f"https://www.youtube.com/watch?v={VALID_ID}\ninvalid\nhttps://youtu.be/{VALID_ID}\n"
    )
    console = DummyConsole([str(links_file)])
    links = cli_utils.ask_youtube_link_file(console=console)
    assert links == [
        f"https://www.youtube.com/watch?v={VALID_ID}",
        f"https://youtu.be/{VALID_ID}",
    ]


def test_ask_numeric_value_validation_error():
    console = DummyConsole(["x", "y", "z"])
    with pytest.raises(ValidationError):
        cli_utils.ask_numeric_value(1, 2, console=console)


def test_ask_youtube_url_validation_error():
    console = DummyConsole(["bad", "nope", "still"])
    with pytest.raises(ValidationError):
        cli_utils.ask_youtube_url(console=console)
