# 🎬 Faceless Video Automation System

> An AI-powered Python automation system for generating and posting faceless vertical short videos (15-60s) to social media with minimal daily effort.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: Private](https://img.shields.io/badge/license-Private-red.svg)](LICENSE)
[![Status: In Development](https://img.shields.io/badge/status-In%20Development-yellow.svg)](https://github.com)

---

## 🌟 What Is This?

A complete end-to-end automation pipeline that:

- 🤖 **Generates AI scripts** from topics using Claude/OpenAI/Bedrock
- 🎨 **Creates animations** with PIL, OpenCV, and optionally Manim
- 🎙️ **Produces voiceovers** using free TTS (gTTS, edge-tts)
- 🎵 **Adds background music** from royalty-free libraries
- 🎞️ **Assembles videos** in vertical format (1080x1920, 30fps)
- 📱 **Posts to social media** (Facebook Reels, YouTube Shorts, Instagram, TikTok)
- ✅ **Provides human approvals** at script, video, and publish stages

**Daily Time Investment**: Less than 1 hour active time
**Monthly Cost**: Less than $5 in API fees

---

## ✨ Key Features

### 🤖 AI-Powered Content Generation
- Multiple LLM providers (Claude Haiku/Sonnet, GPT-4o, AWS Bedrock)
- Smart provider selection and fallback chain
- Cost-optimized: Uses cheaper models by default ($0.02-$0.16 per video)
- Aggressive caching for 80% hit rate after initial runs

### 🎨 Flexible Visual Styles
- Kinetic typography animations (priority)
- OpenCV effects and transitions
- Optional Manim for data visualizations
- Customizable colors, fonts, and animation styles

### 🎙️ Free Audio Pipeline
- **gTTS**: Free Google Text-to-Speech (default)
- **edge-tts**: Free Microsoft TTS (higher quality)
- **pyttsx3**: Offline TTS fallback
- Background music mixing with ducking

### ✅ Human-in-the-Loop Approval
Three approval checkpoints:
1. **Script Review** - Edit or regenerate with feedback
2. **Video Preview** - Approve or adjust parameters
3. **Pre-Publish Review** - Edit captions and hashtags

### ⚙️ Highly Configurable
Web portal with configuration options:
- Content style (educational, storytelling, motivational, news)
- Visual style and color schemes
- TTS provider and voice settings
- Music mood and volume
- Target platforms and metadata

### 📱 Multi-Platform Publishing
- ✅ Facebook Reels (priority)
- ✅ YouTube Shorts
- ⏳ Instagram Reels (planned)
- ⏳ TikTok (planned)

---

## 🏗️ Architecture

```
┌─────────────────────────┐
│   Web Portal (FastAPI)  │  ← Configuration & Approvals
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│  Orchestration Layer    │  ← Job & Workflow Management
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│  Content Pipeline       │
│  ┌──────────────────┐   │
│  │ 1. Script Gen    │   │  ← AI generates script
│  │    ↓ Approval    │   │
│  │ 2. Media Gen     │   │  ← Create animations + audio
│  │    ↓ Approval    │   │
│  │ 3. Publish       │   │  ← Post to platforms
│  │    ↓ Approval    │   │
│  └──────────────────┘   │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│  Storage & Cache        │  ← SQLite + File Storage
└─────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- API keys for at least one LLM provider:
  - [Anthropic Claude](https://console.anthropic.com/) (recommended)
  - [OpenAI](https://platform.openai.com/)
  - [AWS Bedrock](https://aws.amazon.com/bedrock/)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/hello-faceless-content.git
cd hello-faceless-content

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys

# Initialize database
python scripts/init_db.py
```

### Configuration

Edit `.env` with your API keys:

```bash
# LLM API Keys (at least one required)
ANTHROPIC_API_KEY=your_claude_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Optional: AWS Bedrock
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1

# Social Media (for Phase 4)
FB_ACCESS_TOKEN=your_facebook_token
FB_PAGE_ID=your_page_id
YOUTUBE_CREDENTIALS_PATH=data/credentials/youtube_credentials.json
```

### Basic Usage

#### Phase 1: Generate Scripts (Current)

```bash
# Generate a script
python -m src.core.content.script_generator \
    --topic "5 Amazing Space Facts" \
    --style educational \
    --duration 60

# Get topic ideas
python -m src.core.content.topic_selector \
    --category science \
    --count 5
```

#### Phase 3+: Web Portal (Coming Soon)

```bash
# Start the web server
./scripts/start_server.sh

# Open browser to http://localhost:8000
```

---

## 📊 Development Status

### Current Phase: Phase 1 (Foundation & Script Generation)

**Progress**: ~40% complete

#### ✅ Completed
- Project structure and configuration
- Settings management (Pydantic)
- LLM prompt templates
- Logging system (loguru)
- File management utilities
- LLM response caching
- Comprehensive documentation

#### 🔄 In Progress
- Database models (SQLAlchemy)
- LLM provider integrations
- Content generation modules

#### ⏳ Upcoming
- Script parsing and scene extraction
- CLI testing tools
- Unit tests

### Roadmap

| Phase | Timeline | Status | Deliverable |
|-------|----------|--------|-------------|
| **Phase 1** | Week 1-2 | 🔄 In Progress | CLI script generator |
| **Phase 2** | Week 3-4 | ⏳ Planned | CLI video generator |
| **Phase 3** | Week 5-6 | ⏳ Planned | Web portal with approvals |
| **Phase 4** | Week 7-8 | ⏳ Planned | Social media publishing |
| **Phase 5** | Week 9+ | ⏳ Planned | Optimizations & enhancements |

---

## 💰 Cost Analysis

### Per Video Costs

| Component | Cost | Provider |
|-----------|------|----------|
| Script Generation | $0.015 - $0.15 | Claude Haiku/Sonnet |
| TTS | $0 | gTTS/edge-tts |
| Music | $0 | Royalty-free |
| Video Rendering | $0 | Local compute |
| Publishing | $0 | Platform APIs |
| **Total** | **$0.02 - $0.16** | |

### Monthly Costs (30 videos)

- **LLM API**: $0.60 - $4.80
- **Infrastructure**: $0 (runs locally on Mac)
- **Total**: **< $5/month**

### Cost Optimization Features

- ✅ Aggressive response caching (80% hit rate)
- ✅ Use cheap models (Haiku) by default
- ✅ Only use premium models (Sonnet) for complex scripts
- ✅ Batch similar topics to maximize cache hits

---

## 📚 Documentation

Comprehensive documentation is available in the [`docs/`](docs/) directory:

- [**Overview**](docs/overview.md) - Project vision and architecture
- [**Phase 1 Details**](docs/phase1-foundation.md) - Foundation & script generation (current)
- [**CLAUDE.md**](CLAUDE.md) - AI assistant context and guidelines
- [**Setup Guide**](docs/setup.md) - Installation and configuration (coming soon)
- [**User Guide**](docs/user-guide.md) - Using the system (coming soon)
- [**API Reference**](docs/api-reference.md) - Code documentation (coming soon)

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_llm.py

# Run with coverage
pytest --cov=src tests/
```

### Manual Testing (Phase 1)

```bash
# Test LLM connection
python -c "from src.core.llm.claude import ClaudeProvider; \
    p = ClaudeProvider(); \
    print('Connected!' if p.is_available() else 'Not configured')"

# Test script generation
python -m src.core.content.script_generator \
    --topic "Test Topic" \
    --style educational \
    --duration 60

# Check cache stats
python -c "from src.utils.cache import llm_cache; \
    print(llm_cache.get_cache_stats())"
```

---

## 📁 Project Structure

```
hello-faceless-content/
├── src/                      # Source code
│   ├── config/              # Settings & prompts
│   ├── models/              # Database models
│   ├── core/
│   │   ├── llm/            # AI provider integrations
│   │   ├── content/        # Script generation
│   │   ├── media/          # Video/audio generation
│   │   └── publishing/     # Social media APIs
│   ├── workflows/          # Pipeline orchestration
│   ├── web/                # FastAPI web portal
│   └── utils/              # Utilities (logging, caching, etc.)
├── data/                    # Local storage
│   ├── output/             # Generated videos
│   ├── assets/             # Music, fonts
│   ├── cache/              # LLM responses, temp files
│   └── database/           # SQLite database
├── scripts/                # Setup & maintenance scripts
├── tests/                  # Unit & integration tests
├── docs/                   # Documentation
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Project configuration
├── .env.example           # Environment template
└── README.md              # This file
```

---

## 🎯 Success Metrics

### Technical Metrics
- Script generation success rate: > 95%
- Video rendering success rate: > 90%
- Publishing success rate: > 95%
- Total generation time: < 15 minutes
- User active time: < 30 minutes/day

### Quality Metrics
- First-try script approval rate: > 80%
- First-try video approval rate: > 70%

### Cost Metrics
- Monthly API cost: < $10
- Cost per published video: < $0.20

---

## 🤝 Contributing

This is a personal automation project. However, feedback and suggestions are welcome!

### Reporting Issues

If you encounter issues:
1. Check the [documentation](docs/)
2. Review [CLAUDE.md](CLAUDE.md) for common issues
3. Check logs in `logs/` directory
4. Open an issue with details

### Development Guidelines

When contributing:
1. Follow existing code style (see [CLAUDE.md](CLAUDE.md))
2. Add tests for new features
3. Update documentation
4. Consider cost implications of changes

---

## 🔒 Security & Privacy

- ✅ All API keys stored in `.env` (not committed to git)
- ✅ SQLite database is local only
- ✅ No telemetry or external tracking
- ✅ Videos stored locally until manually published
- ⚠️ Review scripts before publishing (approval system)

---

## 📄 License

This is a private project. All rights reserved.

---

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [MoviePy](https://zulko.github.io/moviepy/) - Video editing
- [Anthropic Claude](https://www.anthropic.com/) - AI content generation
- [Pillow](https://python-pillow.org/) - Image processing
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM

---

## 📞 Support

For questions or issues:
- 📖 Read the [documentation](docs/)
- 🤖 Check [CLAUDE.md](CLAUDE.md) for AI assistant guidance
- 📝 Review logs in `logs/` directory
- 💬 Open an issue on GitHub

---

**Made with ❤️ by Tanvir Hossain**

**Status**: 🚧 Phase 1 In Progress (Foundation & Script Generation)

**Last Updated**: December 12, 2024
