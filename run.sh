#!/bin/bash

# Fruit Classification System - Quick Start Script

echo "🍎 Fruit Classification System"
echo "==============================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/.installed" ]; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    touch venv/.installed
fi

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Add your OpenAI API key to .env file!"
    echo "Edit .env and set: OPENAI_API_KEY=sk-your-key-here"
    echo "Get your key at: https://platform.openai.com/api-keys"
    echo ""
    read -p "Press Enter after adding your API key to continue..."
fi

# Check if OpenAI key is set
if ! grep -q "OPENAI_API_KEY=sk-" .env; then
    echo "⚠️  Warning: OpenAI API key not found in .env"
    echo "The application may not work without a valid API key"
    echo ""
fi

# Check if MongoDB is running
echo "🔍 Checking MongoDB..."
if ! pgrep -x "mongod" > /dev/null; then
    echo "⚠️  MongoDB is not running!"
    echo "Starting MongoDB..."
    
    # Try to start MongoDB (macOS)
    if command -v brew &> /dev/null; then
        brew services start mongodb-community
    else
        echo "Please start MongoDB manually:"
        echo "  sudo systemctl start mongodb"
    fi
fi

# Start the Flask application
echo ""
echo "🚀 Starting Flask server with OpenAI Vision..."
echo "📍 Application will be available at: http://localhost:5000"
echo "💰 Note: Each classification uses OpenAI API (check pricing at platform.openai.com)"
echo ""
python backend/app.py
