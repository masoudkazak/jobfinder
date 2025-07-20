from datetime import UTC, datetime
import logging
import os


class DailyLogFileHandler(logging.FileHandler):
    def __init__(self):
        main_dir = os.path.dirname(os.path.abspath(__file__))  # مسیر bot_service
        log_dir = os.path.join(main_dir, "logs")
        os.makedirs(log_dir, exist_ok=True)

        filename = datetime.now(UTC).strftime("%Y-%m-%d") + ".log"
        super().__init__(os.path.join(log_dir, filename), encoding="utf8")


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)d] %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )

    if not logger.handlers:
        file_handler = DailyLogFileHandler()
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
