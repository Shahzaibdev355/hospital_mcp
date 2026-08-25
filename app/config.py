from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # ---------------- PostgreSQL ----------------
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # Groq key
    GROQ_API_KEY: str
    GROQ_MODEL: str

    OPENFDA_BASE_URL: str
    FHIR_BASE_URL: str

    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# single shared instance — import this everywhere you need config
settings = Settings()
