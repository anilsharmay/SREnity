#!/bin/bash

# SREnity Streamlit App Launcher
# This script sets up and runs the Streamlit app

echo "🚀 Starting SREnity Streamlit App..."

# Check if virtual environment exists
if [ ! -d "../.venv" ]; then
    echo "❌ Virtual environment not found. Please create one first:"
    echo "   python -m venv .venv"
    echo "   source .venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source ../.venv/bin/activate

# Check if .env file exists
if [ ! -f "../.env" ]; then
    echo "⚠️  Warning: .env file not found. Make sure to set up your environment variables."
fi

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Run Streamlit app
echo "🎯 Launching Streamlit app..."
echo "   The app will open at: http://localhost:8501"
echo "   Press Ctrl+C to stop the app"
echo ""

streamlit run streamlit_app.py
