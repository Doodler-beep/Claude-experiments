# 🚀 Quick Start Guide

Get your competitive intelligence system running in 10 minutes.

## Installation

```bash
# 1. Clone/download this repository
cd Claude-experiments

# 2. Run setup script
./setup.sh

# 3. Activate virtual environment
source venv/bin/activate
```

## Configuration

Edit `config.json` with your details:

```json
{
  "api_keys": {
    "anthropic_api_key": "sk-ant-..."  // Get from console.anthropic.com
  },
  "competitors": [
    {
      "name": "Notion",
      "urls": {
        "homepage": "https://notion.so",
        "pricing": "https://notion.so/pricing",
        "features": "https://notion.so/product"
      },
      "priority": "high"
    },
    {
      "name": "Coda",
      "urls": {
        "homepage": "https://coda.io",
        "pricing": "https://coda.io/pricing"
      },
      "priority": "medium"
    }
  ],
  "analysis": {
    "focus_areas": [
      "pricing changes",
      "feature additions",
      "messaging shifts"
    ],
    "your_product": {
      "name": "Your Product Name",
      "category": "Productivity Software",
      "key_differentiators": [
        "AI-powered automation",
        "Real-time collaboration"
      ]
    }
  }
}
```

## First Run

```bash
# Scan competitors for the first time
python main.py scan

# Output:
# 🔍 Starting Competitive Intelligence Scan
# Fetching: https://notion.so
# Fetching: https://notion.so/pricing
# ...
# ✓ Scanned 4 pages across 2 competitors
```

## Daily Workflow

### Morning Routine (2 minutes)

```bash
# Check for overnight changes
python main.py scan

# Analyze any changes with AI
python main.py analyze

# If critical changes detected, you'll see:
# 🚨 COMPETITIVE ALERT - CRITICAL
# Competitor: Notion
# Change: Major Content Change
# ...
```

### Weekly Routine (5 minutes)

```bash
# Generate weekly intelligence brief
python main.py report

# Output saved to: reports/intelligence_brief_20260121.md
```

### Monthly Strategic Review (15 minutes)

```bash
# Identify market gaps and opportunities
python main.py gaps

# Review output for:
# - Market whitespace nobody is addressing
# - Positioning opportunities
# - Strategic recommendations
```

## Understanding the Output

### 1. Scan Results

**No changes detected:**
```
No change: Notion - pricing
No change: Coda - homepage
```
This is good! Means market is stable.

**Changes detected:**
```
📊 Change detected: Notion - pricing
```
This triggers AI analysis automatically.

### 2. AI Analysis Alerts

**Example Critical Alert:**
```
🚨 COMPETITIVE ALERT - CRITICAL

Competitor: Notion
Change: Major Content Change
Page: pricing

Notion has restructured their entire pricing model,
introducing a new "AI tier" at $20/user/month.

Strategic Impact: Direct threat to your AI features.
They're commoditizing what you charge premium for.

Recommended Actions:
- Review your AI feature pricing within 48 hours
- Prepare messaging on AI differentiation
- Consider bundling strategy

Threat Level: HIGH
```

**Example Medium Alert:**
```
📊 COMPETITIVE ALERT - MEDIUM

Competitor: Coda
Change: Content Update
Page: features

Coda added 3 new integration partners to their features page.

Strategic Impact: Expanding their ecosystem play.

Opportunities:
- Partner with integrations they don't have
- Highlight your native integrations vs. third-party

Recommended Actions:
- Audit your integration coverage vs. Coda
- Update battle cards with integration comparison
```

### 3. Weekly Brief

Saved to `reports/intelligence_brief_YYYYMMDD.md`:

```markdown
# Competitive Intelligence Brief
**Generated:** January 21, 2026
**Period:** Last 7 days
**Changes Tracked:** 3

## Executive Summary
Three significant movements this week. Notion launched AI pricing tier,
positioning aggressively at $20/user. Coda expanded integrations.
Overall market trend: Consolidation around AI features.

## Critical Developments
1. **Notion AI Pricing** - New tier challenges our positioning...

## Strategic Opportunities
- Pricing gap at $15/user level (Notion jumped from $10 to $20)
- Integration whitespace: Figma, Linear, Jira
- Messaging opportunity: "AI included, not upsold"

## Recommended Actions
1. [HIGH] Review AI pricing strategy by EOW
2. [MEDIUM] Create Notion AI comparison page
3. [LOW] Update competitor battle cards
...
```

### 4. Market Gaps Analysis

