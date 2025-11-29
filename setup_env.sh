#!/bin/bash
# Setup script for Medical Scribe AI

echo "🚀 Setting up Medical Scribe AI..."

# Generate secret key
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")

# Create .env file
cat > .env << EOF
# Local LLM Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2:latest
USE_LOCAL_WHISPER=True
WHISPER_MODEL=base

# Security
SECRET_KEY=$SECRET_KEY
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Database
DATABASE_URL=sqlite:///./medical_scribe.db

# Application
DEBUG=True
API_PORT=8001
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
EOF

echo "✅ .env file created with generated SECRET_KEY"
echo ""
echo "🦙 Using local Ollama with Llama2 model"
echo "📝 Configuration:"
echo "   - Ollama URL: http://localhost:11434"
echo "   - Model: llama2:latest"
echo "   - Whisper: local (base model)"
echo ""
echo "📝 Next steps:"
echo "   1. Ensure Ollama is running: ollama serve"
echo "   2. Check models: ollama list"
echo "   3. Start server: ./start_server.sh"
echo "   4. Visit: http://localhost:8001/docs"
echo ""
