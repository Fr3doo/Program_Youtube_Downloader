# main.py
# pyinstaller --onefile --add-data "mypy.ini;." --hidden-import "youtube_downloader" main.py
import sys

if '__annotations__' not in globals():
    __annotations__ = {}

import youtube_downloader


def main() -> None:
    """Run the main menu loop."""

    # --------------------------------------------------------------------------
    # ------------------------------- PROGRAMME PRINCIPAL ----------------------
    # --------------------------------------------------------------------------

    while True:
        choix_max_menu_accueil = youtube_downloader.afficher_menu_acceuil()
        reponse_utilisateur_pour_choix_dans_menu = youtube_downloader.demander_valeur_numerique_utilisateur(
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
                url_video_send_user: str = youtube_downloader.demander_url_vidéo_youtube()
                url_video_send_user_list.append(url_video_send_user)
                if reponse_utilisateur_pour_choix_dans_menu == 1:
                    download_sound_only = False

                youtube_downloader.download_multiple_videos(url_video_send_user_list, download_sound_only)
            case 2 | 6:
                youtube_video_links: list[str] = youtube_downloader.demander_youtube_link_file()
                if reponse_utilisateur_pour_choix_dans_menu == 2:
                    download_sound_only = False

                youtube_downloader.download_multiple_videos(youtube_video_links, download_sound_only)
            case 3 | 7:
                url_playlist_send_user: str = youtube_downloader.demander_url_vidéo_youtube()
                try:
                    link_url_playlist_youtube = youtube_downloader.Playlist(url_playlist_send_user)
                except:
                    print("[ERREUR] : Connexion à la Playlist impossible")
                else:
                    if reponse_utilisateur_pour_choix_dans_menu == 3:
                        download_sound_only = False

                    youtube_downloader.download_multiple_videos(link_url_playlist_youtube, download_sound_only)  # type: ignore
            case 4 | 8:
                url_channel_send_user: str = youtube_downloader.demander_url_vidéo_youtube()
                try:
                    link_url_channel_youtube = youtube_downloader.Channel(url_channel_send_user)
                except:
                    print("[ERREUR] : Connexion à la chaîne Youtube impossible")
                else:
                    if reponse_utilisateur_pour_choix_dans_menu == 4:
                        download_sound_only = False

                    youtube_downloader.download_multiple_videos(link_url_channel_youtube, download_sound_only)  # type: ignore

    
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

if __name__ == "__main__":
    main()

