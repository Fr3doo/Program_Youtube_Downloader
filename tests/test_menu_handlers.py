import logging
from pathlib import Path

import program_youtube_downloader.main as main_module
from program_youtube_downloader.config import DownloadOptions


class DummyDownloader:
    def __init__(self):
        self.called = None

    def download_multiple_videos(self, urls, options):
        self.called = (list(urls), options)


def test_handle_video_option(monkeypatch, tmp_path):
    dd = DummyDownloader()
    monkeypatch.setattr(main_module.cli_utils, "ask_youtube_url", lambda: "https://youtu.be/x")
    monkeypatch.setattr(main_module, "create_download_options", lambda ao: DownloadOptions(save_path=tmp_path, download_sound_only=ao))
    main_module.handle_video_option(dd, True)
    assert dd.called[0] == ["https://youtu.be/x"]
    assert dd.called[1].download_sound_only is True


def test_handle_videos_option(monkeypatch, tmp_path):
    dd = DummyDownloader()
    monkeypatch.setattr(main_module.cli_utils, "demander_youtube_link_file", lambda: ["https://youtu.be/a", "https://youtu.be/b"])
    monkeypatch.setattr(main_module, "create_download_options", lambda ao: DownloadOptions(save_path=tmp_path, download_sound_only=ao))
    main_module.handle_videos_option(dd, False)
    assert dd.called[0] == ["https://youtu.be/a", "https://youtu.be/b"]
    assert dd.called[1].download_sound_only is False


def test_handle_playlist_option(monkeypatch, tmp_path):
    dd = DummyDownloader()
    monkeypatch.setattr(main_module.cli_utils, "ask_youtube_url", lambda: "https://youtube.com/playlist")
    monkeypatch.setattr(main_module.youtube_downloader, "Playlist", lambda url: ["v1"])
    monkeypatch.setattr(main_module, "create_download_options", lambda ao: DownloadOptions(save_path=tmp_path, download_sound_only=ao))
    main_module.handle_playlist_option(dd, True)
    assert dd.called[0] == ["v1"]
    assert dd.called[1].download_sound_only is True


def test_handle_channel_option_error(monkeypatch):
    dd = DummyDownloader()
    monkeypatch.setattr(main_module.cli_utils, "ask_youtube_url", lambda: "https://youtube.com/channel")
    monkeypatch.setattr(main_module.youtube_downloader, "Channel", lambda url: (_ for _ in ()).throw(ValueError()))
    main_module.handle_channel_option(dd, False)
    assert dd.called is None
