#!/usr/bin/env bash
# setup.sh — Bootstrap Khetika development environment
set -e

echo "🌱 Khetika — Dev Setup"
echo "======================"

# 1. Check Python version
python3 --version | grep -E "3\.(1[0-9])" || {
  echo "❌ Python 3.10+ required"; exit 1
}

# 2. Create virtualenv
if [ ! -d "venv" ]; then
  echo "📦 Creating virtual environment..."
  python3 -m venv venv
fi

# 3. Activate
source venv/bin/activate

# 4. Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# 5. Setup .env
if [ ! -f ".env" ]; then
  cp .env.example .env
  echo "⚠️  .env created — add your GROQ_API_KEY before running!"
else
  echo "✅ .env already exists"
fi

echo ""
echo "✅ Setup complete!"
echo "   1. Edit .env and add GROQ_API_KEY"
echo "   2. Run: source venv/bin/activate"
echo "   3. Run: python app.py"
