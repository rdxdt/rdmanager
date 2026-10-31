import os
from pathlib import Path

from dotenv import load_dotenv

# The .env file lives in the project root, one level above this package
load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def env_bool(name, default=False):
    return os.getenv(name, str(default)).strip().lower() in ("1", "true", "yes", "on")


class Config:
    # Set FLASK_DEBUG=true for development, false (default) for production
    DEBUG = env_bool("FLASK_DEBUG")

    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")

    # SMTP settings consumed by Flask-Mail
    MAIL_SERVER = os.getenv("MAIL_SERVER", "localhost")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "25"))
    MAIL_USE_TLS = env_bool("MAIL_USE_TLS")
    MAIL_USE_SSL = env_bool("MAIL_USE_SSL")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

    HCAPTCHA_SITE_KEY = os.getenv("HCAPTCHA_SITE_KEY")
    HCAPTCHA_SECRET_KEY = os.getenv("HCAPTCHA_SECRET_KEY")
    HCAPTCHA_ENABLED = not DEBUG
