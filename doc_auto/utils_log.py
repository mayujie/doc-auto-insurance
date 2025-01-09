import logging


def setup_logger(name, level=logging.DEBUG):
    """
    Set up a logger with console handler and formatter.

    Args:
        name (str): The name of the logger.
        level (int): The logging level (default is logging.DEBUG).

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create console handler and set level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Create formatter and attach it to the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(console_handler)

    return logger
