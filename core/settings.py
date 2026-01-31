from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

from .const import BASE_DIR


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")


settings = Settings()

__all__ = ["settings"]
