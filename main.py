from pytube import YouTube
from pytube import Playlist
from pytube import Channel
import time
import os
import sys

# Projet "Program_Youtube_Downloader"

# ------------------------------------------------------------------------------------------- #
# ----------------------------------- CONSTANTES -------------------------------------------- #
# ------------------------------------------------------------------------------------------- #
TITLE_PROGRAM = "Program Youtube Downloader"

TITLE_QUESTION_MENU_ACCUEIL = "Que voulez-vous télécharger sur Youtube ?"
CHOICE_MENU_ACCUEIL = (
        "une vidéo                              - (format mp4)",
        "des vidéos                             - (format mp4)",
        "une playlist vidéo                     - (format mp4)",
        "des vidéos d'une chaîne Youtube        - (format mp4)",
        "la piste audio d'une vidéo             - (format mp3)",
        "les pistes audios de plusieurs vidéos  - (format mp3)",
        "les pistes audios d'une playlist       - (format mp3)",
        "les pistes audios d'une chaîne         - (format mp3)",
        "Quitter le programme"
        )

# url de base de youtube:
BASE_YOUTUBE_URL = "https://www.youtube.com"

# ------------------------------------------------------------------------------------------- #
# ----------------------------------- FONCTIONS --------------------------------------------- #
# ------------------------------------------------------------------------------------------- #
def demander_valeur_numerique_utilisateur(valeur_min, valeur_max):
    v_str = input(f"Donnez une valeur entre {valeur_min} et {valeur_max} : \n --> " )
    try:
        v_int = int(v_str)
    except:
        print("ERREUR : Vous devez rentrer une valeur numérique.")
        print()
        return demander_valeur_numerique_utilisateur(valeur_min, valeur_max)
    if not (valeur_min <= v_int <= valeur_max):
        print(f"ERREUR : Vous devez rentrer un nombre (entre {valeur_min} et {valeur_max} ).")
        print()
        return demander_valeur_numerique_utilisateur(valeur_min, valeur_max)

    return v_int


def afficher_menu_acceuil():
    print()
    print()
    print("*************************************************************")
    print(f"*            {TITLE_PROGRAM}                     *")
    print("*************************************************************")
    print(f"{TITLE_QUESTION_MENU_ACCUEIL}                          ")
    print()
    i = 0
    for items in CHOICE_MENU_ACCUEIL:
        choix_menu = items
        i += 1
        print(f"    {i} - {choix_menu}                              ")
    print("                                                           ")
    print("*************************************************************") 
    valeur_choix_maximale = i
    
    return valeur_choix_maximale


def demander_save_file_path():
    print()
    print()
    print("*************************************************************")
    print("*             Sauvegarde fichier                            *")
    print("*************************************************************")
    # save_path =  'C:\Donnees'
    # save_path =  'F:\musique'
    save_path =  input("Indiquez l'endroit où vous voulez stocker le fichier : \n --> ")
    print("*************************************************************")
    return save_path


def demander_url_vidéo_youtube():
    print()
    print()
    print("*************************************************************")
    print("*             Url de votre vidéo Youtube                    *")
    print("*************************************************************")
    url =  input("Indiquez l'url de la vidéo Youtube : \n --> ")
    url = url.replace('https://www.youtube.com/@', 'https://www.youtube.com/c/')
    if url.lower().startswith(BASE_YOUTUBE_URL):
        return url
    else:
        print("ERREUR : Vous devez renter une URL de vidéo youtube")
        print("le prefixe attendu est : https://www.youtube.com/")
        return demander_url_vidéo_youtube()
        
    
