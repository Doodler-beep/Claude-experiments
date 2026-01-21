# 🌐 Web UI Guide - No Terminal Needed!

**NEW: Easy point-and-click interface for managing your competitive intelligence.**

## What is the Web UI?

The Web UI is a simple browser-based interface that lets you:
- ✅ Set up your API key (one-time setup)
- ✅ Automatically discover competitors (just enter your URL!)
- ✅ Add/remove competitors with clicks (no editing files)
- ✅ View reports in your browser
- ✅ Check system status

**No command line needed** (except for the initial setup and running scans).

---

## Setup (5 Minutes)

### Step 1: One-Time Installation

Open Terminal and run:

```bash
cd Desktop/Claude-experiments
./setup.sh
```

That's it! Everything is installed.

### Step 2: Start the Web UI

```bash
source venv/bin/activate
python main.py web
```

You'll see:
```
╔════════════════════════════════════════════════════════════╗
║  Competitive Intelligence Command Center - Web UI         ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  🌐 Open your browser and go to:                          ║
║                                                            ║
║     http://localhost:5000                                 ║
║                                                            ║
║  Press Ctrl+C to stop the server                          ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

### Step 3: Open Your Browser

Go to: **http://localhost:5000**

You'll see the web interface!

---

## Using the Web UI

### First Time Setup (In Browser)

#### 1. Enter Your API Key

On first visit, click "Get Started":

- **Get API Key:** Go to console.anthropic.com
- **Sign in/Create Account** (free)
- **Create Key** and copy it
- **Paste** into the web form
- Click "Save & Continue"

#### 2. Discover Competitors Automatically 🔍

Now the magic happens:

1. Enter your company URL: `https://yourcompany.com`
2. Choose how many competitors to find (10 recommended)
3. Click "Discover Competitors"

**The AI will:**
- Analyze your website
- Understand your industry
- Find 10 direct competitors
- Show you a list to review

#### 3. Review & Select

You'll see a list like:

```
☑ Notion (High Priority)
   Why: Direct competitor in productivity software
   Monitoring: 2 pages

☑ Asana (High Priority)
   Why: Project management platform serving same market
   Monitoring: 2 pages

☐ Monday.com (Medium Priority)
   Why: Similar features, different positioning
   Monitoring: 2 pages
```

- **Check** the ones you want to track
- **Uncheck** any you don't want
- Click "Save & Start Tracking"

Done! Your competitors are now configured.

---

## Managing Competitors

### View All Competitors

Click "📊 Manage Competitors" in the menu

You'll see:
- All tracked competitors
- How many pages monitored
- Priority level
- Remove button

### Add Manually

Scroll down to "Add Competitor Manually":

1. Enter competitor name
2. Enter homepage URL
3. (Optional) Enter pricing URL
4. Choose priority
5. Click "Add Competitor"

### Remove a Competitor

Just click the "Remove" button next to any competitor.

---

## Running Scans (Still Uses Terminal)

**Important:** The web UI is for setup and viewing. To actually scan competitors, you still use Terminal.

### Daily Workflow:

**1. Open Terminal**

**2. Run:**
```bash
cd Desktop/Claude-experiments
source venv/bin/activate
python main.py scan
python main.py analyze
```

**3. View Results in Web UI**

Go back to browser (http://localhost:5000) and click "📄 Reports"

---

## Viewing Reports

Click "📄 Reports" in the web menu.

You'll see:
- `intelligence_brief_YYYYMMDD.md` - Weekly summaries
- `market_gaps_YYYYMMDD.json` - Opportunity analysis
- `alert_*.txt` - Critical change alerts

Click any report to read it in your browser!

---

## System Status

Click "⚙️ Status" to see:
- ✅ API Configured
- Number of competitors tracked
- Recent changes (last 7 days)
- Pending analysis
- Terminal commands reference

---

## Complete Workflow (Web UI + Terminal)

### Setup (One Time)
1. Run `./setup.sh` in Terminal
2. Open Web UI: `python main.py web`
3. Enter API key in browser
4. Discover competitors in browser
5. Review and save

### Daily Use
1. **Terminal:** Run scans
   ```bash
   source venv/bin/activate
   python main.py scan && python main.py analyze
   ```

2. **Browser:** View results
   - Go to http://localhost:5000
   - Click "Reports"
   - Read the latest intelligence brief

### Weekly
1. **Terminal:** Generate report
   ```bash
   python main.py report
   ```

2. **Browser:** Read the report
   - Go to "Reports"
   - Click the latest brief
   - Review strategic recommendations

### Monthly
1. **Terminal:** Find market gaps
   ```bash
   python main.py gaps
   ```

2. **Browser:** Review opportunities
   - Go to "Reports"
   - Click the market_gaps file
   - Plan your strategy

---

## Tips & Tricks

### Keep Web UI Running

Leave Terminal window open with Web UI running. Open a **second Terminal window** for scan commands.

**Terminal 1 (keep open):**
```bash
python main.py web
```

**Terminal 2 (run scans):**
```bash
source venv/bin/activate
python main.py scan
```

### Bookmark It

Bookmark `http://localhost:5000` in your browser!

### Mobile Access

Want to check reports from your phone while on the couch?

When starting web UI, use:
```bash
python -c "from src.web_ui import run_ui; run_ui(host='0.0.0.0')"
```

Then access from your phone at: `http://YOUR-MACBOOK-IP:5000`

---

## Stopping the Web UI

In the Terminal window where it's running, press: **Ctrl + C**

---

## Troubleshooting

**"Address already in use"**
- Another program is using port 5000
- Solution: Stop the other program, or use a different port:
  ```bash
  python -c "from src.web_ui import run_ui; run_ui(port=5001)"
  ```
  Then go to `http://localhost:5001`

**"Config file not found"**
- Run setup first: `./setup.sh`

**Web UI won't open**
- Make sure you activated venv: `source venv/bin/activate`
- Check you're in the right folder: `cd Desktop/Claude-experiments`

---

## Why Use Web UI vs. Terminal Only?

### Web UI is Better For:
✅ Initial setup (API key, competitors)
✅ Viewing reports (prettier, easier to read)
✅ Managing competitors (point-and-click)
✅ Checking status at a glance
✅ Non-technical users

### Terminal is Better For:
✅ Running scans (faster)
✅ Automation (cron jobs)
✅ Advanced features
✅ Scripting

**Best approach: Use both!**
- Web UI for setup and viewing
- Terminal for scanning and analysis

---

## Next Steps

1. ✅ Start Web UI: `python main.py web`
2. ✅ Configure everything in browser
3. ✅ Use Terminal for daily scans
4. ✅ Check results in browser

**You've got the best of both worlds!** 🎉

---

**Questions?** Check the other guides:
- **START_HERE_MACBOOK.md** - Terminal-first approach
- **CHEAT_SHEET.md** - Quick command reference
- **QUICKSTART.md** - Detailed usage guide
