"""Medical Note model."""
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class MedicalNote(Base):
    """Medical note model for structured SOAP notes."""
    
    __tablename__ = "medical_notes"
    
    id = Column(Integer, primary_key=True, index=True)
    recording_id = Column(Integer, ForeignKey("recordings.id"), nullable=False, unique=True)
    
    # SOAP Note sections (stored as JSON for flexibility)
    soap_note = Column(JSON, nullable=True)  # Contains: subjective, objective, assessment, plan
    
    # Extracted information
    chief_complaint = Column(String, nullable=True)
    allergies = Column(JSON, nullable=True)  # List of allergies
    medications = Column(JSON, nullable=True)  # List of medications
    
    # Metadata
    model_used = Column(String, default="gpt-4")
    tokens_used = Column(Integer, nullable=True)
    generation_time_seconds = Column(Float, nullable=True)
    
    # Validation
    validation_status = Column(String, default="pending")  # pending, validated, needs_review
    validation_notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    recording = relationship("Recording", back_populates="medical_note")
