"""Setting pydantic"""
import logging
import os

from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    """Model Settings"""

    log_level: str = os.getenv('LOG_LEVEL')

    if log_level == 'DEBUG':
        log_level = logging.DEBUG
    elif log_level == 'INFO':
        log_level = logging.INFO
    elif log_level == 'WARNING':
        log_level = logging.WARNING
    elif log_level == 'ERROR':
        log_level = logging.ERROR
    elif log_level == 'CRITICAL':
        log_level = logging.CRITICAL

    # Database
    db_user: str = os.getenv('DB_USER')
    db_pass: str = os.getenv('DB_PASS')
    db_host: str = os.getenv('DB_HOST')
    db_port: str = os.getenv('DB_PORT')
    db_namespace: str = os.getenv('DB_NAMESPACE')

    # smtp server
    email_host: str = os.getenv('EMAIL_HOST')
    email_port: int = os.getenv('EMAIL_PORT')
    email_username: str = os.getenv('EMAIL_USERNAME')
    email_password: str = os.getenv('EMAIL_PASSWORD')

    # frontend
    frontend_url: str = os.getenv('FRONTEND_URL')

    # Logging
    LOGGING_CONFIG: dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
        }
    }
