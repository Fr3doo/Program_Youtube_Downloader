# program_youtube_downloader/main.py
# pyinstaller --onefile --add-data "mypy.ini;." --hidden-import "youtube_downloader" program_youtube_downloader/main.py
import os
import sys
import argparse
import logging
from pathlib import Path
from pytube import Playlist, Channel


from pytube.exceptions import PytubeError
from . import cli_utils
from .downloader import YoutubeDownloader
from .exceptions import PlaylistConnectionError, ChannelConnectionError
from .config import DownloadOptions
from .constants import MenuOption
from .cli import CLI

logger = logging.getLogger(__name__)


def setup_logging(level: str) -> None:
    """Configure application-wide logging."""
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.ERROR),
        format="%(levelname)s:%(name)s:%(message)s",
        force=True,
    )

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command line arguments.

    Args:
        argv: Optional list of argument strings. If ``None`` ``sys.argv`` is
            used.

    Returns:
        The populated :class:`argparse.Namespace`.
    """
    parser = argparse.ArgumentParser(description="Program Youtube Downloader")
    parser.add_argument(
        "--log-level",
        default=os.environ.get("PYDL_LOG_LEVEL", "ERROR"),
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set logging level (overrides PYDL_LOG_LEVEL)",
    )
    subparsers = parser.add_subparsers(dest="command")

    video_parser = subparsers.add_parser("video", help="Download one or more videos")
    video_parser.add_argument("urls", nargs="+", help="Video URL(s)")
    video_parser.add_argument("--audio", action="store_true", help="Download audio only")
    video_parser.add_argument(
        "--output-dir",
        type=Path,
        help="Directory to save downloaded files",
    )

    playlist_parser = subparsers.add_parser("playlist", help="Download a playlist")
    playlist_parser.add_argument("url", help="Playlist URL")
    playlist_parser.add_argument("--audio", action="store_true", help="Download audio only")
    playlist_parser.add_argument(
        "--output-dir",
        type=Path,
        help="Directory to save downloaded files",
    )

    channel_parser = subparsers.add_parser("channel", help="Download a channel")
    channel_parser.add_argument("url", help="Channel URL")
    channel_parser.add_argument("--audio", action="store_true", help="Download audio only")
    channel_parser.add_argument(
        "--output-dir",
        type=Path,
        help="Directory to save downloaded files",
    )

    subparsers.add_parser("menu", help="Run interactive menu")

    return parser.parse_args(argv)


def create_download_options(audio_only: bool, output_dir: Path | None = None) -> DownloadOptions:
    """Build and return a :class:`DownloadOptions` instance."""
    cli = CLI()
    return cli.create_download_options(audio_only, output_dir)


def handle_quit_option() -> None:
    """Display the exit banner."""
    CLI().handle_quit_option()


def handle_video_option(yd: YoutubeDownloader, audio_only: bool) -> None:
    """Download a single video or its audio track."""
    CLI(yd).handle_video_option(audio_only)


def handle_videos_option(yd: YoutubeDownloader, audio_only: bool) -> None:
    """Download multiple videos or their audio tracks from a file."""
    CLI(yd).handle_videos_option(audio_only)


def handle_playlist_option(yd: YoutubeDownloader, audio_only: bool) -> None:
    """Download an entire playlist."""
    CLI(yd).handle_playlist_option(audio_only)


def handle_channel_option(yd: YoutubeDownloader, audio_only: bool) -> None:
    """Download all videos from a channel."""
    CLI(yd).handle_channel_option(audio_only)


def menu() -> None:  # pragma: no cover
    """Interactively ask the user what to download and start the process."""

    CLI().menu()

    

def main(
    argv: list[str] | None = None,
    downloader: YoutubeDownloader | None = None,
) -> None:
    """Entry point called by the ``program-youtube-downloader`` script.

    Args:
        argv: Optional list of command line arguments.
        downloader: Existing :class:`YoutubeDownloader` instance to use. If
            ``None`` a new one is created when required.
    """
    args = parse_args(argv)
    setup_logging(args.log_level)
    command = args.command

    cli = CLI(downloader)

    if command is None or command == "menu":
        menu()
        return

    yd = cli.downloader

    if command == "video":
        options = cli.create_download_options(args.audio, args.output_dir)
        yd.download_multiple_videos(
            args.urls,
            options,
        )
    elif command == "playlist":
        try:
            playlist = Playlist(args.url)
        except (PytubeError, KeyError, ValueError) as e:
            raise PlaylistConnectionError("Connexion à la Playlist impossible") from e
        except Exception:
            logger.exception("Unexpected error while connecting to playlist")
            raise
        options = cli.create_download_options(args.audio, args.output_dir)
        yd.download_multiple_videos(
            playlist,
            options,
        )  # type: ignore
    elif command == "channel":
        try:
            channel = Channel(args.url)
        except (PytubeError, KeyError, ValueError) as e:
            raise ChannelConnectionError("Connexion à la chaîne Youtube impossible") from e
        except Exception:
            logger.exception("Unexpected error while connecting to channel")
            raise
        options = cli.create_download_options(args.audio, args.output_dir)
        yd.download_multiple_videos(
            channel,
            options,
        )  # type: ignore
    else:
        raise SystemExit(f"Unknown command: {command}")


if __name__ == "__main__":  # pragma: no cover
    main()

