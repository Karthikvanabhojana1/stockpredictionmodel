#!/bin/bash

# Soros Chatbot Startup Script
# This script starts both the FastAPI backend and React frontend

echo "🤖 Starting Soros Chatbot..."
echo "================================"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
# OpenAI API Configuration
OPENAI_API_KEY=your-api-key-here

# Optional: Customize API settings
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=1000

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_PORT=3000

# Development Settings
DEBUG=true
LOG_LEVEL=INFO
EOF
    echo "✅ Created .env file"
    echo "⚠️  Please edit .env and set your OpenAI API key before continuing"
    echo ""
fi

# Check if OPENAI_API_KEY is set in .env
if grep -q "OPENAI_API_KEY=your-api-key-here" .env; then
    echo "❌ Error: Please set your OpenAI API key in the .env file"
    echo "Edit .env and replace 'your-api-key-here' with your actual API key"
    echo "You can get an API key from: https://platform.openai.com/api-keys"
    exit 1
fi

echo "✅ Configuration looks good"
echo ""

# Function to cleanup background processes
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start the FastAPI backend
echo "🚀 Starting FastAPI backend on http://localhost:8000"
cd "$(dirname "$0")"
python api/main.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Check if backend started successfully
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "❌ Backend failed to start. Check the logs above."
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo "✅ Backend is running"
echo ""

# Start the React frontend
echo "🚀 Starting React frontend on http://localhost:3000"
cd frontend
npm start &
FRONTEND_PID=$!

echo "✅ Frontend is starting..."
echo ""
echo "🌐 Access the application at: http://localhost:3000"
echo "📚 API documentation at: http://localhost:8000/docs"
echo "🔧 Configuration endpoint: http://localhost:8000/config"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for both processes
wait 