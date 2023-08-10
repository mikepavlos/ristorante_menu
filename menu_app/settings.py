from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_NAME: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    REDIS: str

    class Config:
        env_file = '.env'


settings = Settings()
