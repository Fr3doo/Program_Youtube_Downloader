# from asyncio import streams
# https://github.com/JuanBindez/pytubefix
# https://pypi.org/project/pytubefix/
"""Miscellaneous helpers used by the application."""

import time
import os
import subprocess
import logging

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.ERROR)


# Projet "Program Youtube Downloader"

# ------------------------------------------------------------------------------------------- #
# ----------------------------------- CONSTANTES -------------------------------------------- #
# ------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------- #
# ----------------------------------- FONCTIONS --------------------------------------------- #
# ------------------------------------------------------------------------------------------- #
def clear_screen() -> None:
    """Clear the terminal screen on Windows or POSIX systems."""
    if os.name == 'posix':
        subprocess.run(["clear"], check=True)
    else:
        subprocess.run(["cmd", "/c", "cls"], check=True)


def program_break_time(memorization_time: int, affichage_text: str) -> None:
    """Display a short countdown.

    Args:
        memorization_time: Duration of the countdown in seconds.
        affichage_text: Message displayed before the countdown number.
    """
    duree_restante_avant_lancement = memorization_time
    print(
        f"{affichage_text} {memorization_time} secondes ",
        end="",
        flush=True,
    )
    while duree_restante_avant_lancement > 0:
        time.sleep(1)
        print(f"{duree_restante_avant_lancement} ", end="", flush=True)
        duree_restante_avant_lancement -= 1





