from urllib.error import HTTPError
from pathlib import Path
from typing import Optional, Union, Iterable
import logging

from pytubefix import YouTube

from youtube_downloader import (
    demander_save_file_path,
    on_download_progress,
    demander_choice_resolution_vidéo_or_bitrate_audio,
    program_break_time,
    clear_screen,
    print_separator,
)


class YoutubeDownloader:
    """Responsible for fetching streams and saving downloaded files."""

    def streams_video(self, download_sound_only: bool, youtube_video: YouTube):
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
            print(
                f"[ERREUR] : Impossible d'accéder aux flux pour la vidéo. Code HTTP : {e.code}, Message : {e.reason}"
            )
            return None
        except Exception as e:  # pragma: no cover - defensive
            logging.exception("Unexpected error while retrieving streams")
            print(
                f"[ERREUR] : Une erreur inattendue s'est produite lors de la récupération des flux : {e}"
            )
            return None

    def conversion_mp4_in_mp3(self, file_downloaded: Union[str, Path]) -> None:
        file_path = Path(file_downloaded)
        try:
            new_file = file_path.with_suffix(".mp3")
            file_path.rename(new_file)
            if file_path.exists():
                file_path.unlink()
        except OSError:
            logging.exception("Error during MP4 to MP3 conversion")
            print("[WARMING] un fichier MP3 portant le même nom, déjà existant!")
            if file_path.exists():
                file_path.unlink()
            print()

    def download_multiple_videos(
        self, url_youtube_video_links: Iterable[str], download_sound_only: bool
    ) -> Optional[list[str]]:
        """Download multiple YouTube videos or audio tracks."""
        choice_once = True
        save_path = demander_save_file_path()

        url_list = list(url_youtube_video_links)
        if not url_list:
            print("[ERREUR] : il y a aucune vidéo à télécharger")
            return url_list

        for url_video in url_list:
            try:
                youtube_video = YouTube(url_video)
                youtube_video.register_on_progress_callback(on_download_progress)
            except KeyError as e:
                print(f"[ERREUR] : Problème de clé dans les données : {e}")
                continue
            except Exception as e:  # pragma: no cover - defensive
                logging.exception("Unexpected error while connecting to video")
                print(f"[ERREUR] : Connexion à la vidéo impossible : {e}")
                continue

            streams = self.streams_video(download_sound_only, youtube_video)
            if not streams:
                print(
                    f"[ERREUR] : Les flux pour la vidéo ({url_video}) n'ont pas pu être récupérés."
                )
                continue

            try:
                video_title = youtube_video.title
            except KeyError as e:
                print(
                    f"[ERREUR] : Impossible d'accéder au titre de la vidéo {url_video}. Détail : {e}"
                )
                continue
            except Exception as e:  # pragma: no cover - defensive
                logging.exception("Unexpected error while accessing video title")
                print(
                    f"[ERREUR] : Une erreur inattendue s'est produite lors de l'accès au titre : {e}"
                )
                continue

            if choice_once:
                choice_user = demander_choice_resolution_vidéo_or_bitrate_audio(
                    download_sound_only, streams
                )
                choice_once = False
                print()
                print()
                print_separator()
                print("*             Stream vidéo selectionnée:                    *")
                print_separator()
                print(
                    "Number of link url video youtube in file: ",
                    len(url_list),
                )
                print()

            itag = streams[choice_user - 1].itag  # type: ignore
            stream = youtube_video.streams.get_by_itag(itag)

            print(f"Titre: {video_title[0:53]}")

            current_file = save_path / stream.default_filename  # type: ignore
            if current_file.exists():
                print("[WARMING] un fichier MP4 portant le même nom, déjà existant!")

            try:
                out_file = Path(stream.download(output_path=str(save_path)))  # type: ignore
                print()
            except Exception as e:  # pragma: no cover - network/io issues
                logging.exception("Download failed")
                print()
                print(f"[ERREUR] : le téléchargement a échoué : {e}")
                print()
                continue

            if out_file and download_sound_only:
                self.conversion_mp4_in_mp3(out_file)

        print()
        print("Fin du téléchargement")
        print_separator()
        print()
        input("Appuyer sur ENTREE pour revenir au menu d'accueil")
        program_break_time(3, "Le menu d'accueil va revenir dans")
        clear_screen()

        return None

