# Phase 1: Foundation & Script Generation

**Duration**: Week 1-2
**Goal**: Set up infrastructure and implement AI-powered script generation

## 📋 Overview

Phase 1 establishes the foundation for the entire system. By the end of this phase, you'll have a working CLI tool that can generate video scripts from topics using AI.

## 🎯 Objectives

1. ✅ Project structure and dependencies
2. ✅ Configuration management
3. ✅ Database models for jobs and content
4. ✅ LLM provider integrations (Claude, OpenAI, Bedrock)
5. ✅ Script generation system
6. ✅ CLI tool for testing

## 📦 Deliverables

**Main Deliverable**: CLI tool that generates scripts from topics

```bash
python -m src.core.content.script_generator \
    --topic "5 Amazing Space Facts" \
    --style educational \
    --duration 60
```

## 🏗️ Components

### 1. Project Setup

#### 1.1 Directory Structure
```
hello-faceless-content/
├── src/
│   ├── config/
│   ├── models/
│   ├── core/
│   │   ├── llm/
│   │   └── content/
│   ├── workflows/
│   ├── web/
│   └── utils/
├── data/
│   ├── output/
│   ├── assets/
│   ├── cache/
│   └── database/
├── scripts/
├── tests/
└── docs/
```

#### 1.2 Dependencies ([requirements.txt](../requirements.txt))
```txt
# Web Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0

# Database
sqlalchemy==2.0.25
alembic==1.13.1

# LLM APIs
anthropic==0.18.0
openai==1.12.0
boto3==1.34.34

# Utilities
python-dotenv==1.0.0
pydantic==2.5.3
pydantic-settings==2.1.0
loguru==0.7.2
httpx==0.26.0

# ... (see requirements.txt for full list)
```

#### 1.3 Environment Variables ([.env.example](../.env.example))
```bash
# LLM API Keys
ANTHROPIC_API_KEY=your_claude_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1

# Database
DATABASE_URL=sqlite:///data/database/app.db

# File Paths
OUTPUT_DIR=data/output
ASSETS_DIR=data/assets
CACHE_DIR=data/cache

# Application
DEBUG=True
LOG_LEVEL=INFO
```

### 2. Configuration System

#### 2.1 Settings ([src/config/settings.py](../src/config/settings.py))

**Purpose**: Centralized configuration using Pydantic Settings

**Key Features**:
- Loads environment variables automatically
- Type validation
- Default values
- Path management
- Directory creation on startup

**Usage**:
```python
from src.config.settings import settings

# Access API keys
api_key = settings.anthropic_api_key

# Get paths
output_dir = settings.output_dir

# Get video settings
resolution = settings.resolution_tuple  # (1080, 1920)
```

#### 2.2 Prompt Templates ([src/config/prompts.py](../src/config/prompts.py))

**Purpose**: LLM prompt templates for different content styles

**Templates Available**:
- `EDUCATIONAL_SCRIPT_PROMPT` - Facts and information
- `STORYTELLING_SCRIPT_PROMPT` - Narrative content
- `MOTIVATIONAL_SCRIPT_PROMPT` - Inspirational content
- `NEWS_COMMENTARY_SCRIPT_PROMPT` - News analysis

**Helper Functions**:
```python
from src.config.prompts import get_script_prompt

prompt = get_script_prompt(
    style="educational",
    topic="5 Amazing Space Facts",
    duration=60
)
```

### 3. Utilities

#### 3.1 Logger ([src/utils/logger.py](../src/utils/logger.py))

**Purpose**: Structured logging using loguru

**Features**:
- Console output with colors
- Daily rotating log files
- Separate error log file
- Automatic compression
- 30-day retention

**Usage**:
```python
from src.utils.logger import logger

logger.info("Processing job")
logger.warning("Cache miss")
logger.error("API call failed")
```

#### 3.2 File Manager ([src/utils/file_manager.py](../src/utils/file_manager.py))

**Purpose**: File operations and storage management

