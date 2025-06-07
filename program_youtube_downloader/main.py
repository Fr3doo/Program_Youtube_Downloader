# main.py
# pyinstaller --onefile --add-data "mypy.ini;." --hidden-import "youtube_downloader" main.py
import sys
import argparse
import logging
import os

if '__annotations__' not in globals():
    __annotations__ = {}

from . import youtube_downloader
from . import cli_utils
from .downloader import YoutubeDownloader
from .config import DownloadOptions
from .constants import MenuOption



def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Return the parsed CLI arguments."""
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

    playlist_parser = subparsers.add_parser("playlist", help="Download a playlist")
    playlist_parser.add_argument("url", help="Playlist URL")
    playlist_parser.add_argument("--audio", action="store_true", help="Download audio only")

    channel_parser = subparsers.add_parser("channel", help="Download a channel")
    channel_parser.add_argument("url", help="Channel URL")
    channel_parser.add_argument("--audio", action="store_true", help="Download audio only")

    subparsers.add_parser("menu", help="Run interactive menu")

    return parser.parse_args(argv)


def create_download_options(audio_only: bool) -> DownloadOptions:
    """Prompt for destination and return configured options."""
    save_path = cli_utils.demander_save_file_path()
    return DownloadOptions(
        save_path=save_path,
        download_sound_only=audio_only,
        choice_callback=cli_utils.demander_choice_resolution_vidéo_or_bitrate_audio,
    )


def menu() -> None:  # pragma: no cover
    """Run the main menu loop."""

    # --------------------------------------------------------------------------
    # ------------------------------- PROGRAMME PRINCIPAL ----------------------
    # --------------------------------------------------------------------------

    yd = YoutubeDownloader()

    while True:
        choix_max_menu_accueil = cli_utils.afficher_menu_acceuil()
        choix = MenuOption(
            cli_utils.ask_numeric_value(1, choix_max_menu_accueil)
        )
        download_sound_only = True

        match choix:
            case MenuOption.QUIT:
                logging.info("")
                logging.info("")
                logging.info("*************************************************************")
                logging.info("*                                                           *")
                logging.info("*                    Fin du programme                       *")
                logging.info("*                                                           *")
                logging.info("*************************************************************")
                break
            case MenuOption.VIDEO | MenuOption.VIDEO_AUDIO_ONLY:
                url_video_send_user_list: list[str] = []
                url_video_send_user: str = cli_utils.ask_youtube_url()
                url_video_send_user_list.append(url_video_send_user)
                if choix is MenuOption.VIDEO:
                    download_sound_only = False

                options = create_download_options(download_sound_only)
                yd.download_multiple_videos(
                    url_video_send_user_list,
                    options,
                )
            case MenuOption.VIDEOS | MenuOption.VIDEOS_AUDIO_ONLY:
                youtube_video_links: list[str] = cli_utils.demander_youtube_link_file()
                if choix is MenuOption.VIDEOS:
                    download_sound_only = False

                options = create_download_options(download_sound_only)
                yd.download_multiple_videos(
                    youtube_video_links,
                    options,
                )
            case MenuOption.PLAYLIST_VIDEO | MenuOption.PLAYLIST_AUDIO_ONLY:
                url_playlist_send_user: str = cli_utils.ask_youtube_url()
                try:
                    link_url_playlist_youtube = youtube_downloader.Playlist(url_playlist_send_user)
                except Exception as exc:
                    logging.exception("Error connecting to playlist")
                    logging.error("[ERREUR] : Connexion à la Playlist impossible")
                else:
                    if choix is MenuOption.PLAYLIST_VIDEO:
                        download_sound_only = False

                    options = create_download_options(download_sound_only)
                    yd.download_multiple_videos(
                        link_url_playlist_youtube,
                        options,
                    )  # type: ignore
            case MenuOption.CHANNEL_VIDEOS | MenuOption.CHANNEL_AUDIO_ONLY:
                url_channel_send_user: str = cli_utils.ask_youtube_url()
                try:
                    link_url_channel_youtube = youtube_downloader.Channel(url_channel_send_user)
                except Exception as exc:
                    logging.exception("Error connecting to channel")
                    logging.error("[ERREUR] : Connexion à la chaîne Youtube impossible")
                else:
                    if choix is MenuOption.CHANNEL_VIDEOS:
                        download_sound_only = False

                    options = create_download_options(download_sound_only)
                    yd.download_multiple_videos(
                        link_url_channel_youtube,
                        options,
                    )  # type: ignore

    
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
    """Parse arguments and dispatch to subcommands."""
    args = parse_args(argv)
    logging.getLogger().setLevel(args.log_level)
    command = args.command
    yd = YoutubeDownloader()

    if command is None or command == "menu":
        menu()
        return

    if command == "video":
        options = create_download_options(args.audio)
        yd.download_multiple_videos(
            args.urls,
            options,
        )
    elif command == "playlist":
        playlist = youtube_downloader.Playlist(args.url)
        options = create_download_options(args.audio)
        yd.download_multiple_videos(
            playlist,
            options,
        )  # type: ignore
    elif command == "channel":
        channel = youtube_downloader.Channel(args.url)
        options = create_download_options(args.audio)
        yd.download_multiple_videos(
            channel,
            options,
        )  # type: ignore
    else:
        raise SystemExit(f"Unknown command: {command}")


if __name__ == "__main__":  # pragma: no cover
    main()

