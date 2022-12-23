import logging


def get_logger(name, settings) -> logging.Logger:
    logging.basicConfig(
        format=settings.FORMAT,
        datefmt=settings.TIME_FORMAT,
        level=settings.LOGGING_LEVEL,
        filename=settings.LOG_FILENAME
    )

    logger = logging.getLogger(name)
    return logger
