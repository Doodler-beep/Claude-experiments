# 🍎 START HERE - MacBook Setup (Non-Technical Guide)

**Welcome! This guide assumes you've never used Terminal or written code before. That's totally fine.**

Everything is already built and ready. You just need to:
1. Get the files on your MacBook
2. Run a few simple commands (I'll show you exactly what to type)
3. Watch the magic happen

**Total time: 15 minutes**

---

## Step 1: Open Terminal (2 minutes)

**What is Terminal?** It's just a window where you type commands instead of clicking buttons.

**How to open it:**
1. On your MacBook, press `Command + Space` (this opens Spotlight)
2. Type: `terminal`
3. Press `Enter`

A window will open with a white or black screen and a cursor. **This is Terminal.** You're doing great!

---

## Step 2: Get the Files (3 minutes)

You need to download this project to your MacBook.

**Type these commands one at a time, pressing Enter after each:**

```bash
cd Desktop
```
*(This moves you to your Desktop - you'll be able to see the folder appear!)*

```bash
git clone https://github.com/YOUR-USERNAME/Claude-experiments.git
```
*(Replace YOUR-USERNAME with your actual GitHub username)*

```bash
cd Claude-experiments
```
*(This opens the project folder)*

**You should now see a folder called "Claude-experiments" on your Desktop!**

---

## Step 3: Install Everything (5 minutes)

The project needs some software to run. I've created a script that does this automatically.

**Type this command:**

```bash
./setup.sh
```

You'll see a bunch of text scroll by. This is normal! It's downloading and installing things.

**Wait until you see:**
```
✅ Setup complete!
```

**Note:** If you see "Permission denied", type this first:
```bash
chmod +x setup.sh
```
Then try `./setup.sh` again.

---

## Step 4: Get Your Claude API Key (3 minutes)

The system uses Claude AI to analyze competitors. You need a free API key.

**Steps:**
1. Open your browser
2. Go to: **console.anthropic.com**
3. Sign in (or create a free account)
4. Click "Get API Keys" or "API Keys"
5. Click "Create Key"
6. **Copy the key** (it looks like: sk-ant-api03-...)

**Keep this window open - you'll need this key in the next step!**

---

## Step 5: Add Your API Key (2 minutes)

Now you need to add that API key to the config file.

**Option A: Use a Text Editor (Easier)**
1. On your Desktop, open the "Claude-experiments" folder
2. Double-click `config.json`
3. It will open in TextEdit or your default text editor
4. Find this line:
   ```
   "anthropic_api_key": "PLACEHOLDER-get-from-console.anthropic.com"
   ```
5. Replace `PLACEHOLDER-get-from-console.anthropic.com` with your actual API key
6. Save the file (Command + S)

**Option B: Use Terminal (If you're feeling adventurous)**
```bash
nano config.json
```
- Use arrow keys to move to the API key line
- Delete the placeholder text
- Type your actual API key
- Press `Control + X` to exit
- Press `Y` to save
- Press `Enter` to confirm

---

## Step 6: Configure Your Competitors (Optional - 2 minutes)

The system is already set up to track **Notion** and **Asana** as examples.

**Want to track different competitors?**

1. Open `config.json` again (double-click it)
2. Find the "competitors" section
3. Change the company names and URLs to whoever you want to track
4. Save the file

**Example:**
```json
"competitors": [
  {
    "name": "HubSpot",
    "urls": {
      "homepage": "https://www.hubspot.com",
      "pricing": "https://www.hubspot.com/pricing"
    },
    "priority": "high"
  }
]
```

**Keep it simple:** Just add their homepage and pricing page to start.

---

## Step 7: Run Your First Scan! (1 minute)

Back in Terminal, type:

```bash
source venv/bin/activate
python main.py scan
```

**You should see:**
```
🔍 Starting Competitive Intelligence Scan

🔍 Scanning Notion...
Fetching: https://www.notion.so
Fetching: https://www.notion.so/pricing

🔍 Scanning Asana...
Fetching: https://asana.com
Fetching: https://asana.com/pricing

✓ Scanned 4 pages across 2 competitors

============================================================
Scan Complete!
  • New pages tracked: 4
  • Changes detected: 0
============================================================
```

**🎉 Congratulations! You just ran your first competitive intelligence scan!**

---

## Step 8: See What It Found (1 minute)

The scan saved everything to a database. Now let's check the status:

```bash
python main.py status
```

You'll see a table showing:
- Which competitors you're tracking
- How many pages
- Recent activity

---

## What to Do Next

### Tomorrow: Run Another Scan

```bash
source venv/bin/activate
python main.py scan
```

If any competitor changed their website, you'll see:
```
📊 Change detected: Notion - pricing
```

### Analyze Changes with AI

When changes are detected, run:

```bash
python main.py analyze
```

This uses Claude AI to tell you:
- What changed
- Why it matters strategically
- What you should do about it
- Threat level

### Get a Weekly Report

```bash
python main.py report
```

This generates a strategic intelligence brief and saves it to the `reports/` folder on your Desktop.

You can open it in any text editor - it's written in plain English!

### Find Market Gaps

```bash
python main.py gaps
```

This analyzes all your competitors and tells you:
- What nobody is doing (market whitespace)
- Positioning opportunities
- Strategic recommendations

---

## Daily Workflow (Once You're Set Up)

Every morning, just run these two commands:

```bash
source venv/bin/activate
python main.py scan && python main.py analyze
```

**That's it!** Takes 30 seconds. You'll get alerts if anything changed.

---

## Common Issues & Fixes

### "Command not found"

**Problem:** Terminal can't find the command.

**Fix:** Make sure you're in the right folder:
```bash
cd ~/Desktop/Claude-experiments
```

### "ModuleNotFoundError"

**Problem:** Virtual environment isn't activated.

**Fix:** Run this first:
```bash
source venv/bin/activate
```
You should see `(venv)` appear before your cursor.

### "Permission denied"

**Problem:** Script isn't executable.

**Fix:**
```bash
chmod +x setup.sh
chmod +x main.py
```

### "Invalid API key"

**Problem:** Claude API key is wrong.

**Fix:**
1. Go to console.anthropic.com
2. Generate a new key
3. Update config.json with the new key

---

## Understanding the Files

**You'll see these folders/files on your Desktop:**

- `Claude-experiments/` - Main folder
  - `config.json` - Your settings (competitors, API key)
  - `main.py` - The program you run
  - `setup.sh` - Installation script
  - `data/` - Database with all the tracked changes
  - `reports/` - Intelligence reports get saved here
  - `src/` - The code (you don't need to touch this)

**Files you might edit:**
- `config.json` - To add/remove competitors or change settings

**Files you'll read:**
- `reports/intelligence_brief_YYYYMMDD.md` - Weekly reports
- `reports/market_gaps_YYYYMMDD.json` - Gap analysis
- `reports/alert_*.txt` - Critical change alerts

---

## Quick Reference: All Commands

**Activate the environment (do this first every time):**
```bash
source venv/bin/activate
```

**Scan competitors:**
```bash
python main.py scan
```

**Analyze changes:**
```bash
python main.py analyze
```

**Generate weekly report:**
```bash
python main.py report
```

**Find market gaps:**
```bash
python main.py gaps
```

**Check status:**
```bash
python main.py status
```

---

## Making This Automatic (Advanced - Optional)

Want it to run automatically every morning?

**Steps:**
1. Open Terminal
2. Type: `crontab -e`
3. Press `i` to enter insert mode
4. Paste this (change the path to match your username):
```
0 6 * * * cd /Users/YOUR-USERNAME/Desktop/Claude-experiments && source venv/bin/activate && python main.py scan >> scan.log 2>&1
```
5. Press `Esc`
6. Type: `:wq` and press Enter

Now it runs every morning at 6 AM automatically!

---

## Getting Help

**If something breaks:**

1. Take a screenshot of the error
2. Check the error message - it usually tells you what's wrong
3. Try the "Common Issues" section above
4. Google the error message (seriously, this works!)

**Remember:** You can't break anything! Worst case, just delete the folder and start over.

---

## What You've Built

You now have a competitive intelligence system that:

✅ Monitors competitors automatically
✅ Detects changes as they happen
✅ Uses AI to analyze strategic implications
✅ Generates weekly intelligence reports
✅ Identifies market opportunities

**You now have a professional competitive intelligence system.**

---

## Next Steps

1. **Run it daily for a week** - See what changes get detected
2. **Read the reports** - The AI analysis is surprisingly good
3. **Share insights** - Post on LinkedIn about what you built
4. **Customize it** - Add more competitors, track specific pages
5. **Monetize it** - See MONETIZATION.md for ideas

**You've got this!** 🚀

---

**Questions?** All the docs are in the project folder:
- `QUICKSTART.md` - More detailed usage guide
- `MONETIZATION.md` - How to make money from this
- `WEB_UI_GUIDE.md` - Using the web interface

**Pro tip:** Bookmark this guide. You'll reference it until the commands become muscle memory.
