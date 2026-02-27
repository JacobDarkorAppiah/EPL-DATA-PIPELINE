import logging
import os

def setup_logger(name="EPL_Pipeline"):
    if not os.path.exists("logs"):
        os.makedirs("logs")

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Format: Time - Name - Level - Message
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # File Handler (Saves to a file)
    file_handler = logging.FileHandler("logs/pipeline.log")
    file_handler.setFormatter(formatter)

    # Console Handler (Shows in terminal)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger