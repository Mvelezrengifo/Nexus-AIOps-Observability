"""
Configuration settings using pydantic-settings.
Loads from environment variables with validation.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = Field(default="NEXUS-Backend", description="Application name")
    app_env: Literal["development", "staging", "production"] = Field(
        default="development", description="Environment"
    )
    debug: bool = Field(default=False, description="Debug mode")
    app_version: str = Field(default="1.0.0", description="Application version")

    # API
    api_prefix: str = Field(default="/api/v1", description="API route prefix")

    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/nexus_db",
        description="PostgreSQL connection URL (async)",
    )

    # Security
    jwt_secret_key: str = Field(
        default="change-this-secret-key-in-production",
        description="JWT secret key",
    )
    jwt_algorithm: str = Field(default="HS256", description="JWT algorithm")
    jwt_expiration_minutes: int = Field(
        default=30, description="JWT token expiration in minutes"
    )

    # AI Services
    groq_api_key: str = Field(default="", description="Groq API key")
    openai_api_key: str = Field(default="", description="OpenAI API key")

    # AWS
    aws_access_key_id: str = Field(
        default="",
        validation_alias="AWS_ACCESS_KEY_ID",
        description="AWS Access Key ID",
    )
    aws_secret_access_key: str = Field(
        default="",
        validation_alias="AWS_SECRET_ACCESS_KEY",
        description="AWS Secret Access Key",
    )
    aws_region: str = Field(
        default="us-east-1",
        validation_alias="AWS_REGION",
        description="AWS Region",
    )
    aws_sqs_queue_url: str = Field(
        default="",
        validation_alias="AWS_SQS_QUEUE_URL",
        description="AWS SQS Queue URL",
    )
    aws_s3_bucket_name: str = Field(
        default="",
        validation_alias="AWS_S3_BUCKET_NAME",
        description="AWS S3 Bucket Name",
    )
    sns_topic_arn: str = Field(
        default="",
        validation_alias="SNS_TOPIC_ARN",
        description="SNS Topic ARN",
    )

    # Observability
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", description="Logging level"
    )

    # CORS
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        description="Allowed CORS origins",
    )

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.app_env == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.app_env == "production"

    @field_validator("jwt_secret_key")
    @classmethod
    def validate_jwt_secret(cls, v: str, info) -> str:
        """Ensure JWT secret is changed in production."""
        if info.data.get("app_env") == "production":
            if v == "change-this-secret-key-in-production" or len(v) < 32:
                raise ValueError(
                    "JWT secret key must be changed in production "
                    "and be at least 32 characters"
                )
        return v


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Convenience export
settings = get_settings()