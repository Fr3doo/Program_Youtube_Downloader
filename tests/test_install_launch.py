import os
import sys
import subprocess
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


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


def test_cli_script_help_after_install(tmp_path) -> None:
    install_dir = tmp_path / "install"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            ".",
            "--prefix",
            str(install_dir),
            "--no-deps",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    script_dir = install_dir / ("Scripts" if os.name == "nt" else "bin")
    exe = script_dir / (
        "program-youtube-downloader" + (".exe" if os.name == "nt" else "")
    )

    assert exe.exists()

    site_packages = install_dir / (
        ("Lib" if os.name == "nt" else "lib")
    ) / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(site_packages)

    result = subprocess.run(
        [str(exe), "--help"], capture_output=True, text=True, env=env
    )
    assert result.returncode == 0
    assert "usage" in result.stdout.lower()
