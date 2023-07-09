from pydantic import SecretStr
from pydantic_settings import BaseSettings
from typing import List, AnyStr


class Settings(BaseSettings):
    bot_token: SecretStr

    card_number: AnyStr

    class Config:
        env_file = '.env'
        # кодування файла
        env_file_encoding = 'utf-8'


config = Settings()
