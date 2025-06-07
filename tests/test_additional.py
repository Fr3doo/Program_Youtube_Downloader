import os
import builtins
from pathlib import Path
from types import SimpleNamespace
from urllib.error import HTTPError

import pytest

from program_youtube_downloader import cli_utils, youtube_downloader
from program_youtube_downloader.downloader import YoutubeDownloader
from program_youtube_downloader.exceptions import DownloadError
from program_youtube_downloader.config import DownloadOptions
from program_youtube_downloader.progress import progress_bar, ProgressBarHandler
from program_youtube_downloader import constants


# Helper dummy classes reused across tests
class DummyStream:
    def __init__(self):
        self.itag = 1
        self.resolution = "360p"
        self.abr = "128kbps"
        self.default_filename = "sample.mp4"
        self.filesize = 1000

    def download(self, output_path: str) -> str:
        p = Path(output_path) / self.default_filename
        p.write_text("data")
        return str(p)


class DummyStreams(list):
    def get_by_itag(self, itag: int) -> DummyStream:  # pragma: no cover - simple helper
        return self[0]


class DummyYT:
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


# ---------------------------------------------------------------------------
# CLI utility helpers
# ---------------------------------------------------------------------------

def test_afficher_menu_acceuil_count(monkeypatch):
    """The menu should display all choices and return their count."""
    printed = []
    monkeypatch.setattr(builtins, "print", lambda *a, **k: printed.append(a))
    count = cli_utils.afficher_menu_acceuil()
    assert count == len(constants.MenuOption)
    assert any("1 -" in " ".join(map(str, args)) for args in printed)


def test_demander_choice_resolution_audio(monkeypatch):
    """Selection of audio bitrate should delegate range checking."""
    streams = [SimpleNamespace(abr="64k"), SimpleNamespace(abr="128k")]
    called = {}

    def fake_numeric(vmin, vmax):
        called["range"] = (vmin, vmax)
        return 2

    monkeypatch.setattr(cli_utils, "ask_numeric_value", fake_numeric)
    choice = cli_utils.demander_choice_resolution_vidéo_or_bitrate_audio(True, streams)
    assert choice == 2
    assert called["range"] == (1, len(streams))


def test_demander_choice_resolution_video(monkeypatch):
    """Video resolution flow mirrors the audio version."""
    streams = [SimpleNamespace(resolution="360p"), SimpleNamespace(resolution="720p")]
    monkeypatch.setattr(cli_utils, "ask_numeric_value", lambda a, b: 1)
    assert cli_utils.demander_choice_resolution_vidéo_or_bitrate_audio(False, streams) == 1


# ---------------------------------------------------------------------------
# Progress handling
# ---------------------------------------------------------------------------

def test_progress_bar_outputs(capsys):
    """Ensure the textual progress bar displays expected markers."""
    progress_bar(50, size=10, sides="[]", full="#", empty="-", prefix_start="", prefix_end="", color_text="", color_Downloading="", color_Download_OK="")
    out = capsys.readouterr().out
    assert "[#####-----]" in out
    assert "50.00%" in out


def test_progressbarhandler_on_progress(capsys):
    """The default handler should print the current percentage."""
    handler = ProgressBarHandler()
    stream = DummyStream()
    handler.on_progress(stream, b"", bytes_remaining=500)
    out = capsys.readouterr().out
    assert "50.00%" in out


# ---------------------------------------------------------------------------
# Small helpers from youtube_downloader module
# ---------------------------------------------------------------------------

def test_program_break_time(monkeypatch, capsys):
    """Countdown should print dots without sleeping when patched."""
    monkeypatch.setattr(youtube_downloader.time, "sleep", lambda x: None)
    youtube_downloader.program_break_time(3, "Wait")
    out = capsys.readouterr().out
    assert out.count(".") == 3
    assert "Wait 3 secondes" in out


def test_clear_screen(monkeypatch):
    """clear_screen should invoke subprocess.run with the proper command."""
    called = {}

    def fake_run(args, **kwargs):
        called["args"] = list(args)
        called.update(kwargs)

    monkeypatch.setattr(youtube_downloader.subprocess, "run", fake_run)
    youtube_downloader.clear_screen()
    expected = ["clear"] if os.name == "posix" else ["cls"]
    assert called["args"] == expected
    if os.name != "posix":
        assert called.get("shell") is True


