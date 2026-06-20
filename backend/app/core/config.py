from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )

    finnhub_api_key: str
    database_url: str = "./finn_tracker.db"
    cors_origins: list[str] = ["http://localhost:5173"]
    port: int = 3101


settings = Settings()
