# from asyncio import streams
# https://github.com/JuanBindez/pytubefix
# https://pypi.org/project/pytubefix/
from pytube import Playlist
from pytube import Channel
import time
import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.ERROR)


# Projet "Program Youtube Downloader"

# ------------------------------------------------------------------------------------------- #
# ----------------------------------- CONSTANTES -------------------------------------------- #
# ------------------------------------------------------------------------------------------- #
from .constants import (
    TITLE_PROGRAM,
    TITLE_QUESTION_MENU_ACCUEIL,
    CHOICE_MENU_ACCUEIL,
    BASE_YOUTUBE_URL,
)

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





