from pathlib import Path

from program_youtube_downloader.downloader import YoutubeDownloader


def test_conversion_mp4_in_mp3(tmp_path: Path) -> None:
    mp4_path = tmp_path / "sample.mp4"
    mp4_path.write_text("dummy-data")

    yd = YoutubeDownloader()
    yd.conversion_mp4_in_mp3(str(mp4_path))

    assert not mp4_path.exists()
    mp3_path = tmp_path / "sample.mp3"
    assert mp3_path.exists()
    assert mp3_path.read_text() == "dummy-data"
