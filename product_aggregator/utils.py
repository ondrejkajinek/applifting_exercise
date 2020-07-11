"""Util functions for Product aggregator app."""

# std
import logging
import pathlib

# third-party
from django.conf import settings


def setup_cron_logger(logger_name, filename):
    """Set up cron logger."""
    formatter = logging.Formatter(
        "%(asctime)s [%(name)s] %(levelname)s - %(message)s"
    )

    log_file = pathlib.Path(settings.BASE_DIR) / filename
    if not log_file.exists():
        parent = log_file.parent
        if not parent.exists():
            parent.mkdir(parents=True)

        log_file.touch()

    f_handler = logging.FileHandler(str(log_file))
    f_handler.setFormatter(formatter)
    f_handler.setLevel(logging.DEBUG if settings.DEBUG else logging.WARNING)
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG if settings.DEBUG else logging.WARNING)
    logger.addHandler(f_handler)

    return logger
