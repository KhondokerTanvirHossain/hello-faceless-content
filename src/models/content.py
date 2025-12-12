"""
Content models for scripts and scenes.
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from src.models.database import Base


class Script(Base):
    """
    Script model representing a generated video script.

    Multiple versions can exist for a single job (revisions).
    """

    __tablename__ = "scripts"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)

    # Script Content (stored as JSON)
    content = Column(JSON, nullable=False)
    # Example structure:
    # {
    #     "title": "5 Amazing Space Facts",
    #     "hook": "Did you know...",
    #     "scenes": [
    #         {
    #             "text": "Scene content",
    #             "duration": 10,
    #             "visual_hint": "Animation suggestion",
    #             "keywords": ["planet", "space"]
    #         }
    #     ],
    #     "conclusion": "Final statement",
    #     "hashtags": ["space", "facts"],
    #     "estimated_duration": 60
    # }

    # Metadata
    version = Column(Integer, nullable=False, default=1)
    word_count = Column(Integer, nullable=True)
    estimated_duration = Column(Integer, nullable=True)  # in seconds

    # Approval Status
    approved = Column(Boolean, nullable=False, default=False)
    approval_notes = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    job = relationship("Job", back_populates="scripts")

    def __repr__(self) -> str:
        title = self.get_title()
        return f"<Script(id={self.id}, job_id={self.job_id}, title='{title[:30]}...', version={self.version})>"

    def get_title(self) -> str:
        """Get the script title from content."""
        if not self.content:
            return "Untitled"
        return self.content.get("title", "Untitled")

    def get_hook(self) -> Optional[str]:
        """Get the script hook (opening line)."""
        if not self.content:
            return None
        return self.content.get("hook")

    def get_scenes(self) -> list[dict]:
        """Get the list of scenes."""
        if not self.content:
            return []
        return self.content.get("scenes", [])

    def get_conclusion(self) -> Optional[str]:
        """Get the script conclusion."""
        if not self.content:
            return None
        return self.content.get("conclusion")

    def get_hashtags(self) -> list[str]:
        """Get the list of hashtags."""
        if not self.content:
            return []
        return self.content.get("hashtags", [])

    def get_full_text(self) -> str:
        """
        Get the full script text (all scenes combined).

        Returns:
            Complete script text
        """
        parts = []

        if hook := self.get_hook():
            parts.append(hook)

        for scene in self.get_scenes():
            if text := scene.get("text"):
                parts.append(text)

        if conclusion := self.get_conclusion():
            parts.append(conclusion)

        return " ".join(parts)

    def calculate_word_count(self) -> int:
        """
        Calculate and update word count.

        Returns:
            Word count
        """
        full_text = self.get_full_text()
        self.word_count = len(full_text.split())
        return self.word_count

    def calculate_estimated_duration(self) -> int:
        """
        Calculate estimated duration based on scenes.

        Returns:
            Estimated duration in seconds
        """
        total_duration = 0
        for scene in self.get_scenes():
            total_duration += scene.get("duration", 0)

        self.estimated_duration = total_duration
        return self.estimated_duration

    def approve(self, notes: Optional[str] = None) -> None:
        """
        Mark script as approved.

        Args:
            notes: Optional approval notes
        """
        self.approved = True
        self.approval_notes = notes
        self.updated_at = datetime.utcnow()

    def reject(self, notes: str) -> None:
        """
        Mark script as rejected (not approved).

        Args:
            notes: Rejection notes/feedback
        """
        self.approved = False
        self.approval_notes = notes
        self.updated_at = datetime.utcnow()


class Video(Base):
    """
    Video model representing a generated video file.

    Multiple versions can exist (draft vs final).
    """

    __tablename__ = "videos"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    script_id = Column(Integer, ForeignKey("scripts.id"), nullable=True)

    # File Paths
    file_path = Column(String(500), nullable=False)
    thumbnail_path = Column(String(500), nullable=True)

    # Video Metadata
    duration = Column(Integer, nullable=True)  # in seconds
    resolution = Column(String(20), nullable=True)  # e.g., "1080x1920"
    file_size_mb = Column(Integer, nullable=True)
    is_draft = Column(Boolean, nullable=False, default=True)

    # Generation Metadata (stored as JSON)
    metadata = Column(JSON, nullable=True)
    # Example structure:
    # {
    #     "scenes": [
    #         {
    #             "index": 0,
    #             "start_time": 0.0,
    #             "end_time": 10.5,
    #             "animation_type": "kinetic_text"
    #         }
    #     ],
    #     "audio": {
    #         "tts_provider": "gtts",
    #         "music_track": "upbeat_01.mp3"
    #     },
    #     "effects": ["fade_in", "fade_out"]
    # }

    # Approval Status
    approved = Column(Boolean, nullable=False, default=False)
    approval_notes = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Video(id={self.id}, job_id={self.job_id}, draft={self.is_draft}, approved={self.approved})>"

    def approve(self, notes: Optional[str] = None) -> None:
        """Mark video as approved."""
        self.approved = True
        self.approval_notes = notes
        self.updated_at = datetime.utcnow()

    def reject(self, notes: str) -> None:
        """Mark video as rejected."""
        self.approved = False
        self.approval_notes = notes
        self.updated_at = datetime.utcnow()


class Publication(Base):
    """
    Publication model tracking video posts to social media platforms.
    """

    __tablename__ = "publications"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)

    # Platform Details
    platform = Column(String(50), nullable=False)  # facebook, youtube, instagram, tiktok
    post_id = Column(String(200), nullable=True)  # Platform-specific post ID
    post_url = Column(String(500), nullable=True)  # Direct URL to post

    # Metadata (stored as JSON)
    metadata = Column(JSON, nullable=True)
    # Example structure:
    # {
    #     "title": "5 Amazing Space Facts",
    #     "caption": "Did you know...",
    #     "hashtags": ["space", "facts"],
    #     "thumbnail_text": "Space Facts"
    # }

    # Status
    status = Column(String(50), nullable=False, default="pending")  # pending, published, failed
    error_message = Column(Text, nullable=True)

    # Timestamps
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Publication(id={self.id}, platform={self.platform}, status={self.status})>"

    def mark_published(self, post_id: str, post_url: str) -> None:
        """Mark publication as successful."""
        self.status = "published"
        self.post_id = post_id
        self.post_url = post_url
        self.published_at = datetime.utcnow()

    def mark_failed(self, error_message: str) -> None:
        """Mark publication as failed."""
        self.status = "failed"
        self.error_message = error_message
