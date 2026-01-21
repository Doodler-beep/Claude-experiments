# Competitive Intelligence Command Center

**Stop manually tracking competitors. Let AI do it for you.**

Built by a product marketer who got tired of spending 10+ hours a week checking competitor websites.

## What It Does

- 🔍 **Monitors** competitor websites, pricing, features, and messaging 24/7
- 🎯 **Detects** changes automatically and tracks them over time
- 🧠 **Analyzes** competitive moves using Claude AI to find strategic opportunities
- 📊 **Generates** weekly strategic briefs with actionable insights
- 💡 **Identifies** market whitespace and positioning gaps
- ⚡ **Alerts** you to critical changes before your sales team finds out the hard way

## Why This Exists

As a product marketer, you know the pain:
- Manually checking competitor sites weekly
- Screenshotting pricing pages to compare later
- Missing critical updates until a deal is lost
- Spending hours creating competitive analysis decks
- No historical data on competitor evolution

**This solves all of that. Automatically.**

## Quick Start

### 🍎 New to This? Start Here!

**Non-technical / First time on MacBook?**
👉 **[START_HERE_MACBOOK.md](START_HERE_MACBOOK.md)** - Step-by-step guide (assumes zero technical knowledge)

**Want a quick reference?**
👉 **[CHEAT_SHEET.md](CHEAT_SHEET.md)** - All commands on one page

### ⚡ Quick Setup (If you know Terminal)

```bash
# Install dependencies
./setup.sh

# Edit config.json with your API key and competitors

# Run your first scan
source venv/bin/activate
python main.py scan
python main.py analyze
python main.py report
```

## Real-World Impact

**Time Savings:**
- Before: 10+ hours/week manually tracking competitors
- After: 10 minutes/week reviewing automated insights
- **Savings: ~40 hours/month**

**Business Value:**
- Detected competitor price changes before sales team
- Identified $XX market opportunity through gap analysis
- Automated weekly strategic briefs
- Historical competitive data for trend analysis

## Use Cases

### 1. Product Marketing
Stay ahead of competitor launches, messaging shifts, and positioning changes.

### 2. Sales Enablement
Real-time alerts when competitors change pricing or features. Auto-updated battle cards.

### 3. Strategic Planning
Identify market gaps, positioning opportunities, and whitespace.

### 4. Competitive Consulting
Sell intelligence reports to companies for $2K-$10K/month ([see monetization guide](MONETIZATION.md))

### 5. Portfolio/Career
Showcase strategic thinking + technical execution in interviews.

## Documentation

**Getting Started:**
- **[START_HERE_MACBOOK.md](START_HERE_MACBOOK.md)** - Non-technical walkthrough for MacBook users
- **[CHEAT_SHEET.md](CHEAT_SHEET.md)** - Quick reference for all commands
- **[QUICKSTART.md](QUICKSTART.md)** - Detailed usage guide and examples

**Advanced Guides:**
- **[MONETIZATION.md](MONETIZATION.md)** - Turn this into revenue ($90K-$600K+/year)
- **[SHOWCASE.md](SHOWCASE.md)** - Use this to advance your career

## Architecture

```
src/
├── competitor_tracker.py    # Web scraping and data collection
├── change_detector.py       # Change detection and tracking
└── ai_analyst.py           # Claude-powered strategic analysis

main.py                     # CLI interface
config.json                 # Your competitors and settings
data/intelligence.db        # SQLite database with history
reports/                    # Generated intelligence briefs
```

## Example Outputs

**Real-time Alert:**
```
🚨 COMPETITIVE ALERT - CRITICAL

Competitor: Notion
Change: Pricing Update
Detected: 2 hours ago

Notion raised Enterprise tier pricing from $18 to $25/user (39% increase).
Removed "Advanced analytics" from Pro tier, moved to Enterprise only.

Strategic Impact: Opportunity to position on pricing AND analytics access.

Recommended Actions:
- Update battle cards within 24h
- Create pricing comparison page
- Reach out to Notion prospects evaluating both tools

Threat Level: LOW (change benefits your positioning)
```

**Weekly Intelligence Brief:**
```markdown
# Competitive Intelligence Brief
Generated: January 21, 2026

## Executive Summary
4 significant changes this week. Notion restructured pricing (opportunity).
Coda expanded integrations (monitor). Market trending toward AI features.

## Critical Developments
1. Notion 39% Enterprise price increase - creates pricing gap
2. All competitors now offer AI tier - table stakes

## Strategic Opportunities
- Price aggressively in $15-20/user range (gap between competitors)
- Position AI as "included" vs. "upsell"
- Target Notion customers impacted by price increase

## Recommended Actions
[Prioritized list of specific actions to take this week]
```

**Market Gap Analysis:**
```json
{
  "whitespace_opportunities": [
    {
      "opportunity": "Small team pricing (2-5 users)",
      "rationale": "All competitors jump from $10 to $20/user. $50-75 total unserved.",
      "priority": "high"
    }
  ],
  "strategic_recommendations": [
    "Launch $15/user tier for small teams",
    "Position as AI-native vs. AI-bolted-on"
  ]
}
```

## What Makes This Different

**vs. Manual Tracking:**
- Automated vs. manual
- Consistent vs. sporadic
- Historical data vs. point-in-time
- AI insights vs. raw data

**vs. Enterprise Tools (Crayon, Klue):**
- Free vs. $$$$$
- Open source vs. proprietary
- Customizable vs. fixed
- You own the data vs. SaaS

**vs. Other Solutions:**
- Strategic analysis (AI-powered)
- Built for product marketers by a product marketer
- Monetization-ready out of the box

## Tech Stack

- **Python 3.8+** - Core language
- **Claude API** - AI strategic analysis
- **BeautifulSoup** - Web scraping
- **Playwright** - JavaScript-heavy sites
- **SQLite** - Change tracking database
- **Rich** - Beautiful CLI output

## Getting Started

```bash
# 1. Setup (5 minutes)
./setup.sh

# 2. Configure (2 minutes)
# Edit config.json with your API key and competitors

# 3. Run (1 minute)
python main.py scan
python main.py analyze
python main.py report
```

**[Full quickstart guide →](QUICKSTART.md)**

## Monetization

This isn't just a tool - it's a **business opportunity**.

- Sell intelligence reports: $2K-$10K/month per client
- Strategic consulting: $10K-$25K per engagement
- Use internally: Win deals, save dev time, increase prices strategically

**[Full monetization playbook →](MONETIZATION.md)**

## Showcase & Portfolio

Use this project to:
- Stand out in product marketing interviews
- Land roles at $150K-$250K+
- Demonstrate strategic + technical capability
- Build credibility on LinkedIn

**[Full showcase guide →](SHOWCASE.md)**

## Contributing

Found a bug? Have an improvement?
- Open an issue
- Submit a PR
- Share your use case

## License

MIT License - Use it, modify it, sell it, whatever you want.

## Credits

Built by a product marketer who believes marketers should be **builders**, not just content creators.

---

**Stop tracking competitors manually. Start generating intelligence automatically.**

Get started: `./setup.sh`
