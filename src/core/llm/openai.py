"""
OpenAI LLM provider implementation.
"""
import time
from typing import Optional

from openai import OpenAI, APIError, RateLimitError

from src.core.llm.base import BaseLLMProvider
from src.config.settings import settings
from src.utils.logger import logger


class OpenAIProvider(BaseLLMProvider):
    """
    OpenAI API provider.

    Supports GPT-4o, GPT-4o-mini, and other OpenAI models.
    """

    # Model pricing (per million tokens: input/output)
    PRICING = {
        "gpt-4o": (2.50, 10.00),
        "gpt-4o-mini": (0.150, 0.600),
        "gpt-4-turbo": (10.00, 30.00),
        "gpt-3.5-turbo": (0.50, 1.50),
    }

    DEFAULT_MODEL = "gpt-4o-mini"  # Affordable fallback

    def __init__(self, model: Optional[str] = None):
        """
        Initialize OpenAI provider.

        Args:
            model: Model to use (defaults to GPT-4o-mini)
        """
        super().__init__(model or self.DEFAULT_MODEL)

        if not settings.openai_api_key:
            logger.warning("OpenAI API key not configured")
            self.client = None
        else:
            self.client = OpenAI(api_key=settings.openai_api_key)

    def generate(
        self,
        prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Generate text using OpenAI API.

        Args:
            prompt: The prompt to send
            max_tokens: Maximum tokens to generate
            temperature: Temperature for sampling (0.0 - 1.0)
            **kwargs: Additional parameters (system, stop, etc.)

        Returns:
            Generated text

        Raises:
            Exception: If generation fails after retries
        """
        if not self.is_available():
            raise Exception("OpenAI API key not configured")

        # Extract optional parameters
        system = kwargs.get("system", "You are a helpful assistant.")
        stop = kwargs.get("stop", None)

        # Retry logic
        max_retries = 3
        retry_delay = 1

        for attempt in range(max_retries):
            try:
                # Call OpenAI API
                response = self.client.chat.completions.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    stop=stop,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": prompt}
                    ]
                )

                # Extract text from response
                text = response.choices[0].message.content

                # Validate response
                if not self.validate_response(text):
                    raise Exception("Invalid response from OpenAI")

                # Log success
                self.log_generation(
                    prompt_length=len(prompt),
                    response_length=len(text),
                    model=self.model,
                    success=True
                )

                # Log token usage and cost
                input_tokens = response.usage.prompt_tokens
                output_tokens = response.usage.completion_tokens
                cost = self.get_cost(input_tokens, output_tokens)

                logger.info(
                    f"OpenAI tokens: {input_tokens} in / {output_tokens} out | "
                    f"Cost: ${cost:.4f}"
                )

                return text

            except RateLimitError as e:
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)
                    logger.warning(
                        f"OpenAI rate limit hit (attempt {attempt + 1}/{max_retries}). "
                        f"Retrying in {wait_time}s..."
                    )
                    time.sleep(wait_time)
                else:
                    logger.error("OpenAI rate limit exceeded after retries")
                    raise

            except APIError as e:
                logger.error(f"OpenAI API error: {e}")
                self.log_generation(
                    prompt_length=len(prompt),
                    response_length=0,
                    model=self.model,
                    success=False
                )
                raise

            except Exception as e:
                logger.error(f"Unexpected error with OpenAI: {e}")
                self.log_generation(
                    prompt_length=len(prompt),
                    response_length=0,
                    model=self.model,
                    success=False
                )
                raise

    def is_available(self) -> bool:
        """Check if OpenAI is configured."""
        return self.client is not None

    def get_model_name(self) -> str:
        """Get the current model name."""
        return self.model

    def get_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate cost for OpenAI API usage.

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
        """Get the cheapest OpenAI model."""
        return "gpt-4o-mini"

    @classmethod
    def get_quality_model(cls) -> str:
        """Get the highest quality OpenAI model."""
        return "gpt-4o"
