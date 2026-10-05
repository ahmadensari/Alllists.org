import os


class ConfigError(RuntimeError):
    pass


def load_config():
    """Read settings from the environment. Production refuses to start without real secrets."""
    env = os.getenv("APP_ENV", "development")
    secret_key = os.getenv("SECRET_KEY")
    database_url = os.getenv("DATABASE_URL")

    if env == "production":
        missing = [
            name
            for name, value in (("SECRET_KEY", secret_key), ("DATABASE_URL", database_url))
            if not value
        ]
        if missing:
            raise ConfigError("Missing required environment variables: " + ", ".join(missing))

    return {
        "SECRET_KEY": secret_key or "dev-only-secret-change-me",
        "SQLALCHEMY_DATABASE_URI": database_url or "sqlite:///alllists-dev.db",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "JWT_EXPIRY_HOURS": int(os.getenv("JWT_EXPIRY_HOURS", "12")),
    }
