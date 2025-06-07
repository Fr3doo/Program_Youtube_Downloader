from program_youtube_downloader.main import parse_args
from pathlib import Path


def test_parse_video_audio_flag() -> None:
    args = parse_args(["video", "https://youtu.be/abc", "--audio"])
    assert args.command == "video"
    assert args.urls == ["https://youtu.be/abc"]
    assert args.audio is True


def test_parse_playlist_command() -> None:
    url = "https://youtube.com/playlist?list=123"
    args = parse_args(["playlist", url])
    assert args.command == "playlist"
    assert args.url == url
    assert args.audio is False


def test_parse_playlist_audio() -> None:
    url = "https://youtube.com/playlist?list=xyz"
    args = parse_args(["playlist", url, "--audio"])
    assert args.audio is True
    assert args.command == "playlist"
    assert args.url == url


def test_parse_no_subcommand() -> None:
    args = parse_args([])
    assert args.command is None


def test_parse_log_level_cli() -> None:
    args = parse_args(["--log-level", "DEBUG", "video", "https://youtu.be/x"])
    assert args.log_level == "DEBUG"
    assert args.command == "video"


def test_parse_log_level_env(monkeypatch) -> None:
    monkeypatch.setenv("PYDL_LOG_LEVEL", "INFO")
    args = parse_args(["video", "https://youtu.be/x"])
    assert args.log_level == "INFO"


def test_parse_video_output_dir() -> None:
    args = parse_args(["video", "https://youtu.be/x", "--output-dir", "dest"])
    assert args.output_dir == Path("dest")


def test_parse_playlist_output_dir() -> None:
    url = "https://youtube.com/playlist?list=123"
    args = parse_args(["playlist", url, "--output-dir", "/tmp/out"])
    assert args.output_dir == Path("/tmp/out")

