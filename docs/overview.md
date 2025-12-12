# Faceless Video Automation System - Overview

## 🎯 Project Vision

An end-to-end Python automation system that generates and posts faceless vertical short videos (15–60s) with minimal daily input (< 1 hour). The system is cheap to run, simple to use, and allows "human-in-the-loop" approvals at key decision points.

## 🎬 What We're Building

A complete video automation pipeline that:

1. **Generates AI-powered scripts** from topics or prompts
2. **Creates animations** using PIL, OpenCV, and optionally Manim
3. **Produces voiceovers** with free TTS services (gTTS, edge-tts)
4. **Adds background music** from a royalty-free library
5. **Assembles videos** with MoviePy (1080x1920, 30fps)
6. **Posts to social media** (Facebook Reels priority, YouTube Shorts, Instagram, TikTok)
7. **Provides approvals** at script, video, and publish stages via web portal

## 🌟 Key Features

### 🤖 AI-Powered Content
- Multiple LLM providers (Claude, OpenAI, AWS Bedrock) with smart fallback
- Cost-optimized: Uses cheaper models (Haiku) by default, premium models when needed
- Aggressive caching: 80% cache hit rate reduces API costs
- **Cost**: $0.02 - $0.16 per video, < $5/month for 30 videos

### 🎨 Flexible Visuals
- **Priority**: PIL-based kinetic typography and animations
- OpenCV effects for transitions and filters
- Optional Manim for data visualizations
- Customizable color schemes, fonts, animation styles

### 🎙️ Free Audio
- **gTTS**: Free Google TTS (default)
- **edge-tts**: Free Microsoft TTS (higher quality)
- **pyttsx3**: Offline fallback
- Background music from royalty-free libraries

### ✅ Human Control
- **3 approval checkpoints**:
  1. Script review (edit or regenerate)
  2. Video preview (approve or adjust)
  3. Pre-publish review (edit metadata)
- Web-based interface for easy reviews
- Inline editing capabilities

### ⚙️ Highly Configurable
Web portal with "knobs" to adjust:
- Content style (educational, storytelling, motivational, news)
- Visual style (kinetic text, mixed, data viz)
- Color schemes and fonts
- TTS voice and speed
- Music mood and volume
- Target platforms and metadata

### 📱 Multi-Platform
- **Facebook Reels** (priority)
- YouTube Shorts
- Instagram Reels
- TikTok (manual initially)

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│      Web Portal (FastAPI)           │
│  - Configuration Interface          │
│  - Approval Workflow                │
│  - Job Management Dashboard         │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│   Orchestration Layer                │
│  - Job Manager                       │
│  - Pipeline Controller               │
│  - Approval Handler                  │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│   Content Generation Pipeline        │
│                                      │
│  ┌────────────┐  ┌────────────┐    │
│  │  Stage 1   │  │  Stage 2   │    │
│  │  Script    │→ │  Media     │    │
│  │  Gen       │  │  Gen       │    │
│  └─────┬──────┘  └─────┬──────┘    │
│        ↓ Approval      ↓ Approval   │
│                                      │
│  ┌────────────┐                     │
│  │  Stage 3   │                     │
│  │  Publish   │                     │
│  └─────┬──────┘                     │
│        ↓ Approval                   │
└─────────────────────────────────────┘
               ↓
