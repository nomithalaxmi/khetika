#!/usr/bin/env bash
# run.sh — Start Khetika in development mode
set -e

[ ! -f "venv/bin/activate" ] && echo "❌ Run setup.sh first" && exit 1
source venv/bin/activate

[ ! -f ".env" ] && echo "❌ .env missing — copy .env.example and fill in keys" && exit 1

echo "🌱 Starting Khetika on http://127.0.0.1:5000"
python app.py
