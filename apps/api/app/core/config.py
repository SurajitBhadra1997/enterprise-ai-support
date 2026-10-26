from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Enterprise AI Support Agent"
    app_version: str = "0.1.0"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    database_url: str = (
        "postgresql+asyncpg://username:password@localhost:5432/enterprise_ai_support"
    )
    embedding_model: str = "sentence-transformers/all-mpnet-base-v2"
    pinecone_api_key:str = (
        "pcsk_3ZVEvk_QFeK1rFYC27WzQBF9S6gsYvvWwLPbt9thQDJWjaWz25ZacAJWFL3oJT22cz5dm"
    )
    index_name:str = "retrieval-poc"


settings = Settings()
