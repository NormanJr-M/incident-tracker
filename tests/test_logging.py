import logging

from incident_tracker.logging_setup import setup_logging



def test_setup_logging_writes_records_to_file(tmp_path):
    log_file = tmp_path / "test.log"

    logger = setup_logging(str(log_file))

    logging.getLogger("incident_tracker.test").warning(
        "disk almost full"
    )

    for handler in logger.handlers:
        handler.flush()

    assert "disk almost full" in log_file.read_text(
        encoding="utf-8"
    )

    for handler in list(logger.handlers):
        handler.close()
        logger.removeHandler(handler)