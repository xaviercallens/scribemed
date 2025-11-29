"""Medical note schemas."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any


class SOAPNote(BaseModel):
    """Schema for SOAP note structure."""
    subjective: Optional[str] = None
    objective: Optional[str] = None
    assessment: Optional[str] = None
    plan: Optional[str] = None


class MedicalNoteResponse(BaseModel):
    """Schema for medical note response."""
    id: int
    recording_id: int
    soap_note: Optional[Dict[str, Any]] = None
    chief_complaint: Optional[str] = None
    allergies: Optional[List[str]] = None
    medications: Optional[List[str]] = None
    model_used: str
    tokens_used: Optional[int] = None
    generation_time_seconds: Optional[float] = None
    validation_status: str
    validation_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
