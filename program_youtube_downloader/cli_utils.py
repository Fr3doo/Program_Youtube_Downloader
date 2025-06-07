"""Utility helpers for interactive CLI prompts."""

from pathlib import Path
import logging
from typing import Iterable, Any

from .exceptions import ValidationError

from .constants import (
    TITLE_PROGRAM,
    TITLE_QUESTION_MENU_ACCUEIL,
    CHOICE_MENU_ACCUEIL,
)
from .youtube_downloader import program_break_time, clear_screen
from .validators import validate_youtube_url

logger = logging.getLogger(__name__)


def print_separator() -> None:
    """Print a decorative separator line used in menus."""
    print("*************************************************************")


def ask_numeric_value(valeur_min: int, valeur_max: int, max_attempts: int = 3) -> int:
    """Prompt the user to enter a number between ``valeur_min`` and ``valeur_max``.

    Args:
        valeur_min: Minimum acceptable value.
        valeur_max: Maximum acceptable value.
        max_attempts: Number of invalid attempts allowed before a
            :class:`ValidationError` is raised.

    Returns:
        The validated integer entered by the user.

    Raises:
        ValidationError: If the user fails to provide a valid value within the
            allowed number of attempts.
    """
    attempts = 0
    while True:
        v_str = input(
            f"Donnez une valeur entre {valeur_min} et {valeur_max} : \n --> "
        )
        try:
            v_int = int(v_str)
        except ValueError:
            logger.warning("FAIL : Vous devez rentrer une valeur numérique.")
            logger.info("")
            attempts += 1
            if attempts >= max_attempts:
                raise ValidationError("Nombre de tentatives dépassé")
            continue
        if not (valeur_min <= v_int <= valeur_max):
            logger.warning(
                f"FAIL : Vous devez rentrer un nombre (entre {valeur_min} et {valeur_max} )."
            )
            logger.info("")
            attempts += 1
            if attempts >= max_attempts:
                raise ValidationError("Nombre de tentatives dépassé")
            continue

        return v_int


def display_main_menu() -> int:
    """Display the main menu and return the number of choices."""
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


def ask_save_file_path(max_attempts: int = 3) -> Path:
    """Prompt for a destination directory and create it if necessary.

    Args:
        max_attempts: Number of invalid attempts permitted before raising a
            :class:`ValidationError`.

    Returns:
        The resolved :class:`~pathlib.Path` chosen by the user.

    Raises:
        ValidationError: If ``max_attempts`` invalid paths are entered or the
            directory cannot be created.
    """

    attempts = 0
    while True:
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
                    logger.exception("Directory creation failed")
                    logger.error("[ERREUR] : Impossible de créer le dossier")
                    attempts += 1
                    if attempts >= max_attempts:
                        raise ValidationError("Création du dossier impossible")
                    continue
            else:
                logger.error("[ERREUR] : Le dossier n'existe pas")
                attempts += 1
                if attempts >= max_attempts:
                    raise ValidationError("Dossier invalide")
                continue

        return path


def ask_youtube_url(max_attempts: int = 3) -> str:
    """Ask the user to provide a single YouTube video URL.

    Args:
        max_attempts: Number of tries allowed before a
            :class:`ValidationError` is raised.

    Returns:
        A validated URL string.

    Raises:
        ValidationError: If the provided URLs are invalid ``max_attempts``
            times in a row.
    """
    attempts = 0
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
        if validate_youtube_url(url):
            return url

        logger.error("ERREUR : Vous devez renter une URL de vidéo youtube")
        logger.error("le prefixe attendu est : https://www.youtube.com/")
        attempts += 1
        if attempts >= max_attempts:
            raise ValidationError("URL invalide")


def ask_youtube_link_file(max_attempts: int = 3) -> list[str]:
    """Load a list of YouTube URLs from a text file.

    Args:
        max_attempts: Number of times to retry reading a valid file before
            raising :class:`ValidationError`.

    Returns:
        A list containing all valid URLs found in the file.

    Raises:
        ValidationError: If no valid URLs can be read after ``max_attempts``
            attempts or the file is not accessible.
    """

    attempts = 0
    while True:
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
                    logger.error("[ERREUR] : Vous devez fournir un fichier avec au minimum une URL de vidéo youtube")
                    attempts += 1
                    if attempts >= max_attempts:
                        raise ValidationError("Aucune URL valide")
                    continue

                for i in range(0, len(lignes)):
                    url_video = lignes[i].strip()
                    compteur_ligne += 1

                    if validate_youtube_url(url_video):
                        link_url_video_youtube_final.append(url_video)
                    else:
                        logger.error("[ERREUR] : ")
                        logger.error("le prefixe attendu est : https://www.youtube.com/")
                        logger.error(f"  le lien sur la ligne n° {compteur_ligne} ne sera pas télécharger")
                        logger.error("")
                        number_erreur += 1

                if number_erreur == number_links_file:
                    logger.error("[ERREUR] : Vous devez fournir un fichier avec au minimum une URL de vidéo youtube")
                    attempts += 1
                    if attempts >= max_attempts:
                        raise ValidationError("Aucune URL valide")
                    continue
        except OSError:
            logger.exception("[ERREUR] : Le fichier n'est pas accessible")
            logger.error("[ERREUR] : Le fichier n'est pas accessible")
            attempts += 1
            if attempts >= max_attempts:
                raise ValidationError("Fichier inaccessible")
            continue

        return link_url_video_youtube_final


def ask_resolution_or_bitrate(
    download_sound_only: bool, list_available_streams: Iterable[Any]
) -> int:
    """Prompt the user to choose a resolution or bitrate from ``list_available_streams``.

    Args:
        download_sound_only: If ``True`` ``list_available_streams`` contains
            audio streams and the user selects a bitrate. Otherwise it contains
            video streams and the user selects a resolution.
        list_available_streams: Iterable of stream objects returned by
            ``pytubefix``.

    Returns:
        The index (1-based) of the chosen stream in ``list_available_streams``.
    """
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


def print_end_download_message() -> None:
    """Print a short message indicating that all downloads completed."""
    logger.info("")
    logger.info("Fin du téléchargement")
    print_separator()
    logger.info("")


def pause_return_to_menu() -> None:
    """Wait for the user to press ENTER then clear the screen."""
    input("Appuyer sur ENTREE pour revenir au menu d'accueil")
    program_break_time(3, "Le menu d'accueil va revenir dans")
    clear_screen()
