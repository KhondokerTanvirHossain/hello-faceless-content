"""
LLM prompt templates for content generation.
Organized by content style and purpose.
"""

# Script Generation Prompts by Style

EDUCATIONAL_SCRIPT_PROMPT = """You are a script writer for short-form educational video content (15-60 seconds).

Topic: {topic}
Target Duration: {duration} seconds
Style: Educational, engaging, fact-based

Create a compelling video script that:
1. Opens with a hook to grab attention in the first 3 seconds
2. Presents {num_facts} interesting facts or key points about the topic
3. Uses simple, clear language suitable for a general audience
4. Includes smooth transitions between points
5. Ends with a memorable conclusion or call-to-action
6. Is paced for {duration} seconds when read aloud (approximately {word_count} words)

Format your response as a JSON object with this structure:
{{
    "title": "Catchy video title",
    "hook": "Opening hook (first sentence)",
    "scenes": [
        {{"text": "Scene 1 content", "duration": 10, "visual_hint": "Description of what to show"}},
        {{"text": "Scene 2 content", "duration": 10, "visual_hint": "Description of what to show"}}
    ],
    "conclusion": "Final sentence or CTA",
    "hashtags": ["relevant", "hashtags"],
    "estimated_duration": {duration}
}}

Make it engaging, informative, and perfect for social media shorts!"""

STORYTELLING_SCRIPT_PROMPT = """You are a script writer for short-form narrative video content (15-60 seconds).

Topic: {topic}
Target Duration: {duration} seconds
Style: Story-telling, narrative, emotional

Create a compelling story-based video script that:
1. Opens with an intriguing setup or question
2. Develops a simple narrative arc (beginning, middle, end)
3. Uses descriptive, engaging language to paint a picture
4. Builds emotional connection with the audience
5. Delivers a satisfying conclusion or twist
6. Is paced for {duration} seconds when read aloud (approximately {word_count} words)

Format your response as a JSON object with this structure:
{{
    "title": "Compelling story title",
    "hook": "Opening hook (first sentence)",
    "scenes": [
        {{"text": "Scene 1 content", "duration": 10, "visual_hint": "Description of what to show", "emotion": "curious/excited/surprised"}},
        {{"text": "Scene 2 content", "duration": 10, "visual_hint": "Description of what to show", "emotion": "tension/interest"}}
    ],
    "conclusion": "Final sentence or revelation",
    "hashtags": ["relevant", "hashtags"],
    "estimated_duration": {duration}
}}

Make it captivating, emotional, and shareable!"""

MOTIVATIONAL_SCRIPT_PROMPT = """You are a script writer for short-form motivational video content (15-60 seconds).

Topic: {topic}
Target Duration: {duration} seconds
Style: Motivational, inspirational, uplifting

Create an inspiring video script that:
1. Opens with a powerful statement or question
2. Presents motivational insights or life lessons
3. Uses energetic, positive language
4. Builds momentum and energy throughout
5. Ends with an empowering call-to-action
6. Is paced for {duration} seconds when read aloud (approximately {word_count} words)

Format your response as a JSON object with this structure:
{{
    "title": "Inspiring video title",
    "hook": "Powerful opening statement",
    "scenes": [
        {{"text": "Scene 1 content", "duration": 10, "visual_hint": "Motivational visual suggestion", "energy": "building"}},
        {{"text": "Scene 2 content", "duration": 10, "visual_hint": "Motivational visual suggestion", "energy": "peak"}}
    ],
    "conclusion": "Empowering final statement",
    "hashtags": ["relevant", "hashtags"],
    "estimated_duration": {duration}
}}

Make it inspiring, energizing, and action-oriented!"""

NEWS_COMMENTARY_SCRIPT_PROMPT = """You are a script writer for short-form news commentary video content (15-60 seconds).

Topic: {topic}
Target Duration: {duration} seconds
Style: News commentary, informative, analytical

Create a concise commentary script that:
1. Opens with the key news point or development
2. Provides essential context and background
3. Uses clear, journalistic language
4. Presents analysis or implications
5. Ends with a thought-provoking conclusion
6. Is paced for {duration} seconds when read aloud (approximately {word_count} words)

Format your response as a JSON object with this structure:
{{
    "title": "News-style video title",
    "hook": "Opening news statement",
    "scenes": [
        {{"text": "Scene 1 content", "duration": 10, "visual_hint": "Visual representation", "info_type": "context/analysis"}},
        {{"text": "Scene 2 content", "duration": 10, "visual_hint": "Visual representation", "info_type": "implication"}}
    ],
    "conclusion": "Final analysis or question",
    "hashtags": ["relevant", "hashtags"],
    "estimated_duration": {duration}
}}

Make it informative, balanced, and thought-provoking!"""

