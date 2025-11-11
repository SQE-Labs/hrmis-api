import logging
import os
from datetime import datetime


def get_logger(name: str = "APIFramework") -> logging.Logger:
    """
    Returns a logger instance that logs to both console and file.
    Designed for detailed API test logging.
    """

    # Create logs directory
    log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
    os.makedirs(log_dir, exist_ok=True)

    # Timestamped log file (one per test run)
    log_file = os.path.join(
        log_dir, f"api_tests_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )

    # Create or get logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Avoid duplicate handlers (pytest reruns)
    if logger.handlers:
        return logger

    # --- Console Handler ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        "[%(levelname)s] %(message)s"
    )
    console_handler.setFormatter(console_formatter)

    # --- File Handler ---
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_formatter)

    # Attach handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.info(f"🗂️ Log file created at: {log_file}")
    return logger


# Create a default logger instance
logger = get_logger()


def log_request(method: str, url: str, headers=None, body=None):
    """Logs detailed API request information."""
    logger.info(f"➡️ REQUEST: {method.upper()} {url}")

    if headers:
        logger.debug(f"Headers: {headers}")

    if body:
        if isinstance(body, (dict, list)):
            logger.debug(f"Body (JSON): {body}")
        else:
            logger.debug(f"Body (Raw): {body}")


def log_response(response):
    """Logs detailed API response information."""
    try:
        logger.info(f"⬅️ RESPONSE [{response.status_code}] from {response.url}")

        # Headers
        logger.debug(f"Response Headers: {dict(response.headers)}")

        # Try JSON, else fallback to text
        try:
            json_body = response.json()
            logger.debug(f"Response JSON: {json_body}")
        except ValueError:
            text_body = response.text.strip()
            logger.debug(f"Response Text: {text_body if text_body else '[empty response]'}")

    except Exception as e:
        logger.error(f"⚠️ Failed to log response: {e}")
   