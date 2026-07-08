from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://locadora:locadora@localhost:5432/locadora"
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    environment: str = "development"
    cors_origins: str = "http://localhost:5173"

    @field_validator("database_url")
    @classmethod
    def forcar_driver_psycopg3(cls, v: str) -> str:
        """Normaliza o esquema para o driver psycopg (v3), o único instalado no projeto.

        Strings de conexão coladas direto de provedores (Supabase, etc.) costumam vir
        como "postgresql://" ou "postgresql+psycopg2://", que o SQLAlchemy resolve para
        o driver psycopg2 — não instalado aqui — derrubando a aplicação na inicialização.
        """
        if v.startswith("postgresql+psycopg2://"):
            return "postgresql+psycopg://" + v[len("postgresql+psycopg2://") :]
        if v.startswith("postgresql://"):
            return "postgresql+psycopg://" + v[len("postgresql://") :]
        return v

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