```json
{
  "whitespace_opportunities": [
    {
      "opportunity": "Small team pricing (2-5 users)",
      "rationale": "All competitors jump from $10 individual to $20/user team plan. $50-75 total price point is unserved.",
      "priority": "high"
    }
  ],
  "positioning_angles": [
    {
      "angle": "AI-native vs. AI-bolted-on",
      "differentiation": "Competitors added AI as separate tier. You can position as AI-first."
    }
  ],
  "strategic_recommendations": [
    "Launch $15/user tier targeting 2-5 person teams",
    "Position as 'AI included by default' vs. upsell"
  ]
}
```

## Real-World Example Scenarios

### Scenario 1: Competitor Raises Prices

**What happens:**
1. Morning scan detects change on pricing page
2. AI analyzes: "20% price increase across all tiers"
3. Alert generated with recommendations
4. You have the insight before your sales team loses a deal

**What you do:**
- Update sales battle cards same day
- Create comparison page showing your value
- Email customers who were evaluating both solutions

**Value:** Win deals you'd otherwise lose. One $50K deal = instant ROI.

---

### Scenario 2: Competitor Removes a Feature

**What happens:**
1. Scan detects major content change on features page
2. AI notices "Removed: Advanced analytics from Pro tier"
3. Market gap analysis shows opportunity

**What you do:**
- Highlight analytics in next campaign
- Create "Why we include analytics" content
- Reach out to their customers who used that feature

**Value:** Identify product differentiation opportunities automatically.

---

### Scenario 3: New Competitor Enters Market

**What happens:**
1. You add them to config.json
2. First scan captures baseline
3. Weekly monitoring tracks their positioning evolution

**What you do:**
- Track their messaging maturation
- Identify how they differentiate
- Find gaps in their offering

**Value:** Stay ahead of emerging threats.

---

## Automation Setup

### Run Daily Scans Automatically

**Using cron (Linux/Mac):**

```bash
# Edit crontab
crontab -e

# Add this line (runs at 6 AM daily):
0 6 * * * cd /path/to/Claude-experiments && source venv/bin/activate && python main.py scan >> logs/scan.log 2>&1

# Add this line (runs analysis at 6:15 AM):
15 6 * * * cd /path/to/Claude-experiments && source venv/bin/activate && python main.py analyze >> logs/analysis.log 2>&1
```

**Weekly report (Mondays at 9 AM):**
```bash
0 9 * * 1 cd /path/to/Claude-experiments && source venv/bin/activate && python main.py report >> logs/report.log 2>&1
```

Now you wake up to fresh competitive intelligence every morning!

---

## Tips for Maximum Value

### 1. Start Small, Scale Up
- Begin with 2-3 top competitors
- Add more as you see value
- Focus on pages that change frequently (pricing, features, blog)

### 2. Customize Focus Areas
Update `focus_areas` in config.json based on what matters:
```json
"focus_areas": [
  "pricing changes",
  "new product launches",
  "partnership announcements",
  "executive messaging",
  "hiring patterns"  // Add careers page to track expansion
]
```

### 3. Track More Than Homepage
Useful pages to monitor:
- `/pricing` - pricing changes
- `/features` - feature announcements
- `/customers` - case studies (new logos)
- `/about` - team expansion
- `/blog` - thought leadership
- `/careers` - hiring (signals growth areas)

### 4. Use for Sales Enablement
- Share weekly briefs with sales team
- Generate battle cards: "As of [date], Competitor X..."
- Create "vs. Competitor" pages with latest info

### 5. Use for Product Strategy
- Track feature removals (validation of what NOT to build)
- Spot trends across competitors (signals market direction)
- Find underserved segments

---

## Common Issues

**"Module not found" error:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate
```

**"No changes detected" every time:**
- Check if URLs are accessible
- Some sites block scrapers - try different pages
- Verify competitors are in config.json

**API rate limits:**
- Claude API has generous limits
- If hitting limits, reduce analysis frequency
- Focus analysis on high-priority changes only

**403/blocked by website:**
- Some sites block scrapers aggressively
- Try monitoring their blog/changelog instead
- Or use playwright for JavaScript-heavy sites

---

## Next Steps

1. ✅ Run your first scan
2. ✅ Generate your first report
3. ✅ Set up daily automation
4. 📖 Read [MONETIZATION.md](MONETIZATION.md) to turn this into revenue
5. 🚀 Share insights with your team
6. 💡 Customize reports for your specific needs

---

## Support

Found a bug? Have an idea?
- Check existing issues
- Create new issue with details
- Contribute improvements via PR

**This is your competitive intelligence system. Make it yours!**
