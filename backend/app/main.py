"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import get_settings
from .database import init_db

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="Medical Scribe API",
    description="AI-powered medical scribe application for automated clinical documentation",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware configuration
origins = settings.allowed_origins.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()


@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        "message": "Welcome to Medical Scribe API",
        "version": "0.1.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Import and include routers
from .routers import auth, recordings, transcribe
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(recordings.router, prefix="/api/recordings", tags=["Recordings"])
app.include_router(transcribe.router, prefix="/api/recordings", tags=["Transcription"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
