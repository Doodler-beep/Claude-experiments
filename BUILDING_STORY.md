# How I Built a Competitive Intelligence Command Center Over a Weekend with Claude Code

**The messy, real story of building a production system with AI assistance**

---

## Friday, 11:30 PM – The Idea Strikes

### A Lesson from Ryanair

Years ago, while working on a Harvard MBA case study about Ryanair with professors from UCLA, something clicked. Ryanair—the ultra-low-cost airline that became Europe's largest carrier with a market cap of ₹2.833 trillion in 2025—didn't just execute a plan. They executed a **strategy**.

The difference? A plan is internal. A strategy is about playing to win by understanding your market and your competition.

This case study taught me that competitive intelligence isn't optional—it's the foundation of strategy.

### Friday, 11:47 PM – The Product Marketer's Problem

I'm lying in bed, scrolling through LinkedIn on my phone, and I see yet another post about competitive intelligence tools. Product marketers spend an enormous amount of time on this:

- **Several hours per week per competitor** during normal operations
- **Up to 30% of their time** during product launches
- **Constant monitoring** to avoid being blindsided

Modern AI tools like Perplexity have helped, but you're still doing heavy lifting—manually checking sites, taking screenshots, comparing changes, trying to spot patterns.

I wanted something **a level above**. Not just faster research, but **automated strategic intelligence**.

So I opened Claude Code on my phone and started asking questions.

---

## Friday, 11:58 PM – First Attempt (On My Phone)

I'm not technical. I'm a product marketer. But I figured, "Claude Code can help me build this, right?"

**Me:** "Can we build a system that monitors competitor websites automatically?"

**Claude:** "Absolutely. We'll need web scraping, change detection, and AI analysis..."

Wait, what? Web scraping? I just wanted to track some competitors.

**Me:** "Let's start simple. Just... tell me what changed on a website."

And we started building. On my phone. At midnight.

Spoiler: This was a terrible idea.

---

## Saturday, 9:15 AM – Moving to My MacBook

After getting nowhere on my phone (typing Python code on mobile is... not recommended), I decided to pick this up properly on my MacBook.

**Me:** "I'm a non-technical person. Can you walk me through this?"

Claude Code created a complete setup guide. I followed it step by step:

```bash
./setup.sh  # This actually worked!
```

Installed dependencies, set up a virtual environment, got everything running.

Then I tried to start the system...

---

## Saturday, 10:23 AM – First Real Error

```
SyntaxError: invalid syntax
  File "src/web_ui.py", line 101
    flash('API key saved! Now let\'s discover your competitors.', 'success')
                                  ^
```

**Me:** "What does this mean?"

**Claude:** "There's an escaping issue with the apostrophe. Let me fix it."

We fixed it. Restarted. New error. Fixed that. New error.

This pattern would repeat **many, many times**.

---

## Saturday, 12:47 PM – Port 5000 Doesn't Work

Got the web interface running! Opened `localhost:5000` and... nothing.

**Me:** "The browser just hangs."

Ran `lsof -i :5000` and discovered Mac's ControlCenter was blocking port 5000.

**Claude:** "Let's change to port 8000."

We updated the code. Restarted. **Finally!** The web UI loaded.

---

## Saturday, 2:18 PM – The Auto-Discovery Disaster

I entered OpenAI's URL to test competitor discovery. The AI found 10 competitors perfectly:

```
✓ Found 10 potential competitors
  [1/10] Anthropic
  [2/10] Google DeepMind
  [3/10] Microsoft (Azure AI)
  ...
```

I selected 5 competitors and clicked "Save."

```
Error: json.decoder.JSONDecodeError:
Expecting property name enclosed in double quotes: line 1 column 3 (char 2)
```

**Me:** "What?! It just found them!"

Tried again. Same error. Again. Same error.

**Me (getting frustrated):** "Why isn't this working?"

---

## Saturday, 3:45 PM – Debugging Hell

We tried fixing the JSON parsing issue **seven different times**:

1. **Attempt 1:** Unescape HTML entities → didn't work
2. **Attempt 2:** Different form encoding → didn't work
3. **Attempt 3:** Flask session storage → didn't work
4. **Attempt 4:** Base64 encoding → didn't work
5. **Attempt 5:** Changed form method → didn't work
6. **Attempt 6:** Temporary file storage → **WORKED!**

The problem? You can't pass complex JSON through HTML form fields. It gets mangled.

The solution? Save discovery results to a temp file, then load them on the backend.

**Simple. Obvious in hindsight. Took 2 hours to figure out.**

---

## Saturday, 5:32 PM – File Corruption Crisis

I tried to download an updated file from the repository using `curl`:

```bash
curl -o src/web_ui.py https://raw.githubusercontent.com/.../web_ui.py
```

