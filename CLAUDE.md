# CLAUDE.md - AI Assistant Context

This file provides context for AI assistants (like Claude Code) working on this project.

## 🎯 Project Summary

**Faceless Video Automation System** - A Python-based end-to-end automation pipeline for generating and posting short-form vertical videos (15-60s) to social media with minimal daily human input.

**Current Status**: Phase 1 (Foundation & Script Generation) - In Progress

## 🏗️ Architecture Overview

### Tech Stack
- **Language**: Python 3.11+
- **Web Framework**: FastAPI
- **Database**: SQLite + SQLAlchemy
- **Video Processing**: MoviePy, Pillow (PIL), OpenCV
- **Audio**: gTTS, edge-tts, pydub
- **AI**: Anthropic Claude, OpenAI, AWS Bedrock
- **Config**: Pydantic Settings

### Project Structure
```
hello-faceless-content/
├── src/
│   ├── config/          # Settings & prompt templates
│   ├── models/          # SQLAlchemy database models
│   ├── core/
│   │   ├── llm/         # AI provider integrations
│   │   ├── content/     # Script generation
│   │   ├── media/       # Video/audio generation
│   │   └── publishing/  # Social media posting
│   ├── workflows/       # Pipeline orchestration
│   ├── web/             # FastAPI web portal
│   └── utils/           # Logger, cache, file manager
├── data/                # Local storage (videos, cache, db)
├── scripts/             # Setup & maintenance scripts
├── tests/               # Unit & integration tests
└── docs/                # Comprehensive documentation
```

## 🔄 Development Phases

### Phase 1: Foundation & Script Generation (Week 1-2) ✅ In Progress
**Goal**: Infrastructure + AI script generation

**Status**: ~40% complete
- ✅ Project structure
- ✅ Configuration system (settings.py, prompts.py)
- ✅ Utilities (logger, file_manager, cache)
- ⏳ Database models (database.py, job.py, content.py, approval.py)
- ⏳ LLM integration (base.py, claude.py, openai.py, bedrock.py, manager.py)
- ⏳ Content generation (script_generator.py, topic_selector.py, script_parser.py)
- ⏳ Database init script

**Deliverable**: CLI tool for script generation

### Phase 2: Video Generation (Week 3-4)
**Goal**: Animations, audio, video assembly

**Components**:
- PIL-based animations (kinetic typography)
- OpenCV effects (transitions, filters)
- TTS + background music mixing
- MoviePy video compositor
- Platform-specific formatters

**Deliverable**: CLI tool that generates complete videos

### Phase 3: Web Portal & Workflow (Week 5-6)
**Goal**: Web interface with approval workflow

**Components**:
- FastAPI application
- Job management routes
- Approval interface (script, video, publish)
- Configuration editor
- Dashboard with status tracking

**Deliverable**: Web portal for end-to-end video creation

### Phase 4: Platform Publishing (Week 7-8)
**Goal**: Automate social media posting

**Components**:
- Facebook/Instagram publisher
- YouTube Shorts publisher
- Metadata generation
- Upload error handling

**Deliverable**: Full automation from topic to published video

### Phase 5: Optimization & Enhancements (Week 9+)
**Goal**: Performance, quality, UX improvements

**Features**:
- Manim for data visualizations
- Parallel rendering
- Batch job creation
- Analytics dashboard

## 📝 Coding Standards

### Style Guide
- **Line length**: 100 characters (configured in pyproject.toml)
- **Formatting**: Use ruff for linting/formatting
- **Type hints**: Use where helpful, not mandatory
- **Docstrings**: Use for classes and public methods

### Import Order
```python
# Standard library
import json
from pathlib import Path

# Third-party
from fastapi import FastAPI
from sqlalchemy import Column, Integer

# Local
from src.config.settings import settings
from src.utils.logger import logger
```

### Common Patterns

#### 1. Settings Usage
```python
from src.config.settings import settings

api_key = settings.anthropic_api_key
output_dir = settings.output_dir
```

#### 2. Logging
```python
from src.utils.logger import logger

logger.info("Processing job")
logger.error(f"Failed to process: {error}")
```

#### 3. File Paths
```python
from src.utils.file_manager import file_manager

draft_path = file_manager.get_draft_video_path(job_id)
```

#### 4. LLM Cache
```python
from src.utils.cache import llm_cache

# Check cache first
response = llm_cache.get(prompt, model)
if response is None:
    response = llm_api.generate(prompt)
    llm_cache.set(prompt, model, response)
```

