"""
AI Analyst Module
Uses Claude API to analyze competitive intelligence and generate strategic insights
"""

from anthropic import Anthropic
from typing import Dict, List, Optional
import json
from datetime import datetime


class AIAnalyst:
    """AI-powered competitive intelligence analyst using Claude"""

    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-5-20250929"

    def analyze_change(self, change: Dict, your_product: Dict) -> Dict:
        """
        Analyze a detected competitor change for strategic implications

        Args:
            change: Change data from change detector
            your_product: Your product information for context

        Returns:
            Analysis with strategic insights
        """
        change_summary = json.loads(change.get('change_summary', '{}'))

        prompt = f"""You are a strategic competitive intelligence analyst. Analyze this competitor change and provide actionable insights.

COMPETITOR: {change['competitor']}
PAGE TYPE: {change['page_type']}
CHANGE TYPE: {change['change_type']}

CHANGE DETAILS:
{json.dumps(change_summary, indent=2)}

OLD CONTENT EXCERPT:
{change.get('old_content', '')[:2000]}

NEW CONTENT EXCERPT:
{change.get('new_content', '')[:2000]}

YOUR PRODUCT CONTEXT:
Product: {your_product.get('name', 'Unknown')}
Category: {your_product.get('category', 'Unknown')}
Key Differentiators: {', '.join(your_product.get('key_differentiators', []))}

Provide a strategic analysis in this JSON format:
{{
  "severity": "critical|high|medium|low",
  "strategic_impact": "Brief description of strategic impact",
  "key_insights": [
    "Insight 1",
    "Insight 2"
  ],
  "opportunities": [
    "Opportunity 1",
    "Opportunity 2"
  ],
  "recommended_actions": [
    "Action 1",
    "Action 2"
  ],
  "threat_level": "high|medium|low|none",
  "one_liner": "Executive summary in one sentence"
}}

Focus on:
1. What does this change signal about their strategy?
2. How does this affect your competitive position?
3. What opportunities does this create?
4. What immediate actions should you take?
"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Extract JSON from response
            analysis_text = response.content[0].text

            # Try to parse JSON from the response
            try:
                # Look for JSON in the response
                start = analysis_text.find('{')
                end = analysis_text.rfind('}') + 1
                if start != -1 and end > start:
                    analysis = json.loads(analysis_text[start:end])
                else:
                    analysis = json.loads(analysis_text)
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                analysis = {
                    "severity": "medium",
                    "strategic_impact": analysis_text[:200],
                    "key_insights": [analysis_text[:500]],
                    "opportunities": [],
                    "recommended_actions": [],
                    "threat_level": "medium",
                    "one_liner": "Analysis completed"
                }

            analysis['analyzed_at'] = datetime.now().isoformat()
            analysis['change_id'] = change.get('id')

            return analysis

        except Exception as e:
            print(f"Error analyzing change: {e}")
            return {
                "error": str(e),
                "severity": "unknown",
                "one_liner": "Analysis failed"
            }

    def generate_weekly_brief(self, changes: List[Dict],
                             competitor_snapshots: List[Dict],
                             your_product: Dict,
                             focus_areas: List[str]) -> str:
        """
        Generate a comprehensive weekly competitive intelligence brief

        Args:
            changes: List of changes detected this week
            competitor_snapshots: Current state of competitor pages
            your_product: Your product information
            focus_areas: Areas to focus the analysis on

        Returns:
            Formatted intelligence brief
        """
        prompt = f"""You are a strategic competitive intelligence analyst. Generate an executive weekly competitive intelligence brief.

YOUR PRODUCT:
{json.dumps(your_product, indent=2)}

FOCUS AREAS:
{', '.join(focus_areas)}

CHANGES DETECTED THIS WEEK ({len(changes)} total):
{json.dumps(changes[:10], indent=2)}

CURRENT COMPETITOR LANDSCAPE:
{self._summarize_competitors(competitor_snapshots)}

Generate a comprehensive weekly brief with these sections:

