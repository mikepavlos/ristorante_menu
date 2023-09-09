from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        extra='allow'
    )

    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    REDIS: str

    DB_USER_TEST: str
    DB_PASS_TEST: str
    DB_NAME_TEST: str
    DB_HOST_TEST: str
    DB_PORT_TEST: int
    REDIS_TEST: str


settings = Settings()
