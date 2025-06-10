import logging
import sys
import program_youtube_downloader.main as main_module


def test_setup_logging_configures_level(caplog):
    main_module.setup_logging("INFO")
    logging.getLogger().addHandler(caplog.handler)
    logger = logging.getLogger("dummy")
    logger.debug("debug")
    logger.info("info")
    assert "info" in caplog.text
    assert "debug" not in caplog.text


def test_youtube_downloader_does_not_configure_logging(monkeypatch):
    calls = []

    def fake_basicConfig(*args, **kwargs):
        calls.append((args, kwargs))

    monkeypatch.setattr(logging, "basicConfig", fake_basicConfig)
    module_name = "program_youtube_downloader.legacy_utils"
    sys.modules.pop(module_name, None)
    import importlib

    importlib.import_module(module_name)
    assert not calls
