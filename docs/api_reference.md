# Référence de l'API interne

Cette section décrit brièvement les fonctions et classes disponibles dans le package `program_youtube_downloader`.

## `main.py`
- **`parse_args(argv=None)`** : analyse les arguments de la ligne de commande et retourne un objet `argparse.Namespace`.
- **`menu()`** : lance le menu interactif (non couvert par les tests).
- **`main(argv=None)`** : point d'entrée principal qui redirige vers les sous-commandes ou le menu.

## `downloader.py`
- **`YoutubeDownloader`** : classe principale gérant le téléchargement.
  - `streams_video(download_sound_only, youtube_video)` : retourne les flux disponibles pour une vidéo.
  - `conversion_mp4_in_mp3(path)` : convertit un fichier MP4 en MP3 et supprime l'original.
  - `download_multiple_videos(urls, options)` : télécharge une liste d'URL ou de ressources YouTube.

## `cli_utils.py`
Fonctions d'interaction utilisateur :
- `print_separator()` : affiche un séparateur visuel.
- `ask_numeric_value(min, max)` : demande une valeur numérique.
- `afficher_menu_acceuil()` : affiche le menu principal et retourne le nombre de choix.
- `demander_save_file_path()` : demande un dossier de destination et le crée au besoin.
- `ask_youtube_url()` : invite l'utilisateur à saisir une URL YouTube et la valide.
- `demander_youtube_link_file()` : lit un fichier contenant des URLs YouTube.
- `demander_choice_resolution_vidéo_or_bitrate_audio(sound_only, streams)` : sélectionne la qualité désirée.
- `print_end_download_message()` : indique la fin du téléchargement.
- `pause_return_to_menu()` : attend une touche avant de revenir au menu.

## `validators.py`
- `validate_youtube_url(url)` : vérifie qu'une URL appartient bien à YouTube.

## `progress.py`
- `on_download_progress(stream, chunk, remaining)` : gestionnaire simple de progression.
- `ProgressOptions` : configuration de l'affichage de la barre.
- `progress_bar(progress, options=None)` : affiche une barre de progression dans le terminal.
- `ProgressBarHandler` : implémente `on_progress` pour `pytubefix`.

## `config.py`
- `DownloadOptions` : dataclass regroupant les options de téléchargement (dossier, audio seul, callback de choix, gestionnaire de progression).

## `youtube_downloader.py`
Utilitaires généraux :
- `clear_screen()` : nettoie la console selon le système.
- `program_break_time(seconds, text)` : petite minuterie textuelle.

Ces éléments composent l'API interne du projet et sont utilisés par la CLI ainsi que par les tests unitaires.

## Exceptions
- `DownloadError` : échec répété lors du téléchargement d'un flux.
- `ValidationError` : validation utilisateur impossible après plusieurs essais.
- `PlaylistConnectionError` : connexion à une playlist YouTube impossible.
- `ChannelConnectionError` : connexion à une chaîne YouTube impossible.
- `StreamAccessError` : récupération des flux d'une vidéo impossible.
