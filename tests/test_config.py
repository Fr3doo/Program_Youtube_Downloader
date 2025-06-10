from pathlib import Path

from program_youtube_downloader.config import DownloadOptions


def test_max_workers_env(monkeypatch):
    monkeypatch.setenv("PYDL_MAX_WORKERS", "3")
    opts = DownloadOptions()
    assert opts.max_workers == 3


def test_max_workers_env_invalid(monkeypatch):
    monkeypatch.setenv("PYDL_MAX_WORKERS", "foo")
    opts = DownloadOptions()
    assert opts.max_workers == 1


def test_max_workers_env_default(monkeypatch):
    monkeypatch.delenv("PYDL_MAX_WORKERS", raising=False)
    opts = DownloadOptions()
    assert opts.max_workers == 1


def test_output_dir_env(monkeypatch, tmp_path):
    monkeypatch.setenv("PYDL_OUTPUT_DIR", str(tmp_path))
    opts = DownloadOptions()
    assert opts.save_path == tmp_path.resolve()


def test_output_dir_override(monkeypatch, tmp_path):
    monkeypatch.setenv("PYDL_OUTPUT_DIR", str(tmp_path / "env"))
    opts = DownloadOptions(save_path=tmp_path)
    assert opts.save_path == tmp_path


def test_audio_only_env(monkeypatch):
    monkeypatch.setenv("PYDL_AUDIO_ONLY", "1")
    opts = DownloadOptions()
    assert opts.download_sound_only is True


def test_audio_only_default(monkeypatch):
    monkeypatch.delenv("PYDL_AUDIO_ONLY", raising=False)
    opts = DownloadOptions()
    assert opts.download_sound_only is False
