import logging


def initialize_logger() -> logging.Logger:
    """
    Creates and configures a logger for the app.
    """
    logger = logging.getLogger("MT5Alerter")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] %(message)s", datefmt="%d/%m | %H:%M")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
