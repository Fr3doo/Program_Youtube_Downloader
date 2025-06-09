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
