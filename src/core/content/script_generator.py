"""
Script generator using LLM providers.
"""
import json
from typing import Optional, Dict, Any

from src.core.llm.manager import llm_manager
from src.config.prompts import get_script_prompt, get_refinement_prompt
from src.utils.logger import logger


class ScriptGenerator:
    """
    Generates video scripts using AI.

    Handles script generation, refinement, and validation.
    """

    def __init__(self):
        """Initialize script generator."""
        self.llm = llm_manager

    def generate_script(
        self,
        topic: str,
        style: str = "educational",
        duration: int = 60,
        provider: Optional[str] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Generate a video script from a topic.

        Args:
            topic: The topic for the video
            style: Content style (educational, storytelling, motivational, news)
            duration: Target duration in seconds
            provider: Optional specific LLM provider to use
            use_cache: Whether to use cached responses

        Returns:
            Dictionary containing the script:
            {
                "title": str,
                "hook": str,
                "scenes": [{"text": str, "duration": int, "visual_hint": str}],
                "conclusion": str,
                "hashtags": [str],
                "estimated_duration": int
            }

        Raises:
            Exception: If generation or parsing fails
        """
        logger.info(f"Generating script: topic='{topic}', style={style}, duration={duration}s")

        # Get prompt template
        prompt = get_script_prompt(style=style, topic=topic, duration=duration)

        try:
            # Generate script using LLM
            script_json = self.llm.generate_with_json_parsing(
                prompt=prompt,
                provider_name=provider,
                task_type="script_generation",
                use_cache=use_cache,
                max_tokens=3000,
                temperature=0.7
            )

            # Validate script structure
            self._validate_script(script_json)

            logger.info(f"✓ Script generated: {script_json.get('title', 'Untitled')}")

            return script_json

        except Exception as e:
            logger.error(f"Failed to generate script: {e}")
            raise

    def refine_script(
        self,
        original_script: Dict[str, Any],
        feedback: str,
        duration: int = 60,
        provider: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Refine an existing script based on user feedback.

        Args:
            original_script: The original script dictionary
            feedback: User feedback for refinement
            duration: Target duration
            provider: Optional specific LLM provider

        Returns:
            Refined script dictionary

        Raises:
            Exception: If refinement fails
        """
        logger.info(f"Refining script based on feedback: {feedback[:50]}...")

        # Get refinement prompt
        prompt = get_refinement_prompt(
            original_script=json.dumps(original_script, indent=2),
            feedback=feedback,
            duration=duration
        )

        try:
            # Generate refined script
            refined_script = self.llm.generate_with_json_parsing(
                prompt=prompt,
                provider_name=provider,
                task_type="refinement",
                use_cache=False,  # Don't cache refinements
                max_tokens=3000,
                temperature=0.7
            )

            # Validate refined script
            self._validate_script(refined_script)

            logger.info("✓ Script refined successfully")

            return refined_script

        except Exception as e:
            logger.error(f"Failed to refine script: {e}")
            raise

    def _validate_script(self, script: Dict[str, Any]) -> None:
        """
        Validate script structure.

        Args:
            script: Script dictionary to validate

        Raises:
            ValueError: If script is invalid
        """
        required_fields = ["title", "hook", "scenes", "conclusion"]

        for field in required_fields:
            if field not in script:
                raise ValueError(f"Script missing required field: {field}")

        if not isinstance(script["scenes"], list) or len(script["scenes"]) == 0:
            raise ValueError("Script must have at least one scene")

        # Validate scene structure
        for idx, scene in enumerate(script["scenes"]):
            if "text" not in scene:
                raise ValueError(f"Scene {idx} missing 'text' field")
            if "duration" not in scene:
                raise ValueError(f"Scene {idx} missing 'duration' field")

        logger.debug("✓ Script validation passed")

    def calculate_metrics(self, script: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate metrics for a script.

        Args:
            script: Script dictionary

        Returns:
            Dictionary with metrics:
            {
                "word_count": int,
                "scene_count": int,
                "estimated_duration": int,
                "average_scene_duration": float
            }
        """
        # Get all text
        full_text = " ".join([
            script.get("hook", ""),
            " ".join(scene.get("text", "") for scene in script.get("scenes", [])),
            script.get("conclusion", "")
        ])

        word_count = len(full_text.split())
        scene_count = len(script.get("scenes", []))

        # Calculate total duration from scenes
        total_duration = sum(scene.get("duration", 0) for scene in script.get("scenes", []))

        metrics = {
            "word_count": word_count,
            "scene_count": scene_count,
            "estimated_duration": total_duration,
            "average_scene_duration": total_duration / scene_count if scene_count > 0 else 0
        }

        return metrics


# CLI interface
def main():
    """CLI interface for script generation."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate video scripts using AI")
    parser.add_argument("--topic", required=True, help="Video topic")
    parser.add_argument(
        "--style",
        default="educational",
        choices=["educational", "storytelling", "motivational", "news"],
        help="Content style"
    )
    parser.add_argument("--duration", type=int, default=60, help="Target duration in seconds")
    parser.add_argument("--provider", help="LLM provider (claude, openai, bedrock)")
    parser.add_argument("--no-cache", action="store_true", help="Disable response caching")

    args = parser.parse_args()

    # Generate script
    generator = ScriptGenerator()

    try:
        script = generator.generate_script(
            topic=args.topic,
            style=args.style,
            duration=args.duration,
            provider=args.provider,
            use_cache=not args.no_cache
        )

        # Print script as formatted JSON
        print("\n" + "=" * 60)
        print("GENERATED SCRIPT")
        print("=" * 60)
        print(json.dumps(script, indent=2))
        print("=" * 60)

        # Print metrics
        metrics = generator.calculate_metrics(script)
        print("\nMETRICS:")
        print(f"  Word count: {metrics['word_count']}")
        print(f"  Scene count: {metrics['scene_count']}")
        print(f"  Estimated duration: {metrics['estimated_duration']}s")
        print(f"  Avg scene duration: {metrics['average_scene_duration']:.1f}s")
        print()

    except Exception as e:
        print(f"\n✗ Error: {e}\n")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
