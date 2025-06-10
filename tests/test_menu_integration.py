import program_youtube_downloader.cli as cli_module
import program_youtube_downloader.main as main_module
from program_youtube_downloader.config import DownloadOptions
import pytest


class DummyDownloader:
    def __init__(self):
        self.called = None

    def download_multiple_videos(self, urls, options):
        self.called = (list(urls), options)


def run_menu_with_choice(monkeypatch, tmp_path, menu_choice):
    dd = DummyDownloader()
    monkeypatch.setattr(
        main_module.cli_utils,
        "display_main_menu",
        lambda *a, **k: len(cli_module.MenuOption),
    )
    choices = iter([menu_choice, cli_module.MenuOption.QUIT.value])
    monkeypatch.setattr(
        main_module.cli_utils,
        "ask_numeric_value",
        lambda *a, **k: next(choices),
    )
    monkeypatch.setattr(
        main_module.cli_utils,
        "ask_youtube_url",
        lambda *a, **k: "https://youtu.be/x",
    )
    monkeypatch.setattr(
        main_module.cli_utils,
        "ask_youtube_link_file",
        lambda *a, **k: ["https://youtu.be/a", "https://youtu.be/b"],
    )
    monkeypatch.setattr(
        main_module.CLI,
        "load_playlist",
        lambda self, u: ["https://youtu.be/p"],
    )
    monkeypatch.setattr(
        main_module.CLI,
        "load_channel",
        lambda self, u: ["https://youtu.be/c"],
    )
    monkeypatch.setattr(
        main_module.CLI,
        "create_download_options",
        lambda self, ao: DownloadOptions(save_path=tmp_path, download_sound_only=ao),
    )
    main_module.main(["menu"], dd)
    return dd.called


@pytest.mark.parametrize(
    "menu_choice,expected_urls,audio_only",
    [
        (cli_module.MenuOption.VIDEO.value, ["https://youtu.be/x"], False),
        (cli_module.MenuOption.VIDEO_AUDIO_ONLY.value, ["https://youtu.be/x"], True),
        (cli_module.MenuOption.VIDEOS.value, ["https://youtu.be/a", "https://youtu.be/b"], False),
        (cli_module.MenuOption.VIDEOS_AUDIO_ONLY.value, ["https://youtu.be/a", "https://youtu.be/b"], True),
        (cli_module.MenuOption.PLAYLIST_VIDEO.value, ["https://youtu.be/p"], False),
        (cli_module.MenuOption.PLAYLIST_AUDIO_ONLY.value, ["https://youtu.be/p"], True),
        (cli_module.MenuOption.CHANNEL_VIDEOS.value, ["https://youtu.be/c"], False),
        (cli_module.MenuOption.CHANNEL_AUDIO_ONLY.value, ["https://youtu.be/c"], True),
    ],
)
def test_menu_dispatch(monkeypatch, tmp_path, menu_choice, expected_urls, audio_only):
    called = run_menu_with_choice(monkeypatch, tmp_path, menu_choice)
    assert called[0] == expected_urls
    assert called[1].download_sound_only is audio_only


def test_menu_keyboard_interrupt(monkeypatch):
    dd = DummyDownloader()
    monkeypatch.setattr(
        main_module.cli_utils,
        "display_main_menu",
        lambda *a, **k: len(cli_module.MenuOption),
    )

    def raise_interrupt(*args, **kwargs):
        raise KeyboardInterrupt()

    monkeypatch.setattr(
        main_module.cli_utils,
        "ask_numeric_value",
        lambda *a, **k: raise_interrupt(),
    )
    main_module.main(["menu"], dd)