#### 5. Database Sessions
```python
from src.models.database import get_session

with get_session() as session:
    job = session.query(Job).filter_by(id=job_id).first()
    job.status = "completed"
    session.commit()
```

## 🎨 Design Decisions

### 1. Cost Optimization
- **Primary**: Claude Haiku ($0.25/$1.25 per million tokens)
- **Quality**: Claude Sonnet ($3/$15 per million tokens)
- **Fallback**: OpenAI GPT-4o-mini
- **Strategy**: Use Haiku by default, Sonnet for complex scripts only
- **Caching**: Aggressive caching for 80% hit rate

### 2. Animation Approach
- **Phase 1-3**: PIL-based kinetic typography (fast, simple, reliable)
- **Phase 5**: Add Manim for data visualizations (complex, powerful)
- **Rationale**: Start simple, add complexity incrementally

### 3. Approval Workflow
- **Checkpoints**: Script → Video → Publish
- **Method**: Web-based polling (not email)
- **Editing**: Inline editing for scripts, regeneration for videos
- **Rationale**: Keep everything in one interface, easy iteration

### 4. Storage Strategy
- **Database**: SQLite (sufficient for single-user)
- **Files**: Local file storage with organized structure
- **Cache**: LRU cleanup when exceeds 1GB
- **Drafts**: Auto-delete after 7 days

### 5. Platform Priority
- **Phase 4**: Facebook Reels (easiest API, highest priority)
- **Phase 4**: YouTube Shorts (official API, good docs)
- **Future**: Instagram Reels (same as Facebook)
- **Future**: TikTok (API requires approval, manual initially)

## 🔧 Key Files to Understand

### Configuration
- [src/config/settings.py](src/config/settings.py) - All app settings via Pydantic
- [src/config/prompts.py](src/config/prompts.py) - LLM prompt templates

### Utilities
- [src/utils/logger.py](src/utils/logger.py) - Loguru-based logging
- [src/utils/file_manager.py](src/utils/file_manager.py) - File operations
- [src/utils/cache.py](src/utils/cache.py) - LLM response caching

### Database Models (To Be Completed)
- [src/models/database.py](src/models/database.py) - SQLAlchemy setup
- [src/models/job.py](src/models/job.py) - Job model with status enum
- [src/models/content.py](src/models/content.py) - Script model
- [src/models/approval.py](src/models/approval.py) - Approval model

### LLM Integration (To Be Completed)
- [src/core/llm/base.py](src/core/llm/base.py) - Abstract interface
- [src/core/llm/manager.py](src/core/llm/manager.py) - Provider selection & fallback

### Content Generation (To Be Completed)
- [src/core/content/script_generator.py](src/core/content/script_generator.py) - Main generator
- [src/core/content/script_parser.py](src/core/content/script_parser.py) - Parse into scenes

## 🧪 Testing Approach

### Phase 1 Testing
1. **Unit Tests**: Test each component in isolation
2. **Integration Tests**: Test LLM integration, database operations
3. **CLI Testing**: Manual testing of script generation tool
4. **Cost Tracking**: Monitor API usage during tests

### Test Structure
```
tests/
├── unit/
│   ├── test_llm.py
│   ├── test_cache.py
│   └── test_script_generator.py
└── integration/
    └── test_pipeline.py
```

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_llm.py

# Run with coverage
pytest --cov=src tests/
```

## 🐛 Common Issues & Solutions

### Issue: Import Errors
```bash
# Add project to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or use python -m
python -m src.core.content.script_generator
```

### Issue: Database Locked
```python
# Use context managers for sessions
with get_session() as session:
    # Do work
    session.commit()
# Session auto-closed
```

### Issue: LLM Rate Limits
```python
# Manager handles this with retry + fallback
from src.core.llm.manager import llm_manager

response = llm_manager.generate(
    prompt,
    max_retries=3,
    fallback=True
)
```

### Issue: Cache Not Working
```python
# Check cache directory exists
settings.cache_dir.mkdir(parents=True, exist_ok=True)