# ---------------------------------------------------------------------------
# YoutubeDownloader specific behaviour
# ---------------------------------------------------------------------------

def test_streams_video_http_error(monkeypatch):
    """HTTP errors when accessing streams should return None."""
    yt = DummyYT("u")

    def filter_fail(*a, **k):
        raise HTTPError(url=None, code=404, msg="x", hdrs=None, fp=None)

    yt.streams.filter = filter_fail
    yd = YoutubeDownloader()
    assert yd.streams_video(False, yt) is None


def test_streams_video_success(monkeypatch):
    """Successful retrieval should return provided streams object."""
    yt = DummyYT("u")
    result = [1, 2, 3]

    class Chain:
        def filter(self, *a, **k):
            return self

        def order_by(self, *a, **k):
            return self

        def desc(self):
            return result

    yt.streams = Chain()
    yd = YoutubeDownloader()
    assert yd.streams_video(True, yt) is result


def test_conversion_mp4_in_mp3_rename_error(monkeypatch, tmp_path):
    """If renaming fails, the source file should be removed."""
    mp4 = tmp_path / "sample.mp4"
    mp4.write_text("x")

    def rename_fail(self, dst):
        raise OSError()

    monkeypatch.setattr(Path, "rename", rename_fail)
    yd = YoutubeDownloader()
    yd.conversion_mp4_in_mp3(mp4)
    assert not mp4.exists()
    assert not (tmp_path / "sample.mp3").exists()


def test_download_multiple_videos_title_keyerror(monkeypatch, tmp_path):
    """Videos whose title property fails are skipped."""

    class BadTitleYT(DummyYT):
        @property
        def title(self):
            raise KeyError("missing")

    monkeypatch.setattr(YoutubeDownloader, "streams_video", lambda self, dso, yt: yt.streams)
    monkeypatch.setattr(builtins, "input", lambda *a, **k: "")
    monkeypatch.setattr(cli_utils, "print_end_download_message", lambda *a, **k: None)
    monkeypatch.setattr(cli_utils, "pause_return_to_menu", lambda *a, **k: None)

    yd = YoutubeDownloader(youtube_cls=lambda u: BadTitleYT(u))
    options = DownloadOptions(save_path=tmp_path)
    yd.download_multiple_videos(["https://youtu.be/x"], options)
    assert not any(tmp_path.iterdir())


def test_download_multiple_videos_default_choice(monkeypatch, tmp_path):
    """When no callback is provided, the first stream is used."""
    monkeypatch.setattr(YoutubeDownloader, "streams_video", lambda self, dso, yt: yt.streams)
    monkeypatch.setattr(builtins, "input", lambda *a, **k: "")
    monkeypatch.setattr(cli_utils, "print_end_download_message", lambda *a, **k: None)
    monkeypatch.setattr(cli_utils, "pause_return_to_menu", lambda *a, **k: None)

    yd = YoutubeDownloader(youtube_cls=lambda u: DummyYT(u))
    options = DownloadOptions(save_path=tmp_path)
    yd.download_multiple_videos(["https://youtu.be/x"], options)

    assert (tmp_path / "sample.mp4").exists()


def test_download_multiple_videos_download_error(monkeypatch, tmp_path):
    class FailingStream(DummyStream):
        def download(self, output_path: str) -> str:
            raise OSError("boom")

    class FailYT(DummyYT):
        def __init__(self, url: str) -> None:
            super().__init__(url)
            self.streams = DummyStreams([FailingStream()])

    monkeypatch.setattr(YoutubeDownloader, "streams_video", lambda self, dso, yt: yt.streams)
    monkeypatch.setattr(builtins, "input", lambda *a, **k: "")
    monkeypatch.setattr(cli_utils, "print_end_download_message", lambda *a, **k: None)
    monkeypatch.setattr(cli_utils, "pause_return_to_menu", lambda *a, **k: None)

    yd = YoutubeDownloader(youtube_cls=lambda u: FailYT(u))
    options = DownloadOptions(save_path=tmp_path)
    with pytest.raises(DownloadError):
        yd.download_multiple_videos(["https://youtu.be/fail"], options)
