# Medical Scribe AI - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Set Up Environment (1 min)

```bash
cd medical-scribe

# Run setup script (creates .env with generated SECRET_KEY)
./setup_env.sh

# Edit .env and add your OpenAI API key
# Replace: OPENAI_API_KEY=sk-your-openai-api-key-here
# With: OPENAI_API_KEY=sk-proj-actual-key-here
nano .env  # or use your preferred editor
```

### Step 2: Start Backend Server (1 min)

```bash
cd backend
python -m uvicorn app.main:app --reload --port 8001
```

Server will start at: **http://localhost:8001**

> **Note**: Using port 8001 to avoid conflicts. Port 8000 is often used by other services.

### Step 3: Test the API (3 min)

#### Option A: Use Interactive Docs
Visit: **http://localhost:8001/docs**

#### Option B: Use curl

**1. Register a user:**
```bash
curl -X POST http://localhost:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User"
  }'
```

**2. Login:**
```bash
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

Copy the `access_token` from the response.

**3. Get your profile:**
```bash
curl http://localhost:8001/api/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

## ✅ What's Working Now

- ✅ User registration and login
- ✅ JWT authentication
- ✅ Database (SQLite)
- ✅ API documentation
- ✅ CORS configured for frontend

## ⏭️ What's Next

Continue with Day 1 implementation:
- Audio upload endpoint
- Whisper transcription integration
- Medical note generation

See [DAY1_PROGRESS.md](./DAY1_PROGRESS.md) for detailed progress.

## 📚 Full Documentation

- [2-Day Implementation Guide](./docs/WINDSURF_2DAY_GUIDE.md)
- [Quick Reference](./docs/QUICK_REFERENCE.md)
- [Day 1 Progress](./DAY1_PROGRESS.md)

## 🆘 Troubleshooting

**"ValidationError: openai_api_key Field required"**
→ Add your OpenAI API key to `.env` file

**"ModuleNotFoundError"**
→ Run: `pip install -r requirements.txt`

**"Port 8001 already in use"**
→ Kill existing process or use different port:
```bash
# Check what's using the port
lsof -i :8001

# Use a different port
python -m uvicorn app.main:app --reload --port 8002
```

---

**You're all set!** 🎉 The backend is running and ready for development.
