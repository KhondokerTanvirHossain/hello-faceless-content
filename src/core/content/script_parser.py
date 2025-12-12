"""
Script parser for extracting scenes and metadata from scripts.
"""
from typing import Dict, List, Any, Optional

from src.utils.logger import logger


class ScriptParser:
    """
    Parses video scripts into scenes and extracts metadata.
    """

    def parse_into_scenes(self, script: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Parse script into timestamped scenes.

        Args:
            script: Script dictionary from ScriptGenerator

        Returns:
            List of scene dictionaries:
            [
                {
                    "index": int,
                    "text": str,
                    "start_time": float,
                    "end_time": float,
                    "duration": float,
                    "visual_hint": str,
                    "keywords": list
                }
            ]
        """
        logger.info("Parsing script into scenes")

        scenes = []
        current_time = 0.0

        # Extract scenes from script
        raw_scenes = script.get("scenes", [])

        for idx, scene in enumerate(raw_scenes):
            text = scene.get("text", "")
            duration = scene.get("duration", 10)
            visual_hint = scene.get("visual_hint", "")

            # Extract keywords from text
            keywords = self._extract_keywords(text)

            parsed_scene = {
                "index": idx,
                "text": text,
                "start_time": current_time,
                "end_time": current_time + duration,
                "duration": duration,
                "visual_hint": visual_hint,
                "keywords": keywords,
                "visual_type": self._suggest_visual_type(text, visual_hint)
            }

            scenes.append(parsed_scene)
            current_time += duration

        logger.info(f"✓ Parsed {len(scenes)} scenes (total: {current_time:.1f}s)")

        return scenes

    def generate_subtitle_segments(
        self,
        script: Dict[str, Any],
        words_per_segment: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate timed subtitle segments.

        Args:
            script: Script dictionary
            words_per_segment: Words per subtitle segment

        Returns:
            List of subtitle dictionaries:
            [
                {
                    "index": int,
                    "text": str,
                    "start_time": float,
                    "end_time": float
                }
            ]
        """
        logger.info("Generating subtitle segments")

        subtitles = []
        scenes = self.parse_into_scenes(script)

        subtitle_index = 0

        for scene in scenes:
            words = scene["text"].split()
            scene_duration = scene["duration"]
            words_count = len(words)

            if words_count == 0:
                continue

            # Calculate time per word
            time_per_word = scene_duration / words_count

            # Split into segments
            for i in range(0, words_count, words_per_segment):
                segment_words = words[i:i + words_per_segment]
                segment_text = " ".join(segment_words)

                start_time = scene["start_time"] + (i * time_per_word)
                end_time = start_time + (len(segment_words) * time_per_word)

                subtitles.append({
                    "index": subtitle_index,
                    "text": segment_text,
                    "start_time": start_time,
                    "end_time": end_time
                })

                subtitle_index += 1

        logger.info(f"✓ Generated {len(subtitles)} subtitle segments")

        return subtitles

    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract important keywords from text.

        Simple implementation using common words and length.

        Args:
            text: Text to extract keywords from

        Returns:
            List of keywords
        """
        # Common stop words to ignore
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
            "been", "being", "have", "has", "had", "do", "does", "did", "will",
            "would", "should", "could", "can", "may", "might", "must", "this",
            "that", "these", "those", "i", "you", "he", "she", "it", "we", "they"
        }

        # Extract words
        words = text.lower().split()

        # Filter and keep important words
        keywords = [
            word.strip(",.!?;:")
            for word in words
            if len(word) > 3 and word.lower() not in stop_words
        ]

        # Return unique keywords (first 5)
        seen = set()
        unique_keywords = []
        for keyword in keywords:
            if keyword not in seen:
                seen.add(keyword)
                unique_keywords.append(keyword)
                if len(unique_keywords) >= 5:
                    break

        return unique_keywords

    def _suggest_visual_type(self, text: str, visual_hint: str) -> str:
        """
        Suggest animation type based on text and visual hint.

        Args:
            text: Scene text
            visual_hint: Visual hint from script

        Returns:
            Visual type (kinetic_text, data_viz, concept, etc.)
        """
        text_lower = text.lower() + " " + visual_hint.lower()

        # Check for data/statistics
        if any(word in text_lower for word in ["percent", "%", "number", "statistics", "data", "chart"]):
            return "data_viz"

        # Check for concepts/diagrams
        if any(word in text_lower for word in ["diagram", "process", "system", "structure", "how"]):
            return "concept"

        # Check for questions
        if "?" in text or any(word in text_lower for word in ["what", "why", "how", "when", "where"]):
            return "question"

        # Default to kinetic text
        return "kinetic_text"

    def get_full_script_text(self, script: Dict[str, Any]) -> str:
        """
        Get the complete script text.

        Args:
            script: Script dictionary

        Returns:
            Full script as single string
        """
        parts = []

        # Add hook
        if hook := script.get("hook"):
            parts.append(hook)

        # Add all scenes
        for scene in script.get("scenes", []):
            if text := scene.get("text"):
                parts.append(text)

        # Add conclusion
        if conclusion := script.get("conclusion"):
            parts.append(conclusion)

        return " ".join(parts)

    def estimate_speaking_duration(self, text: str, words_per_minute: int = 150) -> float:
        """
        Estimate speaking duration for text.

        Args:
            text: Text to estimate duration for
            words_per_minute: Average speaking rate

        Returns:
            Duration in seconds
        """
        word_count = len(text.split())
        duration_seconds = (word_count / words_per_minute) * 60
        return duration_seconds


# CLI interface
def main():
    """CLI interface for script parsing."""
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Parse video scripts")
    parser.add_argument("script_file", help="Path to script JSON file")
    parser.add_argument("--subtitles", action="store_true", help="Generate subtitles")

    args = parser.parse_args()

    # Load script
    try:
        with open(args.script_file, "r") as f:
            script = json.load(f)
    except Exception as e:
        print(f"✗ Error loading script: {e}")
        return 1

    # Parse script
    script_parser = ScriptParser()

    try:
        # Parse into scenes
        scenes = script_parser.parse_into_scenes(script)

        print("\n" + "=" * 60)
        print("PARSED SCENES")
        print("=" * 60)

        for scene in scenes:
            print(f"\nScene {scene['index']}:")
            print(f"  Time: {scene['start_time']:.1f}s - {scene['end_time']:.1f}s ({scene['duration']:.1f}s)")
            print(f"  Text: {scene['text'][:80]}...")
            print(f"  Visual: {scene['visual_type']}")
            print(f"  Keywords: {', '.join(scene['keywords'])}")

        # Generate subtitles if requested
        if args.subtitles:
            subtitles = script_parser.generate_subtitle_segments(script)

            print("\n" + "=" * 60)
            print("SUBTITLE SEGMENTS")
            print("=" * 60)

            for sub in subtitles[:10]:  # Show first 10
                print(f"\n{sub['start_time']:.1f}s - {sub['end_time']:.1f}s: {sub['text']}")

            if len(subtitles) > 10:
                print(f"\n... and {len(subtitles) - 10} more segments")

        print("\n" + "=" * 60 + "\n")

    except Exception as e:
        print(f"\n✗ Error: {e}\n")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
