"""
Abstract base class for LLM providers.
"""
from abc import ABC, abstractmethod
from typing import Optional

from src.utils.logger import logger


class BaseLLMProvider(ABC):
    """
    Abstract base class for LLM providers.

    All LLM providers (Claude, OpenAI, Bedrock) must implement this interface.
    """

    def __init__(self, model: Optional[str] = None):
        """
        Initialize the LLM provider.

        Args:
            model: Model name to use (provider-specific)
        """
        self.model = model
        self.provider_name = self.__class__.__name__.replace("Provider", "").lower()

    @abstractmethod
    def generate(
        self,
        prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Generate text from a prompt.

        Args:
            prompt: The prompt to send to the LLM
            max_tokens: Maximum tokens to generate
            temperature: Temperature for sampling (0.0 - 1.0)
            **kwargs: Additional provider-specific parameters

        Returns:
            Generated text

        Raises:
            Exception: If generation fails
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the provider is configured and available.

        Returns:
            True if provider can be used, False otherwise
        """
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """
        Get the current model name being used.

        Returns:
            Model name string
        """
        pass

    def get_token_count(self, text: str) -> int:
        """
        Estimate token count for text.

        Simple approximation: ~4 characters per token.
        Override this in subclasses for more accurate counting.

        Args:
            text: Text to count tokens for

        Returns:
            Estimated token count
        """
        return len(text) // 4

    def get_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate cost for token usage.

        Override this in subclasses with actual pricing.

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            Cost in USD
        """
        # Default: return 0 (override in subclasses)
        return 0.0

    def validate_response(self, response: str) -> bool:
        """
        Validate that the response is usable.

        Args:
            response: Generated response

        Returns:
            True if valid, False otherwise
        """
        if not response or not response.strip():
            logger.warning(f"{self.provider_name}: Empty response")
            return False

        if len(response.strip()) < 10:
            logger.warning(f"{self.provider_name}: Response too short")
            return False

        return True

    def log_generation(
        self,
        prompt_length: int,
        response_length: int,
        model: str,
        success: bool = True
    ) -> None:
        """
        Log generation details.

        Args:
            prompt_length: Length of prompt in characters
            response_length: Length of response in characters
            model: Model used
            success: Whether generation succeeded
        """
        status = "✓" if success else "✗"
        logger.info(
            f"{status} {self.provider_name} | "
            f"Model: {model} | "
            f"Prompt: {prompt_length} chars | "
            f"Response: {response_length} chars"
        )
