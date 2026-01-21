# ⚡ Quick Reference Cheat Sheet

**Bookmark this page! Everything you need on one page.**

---

## 🚀 First Time Setup

```bash
# 1. Open Terminal (Command + Space, type "terminal")

# 2. Go to Desktop
cd Desktop

# 3. Download the project
git clone https://github.com/YOUR-USERNAME/Claude-experiments.git

# 4. Enter the folder
cd Claude-experiments

# 5. Run setup
./setup.sh

# 6. Start Web UI for easy setup
source venv/bin/activate
python main.py web

# 7. Open browser and follow setup wizard!
```

---

## 📅 Daily Use (Every Morning)

```bash
# 1. Open Terminal

# 2. Go to project folder
cd ~/Desktop/Claude-experiments

# 3. Activate environment
source venv/bin/activate

# 4. Scan & analyze in one command
python main.py scan && python main.py analyze
```

**That's it! Takes 30 seconds.**

---

## 🌐 NEW: Web UI (Easiest!)

```bash
# Start Web UI
python main.py web

# Then open browser to: http://localhost:5000
```

**What you can do in Web UI:**
- Set up API key (no file editing!)
- Auto-discover competitors
- Add/remove competitors with clicks
- View reports in browser
- Check system status

---

## 📊 All Commands

**Always run this first:**
```bash
source venv/bin/activate
```

**Then run any of these:**

| Command | What it does |
|---------|-------------|
| `python main.py web` | 🌐 Open Web UI (recommended!) |
| `python main.py discover <url>` | 🔍 Auto-find competitors |
| `python main.py scan` | Check all competitors for changes |
| `python main.py analyze` | Get AI insights on detected changes |
| `python main.py report` | Generate weekly intelligence brief |
| `python main.py gaps` | Find market opportunities |
| `python main.py status` | See what you're tracking |

**Example: Auto-discover competitors**
```bash
python main.py discover https://yourcompany.com
```

---

## 🔧 Common Fixes

**"Command not found"**
```bash
cd ~/Desktop/Claude-experiments
```

**"ModuleNotFoundError"**
```bash
source venv/bin/activate
```

**"Permission denied"**
```bash
chmod +x setup.sh main.py
```

---

## 📁 Important Files

| File | What to do |
|------|-----------|
| `config.json` | Edit to add/change competitors |
| `reports/` folder | Read your intelligence briefs here |
| `data/` folder | Database (don't touch) |

---

## ⚙️ Editing config.json

```json
{
  "api_keys": {
    "anthropic_api_key": "your-key-here"
  },
  "competitors": [
    {
      "name": "Competitor Name",
      "urls": {
        "homepage": "https://example.com",
        "pricing": "https://example.com/pricing"
      },
      "priority": "high"
    }
  ]
}
```

**To add a competitor:** Copy the block above and change the name/URLs.

---

## 🎯 Typical Week

**Monday AM:**
```bash
python main.py scan
python main.py analyze
python main.py report
```
*(Get weekly brief)*

**Tuesday-Friday AM:**
```bash
python main.py scan
python main.py analyze
```
*(Quick daily check)*

**End of Month:**
```bash
python main.py gaps
```
*(Strategic planning)*

---

## 💰 What This Gets You

✅ Saves 10+ hours/week of manual competitor tracking
✅ Catch pricing changes before your sales team
✅ Weekly strategic briefs automatically
✅ Market gap analysis on demand
✅ Portfolio piece for your next interview
✅ Potential consulting revenue ($2K-$10K/month)

---

## 🆘 Emergency Reset

If everything breaks, just start over:

```bash
cd ~/Desktop
rm -rf Claude-experiments
git clone https://github.com/YOUR-USERNAME/Claude-experiments.git
cd Claude-experiments
./setup.sh
# Re-add your API key to config.json
```

---

## 📚 More Help

- **WEB_UI_GUIDE.md** - Web interface guide (easiest!)
- **START_HERE_MACBOOK.md** - Terminal walkthrough
- **QUICKSTART.md** - Usage examples
- **MONETIZATION.md** - Make money from this
- **SHOWCASE.md** - Career advancement tips

---

**Keep this page open on your phone when you're at your MacBook!**
