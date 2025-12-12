"""
Caching utilities for LLM responses.
Implements simple file-based caching to reduce API costs.
"""
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Any

from src.config.settings import settings
from src.utils.logger import logger


class LLMCache:
    """File-based cache for LLM responses."""

    def __init__(self, cache_dir: Optional[Path] = None):
        """
        Initialize the LLM cache.

        Args:
            cache_dir: Directory to store cache files (defaults to settings.cache_dir/llm)
        """
        self.cache_dir = cache_dir or (settings.cache_dir / "llm")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _generate_cache_key(self, prompt: str, model: str, **kwargs) -> str:
        """
        Generate a unique cache key from prompt and parameters.

        Args:
            prompt: The LLM prompt
            model: The model name
            **kwargs: Additional parameters (temperature, max_tokens, etc.)

        Returns:
            MD5 hash of the inputs
        """
        # Create a stable string representation of all inputs
        cache_input = {
            "prompt": prompt,
            "model": model,
            **{k: v for k, v in sorted(kwargs.items()) if v is not None}
        }

        # Generate MD5 hash
        cache_str = json.dumps(cache_input, sort_keys=True)
        return hashlib.md5(cache_str.encode()).hexdigest()

    def _get_cache_path(self, cache_key: str) -> Path:
        """Get the file path for a cache key."""
        return self.cache_dir / f"{cache_key}.json"

    def get(self, prompt: str, model: str, max_age_hours: int = 24 * 7, **kwargs) -> Optional[str]:
        """
        Retrieve a cached response if available and not expired.

        Args:
            prompt: The LLM prompt
            model: The model name
            max_age_hours: Maximum age of cache in hours (default: 7 days)
            **kwargs: Additional parameters used for cache key generation

        Returns:
            Cached response or None if not found/expired
        """
        cache_key = self._generate_cache_key(prompt, model, **kwargs)
        cache_path = self._get_cache_path(cache_key)

        if not cache_path.exists():
            logger.debug(f"Cache miss for key: {cache_key}")
            return None

        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                cache_data = json.load(f)

            # Check if cache is expired
            cached_at = datetime.fromisoformat(cache_data["cached_at"])
            age = datetime.now() - cached_at

            if age > timedelta(hours=max_age_hours):
                logger.debug(f"Cache expired for key: {cache_key} (age: {age})")
                cache_path.unlink()  # Delete expired cache
                return None

            logger.info(f"Cache hit for key: {cache_key} (age: {age})")
            return cache_data["response"]

        except Exception as e:
            logger.error(f"Error reading cache for key {cache_key}: {e}")
            return None

    def set(self, prompt: str, model: str, response: str, **kwargs) -> None:
        """
        Store a response in the cache.

        Args:
            prompt: The LLM prompt
            model: The model name
            response: The LLM response to cache
            **kwargs: Additional parameters used for cache key generation
        """
        cache_key = self._generate_cache_key(prompt, model, **kwargs)
        cache_path = self._get_cache_path(cache_key)

        cache_data = {
            "prompt": prompt,
            "model": model,
            "response": response,
            "cached_at": datetime.now().isoformat(),
            "parameters": {k: v for k, v in kwargs.items() if v is not None}
        }

        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)

            logger.debug(f"Cached response for key: {cache_key}")

        except Exception as e:
            logger.error(f"Error writing cache for key {cache_key}: {e}")

    def clear_expired(self, max_age_hours: int = 24 * 7) -> int:
        """
        Clear expired cache entries.

        Args:
            max_age_hours: Maximum age of cache in hours

        Returns:
            Number of entries cleared
        """
        cleared_count = 0
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)

        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    cache_data = json.load(f)

                cached_at = datetime.fromisoformat(cache_data["cached_at"])

                if cached_at < cutoff_time:
                    cache_file.unlink()
                    cleared_count += 1

            except Exception as e:
                logger.error(f"Error processing cache file {cache_file}: {e}")

        if cleared_count > 0:
            logger.info(f"Cleared {cleared_count} expired cache entries")

        return cleared_count

    def clear_all(self) -> int:
        """
        Clear all cache entries.

        Returns:
            Number of entries cleared
        """
        cleared_count = 0

        for cache_file in self.cache_dir.glob("*.json"):
            try:
                cache_file.unlink()
                cleared_count += 1
            except Exception as e:
                logger.error(f"Error deleting cache file {cache_file}: {e}")

        logger.info(f"Cleared all cache: {cleared_count} entries")
        return cleared_count

    def get_cache_stats(self) -> dict[str, Any]:
        """
        Get statistics about the cache.

        Returns:
            Dictionary with cache statistics
        """
        cache_files = list(self.cache_dir.glob("*.json"))
        total_files = len(cache_files)

        if total_files == 0:
            return {
                "total_entries": 0,
                "total_size_mb": 0.0,
                "oldest_entry": None,
                "newest_entry": None,
            }

        total_size = sum(f.stat().st_size for f in cache_files)
        total_size_mb = total_size / (1024 * 1024)

        # Find oldest and newest
        oldest_time = None
        newest_time = None

        for cache_file in cache_files:
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    cache_data = json.load(f)
                    cached_at = datetime.fromisoformat(cache_data["cached_at"])

                    if oldest_time is None or cached_at < oldest_time:
                        oldest_time = cached_at

                    if newest_time is None or cached_at > newest_time:
                        newest_time = cached_at

            except Exception:
                continue

        return {
            "total_entries": total_files,
            "total_size_mb": round(total_size_mb, 2),
            "oldest_entry": oldest_time.isoformat() if oldest_time else None,
            "newest_entry": newest_time.isoformat() if newest_time else None,
        }


# Global cache instance
llm_cache = LLMCache()
