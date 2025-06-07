from urllib.error import HTTPError
from pathlib import Path
from typing import Optional, Union, Iterable, Callable, Any
import logging

logger = logging.getLogger(__name__)

from pytubefix import YouTube

from . import cli_utils
from .config import DownloadOptions
from .progress import ProgressHandler, ProgressBarHandler


class YoutubeDownloader:
    """Responsible for fetching streams and saving downloaded files."""

    def __init__(
        self,
        progress_handler: ProgressHandler | None = None,
        youtube_cls: Callable[[str], YouTube] = YouTube,
    ) -> None:
        self.progress_handler = progress_handler or ProgressBarHandler()
        self.youtube_cls = youtube_cls

    def streams_video(
        self, download_sound_only: bool, youtube_video: YouTube
    ) -> Optional[Any]:
        """Return available streams for ``youtube_video``."""
        try:
            if download_sound_only:
                streams = (
                    youtube_video.streams.filter(progressive=True, file_extension="mp4")
                    .order_by("resolution")
                    .desc()
                )
            else:
                streams = (
                    youtube_video.streams.filter(progressive=True, file_extension="mp4")
                    .order_by("resolution")
                    .desc()
                )
            return streams
        except HTTPError as e:
            logger.error(
                "[ERREUR] : Impossible d'accéder aux flux pour la vidéo. Code HTTP : %s, Message : %s",
                e.code,
                e.reason,
            )
            return None
        except Exception as e:  # pragma: no cover - defensive
            logger.exception("Unexpected error while retrieving streams")
            logger.error(
                "[ERREUR] : Une erreur inattendue s'est produite lors de la récupération des flux : %s",
                e,
            )
            return None

    def conversion_mp4_in_mp3(self, file_downloaded: Union[str, Path]) -> None:
        """Rename the downloaded MP4 file to MP3 and remove the source."""
        file_path = Path(file_downloaded)
        try:
            new_file = file_path.with_suffix(".mp3")
            file_path.rename(new_file)
            if file_path.exists():
                file_path.unlink()
        except OSError:
            logger.exception("Error during MP4 to MP3 conversion")
            logger.warning("[WARMING] un fichier MP3 portant le même nom, déjà existant!")
            if file_path.exists():
                file_path.unlink()
            logger.info("")

    def download_multiple_videos(
        self,
        url_youtube_video_links: Iterable[str],
        options: DownloadOptions,
    ) -> Optional[list[str]]:
        """Download multiple YouTube videos or audio tracks."""

        download_sound_only = options.download_sound_only
        save_path = options.save_path or Path.cwd()
        choice_callback = options.choice_callback
        progress_handler = options.progress_handler or self.progress_handler

        choice_once = True

        url_list = list(url_youtube_video_links)
        if not url_list:
            logger.error("[ERREUR] : il y a aucune vidéo à télécharger")
            return url_list

        for url_video in url_list:
            try:
                youtube_video = self.youtube_cls(url_video)
                if progress_handler:
                    youtube_video.register_on_progress_callback(progress_handler.on_progress)
            except KeyError as e:
                logger.error("[ERREUR] : Problème de clé dans les données : %s", e)
                continue
            except Exception as e:  # pragma: no cover - defensive
                logger.exception("Unexpected error while connecting to video")
                logger.error("[ERREUR] : Connexion à la vidéo impossible : %s", e)
                continue

            streams = self.streams_video(download_sound_only, youtube_video)
            if not streams:
                logger.error(
                    "[ERREUR] : Les flux pour la vidéo (%s) n'ont pas pu être récupérés.",
                    url_video,
                )
                continue

            try:
                video_title = youtube_video.title
            except KeyError as e:
                logger.error(
                    "[ERREUR] : Impossible d'accéder au titre de la vidéo %s. Détail : %s",
                    url_video,
                    e,
                )
                continue
            except Exception as e:  # pragma: no cover - defensive
                logger.exception("Unexpected error while accessing video title")
                logger.error(
                    "[ERREUR] : Une erreur inattendue s'est produite lors de l'accès au titre : %s",
                    e,
                )
                continue

            if choice_once:
                if choice_callback:
                    choice_user = choice_callback(download_sound_only, streams)
                else:
                    choice_user = 1
                choice_once = False
                logger.info("")
                logger.info("")
                cli_utils.print_separator()
                logger.info("*             Stream vidéo selectionnée:                    *")
                cli_utils.print_separator()
                logger.info("Number of link url video youtube in file: %s",
                    len(url_list),
                )
                logger.info("")

            itag = streams[choice_user - 1].itag  # type: ignore
            stream = youtube_video.streams.get_by_itag(itag)

            logger.info("Titre: %s", video_title[0:53])

            current_file = save_path / stream.default_filename  # type: ignore
            if current_file.exists():
                logger.warning("[WARMING] un fichier MP4 portant le même nom, déjà existant!")

            try:
                out_file = Path(stream.download(output_path=str(save_path)))  # type: ignore
                logger.info("")
            except Exception as e:  # pragma: no cover - network/io issues
                logger.exception("Download failed")
                logger.info("")
                logger.error("[ERREUR] : le téléchargement a échoué : %s", e)
                logger.info("")
                continue

            if out_file and download_sound_only:
                self.conversion_mp4_in_mp3(out_file)

        cli_utils.print_end_download_message()
        cli_utils.pause_return_to_menu()

        return None

