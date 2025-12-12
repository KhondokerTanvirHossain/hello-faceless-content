"""
Approval model for tracking user approval requests and decisions.
"""
import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship

from src.models.database import Base


class ApprovalStage(enum.Enum):
    """Approval stage enum."""

    SCRIPT = "script"
    VIDEO = "video"
    PUBLISH = "publish"


class ApprovalStatus(enum.Enum):
    """Approval status enum."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class Approval(Base):
    """
    Approval model tracking approval requests and user decisions.

    Each approval represents a checkpoint in the video generation pipeline.
    """

    __tablename__ = "approvals"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)

    # Approval Details
    stage = Column(SQLEnum(ApprovalStage), nullable=False)
    status = Column(SQLEnum(ApprovalStatus), nullable=False, default=ApprovalStatus.PENDING)

    # User Feedback
    notes = Column(Text, nullable=True)

    # Reference IDs (optional, for tracking what was approved)
    script_id = Column(Integer, ForeignKey("scripts.id"), nullable=True)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=True)

    # Timestamps
    requested_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    responded_at = Column(DateTime, nullable=True)

    # Relationships
    job = relationship("Job", back_populates="approvals")

    def __repr__(self) -> str:
        return f"<Approval(id={self.id}, job_id={self.job_id}, stage={self.stage.value}, status={self.status.value})>"

    @property
    def is_pending(self) -> bool:
        """Check if approval is still pending."""
        return self.status == ApprovalStatus.PENDING

    @property
    def is_approved(self) -> bool:
        """Check if approval was granted."""
        return self.status == ApprovalStatus.APPROVED

    @property
    def is_rejected(self) -> bool:
        """Check if approval was rejected."""
        return self.status == ApprovalStatus.REJECTED

    def approve(self, notes: Optional[str] = None) -> None:
        """
        Approve the request.

        Args:
            notes: Optional approval notes
        """
        self.status = ApprovalStatus.APPROVED
        self.notes = notes
        self.responded_at = datetime.utcnow()

    def reject(self, notes: str) -> None:
        """
        Reject the request.

        Args:
            notes: Rejection notes/feedback (required)
        """
        self.status = ApprovalStatus.REJECTED
        self.notes = notes
        self.responded_at = datetime.utcnow()

    def get_response_time_seconds(self) -> Optional[int]:
        """
        Calculate response time in seconds.

        Returns:
            Response time in seconds, or None if not responded yet
        """
        if not self.responded_at:
            return None

        delta = self.responded_at - self.requested_at
        return int(delta.total_seconds())
