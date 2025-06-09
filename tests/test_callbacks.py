from pathlib import Path
import logging
from concurrent.futures import Future
from typing import Any
import pytest
from program_youtube_downloader import downloader as downloader_module
from program_youtube_downloader import cli_utils
from program_youtube_downloader.downloader import YoutubeDownloader
from program_youtube_downloader.config import DownloadOptions
from program_youtube_downloader.exceptions import DownloadError
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
        self._title = "video"
        self.streams: DummyStreams = DummyStreams([DummyStream()])
        self.progress = None

    @property
    def title(self):
        return self._title

    def register_on_progress_callback(self, cb) -> None:
        self.progress = cb

class DummyHandler:
    called = False

    def on_progress(self, stream, chunk, bytes_remaining) -> None:
        self.called = True


def test_create_youtube_registers_progress(monkeypatch) -> None:
    created = {}

    def fake_constructor(url: str) -> DummyYT:
        yt = DummyYT(url)
        created['yt'] = yt
        return yt

    progress = DummyHandler()
    yd = YoutubeDownloader(progress_handler=progress, youtube_cls=fake_constructor)

    yt = yd._create_youtube("https://youtu.be/x", progress)

    assert yt is created['yt']
    assert created['yt'].progress.__self__ is progress


def test_choose_stream_uses_callback() -> None:
    called = {}

    def cb(sound_only: bool, streams: list[int]) -> int:
        called['args'] = (sound_only, streams)
        return 2

    yd = YoutubeDownloader()
    result = yd._choose_stream(True, [1, 2], cb)

    assert result == 2
    assert called['args'] == (True, [1, 2])


def test_download_stream_error(monkeypatch, tmp_path: Path) -> None:
    class FailStream(DummyStream):
        def download(self, output_path: str) -> str:
            raise OSError("boom")

    stream = FailStream()
    yd = YoutubeDownloader()

    with pytest.raises(DownloadError):
        yd._download_stream(stream, tmp_path, "https://youtu.be/fail", False)


def test_process_url_success(monkeypatch) -> None:
    monkeypatch.setattr(
        YoutubeDownloader, "get_video_streams", lambda self, dso, yt: yt.streams
    )
    progress = DummyHandler()
    yd = YoutubeDownloader(progress_handler=progress, youtube_cls=lambda u: DummyYT(u))

    result = yd._process_url("https://youtu.be/x", False, progress)

    assert result is not None
    streams, yt, title = result
    assert streams is yt.streams
    assert title == "video"
    assert yt.progress.__self__ is progress


def test_submit_download(monkeypatch, tmp_path: Path) -> None:
    called = {}

    def fake_download(stream, path, url, sound_only):
        called["args"] = (stream, path, url, sound_only)

    yd = YoutubeDownloader()
    monkeypatch.setattr(yd, "_download_stream", fake_download)

    class DummyExecutor:
        def __init__(self) -> None:
            self.submitted = None

        def submit(self, func, *args):
            self.submitted = (func, args)
            fut = Future()
            try:
                result = func(*args)
                fut.set_result(result)
            except Exception as e:  # pragma: no cover - defensive
                fut.set_exception(e)
            return fut

    exec = DummyExecutor()
    futures: dict[Any, str] = {}
    stream = DummyStream()
    yd._submit_download(exec, stream, tmp_path, "https://youtu.be/x", True, futures)

    func, args = exec.submitted
    assert func is fake_download
    assert futures and list(futures.values()) == ["https://youtu.be/x"]
    assert called["args"] == (stream, tmp_path, "https://youtu.be/x", True)


def test_report_errors(monkeypatch, caplog) -> None:
    f_ok = Future()
    f_ok.set_result(None)
    f_err = Future()
    f_err.set_exception(DownloadError("boom"))
    futures = {f_ok: "https://youtu.be/a", f_err: "https://youtu.be/b"}

    called = {}
    monkeypatch.setattr(cli_utils, "print_end_download_message", lambda *a, **k: called.setdefault("end", True))
    monkeypatch.setattr(cli_utils, "pause_return_to_menu", lambda *a, **k: called.setdefault("pause", True))

    yd = YoutubeDownloader()
    with caplog.at_level(logging.ERROR):
        yd._report_errors(futures)

    assert "https://youtu.be/b" in caplog.text
    assert "end" not in called
    assert "pause" in called


