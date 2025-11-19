#!/bin/bash
# Gemini Research Papers Chatbot Launcher

echo "🤖 Gemini Research Papers Chatbot"
echo "=================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if API key is configured
if grep -q "your_api_key_here" app.py; then
    echo ""
    echo "⚠️  API Key Not Configured"
    echo "Please get your Google Gemini API key from: https://aistudio.google.com/"
    echo "Then edit app.py and replace 'your_api_key_here' with your actual key."
    echo ""
    read -p "Do you have your API key ready? (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Please configure your API key and run this script again."
        exit 1
    fi
fi

# Run the Streamlit app
echo "🚀 Starting web interface..."
echo "Open your browser to: http://localhost:8501"
echo ""
streamlit run app.py