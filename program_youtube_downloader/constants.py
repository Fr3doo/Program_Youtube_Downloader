"""Shared strings and enumeration used across the application."""

from enum import Enum

# Visual separator used in menus and logs
SEPARATOR = "*************************************************************"

TITLE_PROGRAM = "Program Youtube Downloader"

TITLE_QUESTION_MENU_ACCUEIL = "Que voulez-vous télécharger sur Youtube ?"

CHOICE_MENU_ACCUEIL: tuple[str, ...] = (
    "une vidéo                              - (format mp4)",
    "des vidéos                             - (format mp4)",
    "une playlist vidéo                     - (format mp4)",
    "des vidéos d'une chaîne Youtube        - (format mp4)",
    "la piste audio d'une vidéo             - (format mp3)",
    "les pistes audios de plusieurs vidéos  - (format mp3)",
    "les pistes audios d'une playlist       - (format mp3)",
    "les pistes audios d'une chaîne         - (format mp3)",
    "Quitter le programme",
)


class MenuOption(Enum):
    """Numeric values representing each entry in the main menu."""

    VIDEO = 1
    VIDEOS = 2
    PLAYLIST_VIDEO = 3
    CHANNEL_VIDEOS = 4
    VIDEO_AUDIO_ONLY = 5
    VIDEOS_AUDIO_ONLY = 6
    PLAYLIST_AUDIO_ONLY = 7
    CHANNEL_AUDIO_ONLY = 8
    QUIT = 9

# Base URL used to validate YouTube links throughout the project.
BASE_YOUTUBE_URL = "https://www.youtube.com"

__all__ = [
    "TITLE_PROGRAM",
    "TITLE_QUESTION_MENU_ACCUEIL",
    "CHOICE_MENU_ACCUEIL",
    "MenuOption",
    "BASE_YOUTUBE_URL",
    "SEPARATOR",
]
