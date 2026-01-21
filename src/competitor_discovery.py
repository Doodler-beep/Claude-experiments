"""
Competitor Discovery Module
Automatically discovers competitors based on your company website
"""

from anthropic import Anthropic
import requests
from bs4 import BeautifulSoup
import trafilatura
from typing import Dict, List, Optional
import json


class CompetitorDiscovery:
    """Automatically discover competitors for a company"""

    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-5-20250929"

    def analyze_company_website(self, url: str) -> Dict:
        """
        Analyze a company's website to understand what they do

        Args:
            url: Company website URL

        Returns:
            Dictionary with company analysis
        """
        print(f"🔍 Analyzing {url}...")

        try:
            # Fetch the website
            response = requests.get(url, timeout=30, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            html_content = response.text

            # Extract main content
            main_content = trafilatura.extract(html_content, include_comments=False)

            if not main_content:
                soup = BeautifulSoup(html_content, 'lxml')
                main_content = soup.get_text()[:5000]

            # Use Claude to analyze the company
            prompt = f"""Analyze this company's website and extract key information.

Website URL: {url}
Content:
{main_content[:3000]}

Provide a JSON response with:
{{
  "company_name": "The company name",
  "industry": "The industry/category (e.g., 'Project Management Software', 'CRM', 'Analytics Platform')",
  "description": "Brief description of what the company does (1-2 sentences)",
  "key_features": ["Feature 1", "Feature 2", "Feature 3"],
  "target_market": "Who they serve (e.g., 'Small businesses', 'Enterprises', 'Developers')",
  "business_model": "How they make money (e.g., 'SaaS subscription', 'Freemium', 'Enterprise sales')"
}}

Be concise and accurate."""

            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )

            # Parse JSON from response
            analysis_text = response.content[0].text
            start = analysis_text.find('{')
            end = analysis_text.rfind('}') + 1

            if start != -1 and end > start:
                analysis = json.loads(analysis_text[start:end])
            else:
                analysis = {
                    "company_name": "Unknown",
                    "industry": "Unknown",
                    "description": "Could not analyze",
                    "key_features": [],
                    "target_market": "Unknown",
                    "business_model": "Unknown"
                }

            analysis['url'] = url
            return analysis

        except Exception as e:
            print(f"Error analyzing website: {e}")
            return {
                "company_name": "Unknown",
                "industry": "Unknown",
                "description": f"Error: {str(e)}",
                "url": url
            }

    def discover_competitors(self, company_analysis: Dict, num_competitors: int = 10) -> List[Dict]:
        """
        Discover competitors based on company analysis

        Args:
            company_analysis: Analysis of the company
            num_competitors: Number of competitors to suggest

        Returns:
            List of competitor dictionaries
        """
        print(f"\n🔎 Discovering competitors in the {company_analysis.get('industry', 'Unknown')} space...")

        prompt = f"""You are a market research expert. Based on this company analysis, identify their main competitors.

COMPANY ANALYSIS:
{json.dumps(company_analysis, indent=2)}

Find {num_competitors} direct competitors. For each competitor, provide:
1. Company name
2. Website URL
3. Why they're a competitor (1 sentence)
4. How they differ (1 sentence)
5. Market position (leader/challenger/niche)

Focus on:
- Direct competitors (same industry, similar product)
- Active companies (not dead startups)
- Real, well-known players in the space

Provide response as a JSON array:
[
  {{
    "name": "Competitor Name",
    "website": "https://competitor.com",
    "why_competitor": "Brief reason",
    "differentiation": "How they differ",
    "market_position": "leader/challenger/niche",
    "priority": "high/medium/low"
  }}
]

Be accurate. Only include real companies with real websites."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=3000,
                messages=[{"role": "user", "content": prompt}]
            )

            # Parse JSON array from response
            response_text = response.content[0].text
            start = response_text.find('[')
            end = response_text.rfind(']') + 1

            if start != -1 and end > start:
                competitors = json.loads(response_text[start:end])
            else:
                competitors = []

            print(f"✓ Found {len(competitors)} potential competitors")
            return competitors

        except Exception as e:
            print(f"Error discovering competitors: {e}")
            return []

    def enrich_competitor_info(self, competitor: Dict) -> Dict:
        """
        Enrich competitor information by analyzing their website

        Args:
            competitor: Basic competitor info

        Returns:
            Enriched competitor dictionary with URLs to track
        """
        base_url = competitor.get('website', '')

        # Common page patterns to check
        potential_pages = {
            'homepage': base_url,
            'pricing': f"{base_url}/pricing",
            'features': f"{base_url}/features",
            'about': f"{base_url}/about",
            'blog': f"{base_url}/blog"
        }

        # Check which pages exist
        available_urls = {}
        for page_type, url in potential_pages.items():
            try:
                response = requests.head(url, timeout=5, allow_redirects=True, headers={
                    'User-Agent': 'Mozilla/5.0'
                })
                if response.status_code == 200:
                    available_urls[page_type] = url
            except:
                pass

        # At minimum, include homepage
        if not available_urls:
            available_urls['homepage'] = base_url

        return {
            'name': competitor.get('name'),
            'urls': available_urls,
            'priority': competitor.get('priority', 'medium'),
            'why_competitor': competitor.get('why_competitor', ''),
            'differentiation': competitor.get('differentiation', ''),
            'market_position': competitor.get('market_position', 'unknown')
        }

    def run_discovery(self, company_url: str, num_competitors: int = 10) -> Dict:
        """
        Run complete discovery process

        Args:
            company_url: Your company's website URL
            num_competitors: How many competitors to find

        Returns:
            Complete discovery results
        """
        # Step 1: Analyze your company
        company_analysis = self.analyze_company_website(company_url)

        # Step 2: Discover competitors
        competitors = self.discover_competitors(company_analysis, num_competitors)

        # Step 3: Enrich competitor info
        print("\n📋 Enriching competitor information...")
        enriched_competitors = []
        for i, competitor in enumerate(competitors, 1):
            print(f"  [{i}/{len(competitors)}] {competitor.get('name', 'Unknown')}")
            enriched = self.enrich_competitor_info(competitor)
            enriched_competitors.append(enriched)

        return {
            'your_company': {
                'name': company_analysis.get('company_name', 'Your Company'),
                'category': company_analysis.get('industry', 'Unknown'),
                'description': company_analysis.get('description', ''),
                'key_differentiators': company_analysis.get('key_features', [])[:3]
            },
            'competitors': enriched_competitors,
            'total_found': len(enriched_competitors)
        }

    def format_for_config(self, discovery_results: Dict) -> Dict:
        """
        Format discovery results for config.json

        Args:
            discovery_results: Results from run_discovery

        Returns:
            Formatted config dictionary
        """
        return {
            'your_product': discovery_results['your_company'],
            'competitors': [
                {
                    'name': comp['name'],
                    'urls': comp['urls'],
                    'priority': comp['priority']
                }
                for comp in discovery_results['competitors']
            ]
        }
