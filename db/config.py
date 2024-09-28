from pydantic.env_settings import BaseSettings


class Config(BaseSettings):
    URL: str = 'sqlite:///adapi.db'
    ECHO: bool = False

    class Config:
        env_prefix = 'DB_'


config = Config()
