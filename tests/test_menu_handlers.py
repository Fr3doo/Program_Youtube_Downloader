import logging
import pytest

import program_youtube_downloader.cli as cli_module
from program_youtube_downloader.config import DownloadOptions


class DummyDownloader:
    def __init__(self):
        self.called = None

    def download_multiple_videos(self, urls, options):
        self.called = (list(urls), options)


def test_handle_video_option(monkeypatch, tmp_path):
    dd = DummyDownloader()
    monkeypatch.setattr(cli_module.cli_utils, "ask_youtube_url", lambda: "https://youtu.be/x")
    monkeypatch.setattr(cli_module.CLI, "create_download_options", lambda self, ao: DownloadOptions(save_path=tmp_path, download_sound_only=ao))
    cli = cli_module.CLI(dd)
    cli.handle_video_option(True)
    assert dd.called[0] == ["https://youtu.be/x"]
    assert dd.called[1].download_sound_only is True


def test_handle_videos_option(monkeypatch, tmp_path):
    dd = DummyDownloader()
    monkeypatch.setattr(cli_module.cli_utils, "ask_youtube_link_file", lambda: ["https://youtu.be/a", "https://youtu.be/b"])
    monkeypatch.setattr(cli_module.CLI, "create_download_options", lambda self, ao: DownloadOptions(save_path=tmp_path, download_sound_only=ao))
    cli = cli_module.CLI(dd)
    cli.handle_videos_option(False)
    assert dd.called[0] == ["https://youtu.be/a", "https://youtu.be/b"]
    assert dd.called[1].download_sound_only is False


def test_handle_playlist_option(monkeypatch, tmp_path):
    dd = DummyDownloader()
    monkeypatch.setattr(cli_module.cli_utils, "ask_youtube_url", lambda: "https://youtube.com/playlist")
    monkeypatch.setattr(cli_module.CLI, "load_playlist", lambda self, url: ["v1"])
    monkeypatch.setattr(cli_module.CLI, "create_download_options", lambda self, ao: DownloadOptions(save_path=tmp_path, download_sound_only=ao))
    cli = cli_module.CLI(dd)
    cli.handle_playlist_option(True)
    assert dd.called[0] == ["v1"]
    assert dd.called[1].download_sound_only is True


def test_handle_playlist_option_error(monkeypatch):
    dd = DummyDownloader()
    monkeypatch.setattr(cli_module.cli_utils, "ask_youtube_url", lambda: "https://youtube.com/playlist")
    monkeypatch.setattr(cli_module.CLI, "load_playlist", lambda self, url: (_ for _ in ()).throw(cli_module.PlaylistConnectionError()))
    with pytest.raises(cli_module.PlaylistConnectionError):
        cli_module.CLI(dd).handle_playlist_option(False)


def test_handle_channel_option_error(monkeypatch):
    dd = DummyDownloader()
    monkeypatch.setattr(cli_module.cli_utils, "ask_youtube_url", lambda: "https://youtube.com/channel")
    monkeypatch.setattr(cli_module.CLI, "load_channel", lambda self, url: (_ for _ in ()).throw(cli_module.ChannelConnectionError()))
    with pytest.raises(cli_module.ChannelConnectionError):
        cli_module.CLI(dd).handle_channel_option(False)
