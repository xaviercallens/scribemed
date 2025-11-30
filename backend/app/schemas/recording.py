"""Recording schemas."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class RecordingCreate(BaseModel):
    """Schema for creating a recording (used internally)."""
    audio_file_path: str
    original_filename: str
    file_size: Optional[int] = None


class RecordingResponse(BaseModel):
    """Schema for recording response."""
    id: int
    user_id: int
    audio_file_path: str
    original_filename: str
    file_size: Optional[int] = None
    duration_seconds: Optional[float] = None
    transcript: Optional[str] = None
    transcript_language: str
    status: str
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class RecordingList(BaseModel):
    """Schema for list of recordings."""
    recordings: List[RecordingResponse]
    total: int
    page: int
    per_page: int
