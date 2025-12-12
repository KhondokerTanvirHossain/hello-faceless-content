# Setup Guide

Complete installation and configuration guide for the Faceless Video Automation System.

---

## 📋 Prerequisites

### System Requirements
- **Operating System**: macOS 10.15+, Linux, or Windows 10+
- **Python**: 3.11 or higher
- **Disk Space**: At least 5GB free (for videos, cache, and dependencies)
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Internet**: Required for API calls and dependency installation

### API Keys (At Least One Required)

You'll need API keys for at least one LLM provider:

#### Option 1: Anthropic Claude (Recommended)
- **Cost**: $0.25/$1.25 per million tokens (Haiku), $3/$15 per million tokens (Sonnet)
- **Why recommended**: Best quality/cost balance, fast responses
- **Sign up**: https://console.anthropic.com/
- **Free tier**: $5 credit for new accounts

#### Option 2: OpenAI
- **Cost**: $0.15/$0.60 per million tokens (GPT-4o-mini), $2.50/$10 per million tokens (GPT-4o)
- **Sign up**: https://platform.openai.com/
- **Free tier**: $5 credit for new accounts (expires after 3 months)

#### Option 3: AWS Bedrock
- **Cost**: Varies by model
- **Requirements**: AWS account, IAM credentials
- **Setup**: https://aws.amazon.com/bedrock/

### Optional (For Phase 4 - Publishing)
- **Facebook/Instagram**: Facebook Developer account and app
- **YouTube**: Google Cloud project with YouTube Data API enabled
- **TikTok**: TikTok Developer account (requires approval)

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
# Clone via HTTPS
git clone https://github.com/yourusername/hello-faceless-content.git

# Or via SSH
git clone git@github.com:yourusername/hello-faceless-content.git

# Navigate to project directory
cd hello-faceless-content
```

### Step 2: Create Virtual Environment

#### On macOS/Linux:
```bash
# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify Python version
python --version  # Should show Python 3.11.x
```

#### On Windows:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Verify Python version
python --version  # Should show Python 3.11.x
```

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep fastapi  # Should show fastapi
pip list | grep anthropic  # Should show anthropic
```

**Note**: Installation may take 5-10 minutes depending on your internet speed.

### Step 4: Configure Environment Variables

```bash
# Copy environment template
cp .env.example .env

# Edit .env file
# On macOS/Linux:
nano .env
# Or use your preferred editor: vim, code, etc.

# On Windows:
notepad .env
```

**Minimum Configuration** (add at least one API key):

```bash
# LLM API Keys (at least one required)
ANTHROPIC_API_KEY=sk-ant-api03-...your-key-here...
# OPENAI_API_KEY=sk-...your-key-here...

# Database (default is fine for local use)
DATABASE_URL=sqlite:///data/database/app.db

# Application
DEBUG=True
LOG_LEVEL=INFO
```

**Full Configuration Example**:

```bash
# ============================================
# LLM API Keys (at least one required)
# ============================================
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
AWS_ACCESS_KEY_ID=AKIAxxxxxxxxxxxxx
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxx
AWS_REGION=us-east-1

# ============================================
# Database
# ============================================
DATABASE_URL=sqlite:///data/database/app.db

# ============================================
# File Paths (default values shown)
# ============================================
OUTPUT_DIR=data/output
ASSETS_DIR=data/assets
CACHE_DIR=data/cache

# ============================================
# Video Settings
# ============================================
DEFAULT_RESOLUTION=1080x1920  # Vertical format for social media
DEFAULT_FPS=30
DEFAULT_DURATION=60  # seconds

# ============================================
# Social Media APIs (Phase 4 - Optional for now)
# ============================================
# FB_ACCESS_TOKEN=your_facebook_access_token
# FB_PAGE_ID=your_facebook_page_id
# YOUTUBE_CREDENTIALS_PATH=data/credentials/youtube_credentials.json

# ============================================
# Application
# ============================================
DEBUG=True
LOG_LEVEL=INFO  # Options: DEBUG, INFO, WARNING, ERROR
```

### Step 5: Initialize Database

```bash
# Run database initialization script
python scripts/init_db.py
```

**Expected Output**:
```
Creating database at data/database/app.db...
Creating tables...
✓ Table: jobs
✓ Table: scripts
✓ Table: videos
✓ Table: approvals
✓ Table: publications
Database initialized successfully!
```

### Step 6: Verify Installation

Run these commands to verify everything is set up correctly:

#### Test 1: Check Python Imports
```bash
python -c "import fastapi; import anthropic; import sqlalchemy; print('✓ All imports successful')"
```

#### Test 2: Verify Settings
```bash
python -c "from src.config.settings import settings; print(f'✓ Settings loaded. Debug={settings.debug}')"
```

#### Test 3: Check Database
```bash
python -c "from pathlib import Path; print('✓ Database exists' if Path('data/database/app.db').exists() else '✗ Database not found')"
```

#### Test 4: Test LLM Connection
```bash
# This will test if your API key is configured
python -c "from src.core.llm.claude import ClaudeProvider; p = ClaudeProvider(); print('✓ Claude configured' if p.is_available() else '✗ Claude not configured')"
```

---

## 🧪 Testing the Setup

### Test Script Generation (Phase 1)

Once Phase 1 is complete, you can test the script generator:

```bash
# Generate a test script
python -m src.core.content.script_generator \
    --topic "5 Amazing Facts About Python Programming" \
    --style educational \
    --duration 60
```

**Expected Output**: A JSON object with the generated script.

### Check Logs

```bash
# View application logs
tail -f logs/app_$(date +%Y-%m-%d).log

