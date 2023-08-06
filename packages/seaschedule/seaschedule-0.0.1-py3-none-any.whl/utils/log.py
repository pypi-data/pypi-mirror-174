import logging


def get_logger(name: str, log_file: str, log_level: int, log_format: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    formatter = logging.Formatter(log_format)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def format_log_message(message: str = "") -> str:
    return message.replace("\n", "\\n")
