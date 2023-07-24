from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_NAME: str
    POSTGRES_DB: str
    POSTGRES_PORT: int

    class Config:
        env_file = '.env'


settings = Settings()
