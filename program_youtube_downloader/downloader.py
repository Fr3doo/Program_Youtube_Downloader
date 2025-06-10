from urllib.error import HTTPError
from pathlib import Path
from typing import Union, Iterable, Callable, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

from pytubefix import YouTube
from pytube.exceptions import PytubeError
from .types import YouTubeVideo
from .exceptions import DownloadError, StreamAccessError
from . import cli_utils
from .config import DownloadOptions
from .progress import (
    ProgressHandler,
    ProgressBarHandler,
    create_progress_event,
)

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
            progress_handler: Any object implementing
                :class:`~program_youtube_downloader.progress.ProgressHandler`.
                If ``None`` a :class:`ProgressBarHandler` is used.
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
                def _wrapper(stream, chunk, bytes_remaining):
                    """Translate pytube progress callback to :class:`ProgressEvent`."""
                    event = create_progress_event(stream, bytes_remaining)
                    progress_handler.on_progress(event)

                yt.register_on_progress_callback(_wrapper)
            return yt
        except KeyError as e:
            logger.error(f"Problème de clé dans les données : {e}")
            return None
        except PytubeError as e:
            logger.exception("Erreur lors de la connexion à la vidéo")
            logger.error(f"Connexion à la vidéo impossible : {e}")
            return None
        except Exception as e:  # pragma: no cover - defensive
            logger.exception("Erreur inattendue lors de la connexion à la vidéo")
            logger.error(f"Connexion à la vidéo impossible : {e}")
            return None

    def _select_stream(
        self,
        download_sound_only: bool,
        streams: Any,
        callback: Callable[[bool, Any], int] | None,
    ) -> int:
        """Return the index of the stream chosen by the user."""

        if callback:
            return callback(download_sound_only, streams)
        return 1

    def _download_video(
        self,
        stream: Any,
        save_path: Path,
        video_url: str,
        download_sound_only: bool,
    ) -> None:
        """Download ``stream`` to ``save_path`` with retries.

        Raises :class:`DownloadError` after three failed attempts.
        """

        current_file = save_path / stream.default_filename  # type: ignore
        if current_file.exists():
            logger.warning(
                "Un fichier MP4 portant le même nom existe déjà"
            )

        out_file = None
        for attempt in range(3):
            try:
                out_file = Path(stream.download(output_path=str(save_path)))
                logger.info("")
                break
            except (
                HTTPError,
                OSError,
                PytubeError,
            ) as e:  # pragma: no cover - network/io issues
                logger.exception("Échec du téléchargement")
                logger.info("")
                logger.error(f"Le téléchargement a échoué : {e}")
                logger.info("")
                if attempt == 2:
                    raise DownloadError(
                        f"Echec du téléchargement pour {video_url}"
                    ) from e
            except Exception as e:  # pragma: no cover - defensive
                logger.exception("Erreur inattendue pendant le téléchargement")
                logger.info("")
                logger.error(f"Le téléchargement a échoué : {e}")
                logger.info("")
                if attempt == 2:
                    raise DownloadError(
                        f"Echec du téléchargement pour {video_url}"
                    ) from e

        if out_file and download_sound_only:
            self.conversion_mp4_in_mp3(out_file)

    def get_video_streams(
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
                "Impossible d'accéder aux flux pour la vidéo. "
                f"HTTP {e.code} : {e.reason}"
            )
            raise StreamAccessError(f"HTTP {e.code}: {e.reason}") from e
        except PytubeError as e:
            logger.exception("Erreur lors de la récupération des flux")
            logger.error(
                "Une erreur est survenue lors de la récupération des flux : "
                f"{e}"
            )
            raise StreamAccessError(str(e)) from e
        except Exception as e:  # pragma: no cover - defensive
            logger.exception(
                "Erreur inattendue lors de la récupération des flux"
            )
            logger.error(
                "Une erreur inattendue s'est produite lors de la récupération "
                f"des flux : {e}"
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
            if new_file.exists():
                counter = 1
                candidate = new_file.with_name(
                    f"{new_file.stem}_{counter}{new_file.suffix}"
                )
                while candidate.exists():
                    counter += 1
                    candidate = new_file.with_name(
                        f"{new_file.stem}_{counter}{new_file.suffix}"
                    )
                new_file = candidate
            file_path.rename(new_file)
            if file_path.exists():
                file_path.unlink()
        except OSError:
            logger.exception("Erreur lors de la conversion MP4 vers MP3")
            logger.warning("Un fichier MP3 portant le même nom existe déjà")
            if file_path.exists():
                file_path.unlink()
            logger.info("")

    def _prepare_video(
        self,
        video_url: str,
        download_sound_only: bool,
        progress_handler: ProgressHandler | None,
    ) -> tuple[Any, YouTubeVideo, str] | None:
        """Return streams, video object and title for ``video_url``."""

        youtube_video = self._create_youtube(video_url, progress_handler)
        if youtube_video is None:
            return None

        try:
            streams = self.get_video_streams(download_sound_only, youtube_video)
        except StreamAccessError as e:
            logger.error(
                f"Les flux pour la vidéo {video_url} n'ont pas pu être récupérés : {e}"
            )
            return None

        if not streams:
            logger.error(
                f"Aucun flux disponible pour la vidéo {video_url}."
            )
            return None

        try:
            video_title = youtube_video.title
        except KeyError as e:
            logger.error(
                f"Impossible d'accéder au titre de la vidéo {video_url}. Détail : {e}"
            )
            return None
        except PytubeError as e:
            logger.exception("Erreur lors de l'accès au titre de la vidéo")
            logger.error(
                f"Une erreur est survenue lors de l'accès au titre : {e}"
            )
            return None
        except Exception:  # pragma: no cover - defensive
            logger.exception(
                "Erreur inattendue lors de l'accès au titre de la vidéo"
            )
            return None

        return streams, youtube_video, video_title

    def _submit_download(
        self,
        executor: ThreadPoolExecutor,
        stream: Any,
        save_path: Path,
        video_url: str,
        download_sound_only: bool,
        futures: dict[Any, str],
    ) -> None:
        """Schedule ``stream`` for download using ``executor``."""

        future = executor.submit(
            self._download_video,
            stream,
            save_path,
            video_url,
            download_sound_only,
        )
        futures[future] = video_url

    def _report_errors(self, futures: dict[Any, str]) -> None:
        """Display download results for ``futures``."""

        errors: list[str] = []
        for future in as_completed(futures):
            url = futures[future]
            try:
                future.result()
            except DownloadError:
                errors.append(url)
            except Exception:  # pragma: no cover - defensive
                logger.exception(
                    "Erreur inattendue dans le thread de téléchargement"
                )
                errors.append(url)

        if not errors:
            cli_utils.print_end_download_message()
        else:
            logger.error(
                f"Les téléchargements suivants ont échoué : {', '.join(errors)}"
            )
        cli_utils.pause_return_to_menu()

    def download_multiple_videos(
        self,
        youtube_video_urls: Iterable[str],
        options: DownloadOptions,
    ) -> None:
        """Download one or more videos or audio tracks.

        Args:
            youtube_video_urls: Iterable of YouTube URLs to download.
            options: Download behaviour configuration.

        Returns:
            ``None``. The method does not report which URLs failed to
            download.

        Raises:
            ValueError: If ``options.max_workers`` is less than 1.
        """

        download_sound_only = options.download_sound_only
        save_path = options.save_path or Path.cwd()
        choice_callback = options.choice_callback
        progress_handler = options.progress_handler or self.progress_handler

        choice_once = True
        choice_user = 1

        url_list = list(youtube_video_urls)
        if not url_list:
            logger.error("Il n'y a aucune vidéo à télécharger")
            return None

        if options.max_workers < 1:
            raise ValueError("max_workers must be >= 1")

        futures: dict[Any, str] = {}
        with ThreadPoolExecutor(max_workers=options.max_workers) as executor:
            for video_url in url_list:
                processed = self._prepare_video(
                    video_url,
                    download_sound_only,
                    progress_handler,
                )
                if processed is None:
                    continue

                streams, youtube_video, video_title = processed

                if choice_once:
                    choice_user = self._select_stream(
                        download_sound_only,
                        streams,
                        choice_callback,
                    )
                    choice_once = False
                    logger.info("")
                    logger.info("")
                    cli_utils.print_separator()
                    logger.info("*             Stream vidéo sélectionné :          *")
                    cli_utils.print_separator()
                    logger.info(
                        "Nombre de liens vidéo YouTube dans le fichier : "
                        f"{len(url_list)}"
                    )
                    logger.info("")

                itag = streams[choice_user - 1].itag  # type: ignore
                stream = youtube_video.streams.get_by_itag(itag)

                logger.info(f"Titre : {video_title[0:53]}")

                self._submit_download(
                    executor,
                    stream,
                    save_path,
                    video_url,
                    download_sound_only,
                    futures,
                )

        self._report_errors(futures)
        return None


__all__ = ["YoutubeDownloader"]
