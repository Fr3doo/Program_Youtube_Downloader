import sys
import subprocess
from pathlib import Path
import tomllib


def test_console_script_defined() -> None:
    pyproject = Path("pyproject.toml").read_text()
    data = tomllib.loads(pyproject)
    scripts = data.get("project", {}).get("scripts", {})
    assert scripts.get("program-youtube-downloader") == "program_youtube_downloader.main:main"


def test_module_help_executes() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "program_youtube_downloader.main", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    out = result.stdout.lower()
    assert "usage" in out or "program youtube downloader".lower() in out
