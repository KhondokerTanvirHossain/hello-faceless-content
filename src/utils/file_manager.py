"""
File management utilities for the video automation system.
Handles file operations, path management, and storage.
"""
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

from src.config.settings import settings
from src.utils.logger import logger


class FileManager:
    """Manages file operations and storage for the application."""

    @staticmethod
    def get_draft_video_path(job_id: int) -> Path:
        """Get the path for a draft video file."""
        filename = f"job_{job_id}_draft_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        path = settings.output_dir / "drafts" / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    @staticmethod
    def get_final_video_path(job_id: int) -> Path:
        """Get the path for a final approved video file."""
        filename = f"job_{job_id}_final_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        path = settings.output_dir / "final" / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    @staticmethod
    def get_audio_path(job_id: int, audio_type: str = "voice") -> Path:
        """Get the path for an audio file (voice, music, or mixed)."""
        filename = f"job_{job_id}_{audio_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        path = settings.cache_dir / "audio" / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    @staticmethod
    def get_animation_path(job_id: int, scene_index: int) -> Path:
        """Get the path for an animation file."""
        filename = f"job_{job_id}_scene_{scene_index}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        path = settings.cache_dir / "animations" / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    @staticmethod
    def get_thumbnail_path(job_id: int) -> Path:
        """Get the path for a video thumbnail."""
        filename = f"job_{job_id}_thumbnail_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        path = settings.output_dir / "final" / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    @staticmethod
    def list_music_files(mood: Optional[str] = None) -> list[Path]:
        """
        List available music files from the assets directory.

        Args:
            mood: Optional mood filter (subdirectory name)

        Returns:
            List of paths to music files
        """
        music_dir = settings.assets_dir / "music"
        if mood:
            music_dir = music_dir / mood

        if not music_dir.exists():
            logger.warning(f"Music directory not found: {music_dir}")
            return []

        # Common audio file extensions
        audio_extensions = {".mp3", ".wav", ".m4a", ".ogg"}

        music_files = [
            f for f in music_dir.rglob("*")
            if f.is_file() and f.suffix.lower() in audio_extensions
        ]

        logger.info(f"Found {len(music_files)} music files in {music_dir}")
        return sorted(music_files)

    @staticmethod
    def cleanup_old_drafts(days: int = 7) -> None:
        """
        Delete draft videos older than specified days.

        Args:
            days: Number of days to keep drafts
        """
        drafts_dir = settings.output_dir / "drafts"
        if not drafts_dir.exists():
            return

        cutoff_date = datetime.now() - timedelta(days=days)
        deleted_count = 0

        for file_path in drafts_dir.glob("*.mp4"):
            if file_path.stat().st_mtime < cutoff_date.timestamp():
                try:
                    file_path.unlink()
                    deleted_count += 1
                    logger.info(f"Deleted old draft: {file_path.name}")
                except Exception as e:
                    logger.error(f"Failed to delete {file_path}: {e}")

        if deleted_count > 0:
            logger.info(f"Cleaned up {deleted_count} old draft videos")

    @staticmethod
    def cleanup_cache(max_size_mb: int = 1000) -> None:
        """
        Clean up cache directory if it exceeds max size.

        Args:
            max_size_mb: Maximum cache size in megabytes
        """
        cache_dir = settings.cache_dir
        if not cache_dir.exists():
            return

        # Calculate current cache size
        total_size = sum(
            f.stat().st_size for f in cache_dir.rglob("*") if f.is_file()
        )
        total_size_mb = total_size / (1024 * 1024)

        if total_size_mb > max_size_mb:
            logger.warning(f"Cache size ({total_size_mb:.2f} MB) exceeds limit ({max_size_mb} MB)")

            # Get all files with their modification times
            files = [
                (f, f.stat().st_mtime)
                for f in cache_dir.rglob("*")
                if f.is_file()
            ]

            # Sort by modification time (oldest first)
            files.sort(key=lambda x: x[1])

            # Delete oldest files until under limit
            deleted_count = 0
            for file_path, _ in files:
                try:
                    file_size = file_path.stat().st_size
                    file_path.unlink()
                    total_size -= file_size
                    deleted_count += 1

                    if total_size / (1024 * 1024) <= max_size_mb * 0.8:  # Leave 20% buffer
                        break
                except Exception as e:
                    logger.error(f"Failed to delete cache file {file_path}: {e}")

            logger.info(f"Cleaned up {deleted_count} cache files")

    @staticmethod
    def copy_to_final(draft_path: Path, job_id: int) -> Path:
        """
        Copy a draft video to final directory.

        Args:
            draft_path: Path to the draft video
            job_id: Job ID for naming

        Returns:
            Path to the final video
        """
        final_path = FileManager.get_final_video_path(job_id)
        shutil.copy2(draft_path, final_path)
        logger.info(f"Copied draft to final: {final_path}")
        return final_path

    @staticmethod
    def get_file_size_mb(file_path: Path) -> float:
        """Get file size in megabytes."""
        if not file_path.exists():
            return 0.0
        return file_path.stat().st_size / (1024 * 1024)

    @staticmethod
    def ensure_directory(path: Path) -> None:
        """Ensure a directory exists, create if it doesn't."""
        path.mkdir(parents=True, exist_ok=True)


# Create a global instance
file_manager = FileManager()
