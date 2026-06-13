#!/usr/bin/env bash
# test.sh — Run full test + lint suite
set -e
source venv/bin/activate

echo "🧪 Running tests..."
pytest tests/ -v --cov=. --cov-report=term-missing

echo "🔍 Linting..."
ruff check .
echo "✅ All checks passed"
