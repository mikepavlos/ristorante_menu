from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {'env_file': '.env'}

    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    REDIS: str

    DB_USER_TEST: str | None = None
    DB_PASS_TEST: str | None = None
    DB_NAME_TEST: str | None = None
    DB_HOST_TEST: str | None = None
    DB_PORT_TEST: int | None = None

    POSTGRES_USER: str | None
    POSTGRES_PASSWORD: str | None
    POSTGRES_NAME: str | None
    POSTGRES_HOST_TEST: str | None
    REDIS_TEST: str | None


settings = Settings()
