from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class CORSSettings(BaseModel):
    allow_origins: list[str]
    allow_credentials: bool
    allow_methods: list[str]
    allow_headers: list[str]


class Settings(BaseSettings):
    APP_TIMEZONE: str
    APP_NAME: str
    API_URL: str
    FRONTEND_MAIN_PAGE_URL: str
    CORS: CORSSettings

    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


settings = Settings()
