#!/usr/bin/env bash
set -e

echo "🚀 Starting Web Analytics Agent Skill Setup & Analysis..."

# 1. Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is not installed. Please install Python 3 first."
    exit 1
fi

# 2. Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment (.venv)..."
    python3 -m venv .venv
fi

# 3. Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Suppress Python deprecation warnings and OpenSSL warnings for cleaner output
export PYTHONWARNINGS="ignore"

# 4. Install requirements
echo "📥 Installing/Updating dependencies..."
pip install -q -r requirements.txt > /dev/null 2>&1 || true

# 5. Check and Generate Google OAuth Tokens
echo -e "\n========================================================"
echo "🔐 Checking Google API Authentication..."
python3 scripts/auth_google.py
if [ $? -ne 0 ]; then
    # If auth fails (e.g., missing client_secret.json), stop execution
    exit 1
fi

# 6. Run the analytics scripts
echo -e "\n========================================================"
echo "🔍 Running Google Search Console Analysis..."
python3 scripts/analyze_gsc.py

echo -e "\n========================================================"
echo "📈 Running Google Analytics 4 Analysis..."
python3 scripts/ga4_both.py

echo -e "\n========================================================"
echo "🌐 Running Bing Webmaster Analysis..."
python3 scripts/bing_webmaster.py

echo -e "\n========================================================"
echo "✅ All analysis tasks complete!"
