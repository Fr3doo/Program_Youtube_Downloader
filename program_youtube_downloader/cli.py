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
from .constants import MenuOption, SEPARATOR
from .utils import log_blank_line

logger = logging.getLogger(__name__)


class CLI:
    """Interactive command line interface for the downloader.

    The class exposes small helper methods that orchestrate the user
    interaction logic.  It delegates the actual download work to
    :class:`YoutubeDownloader` and only handles the prompts and menu
    dispatching.
    """

    def __init__(
        self,
        downloader: YoutubeDownloader | None = None,
        console: ConsoleIO = DefaultConsoleIO(),
    ) -> None:
        """Instantiate the interface.

        Parameters
        ----------
        downloader:
            Optional pre-configured :class:`YoutubeDownloader` instance.
            If ``None`` a new one is created.
        console:
            Implementation of :class:`ConsoleIO` used for user interaction.
        """
        self.downloader = downloader or YoutubeDownloader()
        self.console = console

    # ------------------------------------------------------------------
    # Download option helpers
    # ------------------------------------------------------------------
    def create_download_options(
        self, audio_only: bool, output_dir: Path | None = None
    ) -> DownloadOptions:
        """Return a fully initialised :class:`DownloadOptions` instance.

        Parameters
        ----------
        audio_only:
            When ``True`` the downloader will only fetch the audio streams and
            convert them to MP3.
        output_dir:
            Optional directory to save the downloads.  If omitted the user is
            prompted for a path via :func:`cli_utils.ask_save_file_path`.

        Returns
        -------
        DownloadOptions
            The options object to pass to :meth:`YoutubeDownloader.download_multiple_videos`.
        """
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
        """Display the closing banner and end of program message."""
        log_blank_line()
        log_blank_line()
        logger.info(SEPARATOR)
        logger.info("*                                                    *")
        logger.info("*                    Fin du programme                *")
        logger.info("*                                                    *")
        logger.info(SEPARATOR)

    def handle_video_option(self, audio_only: bool) -> None:
        """Handle the "download single video" menu entry.

        Parameters
        ----------
        audio_only:
            When ``True`` only the audio stream of the selected video is
            downloaded.
        """
        url = cli_utils.ask_youtube_url(console=self.console)
        options = self.create_download_options(audio_only)
        self.downloader.download_multiple_videos([url], options)

    def handle_videos_option(self, audio_only: bool) -> None:
        """Handle the "download from file" menu entry.

        Parameters
        ----------
        audio_only:
            When ``True`` only the audio stream of each video is downloaded.
        """
        urls = cli_utils.ask_youtube_link_file(console=self.console)
        options = self.create_download_options(audio_only)
        self.downloader.download_multiple_videos(urls, options)

    # ------------------------------------------------------------------
    # Loader helpers
    # ------------------------------------------------------------------
    def load_playlist(self, url: str) -> Playlist:
        """Instantiate :class:`pytubefix.Playlist` from ``url``.

        Parameters
        ----------
        url:
            URL of the YouTube playlist to load.

        Returns
        -------
        pytubefix.Playlist

        Raises
        ------
        PlaylistConnectionError
            If the playlist cannot be accessed.
        """
        try:
            return Playlist(url)
        except (PytubeError, KeyError, ValueError) as e:
            logger.exception("Erreur lors de la connexion à la playlist")
            raise PlaylistConnectionError("Connexion à la Playlist impossible") from e
        except Exception:
            logger.exception("Erreur inattendue lors de la connexion à la playlist")
            raise

    def load_channel(self, url: str) -> Channel:
        """Instantiate :class:`pytubefix.Channel` from ``url``.

        Parameters
        ----------
        url:
            URL of the YouTube channel to load.

        Returns
        -------
        pytubefix.Channel

        Raises
        ------
        ChannelConnectionError
            If the channel cannot be accessed.
        """
        try:
            return Channel(url)
        except (PytubeError, KeyError, ValueError) as e:
            logger.exception("Erreur lors de la connexion à la chaîne")
            raise ChannelConnectionError("Connexion à la chaîne Youtube impossible") from e
        except Exception:
            logger.exception("Erreur inattendue lors de la connexion à la chaîne")
            raise

    def handle_playlist_option(self, audio_only: bool) -> None:
        """Handle the playlist download menu entry.

        Parameters
        ----------
        audio_only:
            If ``True`` download only the audio tracks from the playlist
            videos.
        """
        url = cli_utils.ask_youtube_url(console=self.console)
        playlist = self.load_playlist(url)
        options = self.create_download_options(audio_only)
        self.downloader.download_multiple_videos(playlist, options)  # type: ignore

    def handle_channel_option(self, audio_only: bool) -> None:
        """Handle the channel download menu entry.

        Parameters
        ----------
        audio_only:
            If ``True`` download only the audio tracks from each video
            of the channel.
        """
        url = cli_utils.ask_youtube_url(console=self.console)
        channel = self.load_channel(url)
        options = self.create_download_options(audio_only)
        self.downloader.download_multiple_videos(channel, options)  # type: ignore

    # ------------------------------------------------------------------
    # Interactive menu
    # ------------------------------------------------------------------
    def menu(self) -> None:  # pragma: no cover - manual user interaction
        """Run the interactive menu until the user decides to quit.

        The method simply loops over user choices, dispatching to the
        appropriate handler.  It catches ``KeyboardInterrupt`` so that
        pressing ``CTRL+C`` results in a clean exit banner.
        """
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