# Clear expired cache
llm_cache.clear_expired(max_age_hours=168)  # 7 days
```

## 💡 When Adding New Features

### Before Writing Code
1. **Check existing patterns** in similar files
2. **Review relevant documentation** in `docs/`
3. **Understand the phase** you're working in
4. **Consider cost implications** (API calls, storage)

### When Adding New API Integration
1. Create provider class inheriting from `BaseLLMProvider`
2. Implement required methods: `generate()`, `is_available()`, `get_cost()`
3. Add to `LLMManager` fallback chain
4. Update settings for API keys
5. Add tests for the provider
6. Document usage in docstrings

### When Adding New Database Model
1. Create model class inheriting from `Base`
2. Define columns with proper types
3. Add relationships if needed
4. Create migration with Alembic
5. Update `init_db.py` script
6. Add to model imports in `__init__.py`

### When Adding New Route (Phase 3+)
1. Create route file in `src/web/routes/`
2. Use FastAPI dependencies for session, settings
3. Create corresponding Jinja2 template
4. Add route to `app.py` router includes
5. Test with browser and curl
6. Document in API reference

## 📊 Performance Targets

### API Costs
- **Script generation**: $0.02 - $0.16 per video
- **Monthly (30 videos)**: < $5
- **Cache hit rate**: > 80% after 10 videos

### Generation Times
- **Script generation**: 30-60 seconds
- **Video rendering**: 3-5 minutes (60s video)
- **Total pipeline**: < 15 minutes

### User Experience
- **Active time per video**: < 30 minutes
- **Approval latency**: < 5 seconds per checkpoint
- **Dashboard load time**: < 2 seconds

## 🔐 Security Considerations

### API Keys
- **Never commit** .env file
- **Use environment variables** for all secrets
- **Rotate keys** if exposed
- **Use read-only keys** where possible

### Database
- **SQLite is local** - no network exposure
- **Backup regularly** for production use
- **Use parameterized queries** (SQLAlchemy handles this)

### File Upload (Phase 4)
- **Validate file types** before upload
- **Check file sizes** against platform limits
- **Sanitize filenames** to prevent path traversal
- **Scan for malware** if accepting user uploads

## 📚 Helpful Resources

### Documentation
- [Overview](docs/overview.md) - Project vision and architecture
- [Phase 1](docs/phase1-foundation.md) - Current phase details
- [Setup Guide](docs/setup.md) - Installation instructions
- [User Guide](docs/user-guide.md) - Using the system

### External References
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [MoviePy Docs](https://zulko.github.io/moviepy/)
- [Anthropic API](https://docs.anthropic.com/)
- [OpenAI API](https://platform.openai.com/docs/)

## 🎯 Current Priority: Phase 1 Completion

**Next Tasks** (in order):
1. ✅ Create comprehensive documentation (this file!)
2. Implement database models (database.py, job.py, content.py, approval.py)
3. Build LLM integration (base.py, claude.py, openai.py, bedrock.py, manager.py)
4. Create content generators (script_generator.py, topic_selector.py, script_parser.py)
5. Write database init script (scripts/init_db.py)
6. Test CLI tool for script generation
7. Write unit tests for critical components

## 🤖 Tips for AI Assistants

### When Helping With This Project
1. **Check phase context** - Don't implement Phase 3 features if we're in Phase 1
2. **Follow existing patterns** - Look at completed files for style guidance
3. **Cost awareness** - Always consider API cost implications
4. **Test incrementally** - Suggest testing after each component
5. **Document as you go** - Update docs when adding features

### When User Asks for Features
1. **Check if planned** - Review phase documentation first
2. **Suggest alternatives** - If something is costly or complex, offer simpler options
3. **Estimate impact** - Discuss time, cost, and complexity trade-offs
4. **Align with vision** - Ensure feature fits the "minimal daily input" goal

### When Debugging
1. **Check logs** - Always look at `logs/app_*.log` and `logs/errors_*.log`
2. **Verify environment** - Confirm .env is configured correctly
3. **Test components** - Isolate the problem to a specific module
4. **Check cache** - Sometimes clearing cache solves issues

### Code Quality Checklist
- [ ] Follows existing code style
- [ ] Has appropriate logging statements
- [ ] Handles errors gracefully
- [ ] Uses type hints where helpful
- [ ] Has docstrings for public methods
- [ ] Considers cost implications
- [ ] Is tested (at least manually)
- [ ] Updates relevant documentation

---

**Last Updated**: 2024-12-12
**Phase**: 1 (Foundation & Script Generation)
**Completion**: ~40%
**Next Milestone**: Database models + LLM integration
