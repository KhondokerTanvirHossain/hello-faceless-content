"""
Configuration settings for the faceless video automation system.
Uses Pydantic Settings for environment variable management.
"""
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # LLM API Keys
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: str = "us-east-1"

    # Database
    database_url: str = "sqlite:///data/database/app.db"

    # File Paths
    output_dir: Path = Path("data/output")
    assets_dir: Path = Path("data/assets")
    cache_dir: Path = Path("data/cache")

    # Video Settings
    default_resolution: str = "1080x1920"
    default_fps: int = 30
    default_duration: int = 60

    # Social Media APIs
    fb_access_token: Optional[str] = None
    fb_page_id: Optional[str] = None
    youtube_credentials_path: Optional[Path] = None

    # Application
    debug: bool = True
    log_level: str = "INFO"

    # LLM Provider Preferences
    default_llm_provider: str = "claude"  # claude, openai, bedrock
    default_llm_model: str = "claude-3-5-haiku-20241022"  # Cost-optimized default
    fallback_llm_providers: list[str] = ["claude", "openai"]

    # Content Generation Defaults
    default_content_style: str = "educational"
    default_tts_provider: str = "gtts"
    default_music_mood: str = "upbeat"
    default_music_volume: float = 0.3

    @property
    def resolution_tuple(self) -> tuple[int, int]:
        """Convert resolution string to tuple (width, height)."""
        width, height = self.default_resolution.split("x")
        return int(width), int(height)

    def ensure_directories(self) -> None:
        """Ensure all required directories exist."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "drafts").mkdir(exist_ok=True)
        (self.output_dir / "final").mkdir(exist_ok=True)
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        (self.assets_dir / "music").mkdir(exist_ok=True)
        (self.assets_dir / "fonts").mkdir(exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        Path("data/database").mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()

# Ensure directories exist on import
settings.ensure_directories()