def demander_youtube_link_file():
    print()
    print()
    print("*************************************************************")
    print("*             Fichier contenant les urls Youtube            *")
    print("*************************************************************")
    fichier_user =  input("Indiquez le nom du fichier : \n --> ")
    print()
    try:
                    # "fichier_url_video.txt"
        fichier = open(fichier_user, "r")
    except:
        print("[ERREUR] : Le fichier n'est pas accessible")
    else:
        lignes = fichier.readlines() # .readlines() pour tout lire et recuperer une List [] en retour
        compteur_ligne = 0
        number_erreur = 0
        number_links_file = len(lignes)
        link_url_video_youtube_final = []
        
        if number_links_file == 0:
            print("[ERREUR] : Vous devez fournir un fichier avec au minimum une URL de vidéo youtube")
            return demander_youtube_link_file()

        else:
            for i in range(0,len(lignes)):
                url_video = lignes[i]
                compteur_ligne += 1
                
                if url_video.lower().startswith(BASE_YOUTUBE_URL):
                    link_url_video_youtube_final.append(url_video)
                else:
                    print("[ERREUR] : ")
                    print("le prefixe attendu est : https://www.youtube.com/")
                    print(f"  le lien sur la ligne n° {compteur_ligne} ne sera pas télécharger")
                    print("")
                    number_erreur += 1
                
        if number_erreur == number_links_file:
            print("[ERREUR] : Vous devez fournir un fichier avec au minimum une URL de vidéo youtube")
            return demander_youtube_link_file()

        fichier.close()

    return link_url_video_youtube_final


def on_download_progress(stream, chunk, bytes_remaining):
    """ 
    Fonction : 
    - Quand il y a une progression dans le téléchargement
    - Permet d'afficher les pourcentages restant à télécharger
    """
    bytes_downloaded = stream.filesize - bytes_remaining
    percent_downloaded = round((bytes_downloaded * 100) / stream.filesize,2)
    
    print("Progression du téléchargement:", percent_downloaded,"%")


def demander_choice_resolution_vidéo_or_bitrate_audio(download_sound_only, list_available_streams):
    i = 0
    if download_sound_only:
        print()
        print()
        print("*************************************************************")
        print("*             Choississez la qualité audio                  *")
        print("*************************************************************")
        for stream in list_available_streams:
            choix_menu = stream.abr # Pour la qualité de l'audio
            i += 1
            print(f"      {i} - {choix_menu} ") 
            valeur_choix_maximale = i
    else:
        print()
        print()
        print("*************************************************************")
        print("*             Choississez la résolution vidéo               *")
        print("*************************************************************")
        for stream in list_available_streams:
            choix_menu = stream.resolution # pour la qualite de la vidéo
            i += 1
            print(f"      {i} - {choix_menu} ") 
            valeur_choix_maximale = i 
    print("*************************************************************")
    
    v_int = demander_valeur_numerique_utilisateur(1, valeur_choix_maximale)
    
    return v_int


def streams_video(download_sound_only, youtube_video):
    if download_sound_only:
        streams = youtube_video.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc()  
    else:
        streams = youtube_video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()

    return streams


def conversion_mp4_in_mp3(file_downloaded):
    base, ext = os.path.splitext(file_downloaded) # os.path.splitext('myFile.txt') : renvoie un tuple ('myFile', '.txt') :
    try:
        new_file = base + '.mp3'
        os.rename(file_downloaded, new_file)
        if os.path.exists(file_downloaded):    # os.path.exists('/myDir/myFile') : renvoie True si le fichier ou directory existe.
                                        # Si c'est un lien symbolique qui pointe vers un fichier qui n'existe pas, renvoie False
            os.remove(file_downloaded)
    except:
        print("[ERREUR] un fichier MP3 portant le même nom, déjà existant!")
        os.remove(file_downloaded)
        print()


