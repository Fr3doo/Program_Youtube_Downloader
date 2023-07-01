import youtube_downloader

# ------------------------------------------------------------------------------------------- #
# ----------------------------------- PROGRAMME PRINCIPAL ----------------------------------- #
# ------------------------------------------------------------------------------------------- #

while True:
    choix_max_menu_accueil = youtube_downloader.afficher_menu_acceuil()
    reponse_utilisateur_pour_choix_dans_menu = youtube_downloader.demander_valeur_numerique_utilisateur(1,choix_max_menu_accueil)
    download_sound_only = True

    match reponse_utilisateur_pour_choix_dans_menu:
        case 9 :
            print()
            print()
            print("*************************************************************")
            print("*                                                           *")
            print("*                    Fin du programme                       *")
            print("*                                                           *")
            print("*************************************************************")
            break
        
        case 1 | 5 : # 1: une vidéo avec l'audio // 5: une piste audio d'une vidéo (sound only)
            url_video_send_user_list = []
            url_video_send_user = youtube_downloader.demander_url_vidéo_youtube()
            url_video_send_user_list.append(url_video_send_user)
            if reponse_utilisateur_pour_choix_dans_menu == 1:
                download_sound_only = False 

            youtube_downloader.download_multiple_videos(url_video_send_user_list, download_sound_only)
        
        case 2 | 6 : # 2: des vidéos avec l'audio // 6: les pistes audios de plusieurs vidéos (sound only)
            youtube_video_links = youtube_downloader.demander_youtube_link_file()
            if reponse_utilisateur_pour_choix_dans_menu == 2:
                download_sound_only = False 

            youtube_downloader.download_multiple_videos(youtube_video_links, download_sound_only)

        case 3 | 7 : # 3: playlist (avec vidéo et audio) // 7: une playlist (sound only) 
            url_playlist_send_user = youtube_downloader.demander_url_vidéo_youtube()
            try:
                link_url_playlist_youtube = youtube_downloader.Playlist(url_playlist_send_user)
            except:
                print("[ERREUR] : Connexion à la Playlist impossible")
            else:
                if reponse_utilisateur_pour_choix_dans_menu == 3:
                    download_sound_only = False 

                youtube_downloader.download_multiple_videos(link_url_playlist_youtube, download_sound_only)
             
        case 4 | 8 : # 4: channel (avec vidéo et audio) // 8: channel (sound only) 
            url_channel_send_user = youtube_downloader.demander_url_vidéo_youtube()
            try:                    
                link_url_channel_youtube = youtube_downloader.Channel(url_channel_send_user)
            except:
                print("[ERREUR] : Connexion à la chaîne Youtube impossible")
            else:
                if reponse_utilisateur_pour_choix_dans_menu == 4:
                    download_sound_only = False
                
                youtube_downloader.download_multiple_videos(link_url_channel_youtube, download_sound_only)
    
