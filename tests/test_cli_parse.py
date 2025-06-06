from program_youtube_downloader.main import parse_args


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

