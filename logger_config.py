import logging
import sys


def setup_logger() -> logging.Logger:
    logger: logging.Logger = logging.getLogger("OllamaBatchProcessor")

    # no duplicate handlers in this code!
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)

    formatter: logging.Formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


log: logging.Logger = setup_logger()

if __name__ == "__main__":
    pass
