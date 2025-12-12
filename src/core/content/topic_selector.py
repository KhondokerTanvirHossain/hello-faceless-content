"""
Topic selector for generating video topic ideas.
"""
from typing import List, Dict, Any

from src.core.llm.manager import llm_manager
from src.config.prompts import get_topic_generation_prompt
from src.utils.logger import logger


class TopicSelector:
    """
    Generates topic ideas for videos using AI.
    """

    def __init__(self):
        """Initialize topic selector."""
        self.llm = llm_manager

    def generate_topic_ideas(
        self,
        category: str = "general",
        style: str = "educational",
        count: int = 5,
        use_cache: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Generate topic ideas.

        Args:
            category: Content category (science, technology, history, etc.)
            style: Content style (educational, storytelling, etc.)
            count: Number of topics to generate
            use_cache: Whether to use cached responses

        Returns:
            List of topic dictionaries:
            [
                {
                    "topic": str,
                    "why": str,
                    "estimated_views": str (low/medium/high)
                }
            ]

        Raises:
            Exception: If generation fails
        """
        logger.info(f"Generating {count} topic ideas: category={category}, style={style}")

        # Get prompt
        prompt = get_topic_generation_prompt(
            category=category,
            style=style,
            count=count
        )

        try:
            # Generate topics using LLM
            topics = self.llm.generate_with_json_parsing(
                prompt=prompt,
                task_type="simple",  # Use cheap model for topic generation
                use_cache=use_cache,
                max_tokens=1500,
                temperature=0.8  # Higher temperature for more creative ideas
            )

            # Ensure topics is a list
            if isinstance(topics, dict):
                topics = [topics]

            logger.info(f"✓ Generated {len(topics)} topic ideas")

            return topics

        except Exception as e:
            logger.error(f"Failed to generate topics: {e}")
            raise


# CLI interface
def main():
    """CLI interface for topic generation."""
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Generate video topic ideas")
    parser.add_argument("--category", default="general", help="Content category")
    parser.add_argument(
        "--style",
        default="educational",
        choices=["educational", "storytelling", "motivational", "news"],
        help="Content style"
    )
    parser.add_argument("--count", type=int, default=5, help="Number of topics to generate")
    parser.add_argument("--no-cache", action="store_true", help="Disable caching")

    args = parser.parse_args()

    # Generate topics
    selector = TopicSelector()

    try:
        topics = selector.generate_topic_ideas(
            category=args.category,
            style=args.style,
            count=args.count,
            use_cache=not args.no_cache
        )

        # Print topics
        print("\n" + "=" * 60)
        print(f"TOPIC IDEAS ({args.category.upper()} - {args.style.upper()})")
        print("=" * 60)

        for idx, topic in enumerate(topics, 1):
            print(f"\n{idx}. {topic.get('topic', 'Unknown')}")
            print(f"   Why: {topic.get('why', 'N/A')}")
            print(f"   Estimated views: {topic.get('estimated_views', 'N/A')}")

        print("\n" + "=" * 60 + "\n")

    except Exception as e:
        print(f"\n✗ Error: {e}\n")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
