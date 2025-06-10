# Journal des modifications

Ce fichier présente l'historique des évolutions du projet **Program Youtube Downloader**.
Toutes les modifications notables sont listées par version.
Le format est inspiré de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/).

## [Unreleased]
- Ajout de la variable d'environnement `PYDL_LOG_LEVEL` pour contrôler la verbosité des logs.
- Nouvelle dataclass `ProgressOptions` et gestionnaires `ProgressBarHandler`/`VerboseProgressHandler` pour suivre l'avancement des téléchargements.
- Renommage de `youtube_downloader.py` en `utils.py`.
- Les URL des vidéos sont tronquées dans les messages de log pour éviter d'afficher
  l'adresse complète.

## [0.1.0] - 2025-06-06
### Added
- Menu CLI interactif permettant de choisir le type de téléchargement.
- Prise en charge des playlists et des chaînes complètes.
- Conversion optionnelle des vidéos téléchargées en MP3.