The file downloaded. I restarted the server.

```
  File "src/web_ui.py", line 1
    404: Not Found
    ^
SyntaxError: illegal target for annotation
```

**The entire file was replaced with a 404 error page.**

I had to restore it manually. Three times. Because I kept making the same mistake.

**Lesson learned:** Don't use `curl` to download files from GitHub when you're tired.

---

## Saturday, 7:45 PM – "Getting Tired of This"

After the fifth syntax error, third file corruption, and second complete restart, I messaged Claude:

**Me:** "Getting tired of this. Analyze the whole thing and debug it completely please."

Claude did a full system analysis, found multiple issues:

1. Escaping problems in flash messages
2. Port configuration inconsistencies
3. JSON parsing in wrong place
4. Missing error handling

We fixed them systematically. One by one.

**It took another hour.**

---

## Saturday, 9:17 PM – Victory (Finally)

I tested the full workflow:

1. **Entered:** `https://slack.com`
2. **AI discovered:** Microsoft Teams, Zoom, Google Chat, Discord...
3. **Selected:** 3 competitors
4. **Clicked:** "Save"
5. **Result:** ✅ Successfully added 3 competitors!

**IT WORKED!**

Then I ran the first scan:

```bash
python main.py scan

🔍 Scanning Microsoft Teams...
✓ Scanned 2 pages

🔍 Scanning Zoom Team Chat...
✓ Scanned 2 pages

🔍 Scanning Google Chat...
✓ Scanned 2 pages

============================================================
Scan Complete!
  • New pages tracked: 6
  • Changes detected: 0 (baseline established)
============================================================
```

**Success.** After 10+ hours of debugging, file corruption, syntax errors, and frustration.

---

## Sunday, 10:34 AM – Testing with Real Data

I woke up and ran another scan. The system detected that Google Chat had updated their pricing page.

The AI analysis was **surprisingly good**:

```
Strategic Impact: Google is positioning Chat as enterprise-focused.
Opportunity: Target small teams with simpler pricing.
Threat Level: LOW (change doesn't impact your positioning)

Recommended Actions:
- Monitor for feature additions in next 2 weeks
- Create comparison page highlighting simplicity
```

**This was the moment I realized:** I didn't just build a tool. I built something **useful**.

---

## Sunday, 2:47 PM – The Cleanup

I spent the afternoon:

- Fixing the last syntax errors
- Updating documentation
- Testing edge cases
- Making it ready for public release

The final system:

**For Users:**
- ✅ Point-and-click web interface (no coding required)
- ✅ Automatic competitor discovery (AI-powered)
- ✅ One-click setup (just enter API key)
- ✅ Real-time change detection
- ✅ AI-generated strategic insights
- ✅ Weekly intelligence briefs

**For Developers:**
- ✅ Clean architecture (modular, extensible)
- ✅ Robust error handling (learned the hard way)
- ✅ Efficient storage (SQLite with content hashing)
- ✅ Scalable scraping (handles JavaScript sites)
- ✅ Professional UI (Flask + responsive templates)

**Technical Stack:**
- Backend: Python, Flask
- AI: Claude API (Anthropic)
- Web Scraping: BeautifulSoup, Trafilatura
- Database: SQLite
- Frontend: HTML5, Jinja2 templates

**Lines of Code:** 1,885 (including the 400+ lines of error handling)

---

## What I Actually Learned

### 1. Building is Messy

The romanticized version: "I built it in one night!"

The reality:
- Multiple debugging sessions over 2 days
- 7 failed attempts at fixing JSON parsing
- 3 file corruptions
- Countless syntax errors
- Several "I quit" moments

**But I kept going.**

### 2. AI Can't Do It Alone

Claude Code was incredible:
- Suggested architecture
- Wrote initial code
- Debugged errors
- Explained concepts

But **I** had to:
- Define what I wanted
- Test everything
- Spot when things didn't work
- Persist through frustration
- Make UX decisions

**AI is a partner, not a replacement.**

### 3. Non-Technical Doesn't Mean Can't Build

I'm a product marketer. I don't write code professionally.

But I built:
- Full-stack web application
- AI-powered analysis engine
- Automated monitoring system
- Database-backed change detection

**Domain expertise + AI assistance = powerful combination.**

### 4. Error Handling is 50% of the Code

My first version: 800 lines
My final version: 1,885 lines

Where did the extra 1,000 lines go?

- Handling 403 errors from scrapers
- Retry logic with exponential backoff
- Temporary file cleanup
- Database connection management
- Form validation
- JSON parsing edge cases

**Production code is mostly error handling.**

### 5. User Experience Matters

**V1:** Required editing JSON files manually
- It worked
- But only I could use it

