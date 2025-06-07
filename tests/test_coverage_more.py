import builtins
import logging
from pathlib import Path
from types import SimpleNamespace

import pytest

from program_youtube_downloader import (
    cli_utils,
    progress,
    validators,
    youtube_downloader,
)
import program_youtube_downloader.main as main_module


def test_progress_bar_complete(capsys):
    opts = progress.ProgressOptions(
        size=10,
        sides="[]",
        full="#",
        empty="-",
        prefix_start="",
        prefix_end="",
        color_text="",
        color_Downloading="",
        color_Download_OK="",
    )
    progress.progress_bar(100, opts)
    out = capsys.readouterr().out
    assert "[##########]" in out
    assert "100.00%" in out


def test_on_download_progress_wrapper(monkeypatch):
    called = {}

    def fake(self, stream, chunk, remaining):
        called["ok"] = True

    monkeypatch.setattr(progress.ProgressBarHandler, "on_progress", fake)
    progress.on_download_progress(None, None, 0)
    assert called.get("ok")


def test_validate_youtube_url_empty():
    assert validators.validate_youtube_url("") is False


def test_clear_screen_windows(monkeypatch):
    called = {}
    monkeypatch.setattr(youtube_downloader.os, "name", "nt", raising=False)

    def fake_run(args, **kwargs):
        called["args"] = list(args)
        called.update(kwargs)

    monkeypatch.setattr(youtube_downloader.subprocess, "run", fake_run)
    youtube_downloader.clear_screen()
    assert called["args"] == ["cls"]
    assert called.get("shell") is True
    assert called.get("check") is True


def test_ask_save_file_path_file(monkeypatch, tmp_path):
    file_p = tmp_path / "file.txt"
    file_p.write_text("x")
    inputs = iter([str(file_p)])
    monkeypatch.setattr(builtins, "input", lambda *a, **k: next(inputs))
    result = cli_utils.ask_save_file_path()
    assert result == tmp_path.resolve()


def test_ask_save_file_path_mkdir_error(monkeypatch, tmp_path):
    new_dir = tmp_path / "newdir"
    inputs = iter([str(new_dir), "y", str(tmp_path)])
    monkeypatch.setattr(builtins, "input", lambda *a, **k: next(inputs))
    orig = Path.mkdir

    def failing(self, *a, **k):
        if failing.calls == 0:
            failing.calls += 1
            raise OSError()
        return orig(self, *a, **k)

    failing.calls = 0
    monkeypatch.setattr(Path, "mkdir", failing)
    result = cli_utils.ask_save_file_path()
    assert result == tmp_path.resolve()


def test_ask_youtube_link_file_all_invalid(monkeypatch, tmp_path):
    bad = tmp_path / "bad.txt"
    bad.write_text("not_a_url\n")
    good = tmp_path / "good.txt"
    good.write_text("https://youtu.be/ok\n")
    inputs = iter([str(bad), str(good)])
    monkeypatch.setattr(builtins, "input", lambda *a, **k: next(inputs))
    links = cli_utils.ask_youtube_link_file()
    assert links == ["https://youtu.be/ok"]


def test_ask_youtube_link_file_oserror(monkeypatch, tmp_path):
    bad = tmp_path / "bad.txt"
    inputs = iter([str(bad), str(bad), str(bad)])
    monkeypatch.setattr(builtins, "input", lambda *a, **k: next(inputs))
    monkeypatch.setattr(
        Path, "open", lambda self, *a, **k: (_ for _ in ()).throw(OSError())
    )
    with pytest.raises(cli_utils.ValidationError):
        cli_utils.ask_youtube_link_file()


def test_print_end_download_message(caplog):
    caplog.set_level(logging.INFO)
    cli_utils.print_end_download_message()
    assert "Fin du téléchargement" in caplog.text


def test_pause_return_to_menu(monkeypatch):
    called = {}
    monkeypatch.setattr(builtins, "input", lambda *a, **k: "")
    monkeypatch.setattr(
        cli_utils, "program_break_time", lambda t, m: called.setdefault("break", (t, m))
    )
    monkeypatch.setattr(
        cli_utils, "clear_screen", lambda: called.setdefault("clear", True)
    )
    cli_utils.pause_return_to_menu()
    assert called["break"] == (3, "Le menu d'accueil va revenir dans")
    assert called["clear"] is True


class DummyDownloader:
    def __init__(self):
        self.called = None

    def download_multiple_videos(self, urls, options):
        self.called = (list(urls), options)


def test_create_download_options(monkeypatch, tmp_path):
    monkeypatch.setattr(
        main_module.cli_utils, "ask_save_file_path", lambda: tmp_path
    )
    monkeypatch.setattr(
        main_module.cli_utils,
        "ask_resolution_or_bitrate",
        lambda *a, **k: 99,
    )
    opt = main_module.create_download_options(True)
    assert opt.save_path == tmp_path
    assert opt.download_sound_only is True
    assert (
        opt.choice_callback
        is main_module.cli_utils.ask_resolution_or_bitrate
    )


def test_main_video_command(monkeypatch, tmp_path):
    dd = DummyDownloader()
    monkeypatch.setattr(
        main_module.cli_utils, "ask_save_file_path", lambda: tmp_path
    )
    monkeypatch.setattr(
        main_module.cli_utils,
        "ask_resolution_or_bitrate",
        lambda *a, **k: 1,
    )
    main_module.main(["video", "https://youtu.be/x"], dd)
    assert dd.called[0] == ["https://youtu.be/x"]
    assert dd.called[1].save_path == tmp_path
    assert dd.called[1].download_sound_only is False


def test_main_playlist_command(monkeypatch, tmp_path):
    dd = DummyDownloader()
    monkeypatch.setattr(
        main_module.youtube_downloader, "Playlist", lambda u: ["https://youtu.be/1"]
    )
    monkeypatch.setattr(
        main_module.cli_utils, "ask_save_file_path", lambda: tmp_path
    )
    monkeypatch.setattr(
        main_module.cli_utils,
        "ask_resolution_or_bitrate",
        lambda *a, **k: 1,
    )
    main_module.main(["playlist", "https://example.com/playlist"], dd)
    assert dd.called[0] == ["https://youtu.be/1"]
    assert dd.called[1].save_path == tmp_path


def test_main_channel_command(monkeypatch, tmp_path):
    dd = DummyDownloader()
    monkeypatch.setattr(
        main_module.youtube_downloader, "Channel", lambda u: ["https://youtu.be/2"]
    )
    monkeypatch.setattr(
        main_module.cli_utils, "ask_save_file_path", lambda: tmp_path
    )
    monkeypatch.setattr(
        main_module.cli_utils,
        "ask_resolution_or_bitrate",
        lambda *a, **k: 1,
    )
    main_module.main(["channel", "https://example.com/channel"], dd)
    assert dd.called[0] == ["https://youtu.be/2"]


def test_main_menu_invocation(monkeypatch):
    called = {}
    monkeypatch.setattr(main_module, "menu", lambda: called.setdefault("menu", True))
    monkeypatch.setattr(main_module, "YoutubeDownloader", lambda: DummyDownloader())
    main_module.main(["menu"])
    assert called.get("menu")


def test_main_unknown_command():
    with pytest.raises(SystemExit):
        main_module.main(["unknown"])
