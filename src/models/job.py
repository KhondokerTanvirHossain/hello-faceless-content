"""
Job model for tracking video generation jobs through the pipeline.
"""
import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship

from src.models.database import Base


class JobStatus(enum.Enum):
    """Job status enum tracking the pipeline stages."""

    PENDING_SCRIPT = "pending_script"
    AWAITING_SCRIPT_APPROVAL = "awaiting_script_approval"
    SCRIPT_APPROVED = "script_approved"
    GENERATING_MEDIA = "generating_media"
    AWAITING_VIDEO_APPROVAL = "awaiting_video_approval"
    VIDEO_APPROVED = "video_approved"
    READY_TO_PUBLISH = "ready_to_publish"
    AWAITING_PUBLISH_APPROVAL = "awaiting_publish_approval"
    PUBLISH_APPROVED = "publish_approved"
    PUBLISHED = "published"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Job(Base):
    """
    Job model representing a video generation job.

    Tracks the entire lifecycle from topic input to published video.
    """

    __tablename__ = "jobs"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Job Details
    topic = Column(String(500), nullable=False)
    status = Column(SQLEnum(JobStatus), nullable=False, default=JobStatus.PENDING_SCRIPT)

    # Configuration (stored as JSON)
    config = Column(JSON, nullable=True)
    # Example config structure:
    # {
    #     "style": "educational",
    #     "duration": 60,
    #     "animation_style": "kinetic_text",
    #     "color_scheme": "vibrant",
    #     "tts_provider": "gtts",
    #     "music_mood": "upbeat",
    #     "music_volume": 0.3,
    #     "platforms": ["facebook", "youtube"]
    # }

    # File Paths
    video_draft_path = Column(String(500), nullable=True)
    video_final_path = Column(String(500), nullable=True)
    thumbnail_path = Column(String(500), nullable=True)

    # Metadata
    error_message = Column(Text, nullable=True)
    published_at = Column(DateTime, nullable=True)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    scripts = relationship("Script", back_populates="job", cascade="all, delete-orphan")
    approvals = relationship("Approval", back_populates="job", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Job(id={self.id}, topic='{self.topic[:30]}...', status={self.status.value})>"

    @property
    def current_script(self) -> Optional["Script"]:
        """Get the most recent script for this job."""
        if not self.scripts:
            return None
        return max(self.scripts, key=lambda s: s.version)

    @property
    def is_complete(self) -> bool:
        """Check if the job has been published."""
        return self.status == JobStatus.PUBLISHED

    @property
    def is_failed(self) -> bool:
        """Check if the job has failed."""
        return self.status == JobStatus.FAILED

    @property
    def is_cancelled(self) -> bool:
        """Check if the job was cancelled."""
        return self.status == JobStatus.CANCELLED

    @property
    def needs_approval(self) -> bool:
        """Check if the job is waiting for approval."""
        return self.status in [
            JobStatus.AWAITING_SCRIPT_APPROVAL,
            JobStatus.AWAITING_VIDEO_APPROVAL,
            JobStatus.AWAITING_PUBLISH_APPROVAL,
        ]

    def update_status(self, new_status: JobStatus, error_message: Optional[str] = None) -> None:
        """
        Update job status.

        Args:
            new_status: New job status
            error_message: Optional error message if status is FAILED
        """
        self.status = new_status
        self.updated_at = datetime.utcnow()

        if error_message:
            self.error_message = error_message

        if new_status == JobStatus.PUBLISHED:
            self.published_at = datetime.utcnow()

    def get_config_value(self, key: str, default=None):
        """
        Get a configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        if not self.config:
            return default
        return self.config.get(key, default)

    def set_config_value(self, key: str, value) -> None:
        """
        Set a configuration value.

        Args:
            key: Configuration key
            value: Configuration value
        """
        if self.config is None:
            self.config = {}
        self.config[key] = value
        self.updated_at = datetime.utcnow()