# View error logs
tail -f logs/errors_$(date +%Y-%m-%d).log
```

### Check Cache

```bash
# View cache statistics
python -c "from src.utils.cache import llm_cache; import json; print(json.dumps(llm_cache.get_cache_stats(), indent=2))"
```

---

## 📁 Directory Structure After Setup

After setup, your project should look like this:

```
hello-faceless-content/
├── venv/                     # Virtual environment (created)
├── .env                      # Your configuration (created)
├── data/
│   ├── output/
│   │   ├── drafts/          # Will store draft videos
│   │   └── final/           # Will store approved videos
│   ├── assets/
│   │   ├── music/           # Add music files here
│   │   └── fonts/           # Add fonts here
│   ├── cache/
│   │   ├── llm/             # LLM response cache
│   │   ├── audio/           # Audio cache
│   │   └── animations/      # Animation cache
│   └── database/
│       └── app.db           # SQLite database (created)
├── logs/                     # Log files (created on first run)
│   ├── app_YYYY-MM-DD.log
│   └── errors_YYYY-MM-DD.log
└── [... rest of project files ...]
```

---

## 🎵 Optional: Download Background Music

To use background music in your videos, download royalty-free tracks:

### Recommended Sources

1. **Pixabay** (https://pixabay.com/music/)
   - Free for commercial use
   - No attribution required
   - Wide variety of moods

2. **YouTube Audio Library** (https://www.youtube.com/audiolibrary/music)
   - Free for YouTube use
   - Check licensing for other platforms
   - High quality

3. **Free Music Archive** (https://freemusicarchive.org/)
   - Creative Commons licensed
   - May require attribution
   - Large selection

### Organizing Music Files

```bash
# Create mood folders
mkdir -p data/assets/music/{upbeat,calm,dramatic,inspirational,educational}

# Example: Download and organize
# Download music files, then:
mv upbeat_track1.mp3 data/assets/music/upbeat/
mv calm_background.mp3 data/assets/music/calm/
```

**Recommended**: Download 5-10 tracks per mood category (20-30 total tracks).

---

## 🔧 Troubleshooting

### Issue: Python Version Wrong

**Error**: `python: command not found` or wrong version

**Solution**:
```bash
# Check Python versions available
python3 --version
python3.11 --version

# Use specific version
python3.11 -m venv venv
```

### Issue: pip install fails

**Error**: `error: externally-managed-environment`

**Solution** (on macOS/Linux with Homebrew Python):
```bash
# Use virtual environment (recommended)
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Or use --break-system-packages (not recommended)
pip install --break-system-packages -r requirements.txt
```

### Issue: Permission Denied

**Error**: `PermissionError: [Errno 13] Permission denied`

**Solution**:
```bash
# Check directory permissions
ls -la data/

# Fix permissions
chmod -R 755 data/
```

### Issue: Module Import Error

**Error**: `ModuleNotFoundError: No module named 'src'`

**Solution**:
```bash
# Make sure you're in the project root
pwd  # Should show: .../hello-faceless-content

# Add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or use python -m
python -m src.core.content.script_generator ...
```

### Issue: API Key Not Working

**Error**: `API key not configured` or `Invalid API key`

**Solution**:
1. Check `.env` file exists in project root
2. Verify no extra spaces around `=` in .env
3. Ensure API key is correct (no newlines)
4. Restart terminal to reload environment

```bash
# Test API key
echo $ANTHROPIC_API_KEY  # Should show your key

# Reload environment
source venv/bin/activate
```

### Issue: Database Not Found

**Error**: `OperationalError: unable to open database file`

**Solution**:
```bash
# Ensure directories exist
mkdir -p data/database

# Re-run initialization
python scripts/init_db.py

# Check permissions
ls -la data/database/
```

### Issue: FFmpeg Not Found (Phase 2+)

**Error**: `FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'`

**Solution**:
```bash
# On macOS:
brew install ffmpeg

# On Ubuntu/Debian:
sudo apt-get install ffmpeg

# On Windows:
# Download from https://ffmpeg.org/download.html
# Add to PATH
```

---

## 🔄 Updating the Project

To update to the latest version:

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install --upgrade -r requirements.txt

# Run any new migrations
python scripts/migrate_db.py  # If available

# Restart services
./scripts/start_server.sh
```

---

## 🧹 Maintenance

### Clean Cache

```bash
# Clean expired LLM cache (> 7 days old)
python -c "from src.utils.cache import llm_cache; llm_cache.clear_expired(max_age_hours=168)"

# Clean all cache
python -c "from src.utils.cache import llm_cache; llm_cache.clear_all()"
```

### Clean Old Drafts

```bash
# Delete draft videos older than 7 days
python -c "from src.utils.file_manager import file_manager; file_manager.cleanup_old_drafts(days=7)"
```

### Backup Database

```bash
# Create backup
cp data/database/app.db data/database/app_backup_$(date +%Y%m%d).db

# List backups
ls -lh data/database/app_backup_*.db
```

### View Disk Usage

```bash
# Check data directory size
du -sh data/

# Breakdown by subdirectory
du -sh data/*
```

---

## 🚦 Next Steps

Once setup is complete:

1. ✅ **Test the system** - Run verification commands above
2. 📖 **Read Phase 1 docs** - [Phase 1 Details](phase1-foundation.md)
3. 🧪 **Try script generation** - Test with various topics
4. 🎵 **Download music** - Add background music files
5. 💻 **Start coding** - Continue Phase 1 implementation

---

## 📞 Getting Help

If you encounter issues:

1. **Check logs**: `tail -f logs/app_*.log`
2. **Review documentation**: See [docs/](.)
3. **Check CLAUDE.md**: [Common issues](../CLAUDE.md#common-issues--solutions)
4. **Verify environment**: Run verification commands above

---

**Setup Complete?** Move on to [Phase 1 Implementation](phase1-foundation.md)!
