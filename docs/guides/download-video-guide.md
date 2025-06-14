# Tutoriel : télécharger une vidéo

Ce guide explique comment utiliser rapidement la CLI pour récupérer une vidéo YouTube.

1. **Installation du paquet**
   ```bash
   pip install .
   ```
   La commande `program-youtube-downloader` devient disponible dans votre terminal.

2. **Lancement de l'outil**
   ```bash
   program-youtube-downloader
   ```
   Le menu principal s'affiche avec les différentes options de téléchargement.

3. **Choisir l'option "une vidéo"**
   Sélectionnez l'entrée correspondant au téléchargement d'une vidéo MP4 ou uniquement de l'audio selon votre besoin.

4. **Indiquer l'URL et le dossier de sauvegarde**
   L'outil vous demandera l'adresse complète de la vidéo puis l'emplacement où stocker le fichier.

5. **Sélectionner la qualité**
   Une liste de résolutions ou de débits audio est proposée. Entrez le numéro désiré.

6. **Téléchargement**
   La barre de progression s'affiche. Une fois terminé, un message signale la fin du téléchargement et vous pouvez revenir au menu principal.

Pour aller plus vite, la CLI accepte également les sous-commandes `video`, `playlist` et `channel`. Chacune dispose des options `--audio` pour ne récupérer que la piste son et `--output-dir` pour choisir un dossier de sortie.

Ce tutoriel reste centré sur le menu interactif, mais ces commandes sont utiles aux utilisateurs avancés qui préfèrent tout passer en arguments.
