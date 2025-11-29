# Medical Scribe AI

An AI-powered medical scribe application that helps healthcare providers by transcribing patient visits and generating structured medical notes.

> 🚀 **New to this project?** Check out our comprehensive **[2-Day Implementation Guide](./docs/README.md)** for step-by-step instructions on building this prototype using Windsurf!

## Features

- 🎙️ Audio recording of patient visits
- 🧠 AI-powered transcription and note generation
- 📝 Structured medical note templates
- 🔐 Secure user authentication
- 📱 Responsive web interface

## Tech Stack

- **Frontend**: React with TypeScript, TailwindCSS
- **Backend**: FastAPI (Python)
- **Database**: SQLite (development), PostgreSQL (production)
- **AI/ML**: OpenAI Whisper for speech-to-text, GPT-4 for note generation
- **Authentication**: JWT

## Getting Started

### Prerequisites

- Node.js 16+ and npm 8+
- Python 3.9+
- pip 20.0.2+

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/medical-scribe.git
   cd medical-scribe
   ```

2. **Set up the backend**
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run the backend server
   cd backend
   uvicorn app.main:app --reload
   ```

3. **Set up the frontend**
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8001/docs
   
   > **Note**: Using port 8001 to avoid conflicts with other services. You can change this in `.env` by setting `API_PORT=8001`

## Environment Variables

Create a `.env` file in the backend directory with the following variables:

```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./medical_scribe.db
OPENAI_API_KEY=your-openai-api-key
```

## 📚 Documentation

Comprehensive guides for building and scaling this prototype:

- **[Documentation Hub](./docs/README.md)** - Start here for navigation
- **[2-Day Implementation Guide](./docs/WINDSURF_2DAY_GUIDE.md)** - Complete hour-by-hour build guide
- **[Quick Reference](./docs/QUICK_REFERENCE.md)** - Developer checklist (print this!)
- **[Windsurf Tips](./docs/WINDSURF_TIPS.md)** - AI-assisted development best practices
- **[Cost Estimates](./docs/COST_ESTIMATE.md)** - Financial planning & scaling costs

### Quick Links by Role

**👨‍💻 Developers**: [2-Day Guide](./docs/WINDSURF_2DAY_GUIDE.md) → [Quick Reference](./docs/QUICK_REFERENCE.md) → [Tips](./docs/WINDSURF_TIPS.md)

**💼 Business/Founders**: [Business Value](./docs/WINDSURF_2DAY_GUIDE.md#-business-value-documentation) → [Cost Estimates](./docs/COST_ESTIMATE.md) → [Roadmap](./docs/WINDSURF_2DAY_GUIDE.md#-evolution--roadmap)

**💰 Investors**: [Cost Estimates](./docs/COST_ESTIMATE.md) → [Financial Projections](./docs/COST_ESTIMATE.md#-financial-projections) → [Business Case](./docs/WINDSURF_2DAY_GUIDE.md#-business-value-documentation)

## 🎯 Project Status

- ✅ Architecture designed
- ✅ Implementation guide complete
- ⏳ Prototype in development
- ⏳ Beta testing phase
- ⏳ Production deployment

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
