#!/usr/bin/env python3
"""
Competitive Intelligence Command Center
Main orchestration script
"""

import sys
import json
import os
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

# Import our modules
from src.competitor_tracker import CompetitorTracker, extract_pricing_info
from src.change_detector import ChangeDetector
from src.ai_analyst import AIAnalyst
from src.competitor_discovery import CompetitorDiscovery


console = Console()


class IntelligenceCenter:
    """Main orchestrator for competitive intelligence"""

    def __init__(self, config_path: str = 'config.json'):
        self.config = self._load_config(config_path)
        self.tracker = CompetitorTracker()
        self.db_path = self.config['output']['database_path']
        self.detector = ChangeDetector(self.db_path)
        self.analyst = AIAnalyst(self.config['api_keys']['anthropic_api_key'])

        # Ensure directories exist
        Path(self.config['output']['reports_directory']).mkdir(parents=True, exist_ok=True)
        Path(os.path.dirname(self.db_path)).mkdir(parents=True, exist_ok=True)

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from JSON file"""
        if not os.path.exists(config_path):
            console.print(f"[red]Error: {config_path} not found![/red]")
            console.print("[yellow]Copy config.example.json to config.json and configure it.[/yellow]")
            sys.exit(1)

        with open(config_path, 'r') as f:
            return json.load(f)

    def scan(self):
        """Run a competitive intelligence scan"""
        console.print("\n[bold cyan]🔍 Starting Competitive Intelligence Scan[/bold cyan]\n")

        competitors = self.config['competitors']

        all_changes = []
        new_pages = 0
        changed_pages = 0

        # Scan all competitors
        results = self.tracker.scan_all_competitors(competitors)

        console.print(f"\n[green]✓ Scanned {len(results)} pages across {len(competitors)} competitors[/green]\n")

        # Process each result
        for page_data in results:
            # Check for changes
            change = self.detector.detect_change(page_data)

            # Store the new snapshot
            snapshot_id = self.detector.store_snapshot(page_data)

            if change:
                # Record the change
                self.detector.record_change(change, snapshot_id)
                all_changes.append(change)
                changed_pages += 1

                console.print(f"[yellow]📊 Change detected:[/yellow] {change['competitor']} - {change['page_type']}")
            else:
                if self.detector.get_latest_snapshot(
                    page_data['competitor'],
                    page_data['page_type'],
                    page_data['url']
                ):
                    console.print(f"[dim]No change:[/dim] {page_data['competitor']} - {page_data['page_type']}")
                else:
                    new_pages += 1
                    console.print(f"[green]New page tracked:[/green] {page_data['competitor']} - {page_data['page_type']}")

        # Summary
        console.print("\n" + "="*60)
        console.print(f"[bold]Scan Complete![/bold]")
        console.print(f"  • New pages tracked: {new_pages}")
        console.print(f"  • Changes detected: {changed_pages}")
        console.print("="*60 + "\n")

        if all_changes:
            console.print("[cyan]Run 'python main.py analyze' to get AI insights on these changes.[/cyan]\n")

    def analyze(self):
        """Analyze unanalyzed changes with AI"""
        console.print("\n[bold cyan]🧠 Analyzing Changes with AI[/bold cyan]\n")

        changes = self.detector.get_unanalyzed_changes()

        if not changes:
            console.print("[yellow]No new changes to analyze.[/yellow]\n")
            return

        console.print(f"Found {len(changes)} changes to analyze...\n")

        your_product = self.config['analysis']['your_product']
        reports_dir = Path(self.config['output']['reports_directory'])

        for i, change in enumerate(changes, 1):
            console.print(f"[{i}/{len(changes)}] Analyzing: {change['competitor']} - {change['page_type']}")

            # Get AI analysis
            analysis = self.analyst.analyze_change(change, your_product)

            # Generate alert if high severity
            if analysis.get('severity') in ['critical', 'high']:
                alert = self.analyst.generate_alert_message(change, analysis)
                console.print(Panel(alert, border_style="red" if analysis['severity'] == 'critical' else "yellow"))

                # Save alert to file
                alert_file = reports_dir / f"alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{change['competitor']}_{change['page_type']}.txt"
                alert_file.write_text(alert)

            # Mark as analyzed
            self.detector.mark_change_analyzed(change['id'])

            console.print(f"  → {analysis.get('one_liner', 'Analysis complete')}\n")

        console.print("[green]✓ Analysis complete![/green]\n")

    def report(self, days: int = 7):
        """Generate a comprehensive intelligence report"""
        console.print(f"\n[bold cyan]📊 Generating {days}-Day Intelligence Report[/bold cyan]\n")

        # Get recent changes
        changes = self.detector.get_recent_changes(days)

        if not changes:
            console.print("[yellow]No changes in the specified period.[/yellow]\n")
            return

        # Get current competitor snapshots
        snapshots = []
        for competitor in self.config['competitors']:
            for page_type, url in competitor['urls'].items():
                snapshot = self.detector.get_latest_snapshot(competitor['name'], page_type, url)
                if snapshot:
                    snapshots.append(snapshot)

        # Generate brief
        console.print("Generating strategic brief with AI...\n")

        brief = self.analyst.generate_weekly_brief(
            changes,
            snapshots,
            self.config['analysis']['your_product'],
            self.config['analysis']['focus_areas']
        )

        # Save to file
        reports_dir = Path(self.config['output']['reports_directory'])
        report_file = reports_dir / f"intelligence_brief_{datetime.now().strftime('%Y%m%d')}.md"
        report_file.write_text(brief)

        console.print(Panel(brief[:1000] + "\n\n[...continued in file...]", title="Intelligence Brief Preview", border_style="cyan"))
        console.print(f"\n[green]✓ Full report saved to: {report_file}[/green]\n")

    def gaps(self):
        """Identify market gaps and opportunities"""
        console.print("\n[bold cyan]🎯 Identifying Market Gaps[/bold cyan]\n")

        # Get all current snapshots
        snapshots = []
        for competitor in self.config['competitors']:
            for page_type, url in competitor['urls'].items():
                snapshot = self.detector.get_latest_snapshot(competitor['name'], page_type, url)
                if snapshot:
                    snapshots.append(snapshot)

        if not snapshots:
            console.print("[yellow]No competitor data available. Run a scan first.[/yellow]\n")
            return

        console.print("Analyzing competitive landscape for opportunities...\n")

        analysis = self.analyst.identify_market_gaps(
            snapshots,
            self.config['analysis']['your_product']
        )

        # Display results
        if 'whitespace_opportunities' in analysis:
            console.print("\n[bold]🔍 Market Whitespace Opportunities:[/bold]")
            for opp in analysis['whitespace_opportunities']:
                priority_color = {'high': 'red', 'medium': 'yellow', 'low': 'white'}.get(opp.get('priority', 'low'))
                console.print(f"  [{priority_color}]•[/{priority_color}] {opp.get('opportunity')}")
                console.print(f"    Rationale: {opp.get('rationale')}\n")

        if 'positioning_angles' in analysis:
            console.print("\n[bold]🎯 Positioning Opportunities:[/bold]")
            for angle in analysis['positioning_angles']:
                console.print(f"  • {angle.get('angle')}")
                console.print(f"    {angle.get('differentiation')}\n")

        if 'strategic_recommendations' in analysis:
            console.print("\n[bold]💡 Strategic Recommendations:[/bold]")
            for rec in analysis['strategic_recommendations']:
                console.print(f"  • {rec}")

        # Save to file
        reports_dir = Path(self.config['output']['reports_directory'])
        gaps_file = reports_dir / f"market_gaps_{datetime.now().strftime('%Y%m%d')}.json"
        gaps_file.write_text(json.dumps(analysis, indent=2))

        console.print(f"\n[green]✓ Full analysis saved to: {gaps_file}[/green]\n")

    def status(self):
        """Show current status and statistics"""
        console.print("\n[bold cyan]📈 Intelligence Center Status[/bold cyan]\n")

        # Competitor summary
        table = Table(title="Tracked Competitors")
        table.add_column("Competitor", style="cyan")
        table.add_column("Pages", style="magenta")
        table.add_column("Priority", style="yellow")

        for comp in self.config['competitors']:
            table.add_row(
                comp['name'],
                str(len(comp['urls'])),
                comp.get('priority', 'medium')
            )

        console.print(table)

        # Recent activity
        recent_changes = self.detector.get_recent_changes(7)
        console.print(f"\n[bold]Recent Activity (7 days):[/bold]")
        console.print(f"  • Changes detected: {len(recent_changes)}")

        unanalyzed = self.detector.get_unanalyzed_changes()
        console.print(f"  • Pending analysis: {len(unanalyzed)}")

        console.print(f"\n[bold]Database:[/bold] {self.db_path}")
        console.print(f"[bold]Reports:[/bold] {self.config['output']['reports_directory']}\n")

    def discover(self, company_url: str, num_competitors: int = 10):
        """Discover competitors automatically"""
        console.print("\n[bold cyan]🔍 Discovering Competitors[/bold cyan]\n")

        discovery = CompetitorDiscovery(self.config['api_keys']['anthropic_api_key'])

        # Run discovery
        results = discovery.run_discovery(company_url, num_competitors)

        # Display results
        console.print(f"\n[green]✓ Found {results['total_found']} competitors![/green]\n")

        console.print("[bold]Your Company:[/bold]")
        console.print(f"  Name: {results['your_company']['name']}")
        console.print(f"  Industry: {results['your_company']['category']}")
        console.print(f"  Description: {results['your_company']['description']}\n")

        # Show competitors
        table = Table(title="Discovered Competitors")
        table.add_column("Name", style="cyan")
        table.add_column("Priority", style="magenta")
        table.add_column("Why Competitor", style="white")

        for comp in results['competitors']:
            table.add_row(
                comp['name'],
                comp['priority'],
                comp.get('why_competitor', '')[:60] + "..."
            )

        console.print(table)

        # Ask if user wants to save
        console.print(f"\n[yellow]To save these competitors, use the web UI:[/yellow]")
        console.print(f"[cyan]python main.py web[/cyan]\n")

        # Optionally save raw results for review
        reports_dir = Path(self.config['output']['reports_directory'])
        discovery_file = reports_dir / f"discovery_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        discovery_file.write_text(json.dumps(results, indent=2))
        console.print(f"[green]Discovery results saved to: {discovery_file}[/green]\n")


def main():
    """Main entry point"""

    if len(sys.argv) < 2:
        console.print("""
