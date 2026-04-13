from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = Field(validation_alias="DATABASE_URL")
    db_echo: bool = Field(default=False, validation_alias="DB_ECHO")
    jwt_secret: str = Field(validation_alias="JWT_SECRET")
    jwt_algorithm: str = Field(validation_alias="JWT_ALGORITHM")
    redis_host: str = Field(default="localhost", validation_alias="REDIS_HOST")
    redis_port: int = Field(default=6379, validation_alias="REDIS_PORT")
    profiling_enabled: bool = Field(default=False, validation_alias="PROFILING_ENABLED")
    mail_username: str = Field(validation_alias="MAIL_USERNAME")
    mail_password: str = Field(validation_alias="MAIL_PASSWORD")
    mail_from: str = Field(validation_alias="MAIL_FROM")
    mail_from_name: str = Field(default="BBS", validation_alias="MAIL_FROM_NAME")
    mail_server: str = Field(default="smtp.gmail.com", validation_alias="MAIL_SERVER")
    mail_port: int = Field(default=587, validation_alias="MAIL_PORT")
    mail_starttls: bool = Field(default=True, validation_alias="MAIL_STARTTLS")
    mail_ssl_tls: bool = Field(default=False, validation_alias="MAIL_SSL_TLS")
    mail_use_credentials: bool = Field(default=True, validation_alias="MAIL_USE_CREDENTIALS")
    domain: str = Field(default="localhost:8000", validation_alias="DOMAIN")
    redis_url: str = Field(default="redis://localhost:6379/0", validation_alias="REDIS_URL")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
