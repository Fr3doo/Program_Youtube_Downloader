# main.py
# pyinstaller --onefile --add-data "mypy.ini;." --hidden-import "youtube_downloader" main.py
import sys
import argparse

if '__annotations__' not in globals():
    __annotations__ = {}

from . import youtube_downloader
from . import cli_utils
from .downloader import YoutubeDownloader


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Return the parsed CLI arguments."""
    parser = argparse.ArgumentParser(description="Program Youtube Downloader")
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


def menu() -> None:
    """Run the main menu loop."""

    # --------------------------------------------------------------------------
    # ------------------------------- PROGRAMME PRINCIPAL ----------------------
    # --------------------------------------------------------------------------

    yd = YoutubeDownloader()

    while True:
        choix_max_menu_accueil = cli_utils.afficher_menu_acceuil()
        reponse_utilisateur_pour_choix_dans_menu = cli_utils.ask_numeric_value(
            1, choix_max_menu_accueil
        )
        download_sound_only = True

        match reponse_utilisateur_pour_choix_dans_menu:
            case 9:
                print()
                print()
                print("*************************************************************")
                print("*                                                           *")
                print("*                    Fin du programme                       *")
                print("*                                                           *")
                print("*************************************************************")
                break
            case 1 | 5:
                url_video_send_user_list: list[str] = []
                url_video_send_user: str = cli_utils.ask_youtube_url()
                url_video_send_user_list.append(url_video_send_user)
                if reponse_utilisateur_pour_choix_dans_menu == 1:
                    download_sound_only = False

                save_path = cli_utils.demander_save_file_path()
                yd.download_multiple_videos(
                    url_video_send_user_list,
                    download_sound_only,
                    save_path=save_path,
                    choice_callback=cli_utils.demander_choice_resolution_vidéo_or_bitrate_audio,
                    progress_callback=youtube_downloader.on_download_progress,
                )
            case 2 | 6:
                youtube_video_links: list[str] = cli_utils.demander_youtube_link_file()
                if reponse_utilisateur_pour_choix_dans_menu == 2:
                    download_sound_only = False

                save_path = cli_utils.demander_save_file_path()
                yd.download_multiple_videos(
                    youtube_video_links,
                    download_sound_only,
                    save_path=save_path,
                    choice_callback=cli_utils.demander_choice_resolution_vidéo_or_bitrate_audio,
                    progress_callback=youtube_downloader.on_download_progress,
                )
            case 3 | 7:
                url_playlist_send_user: str = cli_utils.ask_youtube_url()
                try:
                    link_url_playlist_youtube = youtube_downloader.Playlist(url_playlist_send_user)
                except:
                    print("[ERREUR] : Connexion à la Playlist impossible")
                else:
                    if reponse_utilisateur_pour_choix_dans_menu == 3:
                        download_sound_only = False

                    save_path = cli_utils.demander_save_file_path()
                    yd.download_multiple_videos(
                        link_url_playlist_youtube,
                        download_sound_only,
                        save_path=save_path,
                        choice_callback=cli_utils.demander_choice_resolution_vidéo_or_bitrate_audio,
                        progress_callback=youtube_downloader.on_download_progress,
                    )  # type: ignore
            case 4 | 8:
                url_channel_send_user: str = cli_utils.ask_youtube_url()
                try:
                    link_url_channel_youtube = youtube_downloader.Channel(url_channel_send_user)
                except:
                    print("[ERREUR] : Connexion à la chaîne Youtube impossible")
                else:
                    if reponse_utilisateur_pour_choix_dans_menu == 4:
                        download_sound_only = False

                    save_path = cli_utils.demander_save_file_path()
                    yd.download_multiple_videos(
                        link_url_channel_youtube,
                        download_sound_only,
                        save_path=save_path,
                        choice_callback=cli_utils.demander_choice_resolution_vidéo_or_bitrate_audio,
                        progress_callback=youtube_downloader.on_download_progress,
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
    command = args.command
    yd = YoutubeDownloader()

    if command is None or command == "menu":
        menu()
        return

    if command == "video":
        save_path = cli_utils.demander_save_file_path()
        yd.download_multiple_videos(
            args.urls,
            args.audio,
            save_path=save_path,
            choice_callback=cli_utils.demander_choice_resolution_vidéo_or_bitrate_audio,
            progress_callback=youtube_downloader.on_download_progress,
        )
    elif command == "playlist":
        playlist = youtube_downloader.Playlist(args.url)
        save_path = cli_utils.demander_save_file_path()
        yd.download_multiple_videos(
            playlist,
            args.audio,
            save_path=save_path,
            choice_callback=cli_utils.demander_choice_resolution_vidéo_or_bitrate_audio,
            progress_callback=youtube_downloader.on_download_progress,
        )  # type: ignore
    elif command == "channel":
        channel = youtube_downloader.Channel(args.url)
        save_path = cli_utils.demander_save_file_path()
        yd.download_multiple_videos(
            channel,
            args.audio,
            save_path=save_path,
            choice_callback=cli_utils.demander_choice_resolution_vidéo_or_bitrate_audio,
            progress_callback=youtube_downloader.on_download_progress,
        )  # type: ignore
    else:
        raise SystemExit(f"Unknown command: {command}")


if __name__ == "__main__":
    main()

