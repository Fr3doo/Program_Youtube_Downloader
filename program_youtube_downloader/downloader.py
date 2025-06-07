from urllib.error import HTTPError
from pathlib import Path
from typing import Optional, Union, Iterable, Callable, Any
import logging

from pytubefix import YouTube
from pytube.exceptions import PytubeError
from .types import YouTubeVideo
from .exceptions import DownloadError, StreamAccessError
from . import cli_utils
from .config import DownloadOptions
from .progress import ProgressHandler, ProgressBarHandler

logger = logging.getLogger(__name__)


class YoutubeDownloader:
    """High level interface for downloading YouTube videos and audio."""

    def __init__(
        self,
        progress_handler: ProgressHandler | None = None,
        youtube_cls: Callable[[str], YouTubeVideo] = YouTube,
    ) -> None:
        """Create the downloader.

        Args:
            progress_handler: Handler receiving progress events from
                ``pytubefix``. If ``None`` a :class:`ProgressBarHandler` is used.
            youtube_cls: Factory used to create objects following the
                :class:`~program_youtube_downloader.types.YouTubeVideo` protocol.
                Tests may provide a mock implementation.
        """

        self.progress_handler = progress_handler or ProgressBarHandler()
        self.youtube_cls = youtube_cls

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _create_youtube(
        self, url: str, progress_handler: ProgressHandler | None
    ) -> YouTubeVideo | None:
        """Instantiate a video object and register the progress callback.

        This wrapper centralises error handling around the ``youtube_cls``
        factory provided at construction time.  It returns ``None`` if the
        object cannot be created.
        """

        try:
            yt = self.youtube_cls(url)
            if progress_handler:
                yt.register_on_progress_callback(progress_handler.on_progress)
            return yt
        except KeyError as e:
            logger.error("[ERREUR] : Problème de clé dans les données : %s", e)
            return None
        except PytubeError as e:
            logger.exception("Error while connecting to video")
            logger.error("[ERREUR] : Connexion à la vidéo impossible : %s", e)
            return None
        except Exception as e:  # pragma: no cover - defensive
            logger.exception("Unexpected error while connecting to video")
            logger.error("[ERREUR] : Connexion à la vidéo impossible : %s", e)
            return None

    def _choose_stream(
        self,
        download_sound_only: bool,
        streams: Any,
        callback: Callable[[bool, Any], int] | None,
    ) -> int:
        """Return the index of the stream chosen by the user."""

        if callback:
            return callback(download_sound_only, streams)
        return 1

    def _download_stream(
        self,
        stream: Any,
        save_path: Path,
        url_video: str,
        download_sound_only: bool,
    ) -> None:
        """Download ``stream`` to ``save_path`` with retries.

        Raises :class:`DownloadError` after three failed attempts.
        """

        current_file = save_path / stream.default_filename  # type: ignore
        if current_file.exists():
            logger.warning(
                "[WARNING] un fichier MP4 portant le même nom, déjà existant!"
            )

        out_file = None
        for attempt in range(3):
            try:
                out_file = Path(stream.download(output_path=str(save_path)))
                logger.info("")
                break
            except (HTTPError, OSError, PytubeError) as e:  # pragma: no cover - network/io issues
                logger.exception("Download failed")
                logger.info("")
                logger.error("[ERREUR] : le téléchargement a échoué : %s", e)
                logger.info("")
                if attempt == 2:
                    raise DownloadError(
                        f"Echec du téléchargement pour {url_video}"
                    ) from e
            except Exception as e:  # pragma: no cover - defensive
                logger.exception("Unexpected error during download")
                logger.info("")
                logger.error("[ERREUR] : le téléchargement a échoué : %s", e)
                logger.info("")
                if attempt == 2:
                    raise DownloadError(
                        f"Echec du téléchargement pour {url_video}"
                    ) from e

        if out_file and download_sound_only:
            self.conversion_mp4_in_mp3(out_file)

    def streams_video(
        self, download_sound_only: bool, youtube_video: YouTubeVideo
    ) -> Any:
        """Return the available streams for ``youtube_video``.

        Args:
            download_sound_only: Ignored, kept for backward compatibility.
            youtube_video: An object implementing :class:`YouTubeVideo`.

        Raises:
            StreamAccessError: If retrieving the streams fails.
        """
        try:
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
            raise StreamAccessError(f"HTTP {e.code}: {e.reason}") from e
        except PytubeError as e:
            logger.exception("Error while retrieving streams")
            logger.error(
                "[ERREUR] : Une erreur est survenue lors de la récupération des flux : %s",
                e,
            )
            raise StreamAccessError(str(e)) from e
        except Exception as e:  # pragma: no cover - defensive
            logger.exception("Unexpected error while retrieving streams")
            logger.error(
                "[ERREUR] : Une erreur inattendue s'est produite lors de la récupération des flux : %s",
                e,
            )
            raise StreamAccessError(str(e)) from e

    def conversion_mp4_in_mp3(self, file_downloaded: Union[str, Path]) -> None:
        """Rename the downloaded MP4 file to MP3 and remove the original file.

        Args:
            file_downloaded: Path to the downloaded MP4 file.
        """
        file_path = Path(file_downloaded)
        try:
            new_file = file_path.with_suffix(".mp3")
            file_path.rename(new_file)
            if file_path.exists():
                file_path.unlink()
        except OSError:
            logger.exception("Error during MP4 to MP3 conversion")
            logger.warning("[WARNING] un fichier MP3 portant le même nom, déjà existant!")
            if file_path.exists():
                file_path.unlink()
            logger.info("")

    def download_multiple_videos(
        self,
        url_youtube_video_links: Iterable[str],
        options: DownloadOptions,
    ) -> Optional[list[str]]:
        """Download one or more videos or audio tracks.

        Args:
            url_youtube_video_links: Iterable of YouTube URLs to download.
            options: Download behaviour configuration.

        Returns:
            ``None`` if every download succeeds, otherwise a list of URLs that
            failed to download (currently always returns ``None``).
        """

        download_sound_only = options.download_sound_only
        save_path = options.save_path or Path.cwd()
        choice_callback = options.choice_callback
        progress_handler = options.progress_handler or self.progress_handler

        choice_once = True
        choice_user = 1

        url_list = list(url_youtube_video_links)
        if not url_list:
            logger.error("[ERREUR] : il y a aucune vidéo à télécharger")
            return url_list

        for url_video in url_list:
            youtube_video = self._create_youtube(url_video, progress_handler)
            if youtube_video is None:
                continue

            try:
                streams = self.streams_video(download_sound_only, youtube_video)
            except StreamAccessError as e:
                logger.error(
                    "[ERREUR] : Les flux pour la vidéo (%s) n'ont pas pu être récupérés. %s",
                    url_video,
                    e,
                )
                continue

            if not streams:
                logger.error(
                    "[ERREUR] : Aucun flux disponible pour la vidéo (%s).",
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
            except PytubeError as e:
                logger.exception("Error while accessing video title")
                logger.error(
                    "[ERREUR] : Une erreur est survenue lors de l'accès au titre : %s",
                    e,
                )
                continue
            except Exception:  # pragma: no cover - defensive
                logger.exception("Unexpected error while accessing video title")
                continue

            if choice_once:
                choice_user = self._choose_stream(
                    download_sound_only,
                    streams,
                    choice_callback,
                )
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

            self._download_stream(
                stream,
                save_path,
                url_video,
                download_sound_only,
            )

        cli_utils.print_end_download_message()
        cli_utils.pause_return_to_menu()

        return None

