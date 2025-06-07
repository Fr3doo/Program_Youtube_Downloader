import logging
import program_youtube_downloader.main as main_module


def test_setup_logging_configures_level(caplog):
    main_module.setup_logging("INFO")
    logging.getLogger().addHandler(caplog.handler)
    logger = logging.getLogger("dummy")
    logger.debug("debug")
    logger.info("info")
    assert "info" in caplog.text
    assert "debug" not in caplog.text
