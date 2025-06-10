from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # These are the default test constants to be used if they are not found in the environment or a .env file.
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "finalpassword"
    POSTGRES_DB: str = "contactapp-db"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"

    # JWT Settings with Defaults
    JWT_SECRET_KEY: str = "insecure_default_secret_for_testing"

    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Override the above default settings if .env is found
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


config = Settings()
