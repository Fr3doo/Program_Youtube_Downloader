"""Utility helpers for interactive CLI prompts."""

from pathlib import Path
import logging
from typing import Iterable, Any

from .exceptions import ValidationError, DirectoryCreationError, InvalidURLError

from .constants import (
    TITLE_PROGRAM,
    TITLE_QUESTION_MENU_ACCUEIL,
    CHOICE_MENU_ACCUEIL,
)
from .utils import program_break_time, clear_screen, log_blank_line
from .validators import validate_youtube_url

logger = logging.getLogger(__name__)


def print_separator() -> None:
    """Print a decorative separator line used in menus."""
    print("*************************************************************")


def ask_numeric_value(min_value: int, max_value: int, max_attempts: int = 3) -> int:
    """Prompt the user to enter a number between ``min_value`` and ``max_value``.

    Args:
        min_value: Minimum acceptable value.
        max_value: Maximum acceptable value.
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
            f"Donnez une valeur entre {min_value} et {max_value} : \n --> "
        )
        try:
            v_int = int(v_str)
        except ValueError:
            logger.warning("Entrée invalide : saisissez une valeur numérique.")
            log_blank_line()
            attempts += 1
            if attempts >= max_attempts:
                raise ValidationError("Nombre de tentatives dépassé")
            continue
        if not (min_value <= v_int <= max_value):
            logger.warning(
                "Entrée invalide : saisissez un nombre entre "
                f"{min_value} et {max_value}."
            )
            log_blank_line()
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
        menu_choice = items
        i += 1
        print(f"    {i} - {menu_choice}                              ")
    print("                                                           ")
    print_separator()
    max_choice_value = i

    return max_choice_value


def ask_save_file_path(max_attempts: int = 3) -> Path:
    """Prompt for a destination directory and create it if necessary.

    Args:
        max_attempts: Number of invalid attempts permitted before raising a
            :class:`ValidationError`.

    Returns:
        The resolved :class:`~pathlib.Path` chosen by the user.

    Raises:
        ValidationError: If ``max_attempts`` invalid paths are entered.
        DirectoryCreationError: If the directory cannot be created after
            ``max_attempts`` retries.
    """

    attempts = 0
    while True:
        print()
        print()
        print_separator()
        print("*             Sauvegarde fichier                            *")
        print_separator()

        save_path = input(
            "Indiquez l'endroit où vous voulez stocker le fichier : \n --> "
        )
        path = Path(save_path).expanduser().resolve()

        if path.is_file():
            path = path.parent

        if not path.exists():
            create = input("Le dossier n'existe pas. Voulez-vous le créer ? [y/N] : ")
            if create.lower().startswith("y"):
                try:
                    path.mkdir(parents=True, exist_ok=True)
                except OSError:
                    logger.exception("Échec de la création du dossier")
                    logger.error("Impossible de créer le dossier")
                    attempts += 1
                    if attempts >= max_attempts:
                        raise DirectoryCreationError("Création du dossier impossible")
                    continue
            else:
                logger.error("Le dossier n'existe pas")
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
        try:
            validate_youtube_url(url)
            return url
        except InvalidURLError:
            logger.error("URL invalide : vous devez saisir le lien d'une vidéo YouTube")
            logger.error("Préfixe attendu : https://www.youtube.com/")
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
        valid_urls: list[str] = []
        print()
        print()
        print_separator()
        print("*             Fichier contenant les urls Youtube            *")
        print_separator()
        user_file = input("Indiquez le nom du fichier : \n --> ")
        print()
        try:
            file_path = Path(user_file)
            with file_path.open("r", encoding="utf-8") as f:
                lines = f.readlines()
                error_count = 0
                total_links = len(lines)

                if not total_links:
                    logger.error(
                        "Vous devez fournir un fichier contenant au moins une"
                        " URL de vidéo YouTube"
                    )
                    attempts += 1
                    if attempts >= max_attempts:
                        raise ValidationError("Aucune URL valide")
                    continue

                for line_counter, line in enumerate(lines, 1):
                    video_url = line.strip()

                    try:
                        validate_youtube_url(video_url)
                        valid_urls.append(video_url)
                    except InvalidURLError:
                        logger.error(
                            "URL invalide à la ligne "
                            f"{line_counter} ; le préfixe attendu est : "
                            "https://www.youtube.com/"
                        )
                        logger.error("")
                        error_count += 1

                if error_count == total_links:
                    logger.error(
                        "Vous devez fournir un fichier contenant au moins une"
                        " URL de vidéo YouTube"
                    )
                    attempts += 1
                    if attempts >= max_attempts:
                        raise ValidationError("Aucune URL valide")
                    continue
        except OSError:
            logger.exception("Le fichier n'est pas accessible")
            logger.error("Le fichier n'est pas accessible")
            attempts += 1
            if attempts >= max_attempts:
                raise ValidationError("Fichier inaccessible")
            continue

        return valid_urls


def ask_resolution_or_bitrate(
    download_sound_only: bool, list_available_streams: Iterable[Any]
) -> int:
    """Prompt the user to choose a resolution or bitrate.

    The options are taken from ``list_available_streams``.

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
    max_choice_value = i

    if download_sound_only:
        print()
        print()
        print_separator()
        print("*             Choisissez la qualité audio                  *")
        print_separator()
        for stream in list_available_streams:
            menu_choice = stream.abr  # Audio quality
            i += 1
            print(f"      {i} - {menu_choice} ")
            max_choice_value = i

        print_separator()
        v_int = ask_numeric_value(1, max_choice_value)
        return v_int

    print()
    print()
    print_separator()
    print("*             Choisissez la résolution vidéo               *")
    print_separator()
    for stream in list_available_streams:
        menu_choice = stream.resolution  # Video quality
        i += 1
        print(f"      {i} - {menu_choice} ")
        max_choice_value = i

    print_separator()
    v_int = ask_numeric_value(1, max_choice_value)
    return v_int


def print_end_download_message() -> None:
    """Print a short message indicating that all downloads completed."""
    log_blank_line()
    logger.info("Fin du téléchargement")
    print_separator()
    log_blank_line()


def pause_return_to_menu() -> None:
    """Wait for the user to press ENTER then clear the screen."""
    input("Appuyer sur ENTREE pour revenir au menu d'accueil")
    program_break_time(3, "Le menu d'accueil va revenir dans")
    clear_screen()


__all__ = [
    "print_separator",
    "ask_numeric_value",
    "display_main_menu",
    "ask_save_file_path",
    "ask_youtube_url",
    "ask_youtube_link_file",
    "ask_resolution_or_bitrate",
    "print_end_download_message",
    "pause_return_to_menu",
]