# Executive Summary
[2-3 sentence overview of the week's competitive landscape]

# Critical Developments
[Most important changes and their implications]

# Strategic Opportunities
[Specific opportunities identified based on competitor moves]

# Market Positioning Analysis
[How competitors are positioning vs. your product]

# Recommended Actions
[Specific, prioritized actions for this week]

# Threats to Monitor
[Potential competitive threats on the horizon]

# Market Whitespace
[Gaps in the market that nobody is addressing]

Make it actionable, strategic, and concise. Focus on insights that drive decisions.
"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            brief = response.content[0].text

            # Add metadata
            header = f"""# Competitive Intelligence Brief
**Generated:** {datetime.now().strftime('%B %d, %Y')}
**Period:** Last 7 days
**Changes Tracked:** {len(changes)}

---

"""

            return header + brief

        except Exception as e:
            print(f"Error generating brief: {e}")
            return f"Error generating brief: {e}"

    def identify_market_gaps(self, competitor_data: List[Dict],
                            your_product: Dict) -> Dict:
        """
        Identify whitespace and opportunities in the market

        Args:
            competitor_data: Data about all competitors
            your_product: Your product information

        Returns:
            Market gap analysis
        """
        prompt = f"""You are a strategic market analyst. Analyze the competitive landscape to identify market gaps and opportunities.

YOUR PRODUCT:
{json.dumps(your_product, indent=2)}

COMPETITIVE LANDSCAPE:
{self._summarize_competitors(competitor_data[:20])}

Analyze and identify:

1. **Market Whitespace**: What is NO competitor doing that customers might want?
2. **Underserved Segments**: Which customer segments are poorly served?
3. **Feature Gaps**: What features are missing across the board?
4. **Positioning Opportunities**: How can you differentiate where competitors cluster?
5. **Pricing Opportunities**: Any pricing gaps or opportunities?

Provide response in this JSON format:
{{
  "whitespace_opportunities": [
    {{"opportunity": "description", "rationale": "why this matters", "priority": "high|medium|low"}}
  ],
  "underserved_segments": ["segment 1", "segment 2"],
  "missing_features": ["feature 1", "feature 2"],
  "positioning_angles": [
    {{"angle": "description", "differentiation": "how it differentiates"}}
  ],
  "strategic_recommendations": ["recommendation 1", "recommendation 2"]
}}
"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=3000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Parse JSON response
            analysis_text = response.content[0].text
            start = analysis_text.find('{')
            end = analysis_text.rfind('}') + 1

            if start != -1 and end > start:
                return json.loads(analysis_text[start:end])
            else:
                return {"error": "Could not parse response"}

        except Exception as e:
            print(f"Error identifying market gaps: {e}")
            return {"error": str(e)}

    def analyze_pricing_strategy(self, pricing_data: List[Dict],
                                 your_product: Dict) -> str:
        """
        Analyze competitor pricing strategies

        Args:
            pricing_data: Pricing information from competitors
            your_product: Your product information

        Returns:
            Pricing analysis and recommendations
        """
        prompt = f"""You are a pricing strategy consultant. Analyze the competitive pricing landscape.

YOUR PRODUCT:
{json.dumps(your_product, indent=2)}

COMPETITOR PRICING DATA:
{json.dumps(pricing_data, indent=2)}

Provide:
1. Overview of competitive pricing landscape
2. Pricing patterns and strategies observed
3. Where your product should be positioned
4. Specific pricing recommendations
5. Opportunities to capture value

Format as a clear, actionable analysis.
"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2500,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            return response.content[0].text

        except Exception as e:
            print(f"Error analyzing pricing: {e}")
            return f"Error: {e}"

    def _summarize_competitors(self, competitor_data: List[Dict]) -> str:
        """Create a summary of competitor data for prompts"""
        summaries = []

        for data in competitor_data[:10]:  # Limit to prevent token overflow
            summary = f"""
Competitor: {data.get('competitor', 'Unknown')}
Page: {data.get('page_type', 'Unknown')}
Title: {data.get('title', 'N/A')}
Content Preview: {data.get('main_content', '')[:500]}
"""
            summaries.append(summary)

        return '\n---\n'.join(summaries)

    def generate_alert_message(self, change: Dict, analysis: Dict) -> str:
        """
        Generate a concise alert message for critical changes

        Args:
            change: Change data
            analysis: AI analysis of the change

        Returns:
            Formatted alert message
        """
        severity_emoji = {
            'critical': '🚨',
            'high': '⚠️',
            'medium': '📊',
            'low': '📝'
        }

        emoji = severity_emoji.get(analysis.get('severity', 'medium'), '📊')

        alert = f"""{emoji} COMPETITIVE ALERT - {analysis.get('severity', 'MEDIUM').upper()}

Competitor: {change['competitor']}
Change: {change['change_type'].replace('_', ' ').title()}
Page: {change['page_type']}

{analysis.get('one_liner', 'Significant change detected')}

Strategic Impact: {analysis.get('strategic_impact', 'Unknown')}

Recommended Actions:
{self._format_list(analysis.get('recommended_actions', []))}

Threat Level: {analysis.get('threat_level', 'Unknown').upper()}
"""

        return alert

    def _format_list(self, items: List[str]) -> str:
        """Format a list of items with bullets"""
        if not items:
            return "- None specified"
        return '\n'.join([f"- {item}" for item in items])
