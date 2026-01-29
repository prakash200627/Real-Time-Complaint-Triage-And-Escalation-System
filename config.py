import os


def _env(key: str, default: str | None = None) -> str | None:
    value = os.getenv(key)
    if value is None or value == "":
        return default
    return value


class Config:
    SECRET_KEY = _env("SECRET_KEY", "change-me")
    JWT_SECRET_KEY = _env("JWT_SECRET_KEY", SECRET_KEY)

    SQLALCHEMY_DATABASE_URI = _env("DATABASE_URL", "sqlite:///complaints.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    DEBUG = False
