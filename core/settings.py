from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from .const import BASE_DIR


LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")

    dota_market_api_key: SecretStr

    log_level: LogLevel = "INFO"


settings = Settings()  # type: ignore

__all__ = ["settings"]
