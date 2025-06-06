# from asyncio import streams
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
import logging

logging.basicConfig(level=logging.ERROR)


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


def print_separator() -> None:
    """Display a visual separator used in menus."""
    print("*************************************************************")


def ask_numeric_value(valeur_min: int, valeur_max: int) -> int:
    """Ask the user for a numeric value within a range."""
    v_str = input(f"Donnez une valeur entre {valeur_min} et {valeur_max} : \n --> " )
    try:
        v_int = int(v_str)
    except ValueError:
        print("FAIL : Vous devez rentrer une valeur numérique.")
        print()
        return ask_numeric_value(valeur_min, valeur_max)
    if not (valeur_min <= v_int <= valeur_max):
        print(f"FAIL : Vous devez rentrer un nombre (entre {valeur_min} et {valeur_max} ).")
        print()
        return ask_numeric_value(valeur_min, valeur_max)

    return v_int


def afficher_menu_acceuil() -> int:
    print()
    print()
    print_separator()
    print(f"*            {TITLE_PROGRAM}                     *")
    print_separator()
    print(f"{TITLE_QUESTION_MENU_ACCUEIL}                          ")
    print()
    i = 0
    for items in CHOICE_MENU_ACCUEIL:
        choix_menu = items
        i += 1
        print(f"    {i} - {choix_menu}                              ")
    print("                                                           ")
    print_separator() 
    valeur_choix_maximale = i
    
    return valeur_choix_maximale


def demander_save_file_path() -> Path:
    print()
    print()
    print_separator()
    print("*             Sauvegarde fichier                            *")
    print_separator()
    save_path = input("Indiquez l'endroit où vous voulez stocker le fichier : \n --> ")

    return Path(save_path)


def ask_youtube_url() -> str:
    """Prompt the user for a YouTube video URL."""
    print()
    print()
    print_separator()
    print("*             Url de votre vidéo Youtube                    *")
    print_separator()
    url =  input("Indiquez l'url de la vidéo Youtube : \n --> ")
    url = url.replace('https://www.youtube.com/@', 'https://www.youtube.com/c/')
    if url.lower().startswith(BASE_YOUTUBE_URL):
        return url
    
    print("ERREUR : Vous devez renter une URL de vidéo youtube")
    print("le prefixe attendu est : https://www.youtube.com/")
    return ask_youtube_url()
        
    
def demander_youtube_link_file() -> list[str]:
    link_url_video_youtube_final: list[str] = []
    print()
    print()
    print_separator()
    print("*             Fichier contenant les urls Youtube            *")
    print_separator()
    fichier_user = input("Indiquez le nom du fichier : \n --> ")
    print()
    try:
        file_path = Path(fichier_user)
        with file_path.open("r") as fichier:
            lignes = fichier.readlines()  # .readlines() pour tout lire et recuperer une List [] en retour
            compteur_ligne = 0
            number_erreur = 0
            number_links_file = len(lignes)

            if not number_links_file:
                print("[ERREUR] : Vous devez fournir un fichier avec au minimum une URL de vidéo youtube")
                return demander_youtube_link_file()

            for i in range(0, len(lignes)):
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
    except OSError as e:
        logging.exception("[ERREUR] : Le fichier n'est pas accessible")
        print("[ERREUR] : Le fichier n'est pas accessible")

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
        print_separator()
        print("*             Choississez la qualité audio                  *")
        print_separator()
        for stream in list_available_streams:
            choix_menu = stream.abr # Pour la qualité de l'audio
            i += 1
            print(f"      {i} - {choix_menu} ") 
            valeur_choix_maximale = i
        
        print_separator()
        v_int = ask_numeric_value(1, valeur_choix_maximale)
        return v_int
        
    print()
    print()
    print_separator()
    print("*             Choississez la résolution vidéo               *")
    print_separator()
    for stream in list_available_streams:
        choix_menu = stream.resolution # pour la qualite de la vidéo
        i += 1
        print(f"      {i} - {choix_menu} ")
        valeur_choix_maximale = i
    
    print_separator()
    v_int = ask_numeric_value(1, valeur_choix_maximale)
    return v_int