**Key Methods**:
- `get_draft_video_path(job_id)` - Path for draft videos
- `get_final_video_path(job_id)` - Path for approved videos
- `get_audio_path(job_id, type)` - Path for audio files
- `list_music_files(mood)` - List available music
- `cleanup_old_drafts(days)` - Delete old drafts
- `cleanup_cache(max_size_mb)` - LRU cache cleanup

**Usage**:
```python
from src.utils.file_manager import file_manager

draft_path = file_manager.get_draft_video_path(job_id=1)
music_files = file_manager.list_music_files(mood="upbeat")
```

#### 3.3 LLM Cache ([src/utils/cache.py](../src/utils/cache.py))

**Purpose**: File-based caching for LLM responses

**Features**:
- MD5-based cache keys
- Expiration (default: 7 days)
- Cache statistics
- Automatic cleanup

**Usage**:
```python
from src.utils.cache import llm_cache

# Try to get cached response
response = llm_cache.get(prompt, model="claude-3-5-haiku-20241022")

if response is None:
    # Make API call
    response = llm_api.call(prompt)
    # Cache the response
    llm_cache.set(prompt, model, response)
```

**Cost Savings**:
- First run: 100% API calls
- After 10 similar videos: 80% cache hit rate
- Monthly savings: $3-4 on API costs

### 4. Database Models

#### 4.1 Database Setup ([src/models/database.py](../src/models/database.py))

**Purpose**: SQLAlchemy configuration and session management

**Components**:
- Engine creation (SQLite)
- Session factory
- Base model class
- Table creation utilities

#### 4.2 Job Model ([src/models/job.py](../src/models/job.py))

**Purpose**: Track video generation jobs through the pipeline

**Fields**:
- `id` - Primary key
- `topic` - Video topic/prompt
- `status` - Current stage (enum)
- `config` - Job configuration (JSON)
- `created_at`, `updated_at` - Timestamps
- Relationships: scripts, videos, approvals

**Status Flow**:
```
pending_script
    ↓
awaiting_script_approval
    ↓
generating_media
    ↓
awaiting_video_approval
    ↓
ready_to_publish
    ↓
awaiting_publish_approval
    ↓
published
```

#### 4.3 Content Models ([src/models/content.py](../src/models/content.py))

**Script Model**:
- `id`, `job_id`
- `content` - Full script (JSON)
- `version` - For revisions
- `approved` - Boolean flag
- `approval_notes`

**Scene Model** (embedded in script):
- `text` - Scene content
- `duration` - Estimated seconds
- `visual_hint` - Animation suggestions

#### 4.4 Approval Model ([src/models/approval.py](../src/models/approval.py))

**Purpose**: Track approval requests and decisions

**Fields**:
- `id`, `job_id`
- `stage` - script/video/publish
- `status` - pending/approved/rejected
- `notes` - User feedback
- `timestamp`

### 5. LLM Integration

#### 5.1 Base Interface ([src/core/llm/base.py](../src/core/llm/base.py))

**Purpose**: Abstract base class for LLM providers

**Methods**:
- `generate(prompt, **kwargs)` - Generate text
- `is_available()` - Check if provider is configured
- `get_cost(tokens)` - Calculate cost
- `get_token_count(text)` - Estimate tokens

#### 5.2 Claude Provider ([src/core/llm/claude.py](../src/core/llm/claude.py))

**Purpose**: Anthropic Claude API integration

**Features**:
- Uses Anthropic SDK
- Supports Haiku (cheap) and Sonnet (quality)
- Retry logic with exponential backoff
- Token usage tracking
- Cache integration

**Models**:
- `claude-3-5-haiku-20241022` - $0.25/$1.25 per million tokens (default)
- `claude-3-5-sonnet-20241022` - $3/$15 per million tokens (quality)

#### 5.3 OpenAI Provider ([src/core/llm/openai.py](../src/core/llm/openai.py))

**Purpose**: OpenAI API integration (fallback)

**Models**:
- `gpt-4o-mini` - Affordable fallback
- `gpt-4o` - Premium fallback

#### 5.4 Bedrock Provider ([src/core/llm/bedrock.py](../src/core/llm/bedrock.py))

**Purpose**: AWS Bedrock integration

**Features**:
- boto3 client
- Claude models via Bedrock
- Region configuration

