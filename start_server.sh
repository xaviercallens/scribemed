#!/bin/bash
# Start Medical Scribe AI Backend Server

echo "🚀 Starting Medical Scribe AI Backend..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "   Run ./setup_env.sh first to create it"
    exit 1
fi

# Check if port 8001 is available
if lsof -Pi :8001 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  Port 8001 is already in use!"
    echo ""
    echo "Options:"
    echo "  1. Kill the process using port 8001:"
    echo "     lsof -ti:8001 | xargs kill -9"
    echo ""
    echo "  2. Use a different port:"
    echo "     cd backend && python -m uvicorn app.main:app --reload --port 8002"
    echo ""
    exit 1
fi

# Start the server
cd backend
echo "✅ Starting server on http://localhost:8001"
echo "📚 API Docs: http://localhost:8001/docs"
echo "📖 ReDoc: http://localhost:8001/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
