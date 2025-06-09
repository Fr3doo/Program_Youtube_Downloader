# Présentation de la base de code

Ce document résume le fonctionnement global du projet **Program Youtube Downloader** en français. Il est basé sur une explication destinée à un néophyte.

## Vue d'ensemble

Le dépôt contient un outil en ligne de commande permettant de télécharger des vidéos ou l'audio depuis YouTube. La configuration du projet et l'installation des dépendances sont décrites dans `pyproject.toml`, qui déclare un script `program-youtube-downloader` exécutant `program_youtube_downloader.main:main`.

Le README précise les fichiers clés et leur rôle : `program_youtube_downloader/main.py` pour la boucle de menu, `downloader.py` pour les téléchargements et conversions, `cli_utils.py` pour les interactions utilisateur, `constants.py` pour les messages du menu, `progress.py` pour la barre de progression, `validators.py` pour vérifier les URL, `config.py` pour l'objet `DownloadOptions`, et `youtube_downloader.py` pour des utilitaires divers.

## Nouveautés

- **Classe `CLI`** : la gestion du menu interactif a été déplacée dans une classe dédiée (`program_youtube_downloader/cli.py`) afin de simplifier les tests et la réutilisation.
- **Exécution parallèle** : lorsqu'une liste de liens est fournie, les téléchargements peuvent être lancés simultanément pour gagner du temps.

## Organisation en « agents »

Le fichier `AGENTS.md` décrit chaque *agent* (groupe de responsabilités) en indiquant son point d'entrée principal :

- **Agent CLI** : `main()` dans `program_youtube_downloader/main.py` gère les arguments et lance une sous-commande ou un menu interactif.
- **Agent de téléchargement** : `download_multiple_videos()` dans `downloader.py` se charge d'obtenir les flux vidéo via `pytubefix` et de les enregistrer.
- **Agent de conversion** : `conversion_mp4_in_mp3()` dans `downloader.py` renomme un fichier MP4 en MP3 et supprime l'original.
- **Agent de progression** : `on_download_progress` et `progress_bar` dans `progress.py` pour l'affichage d'une barre de téléchargement.
- **Agent de validation** : fonctions de `cli_utils.py` et `validators.py` pour vérifier les saisies de l'utilisateur.

Un tableau récapitulatif liste chaque agent avec son fichier et ses fonctions principales. Un diagramme d'interaction montre les dépendances entre eux.

## Fonctionnement général

1. L'utilisateur lance `program-youtube-downloader` depuis le terminal.
2. Le **menu interactif** (ou une sous-commande) propose différents choix : télécharger une vidéo, plusieurs vidéos, une playlist, etc. Les options sont définies dans `constants.py` et affichées par `cli_utils.display_main_menu`.
3. Les saisies de l'utilisateur (URL, dossier de destination, choix de résolution) sont validées par `cli_utils.py` et `validators.py`.
4. Le téléchargeur (`YoutubeDownloader`) récupère les flux via `pytubefix` et signale l'avancement à l'aide d'un `ProgressHandler` (par défaut `ProgressBarHandler`). Il enregistre le fichier puis convertit en MP3 si nécessaire. Tout cela est orchestré par `download_multiple_videos`.
5. `cli_utils.print_end_download_message` et `cli_utils.pause_return_to_menu` signalent la fin du téléchargement et renvoient l'utilisateur au menu principal.

## Tests et bonnes pratiques

Le dossier `tests/` contient des scripts `pytest` couvrant l'analyse des arguments, les fonctions d'aide, la validation des URL et différents scénarios de `YoutubeDownloader`. Le fichier `reference/tests-overview.md` résume cette couverture et montre l'utilisation d'objets factices pour simuler les téléchargements sans accès réseau.

`AGENTS.md` fournit également des conseils pour ajouter de nouveaux agents : maintenir des responsabilités séparées et écrire des tests unitaires pour toute nouvelle fonctionnalité.

## Repères pour la suite

- Consulter `AGENTS.md` pour comprendre le rôle de chaque module et leurs points d'entrée.
- Le README détaille la procédure d'installation et un exemple d'utilisation du téléchargeur comme bibliothèque.
- Les tests servent de référence pour voir le comportement attendu et comment simuler les téléchargements.
- Pour développer de nouvelles fonctionnalités, créer un nouvel agent ou étendre un agent existant, en documentant son rôle et en écrivant les tests associés.

En résumé, la base de code se compose d'un ensemble de modules Python organisés par responsabilités (*agents*) autour d'un outil CLI. Les fichiers principaux sont simples : un `main` qui traite les arguments ou affiche le menu, un téléchargeur basé sur `pytubefix`, des utilitaires de validation et d'affichage, le tout accompagné d'une suite de tests.

Pour un descriptif détaillé des agents, consultez [AGENTS.md](../AGENTS.md) à la racine du dépôt.