#### 5.5 LLM Manager ([src/core/llm/manager.py](../src/core/llm/manager.py))

**Purpose**: Provider selection, fallback, and cost optimization

**Features**:
- **Smart routing**: Choose provider based on task complexity
- **Fallback chain**: Try multiple providers if one fails
- **Cost tracking**: Monitor API spending
- **Cache integration**: Check cache before API call

**Provider Selection Logic**:
```python
if task == "simple":
    provider = "claude-haiku"  # Cheapest
elif task == "script_generation":
    provider = "claude-sonnet"  # Best quality/cost
elif task == "refinement":
    provider = "claude-haiku"  # Simple edits
```

**Usage**:
```python
from src.core.llm.manager import llm_manager

response = llm_manager.generate(
    prompt=script_prompt,
    task_type="script_generation",
    max_tokens=2000
)
```

### 6. Content Generation

#### 6.1 Script Generator ([src/core/content/script_generator.py](../src/core/content/script_generator.py))

**Purpose**: Generate video scripts using AI

**Main Class**: `ScriptGenerator`

**Methods**:

1. **`generate_script(topic, style, duration)`**
   - Selects appropriate prompt template
   - Calls LLM with optimized model
   - Parses JSON response
   - Validates structure
   - Returns Script object

2. **`refine_script(script, feedback)`**
   - Takes original script + user feedback
   - Regenerates with improvements
   - Maintains overall structure

3. **`validate_script(script_json)`**
   - Checks required fields
   - Validates scene structure
   - Estimates actual duration
   - Returns validation errors if any

**Output Format** (JSON):
```json
{
    "title": "5 Amazing Space Facts",
    "hook": "Did you know there's a planet made of diamonds?",
    "scenes": [
        {
            "text": "First amazing fact about space...",
            "duration": 10,
            "visual_hint": "Animated stars and planets",
            "keywords": ["planet", "diamonds"]
        },
        // ... more scenes
    ],
    "conclusion": "Space is truly incredible!",
    "hashtags": ["space", "science", "facts"],
    "estimated_duration": 60
}
```

#### 6.2 Topic Selector ([src/core/content/topic_selector.py](../src/core/content/topic_selector.py))

**Purpose**: Generate topic ideas using AI

**Methods**:

1. **`generate_topic_ideas(category, style, count)`**
   - Returns list of topic suggestions
   - Includes "why this is engaging" explanation
   - Estimates potential views (low/medium/high)

2. **`validate_topic(topic)`**
   - Checks if topic is appropriate
   - Estimates content potential
   - Returns suitability score

**Usage**:
```python
from src.core.content.topic_selector import TopicSelector

selector = TopicSelector()
topics = selector.generate_topic_ideas(
    category="science",
    style="educational",
    count=5
)

# Topics: [
#   {"topic": "...", "why": "...", "estimated_views": "high"},
#   ...
# ]
```

#### 6.3 Script Parser ([src/core/content/script_parser.py](../src/core/content/script_parser.py))

**Purpose**: Parse scripts into scenes and extract metadata

**Methods**:

1. **`parse_into_scenes(script_json)`**
   - Breaks script into timestamped scenes
   - Calculates actual timing
   - Extracts visual keywords

2. **`extract_visual_suggestions(scene)`**
   - Analyzes scene content
   - Suggests animation types
   - Maps concepts to visuals

3. **`generate_subtitle_segments(script)`**
   - Creates timed subtitle data
   - Splits into word-level or phrase-level
   - Returns SRT-compatible format

**Usage**:
```python
from src.core.content.script_parser import ScriptParser

parser = ScriptParser()
scenes = parser.parse_into_scenes(script_json)

# Returns: [
#   {
#       "index": 0,
#       "text": "...",
#       "start_time": 0.0,
#       "end_time": 10.5,
#       "visual_type": "kinetic_text",
#       "keywords": ["planet", "diamond"]
#   },
#   ...
# ]
```

### 7. Database Initialization

#### Script: [scripts/init_db.py](../scripts/init_db.py)

**Purpose**: Initialize database and create tables

