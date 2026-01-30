from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env.local', extra='allow', env_prefix='subs_api_')


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env.local', extra='allow', env_prefix='subs_postgres_')

    host: str = Field(default='127.0.0.1')
    port: int = Field(default=5432)
    user: str
    password: str
    db: str

    def get_url(self, driver: str | None, db: str | None = None):
        scheme = f'postgresql{f'+{driver}' if driver else ''}'
        return f'{scheme}://{self.user}:{self.password}@{self.host}:{self.port}/{db or self.db}'


class KafkaSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env.local', extra='allow', env_prefix='subs_kafka_')

    bootstrap_servers: str = Field(default='localhost:19092')


settings = Settings()
pg_settings = PostgresSettings()  # type: ignore
kafka_settings = KafkaSettings()