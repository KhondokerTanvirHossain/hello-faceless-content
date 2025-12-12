# 🚀 Quick Start Guide

Get your Faceless Video Automation System running in **5 minutes**!

---

## ⚡ Prerequisites

- **Python 3.11+** installed
- **API key** for at least ONE of:
  - [Anthropic Claude](https://console.anthropic.com/) (recommended - $5 free credit)
  - [OpenAI](https://platform.openai.com/) ($5 free credit)
  - [AWS Bedrock](https://aws.amazon.com/bedrock/) (AWS account required)

---

## 📝 Step 1: Clone & Setup (2 minutes)

```bash
# Navigate to project directory (if not already there)
cd hello-faceless-content

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies (takes ~2 minutes)
pip install -r requirements.txt
```

**Expected output**: All packages installed successfully ✓

---

## 🔑 Step 2: Configure API Key (1 minute)

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add YOUR API key
nano .env  # or use: code .env, vim .env, etc.
```

**Add at least ONE of these keys to `.env`:**

```bash
# Option 1: Claude (Recommended - best quality/cost)
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxx

# Option 2: OpenAI
OPENAI_API_KEY=sk-xxxxxxxxxxxxx

# Option 3: AWS Bedrock
AWS_ACCESS_KEY_ID=AKIAxxxxxxxxxxxxx
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxx
AWS_REGION=us-east-1
```

**💡 Tip**: Get a free API key:
- **Claude**: https://console.anthropic.com/ → Create account → Get API key
- **OpenAI**: https://platform.openai.com/ → Sign up → Create API key

**Save and close** the file.

---

## 🗄️ Step 3: Initialize Database (30 seconds)

```bash
python scripts/init_db.py
```

**Expected output**:
```
============================================================
Database Initialization Script
============================================================

Database URL: sqlite:///data/database/app.db

✓ Database directory ensured: data/database

Creating database tables...
✓ Database initialized successfully!

Database Information:
------------------------------------------------------------
  Tables: jobs, scripts, videos, approvals, publications
  Total: 5 tables

============================================================
Database initialization complete!
============================================================
```

---

## 🎬 Step 4: Generate Your First Script! (1 minute)

### Option A: Generate Topic Ideas First

```bash
python -m src.core.content.topic_selector \
    --category science \
    --style educational \
    --count 5
```

**Expected output**: 5 trending topic ideas with "why engaging" explanations

### Option B: Generate Script Directly

```bash
python -m src.core.content.script_generator \
    --topic "5 Amazing Facts About Black Holes" \
    --style educational \
    --duration 60
```

**Expected output**: Complete JSON script with:
- Title
- Hook (opening line)
- Scenes with timing and visual hints
- Conclusion
- Hashtags
- Metrics (word count, duration, scene count)

---

## 🎉 Success Indicators

If everything worked, you should see:

### ✅ Script Generation Success:
```
Generating script: topic='5 Amazing Facts About Black Holes', style=educational, duration=60s
✓ Claude | Model: claude-3-5-sonnet-20241022 | Prompt: 450 chars | Response: 1850 chars
Claude tokens: 120 in / 485 out | Cost: $0.0076
✓ Script generated: 5 Amazing Facts About Black Holes

============================================================
GENERATED SCRIPT
============================================================
{
  "title": "5 Amazing Facts About Black Holes",
  "hook": "Did you know black holes aren't actually black?",
  "scenes": [
    {
      "text": "First, black holes emit something called Hawking radiation...",
      "duration": 12,
      "visual_hint": "Animated visualization of radiation particles",
      "keywords": ["black holes", "radiation", "Hawking"]
    },
    ...
  ],
  "conclusion": "Black holes are truly the universe's most mysterious objects!",
  "hashtags": ["blackholes", "space", "science", "physics", "astronomy"],
  "estimated_duration": 60
}
============================================================

METRICS:
  Word count: 245
  Scene count: 5
  Estimated duration: 60s
  Avg scene duration: 12.0s
```

### ✅ Cache Working (Run same command again):
```
✓ Cache hit - returning cached response
```

**🎊 Congratulations! Your system is working!**

---

## 🧪 Additional Test Commands

### Check Available Providers
```bash
python -c "from src.core.llm.manager import llm_manager; print('Available:', llm_manager.get_available_providers())"
```

### View Cache Statistics
```bash
python -c "from src.utils.cache import llm_cache; import json; print(json.dumps(llm_cache.get_cache_stats(), indent=2))"
```

### Generate Different Styles

**Storytelling:**
```bash
python -m src.core.content.script_generator \
    --topic "The Day Einstein Discovered E=mc²" \
    --style storytelling \
    --duration 60
```

**Motivational:**
```bash
python -m src.core.content.script_generator \
    --topic "Why Failure Is Your Greatest Teacher" \
    --style motivational \
    --duration 45
```

**News Commentary:**
```bash
python -m src.core.content.script_generator \
    --topic "Latest AI Breakthrough Explained" \
    --style news \
    --duration 60
```

### Force Fresh Generation (Skip Cache)
```bash
python -m src.core.content.script_generator \
    --topic "Test Topic" \
    --style educational \
    --no-cache
```

### Use Specific Provider
```bash
# Use OpenAI instead of Claude
python -m src.core.content.script_generator \
    --topic "Test Topic" \
    --provider openai
```

---

## 💰 Cost Tracking

Every generation shows the cost:

```
Claude tokens: 120 in / 485 out | Cost: $0.0076
```

**Typical costs:**
- Topic generation: $0.002 - $0.005
- Script generation: $0.015 - $0.15 (depending on model)
- **With caching**: Second request = $0.00

**Monthly estimate (30 videos)**: $0.60 - $4.80

---

## 🐛 Troubleshooting

### Issue: "No LLM providers configured"

**Fix**: Add API key to `.env` file
```bash
# Edit .env
nano .env

# Add your API key:
ANTHROPIC_API_KEY=your_key_here

# Restart terminal or reload environment
source venv/bin/activate
```

### Issue: "Module not found"

**Fix**: Ensure virtual environment is activated
```bash
# Check if (venv) appears in prompt
# If not, activate:
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Verify Python is from venv:
which python  # Should show: .../venv/bin/python
```

### Issue: "API key invalid"

**Fix**:
1. Verify API key is correct (no extra spaces)
2. Check API key is still active on provider's website
3. Ensure no newline characters in `.env`

```bash
# Test API key directly:
python -c "from src.core.llm.claude import ClaudeProvider; p = ClaudeProvider(); print('✓ Connected' if p.is_available() else '✗ Not configured')"
```

### Issue: Rate limit errors

**Fix**: The system automatically retries with exponential backoff. Just wait a few seconds.

### Issue: Empty/invalid responses

**Fix**: Try a different provider or model:
```bash
# Use OpenAI instead
python -m src.core.content.script_generator \
    --topic "Test" \
    --provider openai
```

---

## 📁 Where Things Are Saved

```
hello-faceless-content/
├── data/
│   ├── cache/
│   │   └── llm/              # Cached LLM responses (saves money!)
│   ├── database/
│   │   └── app.db            # SQLite database
│   └── output/               # Future: generated videos
└── logs/
    ├── app_YYYY-MM-DD.log    # Application logs
    └── errors_YYYY-MM-DD.log # Error logs
```

**View logs:**
```bash
# Application logs
tail -f logs/app_$(date +%Y-%m-%d).log

# Error logs
tail -f logs/errors_$(date +%Y-%m-%d).log
```

---

## 🎯 What to Try Next

### 1. **Experiment with Different Topics**
```bash
# Science
python -m src.core.content.script_generator --topic "How DNA Replication Works"

# Technology
python -m src.core.content.script_generator --topic "The Future of Quantum Computing"

# History
python -m src.core.content.script_generator --topic "The Fall of the Roman Empire in 5 Minutes"

# Pop Culture
python -m src.core.content.script_generator --topic "The Evolution of Hip Hop Music"
```

### 2. **Test Different Durations**
```bash
# 30-second short
python -m src.core.content.script_generator --topic "Quick Python Tip" --duration 30

# 90-second deep dive
python -m src.core.content.script_generator --topic "Understanding Bitcoin" --duration 90
```

### 3. **Generate Batch Topics for the Week**
```bash
# Get 10 topic ideas
python -m src.core.content.topic_selector --category technology --count 10 > topics.txt

# Review and pick your favorites
cat topics.txt
```

### 4. **Monitor Cache Savings**
```bash
# Generate same script twice
python -m src.core.content.script_generator --topic "Test" --duration 30

# Second time should show "Cache hit" and be instant!
python -m src.core.content.script_generator --topic "Test" --duration 30

# Check cache stats
python -c "from src.utils.cache import llm_cache; stats = llm_cache.get_cache_stats(); print(f'Cached: {stats[\"total_entries\"]} entries, {stats[\"total_size_mb\"]}MB')"
```

---

## 📖 Learn More

- **Full Documentation**: See [docs/](docs/) folder
- **Phase 1 Details**: [docs/phase1-foundation.md](docs/phase1-foundation.md)
- **Setup Guide**: [docs/setup.md](docs/setup.md)
- **AI Assistant Context**: [CLAUDE.md](CLAUDE.md)
- **Project Overview**: [docs/overview.md](docs/overview.md)

---

## 🚀 What's Next?

You've successfully completed **Phase 1**! The system can now:
- ✅ Generate AI-powered video scripts
- ✅ Parse scripts into timed scenes
- ✅ Suggest topic ideas
- ✅ Cache responses for cost savings
- ✅ Track metrics and costs

**Coming in Phase 2**:
- 🎨 Animation generation (PIL, OpenCV)
- 🎙️ Text-to-speech voiceovers
- 🎵 Background music mixing
- 🎬 Video assembly with MoviePy
- 📹 Complete video rendering

**Coming in Phase 3**:
- 🌐 Web portal (FastAPI)
- ✅ Approval workflow UI
- 📊 Dashboard and job management

**Coming in Phase 4**:
- 📱 Social media publishing
- 🔄 Automated posting to platforms

---

## 💡 Pro Tips

### 💰 Save Money
1. **Always use cache** (default) - saves 80% of API costs after initial runs
2. **Test with short durations** (30s) during development
3. **Batch similar topics** to maximize cache hits

### ⚡ Speed Up Generation
1. Use `--provider claude` with Haiku model (5x cheaper, almost as good)
2. Keep prompts focused and clear
3. Let the cache work - don't use `--no-cache` unless necessary

### 🎨 Better Scripts
1. Be **specific** in topics: "5 Ways AI Improves Healthcare" > "AI facts"
2. Match **style to content**: Educational for facts, Storytelling for narratives
3. Test different **durations**: 30s for quick facts, 60s for detailed content

### 🔍 Debug Issues
1. Check logs first: `tail -f logs/app_*.log`
2. Test provider: `python -c "from src.core.llm.claude import ClaudeProvider; ClaudeProvider().is_available()"`
3. Clear cache if stuck: `python -c "from src.utils.cache import llm_cache; llm_cache.clear_all()"`

---

## ✅ Quick Start Checklist

- [ ] Python 3.11+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] API key added to `.env`
- [ ] Database initialized (`python scripts/init_db.py`)
- [ ] First script generated successfully
- [ ] Cache verified working (run same command twice)
- [ ] Reviewed logs (`logs/app_*.log`)

**All checked?** 🎉 **You're ready to go!**

---

## 📞 Get Help

- **Check logs**: `tail -f logs/app_*.log`
- **Review docs**: [docs/](docs/)
- **Common issues**: [docs/setup.md#troubleshooting](docs/setup.md#troubleshooting)
- **AI context**: [CLAUDE.md](CLAUDE.md)

---

**🎬 Happy Video Creating!**

*Generated with [Claude Code](https://claude.com/claude-code) - Version 1.0.0 - Phase 1 Complete*
