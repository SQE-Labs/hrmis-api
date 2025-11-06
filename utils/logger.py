import logging
import os
from datetime import datetime

def get_logger(name: str = "APIFramework"):
    """
    Returns a logger instance that logs to both console and file.
    Designed for detailed API test logging.
    """

    # Logs directory
    log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
    os.makedirs(log_dir, exist_ok=True)

    # File name with timestamp
    log_file = os.path.join(log_dir, f"api_tests_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Capture everything

    # Avoid duplicate handlers if logger already exists
    if not logger.handlers:
        # Console handler (info & above)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # File handler (all logs)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)

        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


# Default logger instance
logger = get_logger()


def log_request(method, url, headers=None, body=None):
    """Logs API request details."""
    logger.info(f"➡️ REQUEST: {method} {url}")
    if headers:
        logger.debug(f"Headers: {headers}")
    if body:
        logger.debug(f"Body: {body}")


def log_response(response):
    """Logs API response details."""
    try:
        status = response.status_code
        logger.info(f"⬅️ RESPONSE [{status}]: {response.url}")
        logger.debug(f"Response Headers: {dict(response.headers)}")

        # Try to log JSON or fallback to text
        try:
            logger.debug(f"Response Body: {response.json()}")
        except Exception:
            logger.debug(f"Response Body: {response.text}")

    except Exception as e:
        logger.error(f"⚠️ Failed to log response: {e}")