**Usage**:
```bash
python scripts/init_db.py
```

**Actions**:
1. Creates database file if not exists
2. Creates all tables from models
3. Runs any migrations
4. Seeds initial data (optional)

## 🧪 Testing Phase 1

### Test 1: Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
```

### Test 2: Database Initialization

```bash
# Initialize database
python scripts/init_db.py

# Verify database created
ls data/database/app.db
```

### Test 3: LLM Connection

```bash
# Test Claude API
python -c "from src.core.llm.claude import ClaudeProvider; \
    p = ClaudeProvider(); \
    print(p.is_available())"

# Expected output: True (if API key is configured)
```

### Test 4: Script Generation (CLI)

```bash
# Generate a script
python -m src.core.content.script_generator \
    --topic "5 Amazing Space Facts" \
    --style educational \
    --duration 60

# Should output: Generated script JSON
```

### Test 5: Cache Verification

```bash
# Generate same script again
python -m src.core.content.script_generator \
    --topic "5 Amazing Space Facts" \
    --style educational \
    --duration 60

# Should be faster (cache hit)
# Check cache: ls data/cache/llm/
```

## 📊 Success Criteria

- ✅ All dependencies installed without errors
- ✅ Database initialized successfully
- ✅ At least one LLM provider configured and working
- ✅ Script generation CLI produces valid JSON output
- ✅ Cache hits work on subsequent requests
- ✅ Logs are written to `logs/` directory
- ✅ No errors in error log file

## 🐛 Common Issues & Solutions

### Issue 1: Module Import Errors

**Error**: `ModuleNotFoundError: No module named 'src'`

**Solution**:
```bash
# Make sure you're in the project root
cd /path/to/hello-faceless-content

# Add project to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or run with python -m
python -m src.core.content.script_generator ...
```

### Issue 2: API Key Not Found

**Error**: `API key not configured`

**Solution**:
```bash
# Check .env file exists
cat .env

# Verify API key is set
echo $ANTHROPIC_API_KEY

# If not, add to .env:
ANTHROPIC_API_KEY=your_actual_key_here
```

### Issue 3: Database Permission Error

**Error**: `OperationalError: unable to open database file`

**Solution**:
```bash
# Ensure data/database directory exists
mkdir -p data/database

# Check permissions
ls -la data/

# Re-run init script
python scripts/init_db.py
```

### Issue 4: LLM Response Parsing Error

**Error**: `JSONDecodeError: Expecting value`

**Solution**:
- LLM sometimes returns text before/after JSON
- Parser should extract JSON from response
- If persists, try different model or adjust prompt
- Check logs for raw response

## 💡 Tips & Best Practices

### Cost Optimization
1. **Always check cache first** before API calls
2. **Use Haiku for simple tasks** (80% cheaper than Sonnet)
3. **Batch similar requests** to maximize cache hits
4. **Monitor API usage** with cost tracking

### Development Workflow
1. **Test with CLI** before building web UI
2. **Check logs** for debugging (`logs/app_*.log`)
3. **Use DEBUG=True** during development
4. **Commit after each working feature**

### Code Organization
1. **Keep functions small and focused**
2. **Use type hints** for better IDE support
3. **Document complex logic** with comments
4. **Write tests** for critical components

## 🎯 Phase 1 Completion Checklist

- [ ] Virtual environment created and activated
- [ ] All dependencies installed
- [ ] .env file configured with API keys
- [ ] Database initialized
- [ ] LLM providers tested and working
- [ ] Script generation CLI working
- [ ] Cache system verified
- [ ] Logs being written correctly
- [ ] Test script generated successfully
- [ ] Documentation reviewed

## ➡️ Next Steps

Once Phase 1 is complete, move to:

**[Phase 2: Video Generation](phase2-video-generation.md)**

You'll build:
- Animation system (PIL, OpenCV)
- Audio generation (TTS + music)
- Video assembly (MoviePy)
- Full video rendering pipeline

---

**Estimated Time**: 1-2 weeks depending on experience
**Prerequisites**: Python 3.11+, API keys for at least one LLM provider
**Difficulty**: Moderate - Requires API setup and database understanding
