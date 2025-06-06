from pathlib import Path
from program_youtube_downloader import downloader as downloader_module
from program_youtube_downloader.downloader import YoutubeDownloader
from program_youtube_downloader.config import DownloadOptions

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

class DummyYT:
    def __init__(self, url: str) -> None:
        self.url = url
        self.title = "video"
        self.streams: DummyStreams = DummyStreams([DummyStream()])
        self.progress = None

    def register_on_progress_callback(self, cb) -> None:
        self.progress = cb

class DummyHandler:
    called = False

    def on_progress(self, stream, chunk, bytes_remaining) -> None:
        self.called = True


def test_download_multiple_videos_custom_callbacks(monkeypatch, tmp_path: Path) -> None:
    created = {}

    def fake_constructor(url: str) -> DummyYT:
        yt = DummyYT(url)
        created['yt'] = yt
        return yt

    monkeypatch.setattr(downloader_module, "YouTube", fake_constructor)
    monkeypatch.setattr(YoutubeDownloader, "streams_video", lambda self, dso, yt: yt.streams)
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")
    monkeypatch.setattr(downloader_module, "program_break_time", lambda *a, **k: None)
    monkeypatch.setattr(downloader_module, "clear_screen", lambda *a, **k: None)

    called = {}

    def choice_cb(sound_only: bool, streams) -> int:
        called['choice'] = True
        return 1

    progress = DummyHandler()
    yd = YoutubeDownloader(progress_handler=progress)
    options = DownloadOptions(
        save_path=tmp_path,
        download_sound_only=False,
        choice_callback=choice_cb,
    )
    yd.download_multiple_videos([
        "https://youtu.be/dummy"
    ], options)

    assert (tmp_path / "sample.mp4").exists()
    assert created['yt'].progress.__self__ is progress
    assert called['choice']


def test_download_multiple_videos_instantiation_error(monkeypatch, tmp_path: Path) -> None:
    """YouTube constructor failure should be handled gracefully."""

    def fake_constructor(url: str) -> DummyYT:
        raise KeyError("boom")

    monkeypatch.setattr(downloader_module, "YouTube", fake_constructor)
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")
    monkeypatch.setattr(downloader_module, "program_break_time", lambda *a, **k: None)
    monkeypatch.setattr(downloader_module, "clear_screen", lambda *a, **k: None)

    progress = DummyHandler()
    yd = YoutubeDownloader(progress_handler=progress)
    options = DownloadOptions(
        save_path=tmp_path,
        download_sound_only=False,
    )
    yd.download_multiple_videos([
        "https://youtu.be/fail"
    ], options)

    assert not any(tmp_path.iterdir())
    assert not progress.called


def test_download_multiple_videos_no_streams(monkeypatch, tmp_path: Path) -> None:
    """When no streams are returned, nothing should be downloaded."""

    def fake_constructor(url: str) -> DummyYT:
        return DummyYT(url)

    monkeypatch.setattr(downloader_module, "YouTube", fake_constructor)
    monkeypatch.setattr(YoutubeDownloader, "streams_video", lambda self, dso, yt: None)
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")
    monkeypatch.setattr(downloader_module, "program_break_time", lambda *a, **k: None)
    monkeypatch.setattr(downloader_module, "clear_screen", lambda *a, **k: None)

    progress = DummyHandler()
    yd = YoutubeDownloader(progress_handler=progress)
    options = DownloadOptions(
        save_path=tmp_path,
        download_sound_only=False,
    )
    yd.download_multiple_videos([
        "https://youtu.be/nostreams"
    ], options)

    assert not any(tmp_path.iterdir())
    assert not progress.called
