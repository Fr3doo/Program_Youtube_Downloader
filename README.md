# Program Youtube Downloader

Ce projet permet de télécharger tous types de contenus YouTube grâce à la bibliothèque [pytubefix](https://pypi.org/project/pytubefix/). Vous pouvez récupérer des vidéos individuelles, des playlists entières ou même toutes les vidéos d’une chaîne, et choisir de n’enregistrer que la piste audio si besoin. Une interface en ligne de commande vous aide à sélectionner précisément ce que vous voulez et la qualité de sortie.

Principales fonctionnalités :

- Téléchargement de vidéos ou des pistes audio seules
- Support des playlists et des chaînes complètes
- Sélection de la qualité et du dossier de destination
- Interface en ligne de commande simplifiée

---

**English summary**

A simple command-line tool for downloading YouTube content using
[pytubefix](https://pypi.org/project/pytubefix/). It requires Python 3.11 or
newer and the dependencies listed in `requirements.txt` installed inside a
virtual environment. After installing the package with `pip install .`,
run the `program-youtube-downloader` command and follow the menu to
download videos, playlists or channels, or to extract audio only.

## Prérequis

- Python 3.11 ou plus récent
- Créez un environnement virtuel : `python -m venv .venv`
- Les dépendances listées dans `requirements.txt` :
  - `pytubefix` (pour récupérer correctement les flux YouTube)
  - `colorama` (affichage en couleur)
  - et les paquets utilisés pour l’emballage avec `pyinstaller`

Pour automatiser la création de `.venv` et l'installation des dépendances,
vous pouvez lancer :

```bash
scripts/setup_env.sh
```

Installez-les avec :

```bash
pip install -r requirements.txt
```

## Installation

Dans votre environnement virtuel, installez le paquet en mode local :

```bash
pip install .
```

La commande `program-youtube-downloader` est alors disponible dans votre shell.

## Lancement

Une fois le paquet installé, lancez le programme avec :

```bash
program-youtube-downloader
```

Vous pouvez également lancer directement une sous-commande pour cibler une
vidéo particulière. Par exemple :

```bash
program-youtube-downloader video https://youtu.be/dQw4w9WgXcQ --audio
```

Un menu s’affichera pour choisir le type de téléchargement (vidéo ou audio, playlist, chaîne, etc.). Les fichiers récupérés sont enregistrés dans le dossier spécifié par l’utilisateur.

Pour générer une version autonome du programme vous pouvez utiliser `pyinstaller` :

```bash
pyinstaller --onefile --add-data "mypy.ini;." program_youtube_downloader/main.py
```

## Aperçu

Voici un exemple de lancement de l'application montrant les différentes options
du menu :

```
Python version: 3.12.10 (main, May 13 2025, 04:05:34) [GCC 13.3.0]
__annotations__ exists: True

*************************************************************
*            Program Youtube Downloader                     *
*************************************************************
Que voulez-vous télécharger sur Youtube ?

    1 - une vidéo                              - (format mp4)
    2 - des vidéos                             - (format mp4)
    3 - une playlist vidéo                     - (format mp4)
    4 - des vidéos d'une chaîne Youtube        - (format mp4)
    5 - la piste audio d'une vidéo             - (format mp3)
    6 - les pistes audios de plusieurs vidéos  - (format mp3)
    7 - les pistes audios d'une playlist       - (format mp3)
    8 - les pistes audios d'une chaîne         - (format mp3)
    9 - Quitter le programme
```
Image :

![Menu](assets/menu_options.png)

## Nouveautés

- **Classe `CLI`** : le menu interactif et les sous-commandes sont désormais gérés par une classe dédiée dans `program_youtube_downloader/cli.py` pour faciliter les tests et la réutilisation.
- **Exécution parallèle** : lors de la récupération de plusieurs liens, les téléchargements peuvent être lancés simultanément pour accélérer le processus.

## Structure du projet

- `program_youtube_downloader/main.py` : point d’entrée du programme contenant la boucle de menu.
- `downloader.py` : logique principale de téléchargement et conversions.
- `cli_utils.py` : fonctions d'interaction utilisateur et gestion des menus.
- `constants.py` : libellés du menu et URL de base communes.
- `progress.py` : gestion de l'affichage de la barre de progression.
- `validators.py` : vérifications des liens YouTube fournis par l'utilisateur.
- `config.py` : objet `DownloadOptions` pour paramétrer les téléchargements.
- `utils.py` : utilitaires généraux (effacement d'écran, compte à rebours).
- `exceptions.py` : définit la base `PydlError` et toutes les exceptions
  dérivées (`DownloadError`, `ValidationError`, etc.).
- `requirements.txt` : liste des dépendances Python nécessaires.
- `mypy.ini` : configuration minimale pour `mypy`.

Exemple d'utilisation en tant que bibliothèque :

```python
from program_youtube_downloader.downloader import YoutubeDownloader
from program_youtube_downloader.config import DownloadOptions

yd = YoutubeDownloader()
options = DownloadOptions(download_sound_only=True)
yd.download_multiple_videos(["https://youtu.be/dQw4w9WgXcQ"], options)
```

### Gestionnaire de progression personnalisé

Le protocole `ProgressHandler` définit la méthode `on_progress`. En
implémentant ce protocole, vous pouvez contrôler l'affichage de la
progression. Injectez votre gestionnaire via
`DownloadOptions(progress_handler=handler)` ou directement au
constructeur `YoutubeDownloader`. Un guide complet est disponible dans
[docs/guides/custom-progress-handler.md](docs/guides/custom-progress-handler.md).

Exemple d'utilisation d'un gestionnaire de progression personnalisé :

```python
from program_youtube_downloader.progress import VerboseProgressHandler

handler = VerboseProgressHandler()
yd = YoutubeDownloader(progress_handler=handler)
```

Vous pouvez également personnaliser l'apparence de la barre de
progression grâce à la dataclass `ProgressOptions` :

```python
from program_youtube_downloader.progress import ProgressBarHandler, ProgressOptions

options = ProgressOptions(size=50, prefix_end="Fini !")
yd = YoutubeDownloader(progress_handler=ProgressBarHandler(options))
```

Pour une description détaillée des agents internes et de leurs responsabilités,
consultez [AGENTS.md](AGENTS.md) à la racine du dépôt.

## Documentation

- [docs/index.md](docs/index.md)
- [docs/project-overview.md](docs/project-overview.md)
- [docs/guides/](docs/guides/)
- [docs/guides/custom-progress-handler.md](docs/guides/custom-progress-handler.md)
- [docs/guides/custom-cli-class.md](docs/guides/custom-cli-class.md)
- [docs/releases/](docs/releases/)
- [docs/reference/api-reference.md](docs/reference/api-reference.md)
- [docs/reference/architecture.md](docs/reference/architecture.md)
- [docs/reference/tests-overview.md](docs/reference/tests-overview.md)

La documentation est organisée sous le dossier `docs/`. Le fichier `docs/index.md`
agit comme page d'accueil et répertorie les différents liens utiles. Les tutoriels
et guides pratiques sont stockés dans `docs/guides/`, tandis que `docs/releases/`
contient le journal des versions. La sous-arborescence `docs/reference/` regroupe
les informations sur l'API interne et l'architecture.

Ce projet est destiné à un usage personnel pour faciliter la récupération de contenu YouTube.

## Journalisation

L'outil utilise le module `logging` de Python pour afficher les messages d'erreur.
Tous les messages affichés dans la console ou dans les journaux sont rédigés en
**français** afin de conserver une interface cohérente.
Par défaut, seuls les messages de niveau `ERROR` sont affichés. Vous pouvez
activer un niveau plus verbeux de deux manières&nbsp;:

1. En définissant la variable d'environnement `PYDL_LOG_LEVEL` avant d'exécuter
    le programme&nbsp;:

    ```bash
    PYDL_LOG_LEVEL=DEBUG program-youtube-downloader video https://youtu.be/example
    ```

2. Ou en utilisant l'option de ligne de commande `--log-level` qui prend le
   pas sur la variable d'environnement&nbsp;:

    ```bash
    program-youtube-downloader --log-level INFO video https://youtu.be/example
    ```

Vous pouvez également passer le dossier de destination directement avec
`--output-dir` pour les sous-commandes `video`, `playlist` et `channel` :

```bash
program-youtube-downloader video https://youtu.be/example --output-dir /chemin/de/sortie
```

Vous pouvez également contrôler le nombre de téléchargements parallèles
en définissant la variable d'environnement `PYDL_MAX_WORKERS` :

```bash
PYDL_MAX_WORKERS=4 program-youtube-downloader video https://youtu.be/example
```

De même, `PYDL_OUTPUT_DIR` permet de choisir un dossier de sortie par défaut et
`PYDL_AUDIO_ONLY` d'activer automatiquement le téléchargement de la piste
audio :

```bash
PYDL_OUTPUT_DIR=/chemin/de/sortie PYDL_AUDIO_ONLY=1 \
    program-youtube-downloader video https://youtu.be/example
```

## Variables d'environnement

Le programme peut être configuré via plusieurs variables :

- **`PYDL_LOG_LEVEL`** détermine le niveau de verbosité du module `logging`. En l'absence de cette variable, le niveau `ERROR` est utilisé.
- **`PYDL_MAX_WORKERS`** fixe le nombre maximal de téléchargements lancés en parallèle. Une valeur trop élevée peut ralentir la connexion.
- **`PYDL_OUTPUT_DIR`** définit le dossier de destination par défaut.
- **`PYDL_AUDIO_ONLY`** force le téléchargement de la piste audio si sa valeur est ``1`` ou ``true``.

Ces paramètres sont lus lors de la création des `DownloadOptions`. Consultez la [partie configuration](docs/reference/api-reference.md#configpy) pour les détails sur le comportement associé.

## Tests

Les tests unitaires sont écrits avec `pytest`. Après l’installation des dépendances, exécutez :

```bash
pytest
```

### Running the test suite

```bash
pip install -r requirements.txt
pytest
```

L'exécution doit se terminer par `91 passed` indiquant que l'ensemble des tests s'est déroulé sans erreur.

## Vérification du style

Un fichier `.flake8` configure les règles de base. Pour lancer la vérification :

```bash
flake8
```

## Pré-commit

Ce dépôt fournit une configuration pour exécuter automatiquement `flake8` et
`pytest` avant chaque commit. Après avoir installé les dépendances de
développement, installez l'outil puis le hook :

```bash
pip install pre-commit
pre-commit install
```

Lancez toutes les vérifications manuellement avec :

```bash
pre-commit run --all-files
```

## Contribuer

Les contributions sont les bienvenues ! Vous pouvez ouvrir une *issue* pour signaler un problème ou demander une fonctionnalité. Pour proposer une correction ou une amélioration, créez une *pull request* depuis votre fork du dépôt.

Veuillez vous assurer que toute utilisation de cet outil respecte les Conditions d'utilisation de YouTube ainsi que les lois en vigueur dans votre pays. Les auteurs du projet déclinent toute responsabilité quant aux conséquences d'un usage inapproprié ou illégal.


