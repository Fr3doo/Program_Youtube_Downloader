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





