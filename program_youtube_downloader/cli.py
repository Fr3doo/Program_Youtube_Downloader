"""Command line interface helpers and interactive menu."""

from __future__ import annotations

import logging
from pathlib import Path

from pytube import Playlist, Channel
from pytube.exceptions import PytubeError

from . import cli_utils
from .downloader import YoutubeDownloader
from .exceptions import PlaylistConnectionError, ChannelConnectionError
from .config import DownloadOptions
from .constants import MenuOption

logger = logging.getLogger(__name__)


class CLI:
    """Interactive command line interface for the application."""

    def __init__(self, downloader: YoutubeDownloader | None = None) -> None:
        self.downloader = downloader or YoutubeDownloader()

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
            save_path = cli_utils.ask_save_file_path()
        return DownloadOptions(
            save_path=save_path,
            download_sound_only=audio_only,
            choice_callback=cli_utils.ask_resolution_or_bitrate,
        )

    # ------------------------------------------------------------------
    # Menu handlers
    # ------------------------------------------------------------------
    def handle_quit_option(self) -> None:
        """Display the exit banner."""
        logger.info("")
        logger.info("")
        logger.info("******************************************************")
        logger.info("*                                                    *")
        logger.info("*                    Fin du programme                *")
        logger.info("*                                                    *")
        logger.info("******************************************************")

    def handle_video_option(self, audio_only: bool) -> None:
        """Download a single video or its audio track."""
        url = cli_utils.ask_youtube_url()
        options = self.create_download_options(audio_only)
        self.downloader.download_multiple_videos([url], options)

    def handle_videos_option(self, audio_only: bool) -> None:
        """Download multiple videos or their audio tracks from a file."""
        urls = cli_utils.ask_youtube_link_file()
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
            logger.exception("Error connecting to playlist")
            raise PlaylistConnectionError("Connexion à la Playlist impossible") from e
        except Exception:
            logger.exception("Unexpected error while connecting to playlist")
            raise

    def load_channel(self, url: str) -> Channel:
        """Return a :class:`Channel` instance for ``url`` or raise an error."""
        try:
            return Channel(url)
        except (PytubeError, KeyError, ValueError) as e:
            logger.exception("Error connecting to channel")
            raise ChannelConnectionError("Connexion à la chaîne Youtube impossible") from e
        except Exception:
            logger.exception("Unexpected error while connecting to channel")
            raise

    def handle_playlist_option(self, audio_only: bool) -> None:
        """Download an entire playlist."""
        url = cli_utils.ask_youtube_url()
        playlist = self.load_playlist(url)
        options = self.create_download_options(audio_only)
        self.downloader.download_multiple_videos(playlist, options)  # type: ignore

    def handle_channel_option(self, audio_only: bool) -> None:
        """Download all videos from a channel."""
        url = cli_utils.ask_youtube_url()
        channel = self.load_channel(url)
        options = self.create_download_options(audio_only)
        self.downloader.download_multiple_videos(channel, options)  # type: ignore

    # ------------------------------------------------------------------
    # Interactive menu
    # ------------------------------------------------------------------
    def menu(self) -> None:  # pragma: no cover - manual user interaction
        """Interactively ask the user what to download and start the process."""
        while True:
            choix_max_menu_accueil = cli_utils.display_main_menu()
            choix = MenuOption(cli_utils.ask_numeric_value(1, choix_max_menu_accueil))

            match choix:
                case MenuOption.QUIT:
                    self.handle_quit_option()
                    break
                case MenuOption.VIDEO:
                    self.handle_video_option(False)
                case MenuOption.VIDEO_AUDIO_ONLY:
                    self.handle_video_option(True)
                case MenuOption.VIDEOS:
                    self.handle_videos_option(False)
                case MenuOption.VIDEOS_AUDIO_ONLY:
                    self.handle_videos_option(True)
                case MenuOption.PLAYLIST_VIDEO:
                    self.handle_playlist_option(False)
                case MenuOption.PLAYLIST_AUDIO_ONLY:
                    self.handle_playlist_option(True)
                case MenuOption.CHANNEL_VIDEOS:
                    self.handle_channel_option(False)
                case MenuOption.CHANNEL_AUDIO_ONLY:
                    self.handle_channel_option(True)




            # end match
        # end while


__all__ = ["CLI"]
