from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    CASHBACK_EXTERNAL_URL: str
    CASHBACK_EXTERNAL_TOKEN: str
    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SECRET_KEY: str
    ALGORITHM: str
    RESELLER_PURCHASE_APPROVED: str
    LOGGER_LEVEL: str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )
