from pathlib import Path

from program_youtube_downloader.downloader import YoutubeDownloader
from program_youtube_downloader.config import DownloadOptions
from program_youtube_downloader import cli_utils
from program_youtube_downloader.types import YouTubeVideo

class DummyStream:
    itag = 1
    resolution = "360p"
    abr = "128kbps"
    default_filename = "sample.mp4"

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
        self.streams: DummyStreams = DummyStreams([DummyStream()])
        self.progress = None
        self._title = "video"

    @property
    def title(self):
        return self._title

    def register_on_progress_callback(self, cb) -> None:
        self.progress = cb

class Recorder:
    def __init__(self) -> None:
        self.called = False

    def on_progress(self, event) -> None:
        self.called = True


def test_constructor_custom_progress(monkeypatch, tmp_path: Path) -> None:
    created = {}

    def fake_constructor(url: str) -> DummyYT:
        yt = DummyYT(url)
        created["yt"] = yt
        return yt

    monkeypatch.setattr(YoutubeDownloader, "get_video_streams", lambda self, dso, yt: yt.streams)
    monkeypatch.setattr("builtins.input", lambda *a, **k: "")
    monkeypatch.setattr(cli_utils, "print_end_download_message", lambda *a, **k: None)
    monkeypatch.setattr(cli_utils, "pause_return_to_menu", lambda *a, **k: None)

    handler = Recorder()
    yd = YoutubeDownloader(progress_handler=handler, youtube_cls=fake_constructor)
    options = DownloadOptions(save_path=tmp_path)

    yd.download_multiple_videos(["https://youtu.be/x"], options)

    assert (tmp_path / "sample.mp4").exists()
    assert callable(created["yt"].progress)
    created["yt"].progress(None, None, 0)
    assert handler.called