# Topic Generation Prompt

TOPIC_GENERATION_PROMPT = """Generate {count} interesting and engaging topic ideas for short-form video content.

Category: {category}
Content Style: {style}
Target Audience: General social media users

Requirements for each topic:
1. Should be timely, interesting, or trending
2. Can be covered effectively in 30-60 seconds
3. Has visual potential for animations
4. Likely to engage and be shared
5. Appropriate for all audiences

Format your response as a JSON array:
[
    {{"topic": "Topic title", "why": "Brief explanation of why this is engaging", "estimated_views": "low/medium/high"}},
    ...
]

Be creative and focus on topics that would perform well on social media!"""

# Script Refinement Prompt

SCRIPT_REFINEMENT_PROMPT = """Review and refine this video script based on the feedback provided.

Original Script:
{original_script}

User Feedback:
{feedback}

Please revise the script to address the feedback while maintaining:
1. The overall structure and flow
2. The target duration of {duration} seconds
3. The engaging, social-media-friendly tone
4. The JSON format

Return the complete refined script in the same JSON format as the original."""

# Metadata Generation Prompt

METADATA_GENERATION_PROMPT = """Generate optimized metadata for this video to be posted on {platform}.

Script Summary:
{script_summary}

Platform: {platform}
Content Style: {style}

Generate:
1. An attention-grabbing title (optimized for {platform})
2. A compelling caption/description (2-3 sentences)
3. 5-10 relevant hashtags (mix of trending and niche-specific)
4. A suggested thumbnail text overlay (5-7 words max)

Format your response as a JSON object:
{{
    "title": "Platform-optimized title",
    "caption": "Engaging caption text",
    "hashtags": ["hashtag1", "hashtag2", ...],
    "thumbnail_text": "Short catchy text"
}}

Make it optimized for maximum engagement on {platform}!"""

# Prompt Templates Dictionary

SCRIPT_PROMPTS = {
    "educational": EDUCATIONAL_SCRIPT_PROMPT,
    "storytelling": STORYTELLING_SCRIPT_PROMPT,
    "motivational": MOTIVATIONAL_SCRIPT_PROMPT,
    "news": NEWS_COMMENTARY_SCRIPT_PROMPT,
}


def get_script_prompt(style: str, topic: str, duration: int) -> str:
    """
    Get the appropriate script generation prompt for the given style.

    Args:
        style: Content style (educational, storytelling, motivational, news)
        topic: The topic for the video
        duration: Target duration in seconds

    Returns:
        Formatted prompt string
    """
    # Calculate approximate word count (average speaking rate: 150 words/minute)
    word_count = int((duration / 60) * 150)

    # Calculate number of facts/scenes based on duration
    if duration <= 30:
        num_facts = 3
    elif duration <= 45:
        num_facts = 4
    else:
        num_facts = 5

    template = SCRIPT_PROMPTS.get(style.lower(), EDUCATIONAL_SCRIPT_PROMPT)
    return template.format(
        topic=topic,
        duration=duration,
        word_count=word_count,
        num_facts=num_facts
    )


def get_topic_generation_prompt(category: str, style: str, count: int = 5) -> str:
    """
    Get the topic generation prompt.

    Args:
        category: Content category (e.g., "science", "technology", "history")
        style: Content style
        count: Number of topics to generate

    Returns:
        Formatted prompt string
    """
    return TOPIC_GENERATION_PROMPT.format(
        count=count,
        category=category,
        style=style
    )


def get_refinement_prompt(original_script: str, feedback: str, duration: int) -> str:
    """
    Get the script refinement prompt.

    Args:
        original_script: The original script JSON
        feedback: User feedback for refinement
        duration: Target duration in seconds

    Returns:
        Formatted prompt string
    """
    return SCRIPT_REFINEMENT_PROMPT.format(
        original_script=original_script,
        feedback=feedback,
        duration=duration
    )


def get_metadata_prompt(script_summary: str, platform: str, style: str) -> str:
    """
    Get the metadata generation prompt.

    Args:
        script_summary: Summary of the script content
        platform: Target platform (facebook, youtube, instagram, tiktok)
        style: Content style

    Returns:
        Formatted prompt string
    """
    return METADATA_GENERATION_PROMPT.format(
        script_summary=script_summary,
        platform=platform,
        style=style
    )
