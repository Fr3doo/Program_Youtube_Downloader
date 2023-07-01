from pytube import YouTube
from pytube import Playlist
from pytube import Channel
import time
import os
import sys
import colorama

# Projet "Program Youtube Downloader"

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
def clear_screen():
    if(os.name == 'posix'):
        os.system('clear')
    else:
        os.system('cls')


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
    save_path =  input("Indiquez l'endroit où vous voulez stocker le fichier : \n --> ")
    
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
    total_bytes_download = stream.filesize
    bytes_downloaded = stream.filesize - bytes_remaining
    progress_bar(bytes_downloaded, total_bytes_download)


def progress_bar(progress, total=100, size=25, sides="||", full='█', empty=' ' , prefix="Downloading...", color_text=colorama.Fore.WHITE, color_Downloading=colorama.Fore.LIGHTYELLOW_EX, color_Download_OK=colorama.Fore.GREEN):
    x = int(size*progress/total)
    sys.stdout.write(color_text + "\r" + "Downloading ..." + color_Downloading + sides[0] + full*x + empty*(size-x) + sides[1] + ' ' + str(progress).rjust(len(str(total)),' ')+"/"+str(total))
    if progress==total:
        sys.stdout.write("\r" + color_text + "Download OK ..." + color_Download_OK + sides[0] + full*x + empty*(size-x) + sides[1] + ' ' + str(total) + "/" + str(total))


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
        if os.path.exists(file_downloaded): # os.path.exists('/myDir/myFile') : renvoie True si le fichier ou directory existe.
                                            # Si c'est un lien symbolique qui pointe vers un fichier qui n'existe pas, renvoie False
            os.remove(file_downloaded)
    except:
        print("[WARMING] un fichier MP3 portant le même nom, déjà existant!")
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
                    print("*************************************************************")
                    print("*             Stream vidéo selectionnée:                    *")
                    print("*************************************************************")
                    print('Number of link url video youtube in file: ', len(url_youtube_video_links))
                    print()
                
                itag = streams[choice_user-1].itag 
                stream = youtube_video.streams.get_by_itag(itag)
                
                print("Titre: " + youtube_video.title[0:53])
                print(f"le téléchargement va commencer dans 5 secondes ", end="", flush=True)
                duree_restante_avant_lancement = 5
                for i in range(5):
                    time.sleep(1)
                    print(".", end="", flush=True)
                    duree_restante_avant_lancement -= 1
                print()
                
                # control exist the file mp4
                current_file = save_path + "\\" + stream.default_filename
                if os.path.exists(current_file): # os.path.exists('/myDir/myFile') : renvoie True si le fichier ou directory existe.
                                                        # Si c'est un lien symbolique qui pointe vers un fichier qui n'existe pas, renvoie False
                    print("[WARMING] un fichier MP4 portant le même nom, déjà existant!")
                
                # downloading the file mp4
                try:
                    out_file = stream.download(output_path=save_path)
                    print(colorama.Fore.RESET)
                    print("")
                except:
                    print("")
                    print("[ERREUR] le téléchargement a échoué!")
                    print("")
                else:
                    if download_sound_only:
                        conversion_mp4_in_mp3(out_file)

        print()
        print("Fin du téléchargement")
        print("*************************************************************")
        print()
        duree_restante_avant_lancement = 5
        print(f"Le menu d'accueil va revenir dans 5 secondes ", end="", flush=True)
        for i in range(5):
            time.sleep(1)
            print(".", end="", flush=True)
            duree_restante_avant_lancement -= 1
        clear_screen()
