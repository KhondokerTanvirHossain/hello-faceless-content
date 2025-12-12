"""
Claude (Anthropic) LLM provider implementation.
"""
import time
from typing import Optional

from anthropic import Anthropic, APIError, RateLimitError

from src.core.llm.base import BaseLLMProvider
from src.config.settings import settings
from src.utils.logger import logger


class ClaudeProvider(BaseLLMProvider):
    """
    Claude API provider using Anthropic SDK.

    Supports Claude 3.5 Haiku (cheap) and Sonnet (quality) models.
    """

    # Model pricing (per million tokens: input/output)
    PRICING = {
        "claude-3-5-haiku-20241022": (0.25, 1.25),
        "claude-3-5-sonnet-20241022": (3.0, 15.0),
        "claude-3-opus-20240229": (15.0, 75.0),
    }

    DEFAULT_MODEL = "claude-3-5-haiku-20241022"  # Cost-optimized default

    def __init__(self, model: Optional[str] = None):
        """
        Initialize Claude provider.

        Args:
            model: Model to use (defaults to Haiku for cost optimization)
        """
        super().__init__(model or self.DEFAULT_MODEL)

        if not settings.anthropic_api_key:
            logger.warning("Claude API key not configured")
            self.client = None
        else:
            self.client = Anthropic(api_key=settings.anthropic_api_key)

    def generate(
        self,
        prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Generate text using Claude API.

        Args:
            prompt: The prompt to send
            max_tokens: Maximum tokens to generate
            temperature: Temperature for sampling (0.0 - 1.0)
            **kwargs: Additional parameters (system, stop_sequences, etc.)

        Returns:
            Generated text

        Raises:
            Exception: If generation fails after retries
        """
        if not self.is_available():
            raise Exception("Claude API key not configured")

        # Extract optional parameters
        system = kwargs.get("system", None)
        stop_sequences = kwargs.get("stop_sequences", None)

        # Retry logic for rate limits
        max_retries = 3
        retry_delay = 1

        for attempt in range(max_retries):
            try:
                # Call Claude API
                message = self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    system=system,
                    stop_sequences=stop_sequences,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                # Extract text from response
                response = message.content[0].text

                # Validate response
                if not self.validate_response(response):
                    raise Exception("Invalid response from Claude")

                # Log success
                self.log_generation(
                    prompt_length=len(prompt),
                    response_length=len(response),
                    model=self.model,
                    success=True
                )

                # Log token usage and cost
                input_tokens = message.usage.input_tokens
                output_tokens = message.usage.output_tokens
                cost = self.get_cost(input_tokens, output_tokens)

                logger.info(
                    f"Claude tokens: {input_tokens} in / {output_tokens} out | "
                    f"Cost: ${cost:.4f}"
                )

                return response

            except RateLimitError as e:
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)
                    logger.warning(
                        f"Claude rate limit hit (attempt {attempt + 1}/{max_retries}). "
                        f"Retrying in {wait_time}s..."
                    )
                    time.sleep(wait_time)
                else:
                    logger.error("Claude rate limit exceeded after retries")
                    raise

            except APIError as e:
                logger.error(f"Claude API error: {e}")
                self.log_generation(
                    prompt_length=len(prompt),
                    response_length=0,
                    model=self.model,
                    success=False
                )
                raise

            except Exception as e:
                logger.error(f"Unexpected error with Claude: {e}")
                self.log_generation(
                    prompt_length=len(prompt),
                    response_length=0,
                    model=self.model,
                    success=False
                )
                raise

    def is_available(self) -> bool:
        """Check if Claude is configured."""
        return self.client is not None

    def get_model_name(self) -> str:
        """Get the current model name."""
        return self.model

    def get_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate cost for Claude API usage.

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            Cost in USD
        """
        if self.model not in self.PRICING:
            logger.warning(f"Pricing not available for model: {self.model}")
            return 0.0

        input_cost_per_million, output_cost_per_million = self.PRICING[self.model]

        input_cost = (input_tokens / 1_000_000) * input_cost_per_million
        output_cost = (output_tokens / 1_000_000) * output_cost_per_million

        return input_cost + output_cost

    @classmethod
    def get_cheap_model(cls) -> str:
        """Get the cheapest Claude model."""
        return "claude-3-5-haiku-20241022"

    @classmethod
    def get_quality_model(cls) -> str:
        """Get the highest quality Claude model for the price."""
        return "claude-3-5-sonnet-20241022"

    @classmethod
    def get_premium_model(cls) -> str:
        """Get the premium Claude model."""
        return "claude-3-opus-20240229"
