"""
Competitor Tracker Module
Scrapes competitor websites and extracts relevant content
"""

import requests
from bs4 import BeautifulSoup
import trafilatura
import html2text
from datetime import datetime
import hashlib
import json
from typing import Dict, List, Optional
import time


class CompetitorTracker:
    """Tracks competitor websites and extracts content"""

    def __init__(self, user_agent: str = None):
        self.user_agent = user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.user_agent})
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = True

    def fetch_page(self, url: str) -> Optional[Dict]:
        """
        Fetch a webpage and extract its content

        Returns:
            Dictionary with raw HTML, extracted text, and metadata
        """
        try:
            print(f"Fetching: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            html_content = response.text

            # Extract main content using trafilatura (removes nav, footer, etc)
            main_content = trafilatura.extract(html_content, include_comments=False)

            # Also get a markdown version for readability
            markdown_content = self.html_converter.handle(html_content)

            # Extract metadata
            soup = BeautifulSoup(html_content, 'lxml')
            title = soup.find('title').text if soup.find('title') else ""
            meta_description = ""
            meta_tag = soup.find('meta', attrs={'name': 'description'})
            if meta_tag:
                meta_description = meta_tag.get('content', '')

            # Calculate content hash for change detection
            content_hash = hashlib.sha256(
                (main_content or "").encode('utf-8')
            ).hexdigest()

            return {
                'url': url,
                'title': title,
                'meta_description': meta_description,
                'main_content': main_content or markdown_content[:5000],
                'markdown': markdown_content[:10000],  # Limit size
                'raw_html': html_content[:20000],  # Limit size
                'content_hash': content_hash,
                'fetched_at': datetime.now().isoformat(),
                'status_code': response.status_code
            }

        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
        except Exception as e:
            print(f"Error processing {url}: {e}")
            return None

    def scan_competitor(self, competitor: Dict) -> List[Dict]:
        """
        Scan all URLs for a competitor

        Args:
            competitor: Dictionary with 'name' and 'urls' keys

        Returns:
            List of page data dictionaries
        """
        results = []
        competitor_name = competitor.get('name', 'Unknown')
        urls = competitor.get('urls', {})

        print(f"\n🔍 Scanning {competitor_name}...")

        for page_type, url in urls.items():
            page_data = self.fetch_page(url)
            if page_data:
                page_data['competitor'] = competitor_name
                page_data['page_type'] = page_type
                page_data['priority'] = competitor.get('priority', 'medium')
                results.append(page_data)

            # Be respectful - don't hammer servers
            time.sleep(2)

        return results

    def scan_all_competitors(self, competitors: List[Dict]) -> List[Dict]:
        """
        Scan all competitors

        Args:
            competitors: List of competitor dictionaries

        Returns:
            Combined list of all page data
        """
        all_results = []

        for competitor in competitors:
            results = self.scan_competitor(competitor)
            all_results.extend(results)

        return all_results


def extract_pricing_info(content: str) -> Dict:
    """
    Extract pricing-related information from content

    This is a simple heuristic-based approach
    """
    content_lower = content.lower()

    pricing_keywords = ['$', 'price', 'pricing', 'cost', 'subscription', 'plan', 'tier']
    has_pricing = any(keyword in content_lower for keyword in pricing_keywords)

    # Extract sentences with pricing mentions
    pricing_mentions = []
    sentences = content.split('.')
    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in pricing_keywords):
            pricing_mentions.append(sentence.strip())

    return {
        'has_pricing_content': has_pricing,
        'pricing_mentions': pricing_mentions[:10]  # Limit to first 10
    }


def extract_features(content: str) -> List[str]:
    """
    Extract feature-related information from content

    Simple heuristic-based approach
    """
    features = []
    content_lower = content.lower()

    # Look for common feature indicators
    feature_indicators = [
        'feature', 'capability', 'includes', 'offers',
        'integration', 'supports', 'provides'
    ]

    lines = content.split('\n')
    for line in lines:
        line_lower = line.lower()
        # Look for bulleted lists or feature mentions
        if any(indicator in line_lower for indicator in feature_indicators):
            if len(line.strip()) > 10 and len(line.strip()) < 200:
                features.append(line.strip())
        elif line.strip().startswith(('•', '-', '*', '✓', '✔')):
            features.append(line.strip())

    return features[:20]  # Limit to first 20
