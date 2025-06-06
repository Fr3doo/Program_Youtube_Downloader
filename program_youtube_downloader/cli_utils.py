"""Utility helpers for interactive CLI prompts."""

from pathlib import Path
import logging

from .constants import (
    TITLE_PROGRAM,
    TITLE_QUESTION_MENU_ACCUEIL,
    CHOICE_MENU_ACCUEIL,
    BASE_YOUTUBE_URL,
)


def print_separator() -> None:
    """Display a visual separator used in menus."""
    print("*************************************************************")


def ask_numeric_value(valeur_min: int, valeur_max: int) -> int:
    """Ask the user for a numeric value within a range."""
    while True:
        v_str = input(
            f"Donnez une valeur entre {valeur_min} et {valeur_max} : \n --> "
        )
        try:
            v_int = int(v_str)
        except ValueError:
            logging.warning("FAIL : Vous devez rentrer une valeur numérique.")
            logging.info("")
            continue
        if not (valeur_min <= v_int <= valeur_max):
            logging.warning(
                f"FAIL : Vous devez rentrer un nombre (entre {valeur_min} et {valeur_max} )."
            )
            logging.info("")
            continue

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
    """Ask for a destination directory and ensure it exists."""

    print()
    print()
    print_separator()
    print("*             Sauvegarde fichier                            *")
    print_separator()

    save_path = input("Indiquez l'endroit où vous voulez stocker le fichier : \n --> ")
    path = Path(save_path).expanduser().resolve()

    if path.is_file():
        path = path.parent

    if not path.exists():
        create = input("Le dossier n'existe pas. Voulez-vous le créer ? [y/N] : ")
        if create.lower().startswith("y"):
            try:
                path.mkdir(parents=True, exist_ok=True)
            except OSError:
                logging.exception("Directory creation failed")
                logging.error("[ERREUR] : Impossible de créer le dossier")
                return demander_save_file_path()
        else:
            logging.error("[ERREUR] : Le dossier n'existe pas")
            return demander_save_file_path()

    return path


def ask_youtube_url() -> str:
    """Prompt the user for a YouTube video URL."""
    while True:
        print()
        print()
        print_separator()
        print("*             Url de votre vidéo Youtube                    *")
        print_separator()
        url = input("Indiquez l'url de la vidéo Youtube : \n --> ")
        url = url.replace(
            "https://www.youtube.com/@", "https://www.youtube.com/c/"
        )
        if url.lower().startswith(BASE_YOUTUBE_URL):
            return url

        logging.error("ERREUR : Vous devez renter une URL de vidéo youtube")
        logging.error("le prefixe attendu est : https://www.youtube.com/")


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
            lignes = fichier.readlines()
            compteur_ligne = 0
            number_erreur = 0
            number_links_file = len(lignes)

            if not number_links_file:
                logging.error("[ERREUR] : Vous devez fournir un fichier avec au minimum une URL de vidéo youtube")
                return demander_youtube_link_file()

            for i in range(0, len(lignes)):
                url_video = lignes[i]
                compteur_ligne += 1

                if url_video.lower().startswith(BASE_YOUTUBE_URL):
                    link_url_video_youtube_final.append(url_video)
                else:
                    logging.error("[ERREUR] : ")
                    logging.error("le prefixe attendu est : https://www.youtube.com/")
                    logging.error(f"  le lien sur la ligne n° {compteur_ligne} ne sera pas télécharger")
                    logging.error("")
                    number_erreur += 1

            if number_erreur == number_links_file:
                logging.error("[ERREUR] : Vous devez fournir un fichier avec au minimum une URL de vidéo youtube")
                return demander_youtube_link_file()
    except OSError as e:
        logging.exception("[ERREUR] : Le fichier n'est pas accessible")
        logging.error("[ERREUR] : Le fichier n'est pas accessible")

    return link_url_video_youtube_final


def demander_choice_resolution_vidéo_or_bitrate_audio(download_sound_only: bool, list_available_streams) -> int:
    i = 0
    valeur_choix_maximale = i

    if download_sound_only:
        print()
        print()
        print_separator()
        print("*             Choississez la qualité audio                  *")
        print_separator()
        for stream in list_available_streams:
            choix_menu = stream.abr  # Pour la qualité de l'audio
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
        choix_menu = stream.resolution  # pour la qualite de la vidéo
        i += 1
        print(f"      {i} - {choix_menu} ")
        valeur_choix_maximale = i

    print_separator()
    v_int = ask_numeric_value(1, valeur_choix_maximale)
    return v_int
