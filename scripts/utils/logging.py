import logging
from typing import Optional

from rich.logging import RichHandler


def get_logger(name: Optional[str] = None) -> logging.Logger:
    if name is None:
        name = __name__

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    rich_handler = RichHandler(rich_tracebacks=True, markup=True)
    rich_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(message)s')
    rich_handler.setFormatter(formatter)

    logger.addHandler(rich_handler)

    return logger
