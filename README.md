# Competitive Intelligence Command Center

**AI-powered competitive intelligence automation for teams and businesses.**

Built by a product marketer (not a software engineer) using Claude Code as a pair programmer. The idea started late on a Friday night, the core system was built over a weekend, refined during the week in pockets of spare time, and is now being showcased the following weekend. [Read the full building story](BUILDING_STORY.md) or [view the interactive showcase](templates/showcase.html).

An open-source tool that monitors competitors 24/7, detects changes automatically, and generates strategic insights using Claude AI.

## What It Does

- 🔍 **Monitors** competitor websites, pricing, features, and messaging automatically
- 🎯 **Detects** changes in real-time and tracks them over time
- 🧠 **Analyzes** competitive moves using Claude AI to identify strategic opportunities
- 📊 **Generates** weekly intelligence briefs with actionable insights
- 💡 **Identifies** market gaps and positioning opportunities
- ⚡ **Alerts** teams to critical changes before they impact deals

## Why This Exists

Competitive intelligence is critical but time-consuming. Most teams either:
- Manually check competitor sites sporadically
- Miss important updates until it's too late
- Lack historical data for trend analysis
- Spend hours creating competitive analysis reports

This tool automates the entire competitive intelligence workflow, from data collection to strategic analysis.

## ✨ Features

### 🌐 Web UI
Point-and-click interface for easy management. No coding required.

```bash
python src/web_ui.py
# Opens at http://localhost:8000
```

- Set up API keys through web forms
- Add/remove competitors with clicks
- View reports in your browser
- Check system status and metrics

### 🔍 Automatic Competitor Discovery
AI-powered competitor discovery - just enter your company URL.

```bash
python main.py discover https://yourcompany.com
# Or use the Web UI for better experience
```

The system analyzes your website and automatically finds relevant competitors in your market.

### 📊 Intelligent Analysis
Claude AI generates strategic insights from raw data:
- Impact assessment of competitor changes
- Market gap identification
- Positioning recommendations
- Prioritized action items

---

## Quick Start

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Doodler-beep/Claude-experiments.git
cd Claude-experiments

# 2. Run setup script
./setup.sh

# 3. Activate virtual environment
source venv/bin/activate

# 4. Start the web interface
python src/web_ui.py
```

### Configuration

1. Get a Claude API key from [console.anthropic.com](https://console.anthropic.com)
2. Open http://localhost:8000 in your browser
3. Enter your API key in the setup page
4. Use auto-discovery or manually add competitors

### First Scan

```bash
# Run your first competitive scan
python main.py scan

# Analyze detected changes
python main.py analyze

# Generate intelligence report
python main.py report
```

## Use Cases

### Product & Marketing Teams
- Stay ahead of competitor launches and messaging shifts
- Track feature releases and positioning changes
- Identify market gaps and opportunities

### Sales Enablement
- Real-time alerts on competitor pricing changes
- Auto-updated competitive battle cards
- Strategic context for competitive deals

### Strategic Planning
- Historical competitive data for trend analysis
- Market gap identification
- Positioning opportunity discovery

### Consulting & Services
- Deliver competitive intelligence reports to clients
- Strategic consulting backed by data
- Market analysis for portfolio companies

## Architecture

```
src/
├── web_ui.py               # Flask web interface
├── competitor_discovery.py # AI-powered competitor finding
├── competitor_tracker.py   # Web scraping and data collection
├── change_detector.py      # Change detection and tracking
└── ai_analyst.py          # Claude-powered strategic analysis

main.py                    # CLI interface
config.json               # Competitors and settings
data/intelligence.db      # SQLite change tracking database
reports/                  # Generated intelligence briefs
templates/                # Web UI templates
```

## Example Outputs

### Real-time Alert
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
- Target Notion prospects evaluating alternatives

Threat Level: LOW (change benefits your positioning)
```

### Weekly Intelligence Brief
```markdown
# Competitive Intelligence Brief
Generated: January 24, 2026

## Executive Summary
4 significant changes detected this week. Notion restructured pricing
(opportunity). Coda expanded integrations (monitor). Market trending
toward AI-first features.

## Critical Developments
1. Notion 39% Enterprise price increase - creates pricing gap
2. Industry-wide shift to AI-powered features as standard

## Strategic Opportunities
- Price competitively in $15-20/user range (gap in market)
- Position AI features as "included" vs competitor "add-on" model
- Target Notion customers affected by price increase

## Recommended Actions
[Prioritized list of specific actions]
```

## Tech Stack

- **Python 3.8+** - Core language
- **Claude API** - AI-powered strategic analysis
- **Flask** - Web interface
- **BeautifulSoup** - Web scraping
- **SQLite** - Change tracking database
- **Playwright** - JavaScript-heavy sites

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Detailed usage guide
- **[WEB_UI_GUIDE.md](WEB_UI_GUIDE.md)** - Web interface walkthrough
- **[CHEAT_SHEET.md](CHEAT_SHEET.md)** - Quick command reference

## What Makes This Different

**vs. Manual Tracking:**
- Automated vs. manual spot-checks
- Consistent vs. sporadic monitoring
- Historical data vs. point-in-time snapshots
- AI insights vs. raw data collection

**vs. Enterprise Tools (Crayon, Klue, etc.):**
- Open source vs. proprietary
- Free vs. $$$$$
- Customizable vs. fixed features
- Self-hosted - you own your data

**vs. Simple Web Scrapers:**
- Strategic analysis, not just change detection
- AI-powered insights and recommendations
- Built-in intelligence reporting
- Automatic competitor discovery

## Business Applications

### Internal Use
- Launch better products (know what NOT to build)
- Win competitive deals (real-time intelligence)
- Price strategically (see moves before customers do)
- Identify market gaps and opportunities

### Service Business
- Deliver competitive intelligence reports to clients
- Strategic consulting backed by automated data
- Market analysis for agencies or investors
- Ongoing intelligence subscription service

## Contributing

Contributions welcome! Areas for improvement:
- Additional data sources
- More analysis capabilities
- Enhanced reporting formats
- Integration with other tools

Open an issue or submit a PR.

## License

MIT License - Free to use, modify, and distribute.

## The Story Behind This

I'm a product marketer. I don't write code professionally. But I understand competitive intelligence deeply — the hours spent manually checking competitor sites, the screenshots that go stale, the reports that take longer to write than they stay relevant.

The idea started on a Friday night scrolling LinkedIn. The core system was built over a weekend with Claude Code. The week after, I refined it in pockets of spare time — fixing edge cases, improving error handling, polishing the UX. Now I'm showcasing the builder thinking behind it.

- **[Building Story](BUILDING_STORY.md)** — The messy, real story: 12+ syntax errors, 3 file corruptions, 7 failed JSON fixes, and the persistence to ship anyway
- **[Interactive Showcase](templates/showcase.html)** — A visual board walking through problem, product thinking, system design, what broke, and what I learned

**Domain expertise + AI assistance = powerful combination.** You don't need to be a software engineer to build something useful.

## Credits

Built by [Abhishek](https://github.com/Doodler-beep) — a product marketer who wanted a system that thinks before the market shifts, not after. Open sourced because competitive intelligence shouldn't cost $50K/year.

---

**Stop tracking competitors manually. Start generating intelligence automatically.**

Get started: `./setup.sh`
