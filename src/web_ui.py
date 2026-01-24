"""
Web UI for Competitive Intelligence Command Center
Simple interface for non-technical users
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import json
import os
from pathlib import Path
import sys

# Add parent directory to path to import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.competitor_discovery import CompetitorDiscovery
from src.competitor_tracker import CompetitorTracker
from src.change_detector import ChangeDetector
from src.ai_analyst import AIAnalyst


app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')
app.secret_key = 'competitive-intelligence-secret-key-change-in-production'

CONFIG_PATH = 'config.json'


def load_config():
    """Load configuration from file"""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    return None


def save_config(config):
    """Save configuration to file"""
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)


@app.route('/')
def index():
    """Home page"""
    config = load_config()

    # Check if configured
    is_configured = (
        config and
        config.get('api_keys', {}).get('anthropic_api_key') not in [None, '', 'PLACEHOLDER-get-from-console.anthropic.com']
    )

    return render_template('index.html',
                         config=config,
                         is_configured=is_configured)


@app.route('/setup', methods=['GET', 'POST'])
def setup():
    """Setup page for API key and initial configuration"""
    if request.method == 'POST':
        api_key = request.form.get('api_key')

        if not api_key:
            flash('Please enter your Claude API key', 'error')
            return redirect(url_for('setup'))

        # Load existing config or create new
        config = load_config() or {
            'api_keys': {},
            'competitors': [],
            'monitoring': {
                'scan_frequency_hours': 24,
                'alert_on_changes': True,
                'generate_weekly_report': True,
                'weekly_report_day': 'monday'
            },
            'analysis': {
                'focus_areas': [
                    'pricing changes',
                    'feature additions/removals',
                    'messaging shifts',
                    'product launches'
                ],
                'your_product': {
                    'name': 'Your Product',
                    'category': 'Your Category',
                    'key_differentiators': []
                }
            },
            'output': {
                'reports_directory': './reports',
                'database_path': './data/intelligence.db'
            }
        }

        config['api_keys']['anthropic_api_key'] = api_key
        save_config(config)

        flash('API key saved! Now let\'s discover your competitors.', 'success')
        return redirect(url_for('discover'))

    config = load_config()
    return render_template('setup.html', config=config)


@app.route('/discover', methods=['GET', 'POST'])
def discover():
    """Discover competitors automatically"""
    config = load_config()

    if not config or not config.get('api_keys', {}).get('anthropic_api_key'):
        flash('Please set up your API key first', 'error')
        return redirect(url_for('setup'))

    if request.method == 'POST':
        company_url = request.form.get('company_url')
        num_competitors = int(request.form.get('num_competitors', 10))

        if not company_url:
            flash('Please enter your company URL', 'error')
            return redirect(url_for('discover'))

        try:
            # Run discovery
            discovery = CompetitorDiscovery(config['api_keys']['anthropic_api_key'])
            results = discovery.run_discovery(company_url, num_competitors)

            # Store in session for later retrieval
            session['discovery_results'] = results

            # Store discovered competitors for review
            # Don't auto-save to config yet - let user review first
            return render_template('review_competitors.html',
                                 results=results,
                                 your_company=results['your_company'])

        except Exception as e:
            flash(f'Error discovering competitors: {str(e)}', 'error')
            return redirect(url_for('discover'))

    return render_template('discover.html')


@app.route('/save_competitors', methods=['POST'])
def save_competitors():
    """Save selected competitors to config"""
    config = load_config()

    # Get discovery results from session
    discovery_results = session.get('discovery_results')

    if not discovery_results:
        flash('Session expired. Please discover competitors again.', 'error')
        return redirect(url_for('discover'))

    # Get form data
    company_name = request.form.get('company_name')
    company_category = request.form.get('company_category')
    company_description = request.form.get('company_description')

    # Get selected competitors
    selected_competitors = request.form.getlist('selected_competitors')

    if not selected_competitors:
        flash('Please select at least one competitor', 'error')
        return redirect(url_for('discover'))

    # Get competitors data from session
    competitors_data = discovery_results.get('competitors', [])

    # Filter to selected only
    filtered_competitors = [
        comp for comp in competitors_data
        if comp['name'] in selected_competitors
    ]

    # Update config
    config['analysis']['your_product'] = {
        'name': company_name,
        'category': company_category,
        'description': company_description,
        'key_differentiators': []
    }

    config['competitors'] = [
        {
            'name': comp['name'],
            'urls': comp['urls'],
            'priority': comp['priority']
        }
        for comp in filtered_competitors
    ]

    save_config(config)

    flash(f'Successfully added {len(filtered_competitors)} competitors!', 'success')
    return redirect(url_for('competitors'))


@app.route('/competitors')
def competitors():
    """View and manage competitors"""
    config = load_config()

    if not config:
        flash('Please complete setup first', 'error')
        return redirect(url_for('setup'))

    return render_template('competitors.html',
                         config=config,
                         competitors=config.get('competitors', []),
                         your_product=config.get('analysis', {}).get('your_product', {}))


@app.route('/add_competitor', methods=['POST'])
def add_competitor():
    """Manually add a competitor"""
    config = load_config()

    name = request.form.get('name')
    homepage = request.form.get('homepage')
    pricing = request.form.get('pricing')
    priority = request.form.get('priority', 'medium')

    if not name or not homepage:
        flash('Name and homepage URL are required', 'error')
        return redirect(url_for('competitors'))

    # Create competitor object
    new_competitor = {
        'name': name,
        'urls': {'homepage': homepage},
        'priority': priority
    }

    if pricing:
        new_competitor['urls']['pricing'] = pricing

    # Add to config
    if 'competitors' not in config:
        config['competitors'] = []

    config['competitors'].append(new_competitor)
    save_config(config)

    flash(f'Added {name} to tracking list', 'success')
    return redirect(url_for('competitors'))


@app.route('/remove_competitor/<int:index>')
def remove_competitor(index):
    """Remove a competitor"""
    config = load_config()

    if 0 <= index < len(config.get('competitors', [])):
        removed = config['competitors'].pop(index)
        save_config(config)
        flash(f'Removed {removed["name"]}', 'success')
    else:
        flash('Competitor not found', 'error')

    return redirect(url_for('competitors'))


@app.route('/reports')
def reports():
    """View generated reports"""
    config = load_config()
    reports_dir = Path(config.get('output', {}).get('reports_directory', './reports'))

    # Get all report files
    report_files = []
    if reports_dir.exists():
        for file in sorted(reports_dir.glob('*'), reverse=True):
            report_files.append({
                'name': file.name,
                'path': str(file),
                'size': file.stat().st_size,
                'modified': file.stat().st_mtime
            })

    return render_template('reports.html', reports=report_files)


@app.route('/view_report/<path:filename>')
def view_report(filename):
    """View a specific report"""
    config = load_config()
    reports_dir = Path(config.get('output', {}).get('reports_directory', './reports'))
    report_path = reports_dir / filename

    if not report_path.exists():
        flash('Report not found', 'error')
        return redirect(url_for('reports'))

    with open(report_path, 'r') as f:
        content = f.read()

    return render_template('view_report.html',
                         filename=filename,
                         content=content)


@app.route('/status')
def status():
    """Show system status"""
    config = load_config()

    if not config:
        return render_template('status.html', status={})

    # Get database stats
    db_path = config.get('output', {}).get('database_path', './data/intelligence.db')

    status_info = {
        'competitors_tracked': len(config.get('competitors', [])),
        'api_configured': bool(config.get('api_keys', {}).get('anthropic_api_key')),
        'database_exists': os.path.exists(db_path)
    }

    # Get recent changes if database exists
    if status_info['database_exists']:
        try:
            detector = ChangeDetector(db_path)
            recent_changes = detector.get_recent_changes(7)
            status_info['recent_changes'] = len(recent_changes)
            status_info['unanalyzed'] = len(detector.get_unanalyzed_changes())
        except:
            status_info['recent_changes'] = 0
            status_info['unanalyzed'] = 0

    return render_template('status.html',
                         status=status_info,
                         config=config)


def run_ui(host='127.0.0.1', port=5000, debug=True):
    """Run the web UI"""
    print(f"""
╔════════════════════════════════════════════════════════════╗
║  Competitive Intelligence Command Center - Web UI         ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  🌐 Open your browser and go to:                          ║
║                                                            ║
║     http://localhost:{port}                                   ║
║                                                            ║
║  Press Ctrl+C to stop the server                          ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
""")

    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_ui()
