# Guide : gestionnaire de progression personnalisé

Ce tutoriel explique comment créer et utiliser un gestionnaire de progression
autre que ceux fournis dans `program_youtube_downloader.progress`.

## Exemple minimal

Le protocole `ProgressHandler` définit simplement la méthode
`on_progress(event)`. Il suffit de fournir un objet possédant cette méthode
pour recevoir les mises à jour :

```python
from pathlib import Path
from program_youtube_downloader.downloader import YoutubeDownloader
from program_youtube_downloader.config import DownloadOptions
from program_youtube_downloader.progress import ProgressEvent, ProgressHandler

class EmojiHandler:
    def on_progress(self, event: ProgressEvent) -> None:
        print(f"🍿 {event.percent:.0f}%")

handler = EmojiHandler()
yd = YoutubeDownloader(progress_handler=handler)
options = DownloadOptions(save_path=Path("videos"))
yd.download_multiple_videos(["https://youtu.be/example"], options)
```

`YoutubeDownloader` se charge d'enregistrer le callback auprès de `pytubefix` et
convertit les notifications en objets `ProgressEvent`. Vous pouvez également
passer le gestionnaire via `DownloadOptions(progress_handler=handler)`.
