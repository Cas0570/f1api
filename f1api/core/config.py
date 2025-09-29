from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    log_level: str = "info"

    # Postgres / SQLAlchemy
    database_url: str = "postgresql+psycopg://f1:f1password@localhost:5432/f1db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",  # use exact names like DATABASE_URL
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
