import logging
from pathlib import Path
import pytest

from program_youtube_downloader.downloader import YoutubeDownloader
from program_youtube_downloader.config import DownloadOptions
from program_youtube_downloader.exceptions import DownloadError
from program_youtube_downloader.types import YouTubeVideo
from program_youtube_downloader import cli_utils


class DummyStream:
    def __init__(self, name: str) -> None:
        self.itag = 1
        self.resolution = "360p"
        self.abr = "128kbps"
        self.default_filename = f"{name}.mp4"

    def download(self, output_path: str) -> str:
        p = Path(output_path) / self.default_filename
        p.write_text("data")
        return str(p)


class DummyStreams(list):
    def get_by_itag(self, itag: int) -> DummyStream:
        return self[0]


class DummyYT(YouTubeVideo):
    def __init__(self, url: str) -> None:
        self.url = url
        name = url.split("/")[-1]
        self.streams = DummyStreams([DummyStream(name)])
        self._title = "video"
        self.progress = None

    @property
    def title(self):
        return self._title

    def register_on_progress_callback(self, cb) -> None:
        self.progress = cb


def fake_constructor(url: str) -> DummyYT:
    return DummyYT(url)


@pytest.fixture(autouse=True)
def patch_cli(monkeypatch):
    monkeypatch.setattr(cli_utils, "print_end_download_message", lambda *a, **k: None)
    monkeypatch.setattr(cli_utils, "pause_return_to_menu", lambda *a, **k: None)


def test_parallel_success(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(YoutubeDownloader, "get_video_streams", lambda self, dso, yt: yt.streams)
    yd = YoutubeDownloader(youtube_cls=fake_constructor)
    options = DownloadOptions(save_path=tmp_path, max_workers=2)
    urls = ["https://youtu.be/a", "https://youtu.be/b"]
    yd.download_multiple_videos(urls, options)
    for name in ["a.mp4", "b.mp4"]:
        assert (tmp_path / name).exists()


def test_parallel_error_collection(monkeypatch, tmp_path: Path, caplog):
    monkeypatch.setattr(YoutubeDownloader, "get_video_streams", lambda self, dso, yt: yt.streams)

    def failing(self, stream, path, url, sound_only):
        if url.endswith("b"):
            raise DownloadError("boom")
        Path(path / stream.default_filename).write_text("ok")

    monkeypatch.setattr(YoutubeDownloader, "_download_stream", failing)
    yd = YoutubeDownloader(youtube_cls=fake_constructor)
    options = DownloadOptions(save_path=tmp_path, max_workers=2)
    urls = ["https://youtu.be/a", "https://youtu.be/b"]
    with caplog.at_level(logging.ERROR):
        yd.download_multiple_videos(urls, options)
    assert "https://youtu.be/b" in caplog.text
    assert (tmp_path / "a.mp4").exists()
    assert not (tmp_path / "b.mp4").exists()


def test_end_message_skipped_on_error(monkeypatch, tmp_path: Path):
    """The end download message should not be printed when errors occur."""

    monkeypatch.setattr(YoutubeDownloader, "get_video_streams", lambda self, dso, yt: yt.streams)

    def failing(self, stream, path, url, sound_only):
        if url.endswith("b"):
            raise DownloadError("boom")
        Path(path / stream.default_filename).write_text("ok")

    monkeypatch.setattr(YoutubeDownloader, "_download_stream", failing)

    called = {}

    def end_message() -> None:
        called["printed"] = True

    monkeypatch.setattr(cli_utils, "print_end_download_message", end_message)
    monkeypatch.setattr(cli_utils, "pause_return_to_menu", lambda *a, **k: None)

    yd = YoutubeDownloader(youtube_cls=fake_constructor)
    options = DownloadOptions(save_path=tmp_path, max_workers=2)
    urls = ["https://youtu.be/a", "https://youtu.be/b"]
    yd.download_multiple_videos(urls, options)

    assert "printed" not in called
