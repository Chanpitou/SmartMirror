from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_ENGINE: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"