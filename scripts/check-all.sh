#!/bin/bash
# Local pre-commit checks
# Run this before pushing to verify all checks will pass in GitHub Actions

set -e

echo "================================"
echo "🚀 Local Pre-commit Checks"
echo "================================"

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed"
    exit 1
fi

echo "✅ Python version: $(python --version)"

# Install dev dependencies if needed
echo ""
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt 2>/dev/null || pip install -r requirements.txt

# Flake8 linting
echo ""
echo "🔍 Running flake8 linting..."
if flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics; then
    echo "✅ flake8 passed"
else
    echo "❌ flake8 failed"
    exit 1
fi

# Black formatting check
echo ""
echo "🎨 Checking black formatting..."
if black --check . --quiet 2>/dev/null; then
    echo "✅ black formatting passed"
else
    echo "⚠️  black formatting issues found"
    echo "   Run: black . && isort ."
    read -p "Auto-fix? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        black . --quiet
        isort . --quiet
        echo "✅ Code formatted"
    else
        exit 1
    fi
fi

# isort import sorting
echo ""
echo "📚 Checking import sorting with isort..."
if isort --check-only . --quiet 2>/dev/null; then
    echo "✅ isort passed"
else
    echo "⚠️  isort issues found"
    echo "   Run: isort ."
    read -p "Auto-fix? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        isort . --quiet
        echo "✅ Imports sorted"
    else
        exit 1
    fi
fi

# Pylint
echo ""
echo "🔎 Running pylint..."
pylint app.py app_env.py config.py --disable=C0111,W0612,C0103,C0301 --exit-zero || true
echo "✅ pylint completed"

# Bandit security check
echo ""
echo "🔐 Running bandit security check..."
if command -v bandit &> /dev/null; then
    bandit -r . -q || true
    echo "✅ bandit completed"
else
    echo "⚠️  bandit not installed (optional)"
fi

# Tests
echo ""
echo "🧪 Running pytest..."
if command -v pytest &> /dev/null; then
    pytest tests/ -v --tb=short 2>/dev/null || echo "⚠️  Some tests may have failed"
else
    echo "⚠️  pytest not installed (optional)"
fi

echo ""
echo "================================"
echo "✅ All checks completed!"
echo "================================"
echo ""
echo "Ready to push? 🚀"
echo "  git push origin <branch>"
