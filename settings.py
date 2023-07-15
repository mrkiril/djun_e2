from pydantic import SecretStr, BaseSettings
from typing import List, AnyStr


class Settings(BaseSettings):
    bot_token: SecretStr

    class Config:
        env_file = '.env'
        # кодування файла
        env_file_encoding = 'utf-8'


config = Settings()
