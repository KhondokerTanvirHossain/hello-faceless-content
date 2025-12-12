"""
AWS Bedrock LLM provider implementation.
"""
import json
import time
from typing import Optional

try:
    import boto3
    from botocore.exceptions import ClientError
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False

from src.core.llm.base import BaseLLMProvider
from src.config.settings import settings
from src.utils.logger import logger


class BedrockProvider(BaseLLMProvider):
    """
    AWS Bedrock API provider.

    Supports Claude models via AWS Bedrock.
    """

    # Model pricing (per million tokens: input/output)
    # Note: Bedrock pricing may vary by region
    PRICING = {
        "anthropic.claude-3-5-sonnet-20241022-v2:0": (3.0, 15.0),
        "anthropic.claude-3-5-haiku-20241022-v1:0": (0.25, 1.25),
        "anthropic.claude-3-opus-20240229-v1:0": (15.0, 75.0),
    }

    DEFAULT_MODEL = "anthropic.claude-3-5-haiku-20241022-v1:0"

    def __init__(self, model: Optional[str] = None):
        """
        Initialize Bedrock provider.

        Args:
            model: Model to use
        """
        super().__init__(model or self.DEFAULT_MODEL)

        if not BOTO3_AVAILABLE:
            logger.warning("boto3 not installed. AWS Bedrock unavailable.")
            self.client = None
            return

        if not settings.aws_access_key_id or not settings.aws_secret_access_key:
            logger.warning("AWS credentials not configured")
            self.client = None
        else:
            try:
                self.client = boto3.client(
                    "bedrock-runtime",
                    region_name=settings.aws_region,
                    aws_access_key_id=settings.aws_access_key_id,
                    aws_secret_access_key=settings.aws_secret_access_key,
                )
            except Exception as e:
                logger.error(f"Failed to initialize Bedrock client: {e}")
                self.client = None

    def generate(
        self,
        prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Generate text using AWS Bedrock.

        Args:
            prompt: The prompt to send
            max_tokens: Maximum tokens to generate
            temperature: Temperature for sampling (0.0 - 1.0)
            **kwargs: Additional parameters

        Returns:
            Generated text

        Raises:
            Exception: If generation fails after retries
        """
        if not self.is_available():
            raise Exception("AWS Bedrock not configured or boto3 not installed")

        # Extract optional parameters
        system = kwargs.get("system", None)
        stop_sequences = kwargs.get("stop_sequences", None)

        # Prepare request body for Claude models
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        if system:
            body["system"] = system

        if stop_sequences:
            body["stop_sequences"] = stop_sequences

        # Retry logic
        max_retries = 3
        retry_delay = 1

        for attempt in range(max_retries):
            try:
                # Call Bedrock API
                response = self.client.invoke_model(
                    modelId=self.model,
                    body=json.dumps(body)
                )

                # Parse response
                response_body = json.loads(response['body'].read())

                # Extract text (Claude format)
                text = response_body.get('content', [{}])[0].get('text', '')

                # Validate response
                if not self.validate_response(text):
                    raise Exception("Invalid response from Bedrock")

                # Log success
                self.log_generation(
                    prompt_length=len(prompt),
                    response_length=len(text),
                    model=self.model,
                    success=True
                )

                # Log token usage if available
                usage = response_body.get('usage', {})
                input_tokens = usage.get('input_tokens', 0)
                output_tokens = usage.get('output_tokens', 0)

                if input_tokens > 0:
                    cost = self.get_cost(input_tokens, output_tokens)
                    logger.info(
                        f"Bedrock tokens: {input_tokens} in / {output_tokens} out | "
                        f"Cost: ${cost:.4f}"
                    )

                return text

            except ClientError as e:
                error_code = e.response.get('Error', {}).get('Code', '')

                if error_code == 'ThrottlingException' and attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)
                    logger.warning(
                        f"Bedrock throttling (attempt {attempt + 1}/{max_retries}). "
                        f"Retrying in {wait_time}s..."
                    )
                    time.sleep(wait_time)
                else:
                    logger.error(f"Bedrock client error: {e}")
                    self.log_generation(
                        prompt_length=len(prompt),
                        response_length=0,
                        model=self.model,
                        success=False
                    )
                    raise

            except Exception as e:
                logger.error(f"Unexpected error with Bedrock: {e}")
                self.log_generation(
                    prompt_length=len(prompt),
                    response_length=0,
                    model=self.model,
                    success=False
                )
                raise

    def is_available(self) -> bool:
        """Check if Bedrock is configured."""
        return BOTO3_AVAILABLE and self.client is not None

    def get_model_name(self) -> str:
        """Get the current model name."""
        return self.model

    def get_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate cost for Bedrock API usage.

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
