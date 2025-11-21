from pathlib import Path

import yaml
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    name: str
    user: str
    password: str
    host: str
    port: int


class DjangoSettings(BaseSettings):
    secret_key: str
    debug: bool
    allowed_hosts: list[str]


class AppSettings(BaseSettings):
    host: str
    port: int


class Settings(BaseSettings):
    database: DatabaseSettings
    django: DjangoSettings
    app: AppSettings


def load_config() -> Settings:
    config_path = Path(__file__).parent.parent / "config.yaml"
    if not config_path.exists():
        raise FileNotFoundError(
            f"Файл конфигурации не найден: {config_path}\n"
            "Скопируйте config.yaml.example в config.yaml и заполните его."
        )
    
    with open(config_path, "r", encoding="utf-8") as f:
        config_data = yaml.safe_load(f)
    
    return Settings(**config_data)


config = load_config()
