#!/bin/bash

# Competitive Intelligence Command Center - Setup Script

echo "🚀 Setting up Competitive Intelligence Command Center..."
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Found Python $PYTHON_VERSION"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Install playwright browsers (for advanced scraping)
echo "🌐 Installing Playwright browsers (this may take a minute)..."
playwright install chromium

# Create config from example if it doesn't exist
if [ ! -f "config.json" ]; then
    echo "⚙️  Creating config.json from example..."
    cp config.example.json config.json
    echo ""
    echo "⚠️  IMPORTANT: Edit config.json and add:"
    echo "   1. Your Claude API key"
    echo "   2. Your competitors' URLs"
    echo "   3. Your product information"
    echo ""
else
    echo "✓ config.json already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit config.json with your API key and competitors"
echo "  2. Run: python main.py scan"
echo "  3. Run: python main.py analyze"
echo ""
echo "To activate the virtual environment later:"
echo "  source venv/bin/activate"
echo ""
