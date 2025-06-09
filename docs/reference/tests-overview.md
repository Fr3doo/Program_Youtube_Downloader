# Vue d'ensemble des tests

Ce document résume les tests unitaires situés dans le dossier `tests/`. Chaque section explique le but d’un fichier de test ou d’un groupe logique de tests.

## `test_additional.py`

```text
# Classes factices (dummy) réutilisées entre les tests
# Fonctions utilitaires pour l’interface en ligne de commande (CLI)
# Gestion de la progression
# Petites fonctions utilitaires du module youtube_downloader
# Comportements spécifiques à YoutubeDownloader

    Utilitaires CLI – vérifie l'affichage des menus, la sélection de résolution/bitrate,
    la gestion des chemins de fichiers et le traitement des listes d’URLs.

    Utilitaires de progression – teste l’affichage de la barre de progression et le gestionnaire par défaut.

    Fonctions d’aide – teste `program_break_time` et `clear_screen`.

    Comportement du téléchargeur – teste `get_video_streams`, `conversion_mp4_in_mp3`
    et certaines parties de `download_multiple_videos`, y compris les scénarios d’erreur.
```

## `test_callbacks.py`

Vérifie que `YoutubeDownloader.download_multiple_videos` interagit correctement avec les callbacks personnalisés et gère les erreurs du constructeur ou des flux sans planter.

## `test_cli_parse.py`

Valide l’analyse des arguments en ligne de commande :

- bonne détection des sous-commandes et des options
- gestion de l’argument `--log-level` et de la variable d’environnement associée

## `test_cli_utils.py`

Couvre les fonctions d’aide pour les saisies utilisateur :

- validation numérique (`ask_numeric_value`)
- logique d'entrée d’URL (`ask_youtube_url`)
- sélection et création de dossier (`ask_save_file_path`)
- lecture d’un fichier contenant des liens YouTube

## `test_coverage_more.py`

Couvre des cas supplémentaires pour les utilitaires et le point d’entrée principal :

- vérification complète de la barre de progression
- cas limites supplémentaires pour la sélection de chemin et l’analyse de fichiers d’URLs
- tests de type intégration pour les commandes vidéo, playlist, chaîne et menu

## `test_install_launch.py`

Vérifie que le script console est bien déclaré dans `pyproject.toml` et que son
exécution fonctionne après installation dans un environnement temporaire.

## `test_logging_setup.py`

Teste que `setup_logging` définit correctement le niveau de log et qu'aucun
message en dessous de ce niveau n'est émis.

## `test_menu_handlers.py`

Couvre les fonctions de traitement des choix de menu (`handle_*_option`). Les
tests simulent les entrées utilisateur et vérifient la création des options de
téléchargement ainsi que la gestion des erreurs pour les playlists et les
chaînes.

## `test_menu_integration.py`

Valide la fonction interactive `menu()` en simulant les entrées utilisateur avec
`monkeypatch`. Les tests s’assurent qu’un téléchargement est lancé avec les
bonnes options (vidéo ou audio uniquement) selon le choix fourni.

## `test_validators.py`

Confirme que `validate_youtube_url` accepte les URLs valides de YouTube et rejette celles malformées.

## `test_youtube_downloader.py`

Test de régression pour `conversion_mp4_in_mp3` : s’assure que le fichier MP4 est bien supprimé après la conversion.

---

## Résumé de la couverture fonctionnelle

La suite de tests couvre collectivement :

- Les assistants de saisie utilisateur : choix numériques, normalisation d’URL, gestion des fichiers.
- Les parcours menu et ligne de commande.
- Le cœur du téléchargement : callbacks de progression, conversion de fichiers.
- Les fonctions utilitaires pour l’affichage terminal (`clear_screen`, `progress_bar`) et les minuteries.
- Les scripts d’installation et l’exécution de la CLI.
- La configuration du niveau de log.
- La gestion des erreurs : URLs invalides, erreurs de chemin système, échecs HTTP, exceptions au moment de l’instanciation.

Ces tests utilisent des objets factices et le `monkeypatching` pour simuler les téléchargements, ce qui permet de garantir que l’interface en ligne de commande et la logique du téléchargeur se comportent comme prévu, sans effectuer de véritables opérations réseau.
