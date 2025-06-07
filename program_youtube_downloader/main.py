# main.py
# pyinstaller --onefile --add-data "mypy.ini;." --hidden-import "youtube_downloader" main.py
import sys
import argparse
import logging
from pathlib import Path


def setup_logging(level: str) -> None:
    """Configure application-wide logging."""
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.ERROR),
        format="%(levelname)s:%(name)s:%(message)s",
        force=True,
    )


logger = logging.getLogger(__name__)
import os

if '__annotations__' not in globals():
    __annotations__ = {}

from . import youtube_downloader
from . import cli_utils
from .downloader import YoutubeDownloader
from .exceptions import PlaylistConnectionError, ChannelConnectionError
from .config import DownloadOptions
from .constants import MenuOption



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
    """Build a :class:`DownloadOptions` instance.

    Args:
        audio_only: Whether to download only audio streams.
        output_dir: Directory where files will be saved. If ``None`` the user is
            prompted for a location.

    Returns:
        A fully configured :class:`DownloadOptions` object.
    """
    if output_dir is not None:
        save_path = output_dir.expanduser().resolve()
    else:
        save_path = cli_utils.demander_save_file_path()
    return DownloadOptions(
        save_path=save_path,
        download_sound_only=audio_only,
        choice_callback=cli_utils.demander_choice_resolution_vidéo_or_bitrate_audio,
    )


def handle_quit_option() -> None:
    """Display the exit banner."""
    logger.info("")
    logger.info("")
    logger.info("******************************************************")
    logger.info("*                                                    *")
    logger.info("*                    Fin du programme                *")
    logger.info("*                                                    *")
    logger.info("******************************************************")


def handle_video_option(yd: YoutubeDownloader, audio_only: bool) -> None:
    """Download a single video or its audio track."""
    url = cli_utils.ask_youtube_url()
    options = create_download_options(audio_only)
    yd.download_multiple_videos([url], options)


def handle_videos_option(yd: YoutubeDownloader, audio_only: bool) -> None:
    """Download multiple videos or their audio tracks from a file."""
    urls = cli_utils.demander_youtube_link_file()
    options = create_download_options(audio_only)
    yd.download_multiple_videos(urls, options)


def handle_playlist_option(yd: YoutubeDownloader, audio_only: bool) -> None:
    """Download an entire playlist."""
    url = cli_utils.ask_youtube_url()
    try:
        playlist = youtube_downloader.Playlist(url)
    except Exception as e:
        logger.exception("Error connecting to playlist")
        raise PlaylistConnectionError("Connexion à la Playlist impossible") from e
    options = create_download_options(audio_only)
    yd.download_multiple_videos(playlist, options)  # type: ignore


def handle_channel_option(yd: YoutubeDownloader, audio_only: bool) -> None:
    """Download all videos from a channel."""
    url = cli_utils.ask_youtube_url()
    try:
        channel = youtube_downloader.Channel(url)
    except Exception as e:
        logger.exception("Error connecting to channel")
        raise ChannelConnectionError("Connexion à la chaîne Youtube impossible") from e
    options = create_download_options(audio_only)
    yd.download_multiple_videos(channel, options)  # type: ignore


def menu() -> None:  # pragma: no cover
    """Interactively ask the user what to download and start the process."""

    # --------------------------------------------------------------------------
    # ------------------------------- PROGRAMME PRINCIPAL ----------------------
    # --------------------------------------------------------------------------
    yd = YoutubeDownloader()

    while True:
        choix_max_menu_accueil = cli_utils.afficher_menu_acceuil()
        choix = MenuOption(cli_utils.ask_numeric_value(1, choix_max_menu_accueil))

        match choix:
            case MenuOption.QUIT:
                handle_quit_option()
                break
            case MenuOption.VIDEO:
                handle_video_option(yd, False)
            case MenuOption.VIDEO_AUDIO_ONLY:
                handle_video_option(yd, True)
            case MenuOption.VIDEOS:
                handle_videos_option(yd, False)
            case MenuOption.VIDEOS_AUDIO_ONLY:
                handle_videos_option(yd, True)
            case MenuOption.PLAYLIST_VIDEO:
                handle_playlist_option(yd, False)
            case MenuOption.PLAYLIST_AUDIO_ONLY:
                handle_playlist_option(yd, True)
            case MenuOption.CHANNEL_VIDEOS:
                handle_channel_option(yd, False)
            case MenuOption.CHANNEL_AUDIO_ONLY:
                handle_channel_option(yd, True)

    
# import sys
# from pytubefix import YouTube

# youtube_episode_id = '9LP71ypf2qg'

# # list_of_clients = [
# #     'WEB', 'WEB_EMBED', 'WEB_MUSIC', 'WEB_CREATOR', 'WEB_SAFARI',
# #     'ANDROID', 'ANDROID_MUSIC', 'ANDROID_CREATOR', 'ANDROID_VR',
# #     'ANDROID_PRODUCER', 'ANDROID_TESTSUITE', 'IOS', 'IOS_MUSIC',
# #     'IOS_CREATOR', 'MWEB', 'TV', 'TV_EMBED', 'MEDIA_CONNECT'
# # ]

# list_of_clients = ['WEB']

# # Liste des itags précis à tester
# list_of_itag = [18, 137, 248, 399, 136, 247, 398, 135, 244, 397, 134, 
#                 243, 396, 133, 242, 395, 160, 278, 394, 140, 249, 250, 251]

# for client in list_of_clients:
#     for itag in list_of_itag:
#         try:
#             yt = YouTube(f'https://www.youtube.com/watch?v={youtube_episode_id}', client=client)
#             stream = yt.streams.get_by_itag(itag)
#             if stream:
#                 stream.download(filename=f'{youtube_episode_id}___{client}___itag{itag}.m4a')
#                 print(f"Succès avec le client {client} et l'itag {itag}\n\n\n\n")
#             else:
#                 print(f"Aucun flux trouvé pour le client {client} et l'itag {itag}\n\n\n\n")
#         except Exception as e:
#             error_type, _, error_traceback = sys.exc_info()
#             print(f"Échec avec le client : {client}, itag : {itag} avec l'erreur : {e}\n\n\n\n")

def main(argv: list[str] | None = None) -> None:
    """Entry point called by the ``program-youtube-downloader`` script.

    Args:
        argv: Optional list of command line arguments.
    """
    args = parse_args(argv)
    setup_logging(args.log_level)
    command = args.command
    yd = YoutubeDownloader()

    if command is None or command == "menu":
        menu()
        return

    if command == "video":
        options = create_download_options(args.audio, args.output_dir)
        yd.download_multiple_videos(
            args.urls,
            options,
        )
    elif command == "playlist":
        try:
            playlist = youtube_downloader.Playlist(args.url)
        except Exception as e:
            raise PlaylistConnectionError("Connexion à la Playlist impossible") from e
        options = create_download_options(args.audio, args.output_dir)
        yd.download_multiple_videos(
            playlist,
            options,
        )  # type: ignore
    elif command == "channel":
        try:
            channel = youtube_downloader.Channel(args.url)
        except Exception as e:
            raise ChannelConnectionError("Connexion à la chaîne Youtube impossible") from e
        options = create_download_options(args.audio, args.output_dir)
        yd.download_multiple_videos(
            channel,
            options,
        )  # type: ignore
    else:
        raise SystemExit(f"Unknown command: {command}")


if __name__ == "__main__":  # pragma: no cover
    main()

