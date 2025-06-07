import program_youtube_downloader.main as main_module
from program_youtube_downloader.config import DownloadOptions


class DummyDownloader:
    def __init__(self):
        self.called = None

    def download_multiple_videos(self, urls, options):
        self.called = (list(urls), options)


def run_menu_with_choice(monkeypatch, tmp_path, menu_choice):
    dd = DummyDownloader()
    monkeypatch.setattr(main_module, "YoutubeDownloader", lambda: dd)
    monkeypatch.setattr(main_module.cli_utils, "afficher_menu_acceuil", lambda: len(main_module.MenuOption))
    choices = iter([menu_choice, main_module.MenuOption.QUIT.value])
    monkeypatch.setattr(main_module.cli_utils, "ask_numeric_value", lambda a, b: next(choices))
    monkeypatch.setattr(main_module.cli_utils, "ask_youtube_url", lambda: "https://youtu.be/x")
    monkeypatch.setattr(main_module, "create_download_options", lambda ao: DownloadOptions(save_path=tmp_path, download_sound_only=ao))
    main_module.menu()
    return dd.called


def test_menu_video_triggers_download(monkeypatch, tmp_path):
    called = run_menu_with_choice(monkeypatch, tmp_path, main_module.MenuOption.VIDEO.value)
    assert called[0] == ["https://youtu.be/x"]
    assert called[1].download_sound_only is False


def test_menu_audio_only_triggers_download(monkeypatch, tmp_path):
    called = run_menu_with_choice(monkeypatch, tmp_path, main_module.MenuOption.VIDEO_AUDIO_ONLY.value)
    assert called[0] == ["https://youtu.be/x"]
    assert called[1].download_sound_only is True
