import logging
import os
from logging.handlers import RotatingFileHandler

# Define the log levels
log_levels = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

# Set up environment-specific log level
env_log_level = os.getenv("LOG_LEVEL", "INFO").upper()
log_level = log_levels.get(env_log_level, logging.INFO)

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(log_level)

# Create handlers
console_handler = logging.StreamHandler()
file_handler = RotatingFileHandler(
    "app.log", maxBytes=1024 * 20, backupCount=10  # 20 KB
)

# Create formatters and add it to handlers
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
console_formatter = logging.Formatter(log_format)
file_formatter = logging.Formatter(log_format)

console_handler.setFormatter(console_formatter)
file_handler.setFormatter(file_formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)