[bold cyan]Competitive Intelligence Command Center[/bold cyan]

Usage:
  python main.py web                      - Open web UI (easy mode!)
  python main.py discover <url>           - Auto-discover competitors
  python main.py scan                     - Scan all competitors for changes
  python main.py analyze                  - Analyze detected changes with AI
  python main.py report                   - Generate weekly intelligence brief
  python main.py gaps                     - Identify market gaps and opportunities
  python main.py status                   - Show current status

Examples:
  python main.py web
  python main.py discover https://yourcompany.com
  python main.py scan && python main.py analyze
  python main.py report
        """)
        sys.exit(0)

    command = sys.argv[1].lower()

    # Web UI doesn't need IntelligenceCenter
    if command == 'web':
        from src.web_ui import run_ui
        run_ui()
        return

    # Discover command
    if command == 'discover':
        if len(sys.argv) < 3:
            console.print("[red]Please provide your company URL:[/red]")
            console.print("  python main.py discover https://yourcompany.com")
            sys.exit(1)

        company_url = sys.argv[2]
        num_competitors = int(sys.argv[3]) if len(sys.argv) > 3 else 10

        center = IntelligenceCenter()
        center.discover(company_url, num_competitors)
        return

    # Other commands
    center = IntelligenceCenter()

    if command == 'scan':
        center.scan()
    elif command == 'analyze':
        center.analyze()
    elif command == 'report':
        center.report()
    elif command == 'gaps':
        center.gaps()
    elif command == 'status':
        center.status()
    else:
        console.print(f"[red]Unknown command: {command}[/red]")
        sys.exit(1)


if __name__ == '__main__':
    main()
