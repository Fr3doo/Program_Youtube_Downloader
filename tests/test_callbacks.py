from pathlib import Path
from program_youtube_downloader import downloader as downloader_module
from program_youtube_downloader.downloader import YoutubeDownloader

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

    def progress_cb(stream, chunk, bytes_remaining) -> None:
        called['progress'] = True

    yd = YoutubeDownloader()
    yd.download_multiple_videos([
        "https://youtu.be/dummy"
    ], False, save_path=tmp_path, choice_callback=choice_cb, progress_callback=progress_cb)

    assert (tmp_path / "sample.mp4").exists()
    assert created['yt'].progress is progress_cb
    assert called['choice']