**V2:** Web UI with auto-discovery
- Still works
- **Anyone** can use it

**The extra day of work made it 10x more valuable.**

---

## The Real Numbers

**Time Investment:**
- Friday night: 2 hours (exploration on phone)
- Saturday: 8 hours (building + debugging)
- Sunday: 4 hours (testing + polish)
- **Total: ~14 hours over 3 days**

**Bugs Fixed:**
- Syntax errors: 12+
- File corruptions: 3
- JSON parsing issues: 7 attempts
- Port conflicts: 2
- Import errors: 5+

**Code Written:**
- Initial version: ~800 lines
- Final version: 1,885 lines
- Error handling: ~40% of code
- Documentation: 6 markdown files

**Business Value:**
- Time saved per week: 10+ hours
- Time saved per month: 40+ hours
- Equivalent consulting value: $2K-$10K/month
- **ROI: Paid for itself in week 1**

---

## What This System Actually Does

### Automatic Competitor Discovery

**You enter:** `https://yourcompany.com`

**System does:**
1. Scrapes your website
2. Analyzes your business category
3. Uses Claude AI to find similar companies
4. Returns 10 ranked competitors
5. You select which ones to track

**Result:** No manual research. No Google searches. Just click and track.

### Change Detection

**System monitors:**
- Pricing pages
- Feature pages
- Homepage messaging
- Product launches

**When something changes:**
- Detects exact diff
- Flags new/removed content
- Stores historical snapshot
- Triggers AI analysis

### AI Strategic Analysis

**Raw change:** "Pricing page updated"

**AI insight:**
```
Competitor raised Enterprise tier 25%.
Removed "Analytics" from Pro plan.

Strategic Impact: Creates pricing gap at $20-25/user range.

Opportunity: Position analytics as included vs. upsell.

Recommended Actions:
1. Update battle cards within 24h
2. Create pricing comparison page
3. Target their customers evaluating alternatives

Threat Level: LOW (benefits your positioning)
```

**This is the difference between data and intelligence.**

---

## Try It Yourself

