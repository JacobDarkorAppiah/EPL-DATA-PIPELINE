import logging
import os

def setup_logger(name="EPL_Pipeline"):
    if not os.path.exists("logs"):
        os.makedirs("logs")

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Standard format for the console
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # File Handler: We FORCE utf-8 here to handle emojis/special chars
    file_handler = logging.FileHandler("logs/pipeline.log", encoding='utf-8')
    file_handler.setFormatter(formatter)

    # Console Handler: Keep it simple for the Windows Terminal
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger