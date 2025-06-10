# Référence de l'API interne

Cette section décrit brièvement les fonctions et classes disponibles dans le package `program_youtube_downloader`.

## `program_youtube_downloader/main.py`
- **`setup_logging(level)`** : configure le module `logging` pour l'application.
- **`parse_args(argv=None)`** : analyse les arguments de la ligne de commande et lit la variable d'environnement `PYDL_LOG_LEVEL` pour le niveau par défaut.
- **`menu()`** : lance le menu interactif (non couvert par les tests).
 - **`main(argv=None, downloader=None, cli_cls=CLI)`** : point d'entrée principal
   qui redirige vers les sous-commandes ou le menu. Le paramètre `cli_cls`
   permet d'utiliser une sous-classe personnalisée de `CLI`.
- **`create_download_options(audio_only, output_dir=None)`** : construit un objet `DownloadOptions` prêt à l'emploi.

## `downloader.py`
- **`YoutubeDownloader`** : classe principale gérant le téléchargement.
  - `get_video_streams(download_sound_only, youtube_video)` : retourne les flux disponibles pour une vidéo.
  - `conversion_mp4_in_mp3(path)` : convertit un fichier MP4 en MP3 et supprime l'original.
  - `download_multiple_videos(urls, options)` : télécharge une liste d'URL ou de ressources YouTube.

## `cli.py`
- `CLI` : interface interactive basée sur `YoutubeDownloader`.

## `cli_utils.py`
Fonctions d'interaction utilisateur :
- `print_separator()` : affiche un séparateur visuel.
- `ask_numeric_value(min, max)` : demande une valeur numérique.
- `display_main_menu()` : affiche le menu principal et retourne le nombre de choix.
- `ask_save_file_path()` : demande un dossier de destination et le crée au besoin.
- `ask_youtube_url()` : invite l'utilisateur à saisir une URL YouTube et la valide.
- `ask_youtube_link_file()` : lit un fichier contenant des URLs YouTube.
- `ask_resolution_or_bitrate(sound_only, streams)` : sélectionne la qualité désirée.
- `print_end_download_message()` : indique la fin du téléchargement.
- `pause_return_to_menu()` : attend une touche avant de revenir au menu.

## `validators.py`
- `validate_youtube_url(url)` : s'assure que le domaine est
  `youtube.com`, `www.youtube.com` ou `youtu.be` et qu'un identifiant vidéo
  unique de 11 caractères est présent (paramètre `v` ou segment
  `youtu.be/<id>`).

## `progress.py`
- `on_download_progress(stream, chunk, remaining)` : gestionnaire simple de progression.
- `ProgressOptions` : dataclass de configuration de la barre.
- `ProgressEvent` : informations structurées sur l'avancement d'un téléchargement.
- `progress_bar(progress, options=None)` : affiche une barre de progression dans le terminal.
- `ProgressBarHandler` : implémente `on_progress` pour `pytubefix`.
- `VerboseProgressHandler` : affiche uniquement le pourcentage sans barre.

## `config.py`
- `DownloadOptions` : dataclass regroupant les options de téléchargement (dossier, audio seul, callback de choix, gestionnaire de progression, nombre de threads). Le champ `max_workers` est initialisé depuis la variable d'environnement `PYDL_MAX_WORKERS` si elle est définie.
- `_max_workers_from_env()` : récupère `PYDL_MAX_WORKERS` et retourne `1` en cas de valeur invalide.

## `legacy_utils.py`
Utilitaires généraux :
- `clear_screen()` : nettoie la console selon le système.
- `program_break_time(seconds, text)` : petite minuterie textuelle.

Ces éléments composent l'API interne du projet et sont utilisés par la CLI ainsi que par les tests unitaires.

## `types.py`
- `YouTubeVideo` : protocole minimal pour représenter un objet `YouTube`.

## `exceptions.py`
- `PydlError` : classe de base pour toutes les erreurs personnalisées.
- `DownloadError` : échec répété lors du téléchargement d'un flux.
- `ValidationError` : validation utilisateur impossible après plusieurs essais.
- `PlaylistConnectionError` : connexion à une playlist YouTube impossible.
- `ChannelConnectionError` : connexion à une chaîne YouTube impossible.
- `StreamAccessError` : récupération des flux d'une vidéo impossible.
- `DirectoryCreationError` : levée lorsque le dossier de destination ne peut pas être créé.
- `InvalidURLError` : levée lorsque une URL ne correspond pas aux schémas YouTube attendus.