**GitHub:** [github.com/Doodler-beep/Claude-experiments](https://github.com/Doodler-beep/Claude-experiments)

**Quick Start:**
```bash
git clone https://github.com/Doodler-beep/Claude-experiments.git
cd Claude-experiments
./setup.sh
python src/web_ui.py
# Open http://localhost:8000
```

**Requirements:**
- Python 3.8+
- Claude API key (get free credits at console.anthropic.com)
- 10 minutes

**What you'll get:**
- Automatic competitor discovery
- Real-time change detection
- AI strategic analysis
- Weekly intelligence briefs
- Battle card automation

---

## What's Next (V3 Ideas)

**Community contributions welcome:**

- **Real-time Alerts** - Slack/email notifications for critical changes
- **Multi-user Support** - Team collaboration features
- **Custom Dashboards** - Visualize competitive trends
- **API Integrations** - Connect to CRM, Notion, Salesforce
- **Scheduled Reports** - Automated weekly briefs via email
- **Sentiment Analysis** - Track competitor perception over time
- **Market Mapping** - Visualize competitive positioning

---

## Monetization Paths (If You Want)

**Service Business:**
- Deliver intelligence reports: $2K-$10K/month per client
- Target mid-size companies who can't afford enterprise tools
- White-label for agencies

**SaaS Product:**
- Multi-tenant hosted version: $49-$299/month
- Enterprise tools cost $50K-$200K/year
- Serve the underserved mid-market

**Strategic Consulting:**
- Market analysis backed by automated data: $10K-$25K
- Positioning strategy engagements
- Win/loss analysis enhancement

**Internal Use:**
- Better products (know what NOT to build)
- Win competitive deals (real-time intelligence)
- Strategic pricing (see moves before customers)
- **Value: Priceless**

---

## The Bottom Line

**The Romanticized Version:**
"I built a competitive intelligence system in one caffeinated all-nighter!"

**The Real Version:**
"I spent a weekend debugging syntax errors, fighting file corruption, fixing JSON parsing issues, and nearly quitting three times. But I persisted, learned a ton, and built something genuinely useful."

**Which story is better?**

The real one. Because it's true.

---

## What This Proves

### 1. You Don't Need to Be a Software Engineer

I'm a product marketer. I built this with:
- Domain knowledge (I understand competitive intelligence)
- AI assistance (Claude Code as my pair programmer)
- Persistence (debugging sucks but it's necessary)
- User focus (built for non-technical users like me)

**Domain expertise + AI = superpower.**

### 2. Messy Journeys Create Better Products

If everything worked first try, I would have:
- Worse error handling
- No temp file solution
- Port 5000 hardcoded (broken on Mac)
- Confusing UX

**Every bug I fixed made the product better.**

### 3. Open Source Wins

Enterprise competitive intelligence tools:
- Crayon: $50K-$100K+/year
- Klue: $30K-$80K/year
- Kompyte: $40K-$100K/year

**This tool:** Free. Open source. You own your data.

**The market for competitive intelligence is huge. The tools are expensive. There's opportunity here.**

---

## Resources

**Try the Tool:**
- [GitHub Repository](https://github.com/Doodler-beep/Claude-experiments)
- [Quick Start Guide](https://github.com/Doodler-beep/Claude-experiments/blob/Main/QUICKSTART.md)
- [Web UI Guide](https://github.com/Doodler-beep/Claude-experiments/blob/Main/WEB_UI_GUIDE.md)

**Learn More:**
- [Monetization Playbook](https://github.com/Doodler-beep/Claude-experiments/blob/Main/MONETIZATION.md)
- [Technical Architecture](https://github.com/Doodler-beep/Claude-experiments/blob/Main/BUILDING_STORY.md#appendix-technical-architecture-deep-dive)

**Connect:**
- Questions? Open an issue on GitHub
- Want to contribute? Submit a PR
- Built something cool with this? Share it!

---

## Final Thoughts

It's Sunday evening. I'm exhausted. My git history is full of commits like:

- "Fix syntax error... again"
- "Why is this still broken"
- "PLEASE WORK THIS TIME"
- "Actually fixed it for real this time"

But I built something real:

✅ 1,885 lines of production code
✅ Full-stack web application
✅ AI-powered competitive intelligence
✅ Automated monitoring system
✅ Professional-grade UX

**Not in one night. Not perfectly. But it works.**

And that's what matters.

---

*Built over a weekend with Claude Code, debugging, persistence, and way too much coffee.*

*Open sourced because competitive intelligence shouldn't cost $50K/year.*

**Questions? Contributions? Ideas?**
Find me on GitHub or LinkedIn.

---

## Appendix: Technical Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Web UI (Flask)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │  Setup   │  │ Discover │  │  Manage  │  │Reports │ │
│  └──────────┘  └──────────┘  └──────────┘  └────────┘ │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────┐
│              Core Intelligence Engine                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Tracker    │  │   Detector   │  │   Analyst    │  │
│  │              │  │              │  │              │  │
│  │ Web Scraping │─▶│    Change    │─▶│  AI Insights │  │
│  │   Module     │  │   Detection  │  │  Generation  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
    ┌────▼────┐          ┌───────▼────────┐
    │ SQLite  │          │  Claude API    │
    │Database │          │  (Anthropic)   │
    └─────────┘          └────────────────┘
```

### Key Technologies

**Backend:**
- Python 3.8+ (core language)
- Flask (web framework)
- SQLite (database)

**AI & Analysis:**
- Claude API (Anthropic) - strategic analysis
- BeautifulSoup - HTML parsing
- Trafilatura - content extraction
- Playwright - JavaScript rendering

**Frontend:**
- HTML5 + Jinja2 templates
- Responsive design (works on mobile)
- No JavaScript dependencies

### Why These Choices?

**SQLite over PostgreSQL:**
- No server setup required
- Perfect for single-user/small team
- Handles millions of rows efficiently
- Easy backups (copy one file)

**Flask over Django:**
- Lightweight and fast
- Easy to understand
- Perfect for prototypes → production
- Minimal boilerplate

**Claude over GPT:**
- Better reasoning for strategic analysis
- Handles longer contexts
- More structured outputs
- Reasonable pricing

**BeautifulSoup + Trafilatura:**
- Industry standard for web scraping
- Robust HTML parsing
- Excellent content extraction
- Handles messy real-world HTML

### Performance Characteristics

**Scraping:**
- 2-5 seconds per page (static sites)
- 5-10 seconds per page (JavaScript sites)
- Respects rate limits (1 req/sec per domain)
- Concurrent scraping (3-5 threads)

**Storage:**
- ~100KB per page snapshot
- 1,000 pages = ~100MB database
- Content hashing reduces duplication
- Configurable retention policy

**AI Analysis:**
- 30-60 seconds per change
- Batches multiple changes together
- Cost: ~$0.02-$0.05 per analysis
- Quality: Consistently high value

### Security & Privacy

**Data Ownership:**
- All data stored locally (you own it)
- No external services except Claude API
- No tracking or telemetry
- Easy to backup/export

**API Security:**
- Keys never committed to git
- Stored in gitignored config.json
- Clear setup instructions
- Environment variable support

**Web Scraping Ethics:**
- Respects robots.txt
- Rate limiting prevents overload
- Proper user-agent identification
- Retry logic with exponential backoff

---

*Last updated: January 26, 2026*
