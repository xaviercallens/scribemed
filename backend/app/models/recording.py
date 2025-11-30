"""Recording model."""
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Recording(Base):
    """Recording model for audio files and transcripts."""
    
    __tablename__ = "recordings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # File information
    audio_file_path = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_size = Column(Integer, nullable=True)  # in bytes
    duration_seconds = Column(Float, nullable=True)
    
    # Transcription
    transcript = Column(Text, nullable=True)
    transcript_language = Column(String, default="en")
    
    # Status tracking
    status = Column(String, default="uploaded")  # uploaded, transcribing, transcribed, processing, completed, failed
    error_message = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="recordings")
    medical_note = relationship("MedicalNote", back_populates="recording", uselist=False, cascade="all, delete-orphan")