def test_download_multiple_videos_custom_callbacks(monkeypatch, tmp_path: Path) -> None:
    created = {}

    def fake_constructor(url: str) -> DummyYT:
        yt = DummyYT(url)
        created['yt'] = yt
        return yt

    monkeypatch.setattr(YoutubeDownloader, "get_video_streams", lambda self, dso, yt: yt.streams)
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")
    monkeypatch.setattr(cli_utils, "print_end_download_message", lambda *a, **k: None)
    monkeypatch.setattr(cli_utils, "pause_return_to_menu", lambda *a, **k: None)

    called = {}

    def choice_cb(sound_only: bool, streams) -> int:
        called['choice'] = True
        return 1

    progress = DummyHandler()
    yd = YoutubeDownloader(progress_handler=progress, youtube_cls=fake_constructor)
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

    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")
    monkeypatch.setattr(cli_utils, "print_end_download_message", lambda *a, **k: None)
    monkeypatch.setattr(cli_utils, "pause_return_to_menu", lambda *a, **k: None)

    progress = DummyHandler()
    yd = YoutubeDownloader(progress_handler=progress, youtube_cls=fake_constructor)
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

    monkeypatch.setattr(YoutubeDownloader, "get_video_streams", lambda self, dso, yt: [])
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")
    monkeypatch.setattr(cli_utils, "print_end_download_message", lambda *a, **k: None)
    monkeypatch.setattr(cli_utils, "pause_return_to_menu", lambda *a, **k: None)

    progress = DummyHandler()
    yd = YoutubeDownloader(progress_handler=progress, youtube_cls=fake_constructor)
    options = DownloadOptions(
        save_path=tmp_path,
        download_sound_only=False,
    )
    yd.download_multiple_videos([
        "https://youtu.be/nostreams"
    ], options)

    assert not any(tmp_path.iterdir())
    assert not progress.called


def test_download_multiple_videos_constructor_exception(monkeypatch, tmp_path: Path) -> None:
    """Generic constructor exceptions should be ignored."""

    def fake_constructor(url: str) -> DummyYT:
        raise RuntimeError("boom")

    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")
    monkeypatch.setattr(cli_utils, "print_end_download_message", lambda *a, **k: None)
    monkeypatch.setattr(cli_utils, "pause_return_to_menu", lambda *a, **k: None)

    progress = DummyHandler()
    yd = YoutubeDownloader(progress_handler=progress, youtube_cls=fake_constructor)
    options = DownloadOptions(
        save_path=tmp_path,
        download_sound_only=False,
    )
    yd.download_multiple_videos([
        "https://youtu.be/boom",
    ], options)

    assert not any(tmp_path.iterdir())
    assert not progress.called


def test_download_multiple_videos_streams_error(monkeypatch, tmp_path: Path) -> None:
    """HTTPError during stream retrieval should skip download."""

    class FailingStreams:
        def filter(self, *a, **k):
            raise HTTPError(url="u", code=404, msg="x", hdrs=None, fp=None)

    def fake_constructor(url: str) -> DummyYT:
        yt = DummyYT(url)
        yt.streams = FailingStreams()
        return yt

    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")
    monkeypatch.setattr(cli_utils, "print_end_download_message", lambda *a, **k: None)
    monkeypatch.setattr(cli_utils, "pause_return_to_menu", lambda *a, **k: None)

    progress = DummyHandler()
    yd = YoutubeDownloader(progress_handler=progress, youtube_cls=fake_constructor)
    options = DownloadOptions(
        save_path=tmp_path,
        download_sound_only=False,
    )
    yd.download_multiple_videos([
        "https://youtu.be/error",
    ], options)

    assert not any(tmp_path.iterdir())
    assert not progress.called


def test_download_multiple_videos_download_error(monkeypatch, tmp_path: Path, caplog) -> None:
    class FailingStream(DummyStream):
        def download(self, output_path: str) -> str:
            raise OSError("boom")

    class FailYT(DummyYT):
        def __init__(self, url: str) -> None:
            super().__init__(url)
            self.streams = DummyStreams([FailingStream()])

    def fake_constructor(url: str) -> DummyYT:
        return FailYT(url)

    monkeypatch.setattr(YoutubeDownloader, "get_video_streams", lambda self, dso, yt: yt.streams)
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")
    monkeypatch.setattr(cli_utils, "print_end_download_message", lambda *a, **k: None)
    monkeypatch.setattr(cli_utils, "pause_return_to_menu", lambda *a, **k: None)

    yd = YoutubeDownloader(youtube_cls=fake_constructor)
    options = DownloadOptions(save_path=tmp_path)
    with caplog.at_level(logging.ERROR):
        yd.download_multiple_videos(["https://youtu.be/fail"], options)
    assert "https://youtu.be/fail" in caplog.text
    assert not any(tmp_path.iterdir())


def test_download_multiple_videos_custom_progress(monkeypatch, tmp_path: Path) -> None:
    """A custom progress handler can be injected via DownloadOptions."""

    created = {}

    def fake_constructor(url: str) -> DummyYT:
        yt = DummyYT(url)
        created["yt"] = yt
        return yt

    class SimpleHandler:
        def __init__(self) -> None:
            self.called = False

        def on_progress(self, stream, chunk, bytes_remaining) -> None:
            self.called = True

    handler = SimpleHandler()

    monkeypatch.setattr(YoutubeDownloader, "get_video_streams", lambda self, dso, yt: yt.streams)
    monkeypatch.setattr("builtins.input", lambda *a, **k: "")
    monkeypatch.setattr(cli_utils, "print_end_download_message", lambda *a, **k: None)
    monkeypatch.setattr(cli_utils, "pause_return_to_menu", lambda *a, **k: None)

    yd = YoutubeDownloader(youtube_cls=fake_constructor)
    options = DownloadOptions(save_path=tmp_path, progress_handler=handler)

    yd.download_multiple_videos(["https://youtu.be/x"], options)

    assert (tmp_path / "sample.mp4").exists()
    assert created["yt"].progress.__self__ is handler
