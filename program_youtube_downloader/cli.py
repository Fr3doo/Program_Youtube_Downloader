"""Command line interface helpers and interactive menu."""

from __future__ import annotations

import logging
from pathlib import Path
from functools import partial

from pytube import Playlist, Channel
from pytube.exceptions import PytubeError

from . import cli_utils
from .types import ConsoleIO, DefaultConsoleIO
from .downloader import YoutubeDownloader
from .exceptions import PlaylistConnectionError, ChannelConnectionError
from .config import DownloadOptions
from .constants import MenuOption
from .utils import log_blank_line

logger = logging.getLogger(__name__)


class CLI:
    """Interactive command line interface for the application."""

    def __init__(
        self,
        downloader: YoutubeDownloader | None = None,
        console: ConsoleIO = DefaultConsoleIO(),
    ) -> None:
        """Create the CLI wrapper around ``YoutubeDownloader``.

        Args:
            downloader: Optional custom downloader instance. When ``None`` a
                new :class:`YoutubeDownloader` is created.
            console: Object used for ``input``/``print`` operations.
        """
        self.downloader = downloader or YoutubeDownloader()
        self.console = console

    # ------------------------------------------------------------------
    # Download option helpers
    # ------------------------------------------------------------------
    def create_download_options(
        self, audio_only: bool, output_dir: Path | None = None
    ) -> DownloadOptions:
        """Build a :class:`DownloadOptions` with destination and callbacks."""
        if output_dir is not None:
            save_path = output_dir.expanduser().resolve()
        else:
            save_path = cli_utils.ask_save_file_path(console=self.console)
        return DownloadOptions(
            save_path=save_path,
            download_sound_only=audio_only,
            choice_callback=partial(
                cli_utils.ask_resolution_or_bitrate, console=self.console
            ),
        )

    # ------------------------------------------------------------------
    # Menu handlers
    # ------------------------------------------------------------------
    def handle_quit_option(self) -> None:
        """Display the exit banner."""
        log_blank_line()
        log_blank_line()
        logger.info("******************************************************")
        logger.info("*                                                    *")
        logger.info("*                    Fin du programme                *")
        logger.info("*                                                    *")
        logger.info("******************************************************")

    def handle_video_option(self, audio_only: bool) -> None:
        """Download a single video or its audio track."""
        url = cli_utils.ask_youtube_url(console=self.console)
        options = self.create_download_options(audio_only)
        self.downloader.download_multiple_videos([url], options)

    def handle_videos_option(self, audio_only: bool) -> None:
        """Download multiple videos or their audio tracks from a file."""
        urls = cli_utils.ask_youtube_link_file(console=self.console)
        options = self.create_download_options(audio_only)
        self.downloader.download_multiple_videos(urls, options)

    # ------------------------------------------------------------------
    # Loader helpers
    # ------------------------------------------------------------------
    def load_playlist(self, url: str) -> Playlist:
        """Return a :class:`Playlist` instance for ``url`` or raise an error."""
        try:
            return Playlist(url)
        except (PytubeError, KeyError, ValueError) as e:
            logger.exception("Erreur lors de la connexion à la playlist")
            raise PlaylistConnectionError("Connexion à la Playlist impossible") from e
        except Exception:
            logger.exception("Erreur inattendue lors de la connexion à la playlist")
            raise

    def load_channel(self, url: str) -> Channel:
        """Return a :class:`Channel` instance for ``url`` or raise an error."""
        try:
            return Channel(url)
        except (PytubeError, KeyError, ValueError) as e:
            logger.exception("Erreur lors de la connexion à la chaîne")
            raise ChannelConnectionError("Connexion à la chaîne Youtube impossible") from e
        except Exception:
            logger.exception("Erreur inattendue lors de la connexion à la chaîne")
            raise

    def handle_playlist_option(self, audio_only: bool) -> None:
        """Download an entire playlist."""
        url = cli_utils.ask_youtube_url(console=self.console)
        playlist = self.load_playlist(url)
        options = self.create_download_options(audio_only)
        self.downloader.download_multiple_videos(playlist, options)  # type: ignore

    def handle_channel_option(self, audio_only: bool) -> None:
        """Download all videos from a channel."""
        url = cli_utils.ask_youtube_url(console=self.console)
        channel = self.load_channel(url)
        options = self.create_download_options(audio_only)
        self.downloader.download_multiple_videos(channel, options)  # type: ignore

    # ------------------------------------------------------------------
    # Interactive menu
    # ------------------------------------------------------------------
    def menu(self) -> None:  # pragma: no cover - manual user interaction
        """Interactively ask the user what to download and start the process."""
        try:
            handlers = {
                MenuOption.VIDEO: self.handle_video_option,
                MenuOption.VIDEO_AUDIO_ONLY: self.handle_video_option,
                MenuOption.VIDEOS: self.handle_videos_option,
                MenuOption.VIDEOS_AUDIO_ONLY: self.handle_videos_option,
                MenuOption.PLAYLIST_VIDEO: self.handle_playlist_option,
                MenuOption.PLAYLIST_AUDIO_ONLY: self.handle_playlist_option,
                MenuOption.CHANNEL_VIDEOS: self.handle_channel_option,
                MenuOption.CHANNEL_AUDIO_ONLY: self.handle_channel_option,
            }

            while True:
                choix_max_menu_accueil = cli_utils.display_main_menu(
                    console=self.console
                )
                choix = MenuOption(
                    cli_utils.ask_numeric_value(
                        1, choix_max_menu_accueil, console=self.console
                    )
                )

                if choix is MenuOption.QUIT:
                    self.handle_quit_option()
                    break

                audio_only = choix in (
                    MenuOption.VIDEO_AUDIO_ONLY,
                    MenuOption.VIDEOS_AUDIO_ONLY,
                    MenuOption.PLAYLIST_AUDIO_ONLY,
                    MenuOption.CHANNEL_AUDIO_ONLY,
                )

                handlers[choix](audio_only)

            # end while
        except KeyboardInterrupt:
            self.handle_quit_option()
            return


__all__ = ["CLI"]
