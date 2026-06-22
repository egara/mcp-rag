from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings, loaded from environment variables or a .env file.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # PostgreSQL / pgvector
    postgres_host: str = "localhost"
    postgres_port: int = 5433
    postgres_user: str = "rag_user"
    postgres_password: str = "rag_password"
    postgres_db: str = "rag_db"
    pgvector_collection: str = "documents"

    # Embeddings
    embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

    @property
    def postgres_connection_string(self) -> str:
        """Constructs the SQLAlchemy connection string for PostgreSQL.

        Returns:
            str: The formatted PostgreSQL connection URI.
        """
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

settings = Settings()
