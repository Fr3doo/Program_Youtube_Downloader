from asyncio import streams
from urllib.error import HTTPError
# from pytube import YouTube
from pytubefix import YouTube 
# https://github.com/JuanBindez/pytubefix
# https://pypi.org/project/pytubefix/
from pytube import Playlist
from pytube import Channel
import time
import os
import sys
import colorama
from colorama import init
init(autoreset=True)
from pathlib import Path
from typing import Optional


# Projet "Program Youtube Downloader"

# ------------------------------------------------------------------------------------------- #
# ----------------------------------- CONSTANTES -------------------------------------------- #
# ------------------------------------------------------------------------------------------- #
TITLE_PROGRAM = "Program Youtube Downloader"

TITLE_QUESTION_MENU_ACCUEIL = "Que voulez-vous télécharger sur Youtube ?"
CHOICE_MENU_ACCUEIL : tuple[str, ...] = (
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
def clear_screen() -> None:
    if(os.name == 'posix'):
        os.system('clear')
    else:
        os.system('cls')


def program_break_time(memorization_time:int, affichage_text:str) -> None:
    duree_restante_avant_lancement = memorization_time
    print(f"{affichage_text} {memorization_time} secondes ", end="", flush=True)
    for i in range(memorization_time):
        time.sleep(1)
        print(".", end="", flush=True)
        duree_restante_avant_lancement -= 1


def seprateur_menu_affichage() -> None:
    print("*************************************************************")


def demander_valeur_numerique_utilisateur(valeur_min:int, valeur_max:int) -> int:
    v_str = input(f"Donnez une valeur entre {valeur_min} et {valeur_max} : \n --> " )
    try:
        v_int = int(v_str)
    except:
        print("FAIL : Vous devez rentrer une valeur numérique.")
        print()
        return demander_valeur_numerique_utilisateur(valeur_min, valeur_max)
    if not (valeur_min <= v_int <= valeur_max):
        print(f"FAIL : Vous devez rentrer un nombre (entre {valeur_min} et {valeur_max} ).")
        print()
        return demander_valeur_numerique_utilisateur(valeur_min, valeur_max)

    return v_int


def afficher_menu_acceuil() -> int:
    print()
    print()
    seprateur_menu_affichage()
    print(f"*            {TITLE_PROGRAM}                     *")
    seprateur_menu_affichage()
    print(f"{TITLE_QUESTION_MENU_ACCUEIL}                          ")
    print()
    i = 0
    for items in CHOICE_MENU_ACCUEIL:
        choix_menu = items
        i += 1
        print(f"    {i} - {choix_menu}                              ")
    print("                                                           ")
    seprateur_menu_affichage() 
    valeur_choix_maximale = i
    
    return valeur_choix_maximale


def demander_save_file_path() -> str:
    print()
    print()
    seprateur_menu_affichage()
    print("*             Sauvegarde fichier                            *")
    seprateur_menu_affichage()
    save_path =  input("Indiquez l'endroit où vous voulez stocker le fichier : \n --> ")
    
    return save_path


def demander_url_vidéo_youtube() -> str:
    print()
    print()
    seprateur_menu_affichage()
    print("*             Url de votre vidéo Youtube                    *")
    seprateur_menu_affichage()
    url =  input("Indiquez l'url de la vidéo Youtube : \n --> ")
    url = url.replace('https://www.youtube.com/@', 'https://www.youtube.com/c/')
    if url.lower().startswith(BASE_YOUTUBE_URL):
        return url
    
    print("ERREUR : Vous devez renter une URL de vidéo youtube")
    print("le prefixe attendu est : https://www.youtube.com/")
    return demander_url_vidéo_youtube()
        
    
def demander_youtube_link_file() -> list[str]:
    link_url_video_youtube_final: list[str] = []
    print()
    print()
    seprateur_menu_affichage()
    print("*             Fichier contenant les urls Youtube            *")
    seprateur_menu_affichage()
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
        
        if not number_links_file:
            print("[ERREUR] : Vous devez fournir un fichier avec au minimum une URL de vidéo youtube")
            return demander_youtube_link_file()

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


def on_download_progress(stream, chunk, bytes_remaining) -> None:
    """ 
    Fonction : 
    - Quand il y a une progression dans le téléchargement
    - Permet d'afficher les pourcentages restant à télécharger
    """
    total_bytes_download = stream.filesize
    bytes_downloaded = stream.filesize - bytes_remaining
    progress = (bytes_downloaded / total_bytes_download) * 100
    progress_bar(progress)
    

def progress_bar(progress: float, size=35, sides="||", full='█', empty=' ' , prefix_start="Downloading ...", prefix_end = "Download OK ...", color_text=colorama.Fore.WHITE, color_Downloading=colorama.Fore.LIGHTYELLOW_EX, color_Download_OK=colorama.Fore.GREEN) -> None:
    """
        progress: Un nombre représentant l'état d'avancement, exprimé en pourcentage (de 00.00 à 100.00).
        size: La taille totale de la barre de progression, exprimé en nombre de caractères utilisés pour afficher la barre (par défaut, 30).
        sides: Les caractères utilisés pour dessiner les bords de la barre de progression (par défaut, "||").
        full: Le caractère utilisé pour représenter la partie "remplie" de la bar de téléchargement. c'est la partie téléchargé (par défaut, "█").
        empty: Le caractère utilisé pour représenter la partie "vide" de la bar de téléchargement. c'est la partie non téléchargée (par défaut, un espace).
        prefix: Un texte optionnel à afficher avant la barre de progression (par défaut, "Downloading...").
        color_text, color_Downloading, color_Download_OK: Des paramètres pour spécifier les couleurs du texte affiché.

        variable (x) : multiplie la taille totale de la barre de progression (size) par la valeur décimale du pourcentage d'avancement (progress / 100).
        Cela donne la position relative de la progression en fonction de la taille totale de la barre de progression. 
        Par exemple, si (size) est de 30 caractères et (progress) est de 50%, cela donnerait 15, ce qui signifie que la moitié de la barre de progression doit être remplie. 
    """
    x = int(size * progress / 100)
    bar = sides[0] + full * x + empty * (size - x) + sides[1]
    sys.stdout.write(color_text + "\r" + prefix_start + color_Downloading + bar + f" {progress:.2f}% ")
    
    if progress == 100:
        sys.stdout.write("\r" + color_text + prefix_end + color_Download_OK + bar + f" {progress:.2f}% ")
        print(colorama.Fore.RESET)
    
    sys.stdout.flush()


def demander_choice_resolution_vidéo_or_bitrate_audio(download_sound_only:bool, list_available_streams) -> int:
    i = 0
    valeur_choix_maximale = i
    
    if download_sound_only:
        print()
        print()
        seprateur_menu_affichage()
        print("*             Choississez la qualité audio                  *")
        seprateur_menu_affichage()
        for stream in list_available_streams:
            choix_menu = stream.abr # Pour la qualité de l'audio
            i += 1
            print(f"      {i} - {choix_menu} ") 
            valeur_choix_maximale = i
        
        seprateur_menu_affichage()
        v_int = demander_valeur_numerique_utilisateur(1, valeur_choix_maximale)
        return v_int
        
    print()
    print()
    seprateur_menu_affichage()
    print("*             Choississez la résolution vidéo               *")
    seprateur_menu_affichage()
    for stream in list_available_streams:
        choix_menu = stream.resolution # pour la qualite de la vidéo
        i += 1
        print(f"      {i} - {choix_menu} ")
        valeur_choix_maximale = i
    
    seprateur_menu_affichage()
    v_int = demander_valeur_numerique_utilisateur(1, valeur_choix_maximale)
    return v_int


def streams_video(download_sound_only: bool, youtube_video: YouTube):
    try:
        if download_sound_only:
            # streams = youtube_video.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc()
            streams = youtube_video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
        else:
            streams = youtube_video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
        
        return streams

    except HTTPError as e:
        print(f"[ERREUR] : Impossible d'accéder aux flux pour la vidéo. Code HTTP : {e.code}, Message : {e.reason}")
        return None

    except Exception as e:
        print(f"[ERREUR] : Une erreur inattendue s'est produite lors de la récupération des flux : {e}")
        return None



def conversion_mp4_in_mp3(file_downloaded:str) -> None:
    base, ext = os.path.splitext(file_downloaded) # os.path.splitext('myFile.txt') : renvoie un tuple ('myFile', '.txt') :
    try:
        new_file = base + '.mp3'
        os.rename(file_downloaded, new_file)
        if Path(file_downloaded).exists():
        # if os.path.exists(file_downloaded): # os.path.exists('/myDir/myFile') : renvoie True si le fichier ou directory existe.
                                            # Si c'est un lien symbolique qui pointe vers un fichier qui n'existe pas, renvoie False
            os.remove(file_downloaded)
    except:
        print("[WARMING] un fichier MP3 portant le même nom, déjà existant!")
        os.remove(file_downloaded)
        print()


# def download_multiple_videos(url_youtube_video_links:list[str], download_sound_only:bool) -> list[str] | None:
def download_multiple_videos(url_youtube_video_links: list[str], download_sound_only: bool) -> Optional[list[str]]:
    """ 
    Fonction général qui contient 7 autres fonctions : 
    - step 1 : choisir l'endroit de la sauvegarde
        # demander_save_file_path()
    - step 2 : affiche la progression de téléchargement de la vidéo
        # youtube_video.register_on_progress_callback(on_download_progress)
    - step 3 : recuperation des différents streams du lien de la vidéo
        # streams_video(download_sound_only, youtube_video)
    - step 4 : choisir la resolution vidéo ou qualité audio
        # demander_choice_resolution_vidéo_or_bitrate_audio(download_sound_only, streams)
    - step 5 : permet de faire des pause dans le programm en affichant un texte
        # program_break_time(5,"le téléchargement va commencer dans" )
    - step 6 : téléchargement du fichier
        # stream.download(output_path=save_path)
    - step 7 : conversion mp4 en mp3, si necessaire
        # conversion_mp4_in_mp3(out_file)
    """
    choice_once_bitrate_audio_or_resolution_video_user = True
    save_path = demander_save_file_path()

    if not url_youtube_video_links:
        print("[ERREUR] : il y a aucune vidéo à télécharger")
        return url_youtube_video_links

    for url_video in url_youtube_video_links:
        try:
            youtube_video = YouTube(url_video)
            youtube_video.register_on_progress_callback(on_download_progress)
        except KeyError as e:
            print(f"[ERREUR] : Problème de clé dans les données : {e}")
            continue
        except Exception as e:
            print(f"[ERREUR] : Connexion à la vidéo impossible : {e}")
            continue

        streams = streams_video(download_sound_only, youtube_video)
        if not streams:
            print(f"[ERREUR] : Les flux pour la vidéo ({url_video}) n'ont pas pu être récupérés.")
            continue

        try:
            video_title = youtube_video.title
        except KeyError as e:
            print(f"[ERREUR] : Impossible d'accéder au titre de la vidéo {url_video}. Détail : {e}")
            continue
        except Exception as e:
            print(f"[ERREUR] : Une erreur inattendue s'est produite lors de l'accès au titre : {e}")
            continue

        if choice_once_bitrate_audio_or_resolution_video_user: # au premier passage, on choisit la qualité et on télécharge toutes les pistes avec cette qualité
            choice_user = demander_choice_resolution_vidéo_or_bitrate_audio(download_sound_only, streams)
            choice_once_bitrate_audio_or_resolution_video_user = False 
            print()
            print()
            seprateur_menu_affichage()
            print("*             Stream vidéo selectionnée:                    *")
            seprateur_menu_affichage()
            print('Number of link url video youtube in file: ', len(url_youtube_video_links))
            print()

        itag = streams[choice_user-1].itag # type: ignore
        stream = youtube_video.streams.get_by_itag(itag)
        
        print(f"Titre: {video_title[0:53]}")
        # print(f"Titre: " + youtube_video.title[0:53])
        # program_break_time(5,"le téléchargement va commencer dans" )
        # print()
        
        # control exist the file mp4
        current_file = save_path + "\\" + stream.default_filename # type: ignore
        if Path(current_file).exists(): # os.path.exists('/myDir/myFile') : renvoie True si le fichier ou directory existe.
                                        # Si c'est un lien symbolique qui pointe vers un fichier qui n'existe pas, renvoie False
            print("[WARMING] un fichier MP4 portant le même nom, déjà existant!")   
        
        # downloading the file mp4
        try:
            out_file = stream.download(output_path=save_path) # type: ignore
            print("")  
        except Exception as e:
            print("")
            print(f"[ERREUR] : le téléchargement a échoué : {e}")
            print("")
            continue
        
        if out_file:
            if download_sound_only:
                conversion_mp4_in_mp3(out_file)
        else:
            print("[ERREUR] : Fichier de sortie non valide. Le fichier n'a pas pu être téléchargé.")


    print()
    print("Fin du téléchargement")
    seprateur_menu_affichage()
    print()
    input("Appuyer sur ENTREE pour revenir au menu d'accueil")
    program_break_time(3,"Le menu d'accueil va revenir dans" )
    clear_screen()
    
    return None