┌─────────────────────────────────────┐
│     Storage & Cache                  │
│  - SQLite Database                   │
│  - File Storage                      │
│  - LLM Response Cache                │
└─────────────────────────────────────┘
```

## 📊 Tech Stack

### Core
- **Python 3.11+** - Modern async support
- **FastAPI** - Web framework
- **SQLite + SQLAlchemy** - Database
- **Pydantic** - Settings & validation

### Video & Media
- **MoviePy** - Video editing
- **Pillow (PIL)** - Image manipulation
- **OpenCV** - Effects & transitions
- **imageio** - I/O operations

### Audio
- **gTTS** - Free TTS (default)
- **edge-tts** - High-quality free TTS
- **pyttsx3** - Offline TTS
- **pydub** - Audio mixing

### AI
- **Anthropic** - Claude API
- **OpenAI** - GPT API
- **boto3** - AWS Bedrock

### Social Media
- **facebook-sdk** - Facebook/Instagram
- **google-api-python-client** - YouTube

## 💰 Cost Analysis

### Per Video
- **LLM API**: $0.02 - $0.16
- **TTS**: $0 (free)
- **Music**: $0 (royalty-free)
- **Rendering**: $0 (local)
- **Total**: **$0.02 - $0.16 per video**

### Monthly (30 videos)
- **LLM costs**: $0.60 - $4.80
- **Infrastructure**: $0 (runs locally)
- **Total**: **< $5/month**

### Cost Optimization
- ✅ Cache LLM responses (80% hit rate)
- ✅ Use Claude Haiku for simple tasks
- ✅ Only use Sonnet for complex scripts
- ✅ Pre-render common elements
- ✅ Batch similar topics

## ⏱️ Daily Workflow (< 1 hour)

### Morning (15 minutes active)
1. Open web portal (http://localhost:8000)
2. Create new job with topic
3. Review & approve AI-generated script

### Midday (5 minutes active)
4. Review generated video preview
5. Approve or request changes

### Afternoon (5 minutes active)
6. Review publish settings
7. Approve & publish to platforms

**Total Active Time**: ~25 minutes
**Passive Time**: 8-12 minutes (AI generation, rendering, uploading)

## 🎯 Success Metrics

### Technical
- Script generation success: > 95%
- Video rendering success: > 90%
- Publishing success: > 95%
- Total generation time: < 15 minutes
- User active time: < 30 minutes/day

### Quality
- First-try script approval: > 80%
- First-try video approval: > 70%

### Cost
- Monthly API cost: < $10
- Cost per video: < $0.20

## 🚀 Implementation Approach

We're building this in **5 phases**:

1. **Phase 1** (Week 1-2): Foundation & Script Generation
2. **Phase 2** (Week 3-4): Video Generation (animations + audio)
3. **Phase 3** (Week 5-6): Web Portal & Workflow
4. **Phase 4** (Week 7-8): Platform Publishing
5. **Phase 5** (Week 9+): Optimization & Enhancements

Each phase delivers a working, testable system before moving to the next.

## 📁 Project Structure

```
hello-faceless-content/
├── src/
│   ├── config/          # Settings & prompts
│   ├── models/          # Database models
│   ├── core/
│   │   ├── llm/         # AI providers
│   │   ├── content/     # Script generation
│   │   ├── media/       # Video/audio generation
│   │   └── publishing/  # Social media posting
│   ├── workflows/       # Orchestration
│   ├── web/             # Web portal
│   └── utils/           # Utilities
├── data/
│   ├── output/          # Generated videos
│   ├── assets/          # Music, fonts
│   ├── cache/           # LLM responses, temp files
│   └── database/        # SQLite database
├── scripts/             # Setup & maintenance
├── tests/               # Unit & integration tests
└── docs/                # Documentation
```

## 🔄 Next Steps

1. ✅ **Setup Complete**: Project structure, config, utilities
2. 🔄 **Current**: Building database models & LLM integration
3. ⏭️ **Next**: Content generation & script parser
4. ⏭️ **Then**: Video generation pipeline
5. ⏭️ **Finally**: Web portal & publishing

## 📚 Documentation

- [Phase 1 Details](phase1-foundation.md) - Foundation & Script Generation
- [Phase 2 Details](phase2-video-generation.md) - Video & Audio Generation
- [Phase 3 Details](phase3-web-portal.md) - Web Portal & Workflow
- [Phase 4 Details](phase4-publishing.md) - Platform Publishing
- [Phase 5 Details](phase5-optimization.md) - Optimization & Enhancements
- [Setup Guide](setup.md) - Installation & Configuration
- [User Guide](user-guide.md) - Using the System
- [API Reference](api-reference.md) - Code Documentation

## 🤝 Contributing

This is a personal automation project, but feedback and suggestions are welcome!

## 📄 License

Private project - All rights reserved
