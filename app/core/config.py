from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    MODE: Literal['DEV', 'TEST', 'PROD']
    DATABASE_URL: str
    TEST_DATABASE_URL: str
    SECRET_KEY: str
    REDIS: str
    SMTP_HOST: str
    SMTP_PORT: str
    SMTP_USER: str
    SMTP_PASS: str

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()