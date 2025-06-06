# Program Youtube Downloader

Ce projet permet de télécharger des vidéos ou uniquement la piste audio depuis YouTube grâce à la bibliothèque [pytubefix](https://pypi.org/project/pytubefix/). Une interface en ligne de commande guide l’utilisateur dans le choix du contenu à récupérer (vidéos unitaires, playlists ou chaînes complètes) et dans la qualité souhaitée.

## Prérequis

- Python 3.10 ou plus récent
- Créez un environnement virtuel : `python -m venv .venv`
- Les dépendances listées dans `requirements.txt` :
  - `pytubefix` (pour récupérer correctement les flux YouTube)
  - `colorama` (affichage en couleur)
  - et les paquets utilisés pour l’emballage avec `pyinstaller`

Installez-les avec :

```bash
pip install -r requirements.txt
```

## Lancement

Exécutez simplement le script principal :

```bash
python main.py
```

Un menu s’affichera pour choisir le type de téléchargement (vidéo ou audio, playlist, chaîne, etc.). Les fichiers récupérés sont enregistrés dans le dossier spécifié par l’utilisateur.

Pour générer une version autonome du programme vous pouvez utiliser `pyinstaller` :

```bash
pyinstaller --onefile --add-data "mypy.ini;." --hidden-import "youtube_downloader" main.py
```

## Structure du projet

- `main.py` : point d’entrée du programme contenant la boucle de menu.
- `youtube_downloader.py` : toutes les fonctions de téléchargement (gestion des flux, choix de qualité, conversion en MP3, etc.).
- `requirements.txt` : liste des dépendances Python nécessaires.
- `mypy.ini` : configuration minimale pour `mypy`.

Ce projet est destiné à un usage personnel pour faciliter la récupération de contenu YouTube.