def download_multiple_videos(url_youtube_video_links, download_sound_only):
    """ 
    Fonction général qui contient 6 autres fonctions : 
    - step 1 : choisir l'endroit de la sauvegarde
        # demander_save_file_path()
    - step 2 : affiche la progression de téléchargement de la vidéo
        # youtube_video.register_on_progress_callback(on_download_progress)
    - step 3 : recuperation des différents streams du lien de la vidéo
        # streams_video(download_sound_only, youtube_video)
    - step 4 : choisir la resolution vidéo ou qualité audio
        # demander_choice_resolution_vidéo_or_bitrate_audio(download_sound_only, streams)
    - step 5 : téléchargement du fichier
        # stream.download(output_path=save_path)
    - step 6 : conversion mp4 en mp3, si necessaire
        # conversion_mp4_in_mp3(out_file)
    """
    choice_once_bitrate_audio_or_resolution_video_user = True
    save_path = demander_save_file_path()

    if len(url_youtube_video_links) == 0:
        print("[ERREUR] : il y a aucune vidéo à télécharger")
        return url_youtube_video_links
    else:
        for url_video in url_youtube_video_links:
            try:
                youtube_video = YouTube(url_video)
                youtube_video.register_on_progress_callback(on_download_progress)
            except:
                print("[ERREUR] : Connexion à la vidéo impossible")
            else: 
                streams = streams_video(download_sound_only, youtube_video)
                
                if choice_once_bitrate_audio_or_resolution_video_user: # au premier passage, on choisit la qualité et on télécharge toutes les pistes avec cette qualité
                    choice_user = demander_choice_resolution_vidéo_or_bitrate_audio(download_sound_only, streams)
                    choice_once_bitrate_audio_or_resolution_video_user = False 
                    print()
                    print()
                    print("***********************************************************")
                    print("*             Stream vidéo selectionnée:                  *")
                    print("***********************************************************")
                    print('Number of link url video youtube in file: ', len(url_youtube_video_links))
                    print()
                
                itag = streams[choice_user-1].itag 
                stream = youtube_video.streams.get_by_itag(itag)
                
                print("Titre : " + youtube_video.title)
                print(f"le téléchargement va commencer dans 5 secondes ", end="", flush=True)
                duree_restante_avant_lancement = 5
                for i in range(5):
                    time.sleep(1)
                    print(".", end="", flush=True)
                    duree_restante_avant_lancement -= 1
                print()
                
                # downloading the file mp4
                try:
                    out_file = stream.download(output_path=save_path)
                    print()
                except:
                    print("[ERREUR] le téléchargement de " + youtube_video.title + " a échoué!")
                else:
                    if download_sound_only:
                        conversion_mp4_in_mp3(out_file)

        print()
        print("Fin du téléchargement")
        print("***********************************************************")

# ------------------------------------------------------------------------------------------- #
# ----------------------------------- PROGRAMME PRINCIPAL ----------------------------------- #
# ------------------------------------------------------------------------------------------- #

while True:
    choix_max_menu_accueil = afficher_menu_acceuil()
    reponse_utilisateur_pour_choix_dans_menu = demander_valeur_numerique_utilisateur(1,choix_max_menu_accueil)
    download_sound_only = True
                        # True  = sound_only (= file mp3)
                        # False = download video with sound (= file mp4)
    
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
            url_video_send_user = demander_url_vidéo_youtube()
            url_video_send_user_list.append(url_video_send_user)
            if reponse_utilisateur_pour_choix_dans_menu == 1:
                download_sound_only = False 

            download_multiple_videos(url_video_send_user_list, download_sound_only)
        
        case 2 | 6 : # 2: des vidéos avec l'audio // 6: les pistes audios de plusieurs vidéos (sound only)
            youtube_video_links = demander_youtube_link_file()
            if reponse_utilisateur_pour_choix_dans_menu == 2:
                download_sound_only = False 

            download_multiple_videos(youtube_video_links, download_sound_only)

        case 3 | 7 : # 3: playlist (avec vidéo et audio) // 7: une playlist (sound only) 
            url_playlist_send_user = demander_url_vidéo_youtube()
            try:
                link_url_playlist_youtube = Playlist(url_playlist_send_user)
            except:
                print("[ERREUR] : Connexion à la Playlist impossible")
            else:
                if reponse_utilisateur_pour_choix_dans_menu == 3:
                    download_sound_only = False 

                download_multiple_videos(link_url_playlist_youtube, download_sound_only)
             
        case 4 | 8 : # 4: channel (avec vidéo et audio) // 8: channel (sound only) 
            url_channel_send_user = demander_url_vidéo_youtube()
            try:                    
                link_url_channel_youtube = Channel(url_channel_send_user)
            except:
                print("[ERREUR] : Connexion à la chaîne Youtube impossible")
            else:
                if reponse_utilisateur_pour_choix_dans_menu == 4:
                    download_sound_only = False
                
                download_multiple_videos(link_url_channel_youtube, download_sound_only)                
