"""
LLM Manager for provider selection, fallback, and caching.
"""
from typing import Optional, List

from src.core.llm.base import BaseLLMProvider
from src.core.llm.claude import ClaudeProvider
from src.core.llm.openai import OpenAIProvider
from src.core.llm.bedrock import BedrockProvider
from src.config.settings import settings
from src.utils.cache import llm_cache
from src.utils.logger import logger


class LLMManager:
    """
    Manages LLM providers with smart routing, fallback, and caching.

    Features:
    - Provider selection based on task complexity
    - Automatic fallback chain
    - Response caching
    - Cost tracking
    """

    def __init__(self):
        """Initialize LLM manager with available providers."""
        self.providers = {
            "claude": ClaudeProvider(),
            "openai": OpenAIProvider(),
            "bedrock": BedrockProvider(),
        }

        # Filter to only available providers
        self.available_providers = {
            name: provider
            for name, provider in self.providers.items()
            if provider.is_available()
        }

        if not self.available_providers:
            logger.warning("No LLM providers configured!")
        else:
            logger.info(f"Available LLM providers: {list(self.available_providers.keys())}")

    def get_provider(
        self,
        provider_name: Optional[str] = None,
        task_type: str = "general"
    ) -> Optional[BaseLLMProvider]:
        """
        Get an LLM provider based on name or task type.

        Args:
            provider_name: Specific provider to use (claude, openai, bedrock)
            task_type: Type of task (simple, script_generation, refinement, etc.)

        Returns:
            LLM provider instance or None if not available
        """
        # If specific provider requested, use it
        if provider_name:
            provider = self.available_providers.get(provider_name.lower())
            if provider:
                return provider
            logger.warning(f"Requested provider '{provider_name}' not available")

        # Smart routing based on task type
        if task_type == "simple":
            # Use cheapest model for simple tasks
            for name in ["claude", "openai", "bedrock"]:
                if name in self.available_providers:
                    provider = self.available_providers[name]
                    # Use cheap model
                    if hasattr(provider, "get_cheap_model"):
                        provider.model = provider.get_cheap_model()
                    return provider

        elif task_type == "script_generation":
            # Use quality model for script generation
            if "claude" in self.available_providers:
                provider = self.available_providers["claude"]
                provider.model = ClaudeProvider.get_quality_model()  # Sonnet
                return provider
            elif "openai" in self.available_providers:
                provider = self.available_providers["openai"]
                provider.model = OpenAIProvider.get_quality_model()  # GPT-4o
                return provider

        elif task_type == "refinement":
            # Use cheap model for refinements
            for name in ["claude", "openai", "bedrock"]:
                if name in self.available_providers:
                    provider = self.available_providers[name]
                    if hasattr(provider, "get_cheap_model"):
                        provider.model = provider.get_cheap_model()
                    return provider

        # Default: return first available provider
        if self.available_providers:
            return next(iter(self.available_providers.values()))

        return None

    def generate(
        self,
        prompt: str,
        provider_name: Optional[str] = None,
        task_type: str = "general",
        use_cache: bool = True,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        fallback: bool = True,
        **kwargs
    ) -> str:
        """
        Generate text with provider selection, caching, and fallback.

        Args:
            prompt: The prompt to send
            provider_name: Specific provider to use (optional)
            task_type: Type of task for smart routing
            use_cache: Whether to use response caching
            max_tokens: Maximum tokens to generate
            temperature: Temperature for sampling
            fallback: Whether to try other providers on failure
            **kwargs: Additional provider-specific parameters

        Returns:
            Generated text

        Raises:
            Exception: If all providers fail
        """
        # Check cache first
        if use_cache:
            cached_response = llm_cache.get(
                prompt=prompt,
                model=task_type,  # Use task_type as part of cache key
                max_age_hours=168  # 7 days
            )
            if cached_response:
                logger.info("✓ Cache hit - returning cached response")
                return cached_response

        # Get primary provider
        provider = self.get_provider(provider_name, task_type)

        if not provider:
            raise Exception("No LLM providers available")

        # Build fallback chain
        fallback_providers: List[BaseLLMProvider] = []
        if fallback:
            # Try all other available providers as fallbacks
            for name, fallback_provider in self.available_providers.items():
                if fallback_provider != provider:
                    fallback_providers.append(fallback_provider)

        # Try primary provider
        providers_to_try = [provider] + fallback_providers

        last_error = None

        for idx, current_provider in enumerate(providers_to_try):
            provider_name = current_provider.provider_name
            is_fallback = idx > 0

            try:
                if is_fallback:
                    logger.info(f"Trying fallback provider: {provider_name}")

                response = current_provider.generate(
                    prompt=prompt,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    **kwargs
                )

                # Cache the response
                if use_cache:
                    llm_cache.set(
                        prompt=prompt,
                        model=task_type,
                        response=response
                    )

                return response

            except Exception as e:
                last_error = e
                logger.error(f"Provider '{provider_name}' failed: {e}")

                if not fallback or idx == len(providers_to_try) - 1:
                    # No fallback or last provider
                    break

                # Continue to next provider
                continue

        # All providers failed
        raise Exception(f"All LLM providers failed. Last error: {last_error}")

    def generate_with_json_parsing(
        self,
        prompt: str,
        task_type: str = "general",
        **kwargs
    ) -> dict:
        """
        Generate JSON response and parse it.

        Useful for structured outputs like scripts.

        Args:
            prompt: The prompt (should request JSON output)
            task_type: Type of task
            **kwargs: Additional parameters

        Returns:
            Parsed JSON as dictionary

        Raises:
            Exception: If generation or parsing fails
        """
        import json
        import re

        response = self.generate(prompt=prompt, task_type=task_type, **kwargs)

        # Try to extract JSON from response
        # Sometimes LLMs add text before/after JSON
        try:
            # First, try direct parsing
            return json.loads(response)
        except json.JSONDecodeError:
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(0))
                except json.JSONDecodeError:
                    pass

            # Try with array
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(0))
                except json.JSONDecodeError:
                    pass

        raise Exception(f"Failed to parse JSON from LLM response: {response[:200]}")

    def get_available_providers(self) -> List[str]:
        """Get list of available provider names."""
        return list(self.available_providers.keys())

    def clear_cache(self) -> int:
        """
        Clear all cached LLM responses.

        Returns:
            Number of entries cleared
        """
        return llm_cache.clear_all()

    def get_cache_stats(self) -> dict:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache stats
        """
        return llm_cache.get_cache_stats()


# Global LLM manager instance
llm_manager = LLMManager()
