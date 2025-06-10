import logging
import pytest
from pathlib import Path

from program_youtube_downloader import cli_utils
from program_youtube_downloader.exceptions import (
    ValidationError,
    DirectoryCreationError,
)

VALID_ID = "dQw4w9WgXcQ"


def test_ask_numeric_value_retries(monkeypatch):
    inputs = iter(["foo", "5", "2"])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))
    value = cli_utils.ask_numeric_value(1, 3)
    assert value == 2


def test_ask_youtube_url_normalizes_channel(monkeypatch):
    inputs = iter([
        "https://www.youtube.com/@MyChannel",
        f"https://www.youtube.com/watch?v={VALID_ID}",
    ])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))
    url = cli_utils.ask_youtube_url()
    assert url == f"https://www.youtube.com/watch?v={VALID_ID}"


def test_ask_youtube_url_invalid_prefix(monkeypatch):
    inputs = iter([
        "http://example.com/video",
        f"https://www.youtube.com/watch?v={VALID_ID}",
    ])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))
    url = cli_utils.ask_youtube_url()
    assert url == f"https://www.youtube.com/watch?v={VALID_ID}"


def test_ask_youtube_url_invalid_then_valid(monkeypatch):
    inputs = iter([
        "invalid",
        f"https://www.youtube.com/watch?v={VALID_ID}",
    ])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))
    url = cli_utils.ask_youtube_url()
    assert url == f"https://www.youtube.com/watch?v={VALID_ID}"


def test_ask_save_file_path_existing(tmp_path, monkeypatch):
    inputs = iter([str(tmp_path)])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))
    p = cli_utils.ask_save_file_path()
    assert p == tmp_path.resolve()


def test_ask_save_file_path_create(tmp_path, monkeypatch):
    new_dir = tmp_path / "newdir"
    inputs = iter([str(new_dir), "y"])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))
    p = cli_utils.ask_save_file_path()
    assert p == new_dir.resolve()
    assert new_dir.exists()


def test_ask_save_file_path_retry(monkeypatch, tmp_path):
    missing = tmp_path / "missing"
    existing = tmp_path / "exists"
    existing.mkdir()
    inputs = iter([str(missing), "n", str(existing)])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))
    p = cli_utils.ask_save_file_path()
    assert p == existing.resolve()


def test_ask_save_file_path_mkdir_failure(monkeypatch, tmp_path, caplog):
    new_dir = tmp_path / "newdir"
    inputs = iter([str(new_dir), "y", str(tmp_path)])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))

    def fail_once(self, *a, **k):
        fail_once.calls += 1
        raise OSError()

    fail_once.calls = 0
    monkeypatch.setattr(Path, "mkdir", fail_once)

    with caplog.at_level(logging.ERROR):
        result = cli_utils.ask_save_file_path()
    assert result == tmp_path.resolve()
    assert "Échec de la création du dossier" in caplog.text


def test_ask_save_file_path_dircreation_error(monkeypatch, tmp_path):
    missing = tmp_path / "missing"
    inputs = iter([str(missing), "y", str(missing), "y"])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))

    def always_fail(self, *a, **k):
        raise OSError()

    monkeypatch.setattr(Path, "mkdir", always_fail)

    with pytest.raises(DirectoryCreationError):
        cli_utils.ask_save_file_path(max_attempts=2)


def test_ask_youtube_link_file(monkeypatch, tmp_path):
    links_file = tmp_path / "links.txt"
    links_file.write_text(
        f"https://www.youtube.com/watch?v={VALID_ID}\ninvalid\nhttps://youtu.be/{VALID_ID}\n"
    )
    inputs = iter([str(links_file)])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))
    links = cli_utils.ask_youtube_link_file()
    assert links == [
        f"https://www.youtube.com/watch?v={VALID_ID}",
        f"https://youtu.be/{VALID_ID}",
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
