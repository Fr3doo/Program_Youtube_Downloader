import program_youtube_downloader.cli as cli_module
from program_youtube_downloader.config import DownloadOptions


class DummyDownloader:
    def __init__(self):
        self.called = None

    def download_multiple_videos(self, urls, options):
        self.called = (list(urls), options)


def run_menu_with_choice(monkeypatch, tmp_path, menu_choice):
    dd = DummyDownloader()
    monkeypatch.setattr(cli_module.cli_utils, "display_main_menu", lambda: len(cli_module.MenuOption))
    choices = iter([menu_choice, cli_module.MenuOption.QUIT.value])
    monkeypatch.setattr(cli_module.cli_utils, "ask_numeric_value", lambda a, b: next(choices))
    monkeypatch.setattr(cli_module.cli_utils, "ask_youtube_url", lambda: "https://youtu.be/x")
    monkeypatch.setattr(cli_module.CLI, "create_download_options", lambda self, ao: DownloadOptions(save_path=tmp_path, download_sound_only=ao))
    cli_module.CLI(dd).menu()
    return dd.called


def test_menu_video_triggers_download(monkeypatch, tmp_path):
    called = run_menu_with_choice(monkeypatch, tmp_path, cli_module.MenuOption.VIDEO.value)
    assert called[0] == ["https://youtu.be/x"]
    assert called[1].download_sound_only is False


def test_menu_audio_only_triggers_download(monkeypatch, tmp_path):
    called = run_menu_with_choice(monkeypatch, tmp_path, cli_module.MenuOption.VIDEO_AUDIO_ONLY.value)
    assert called[0] == ["https://youtu.be/x"]
    assert called[1].download_sound_only is True
