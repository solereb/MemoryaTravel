from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Конфиг с чувствительными данными из .env"""
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    JWT_SECRET_KEY: str
    REFRESH_TOKEN_SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    REFRESH_WITHOUT_CHECKED: int
    POSTGRESQL_USER: str
    POSTGRESQL_PASSWORD: str
    POSTGRESQL_IP: str
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    GOOGLE_PASSWORD: str
    EMAIL: str
    PASSWORD: str


settings = Settings()