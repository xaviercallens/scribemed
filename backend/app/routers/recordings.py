"""Recordings router for audio upload and management."""
import os
import uuid
from pathlib import Path
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, BackgroundTasks
from sqlalchemy.orm import Session
import logging

from ..database import get_db
from ..models.user import User
from ..models.recording import Recording
from ..schemas.recording import RecordingResponse, RecordingList
from ..utils.auth import get_current_user
from ..config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter()

# Allowed audio formats
ALLOWED_EXTENSIONS = {'.wav', '.mp3', '.m4a', '.ogg', '.flac', '.webm'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

# Upload directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def validate_audio_file(file: UploadFile) -> None:
    """Validate uploaded audio file.
    
    Args:
        file: Uploaded file
        
    Raises:
        HTTPException: If file is invalid
    """
    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file format. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Check content type
    if file.content_type and not file.content_type.startswith('audio/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an audio file"
        )


def save_upload_file(file: UploadFile, user_id: int) -> tuple[str, int]:
    """Save uploaded file to disk.
    
    Args:
        file: Uploaded file
        user_id: User ID for organizing files
        
    Returns:
        Tuple of (file_path, file_size)
    """
    # Create user directory
    user_dir = UPLOAD_DIR / str(user_id)
    user_dir.mkdir(exist_ok=True)
    
    # Generate unique filename
    file_ext = Path(file.filename).suffix.lower()
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = user_dir / unique_filename
    
    # Save file
    file_size = 0
    with open(file_path, "wb") as f:
        while chunk := file.file.read(8192):
            file_size += len(chunk)
            if file_size > MAX_FILE_SIZE:
                # Clean up partial file
                file_path.unlink(missing_ok=True)
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"File too large. Maximum size: {MAX_FILE_SIZE / 1024 / 1024}MB"
                )
            f.write(chunk)
    
    return str(file_path), file_size


@router.post("/upload", response_model=RecordingResponse, status_code=status.HTTP_201_CREATED)
async def upload_recording(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload an audio recording.
    
    Args:
        file: Audio file to upload
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Created recording
    """
    try:
        # Validate file
        validate_audio_file(file)
        
        logger.info(f"Uploading file: {file.filename} for user {current_user.id}")
        
        # Save file
        file_path, file_size = save_upload_file(file, current_user.id)
        
        # Create database record
        recording = Recording(
            user_id=current_user.id,
            audio_file_path=file_path,
            original_filename=file.filename,
            file_size=file_size,
            status="uploaded"
        )
        
        db.add(recording)
        db.commit()
        db.refresh(recording)
        
        logger.info(f"Recording created: {recording.id}")
        
        return RecordingResponse.model_validate(recording)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}"
        )


@router.get("/", response_model=RecordingList)
async def list_recordings(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List user's recordings.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List of recordings
    """
    # Get total count
    total = db.query(Recording).filter(Recording.user_id == current_user.id).count()
    
    # Get recordings
    recordings = (
        db.query(Recording)
        .filter(Recording.user_id == current_user.id)
        .order_by(Recording.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    return RecordingList(
        recordings=[RecordingResponse.model_validate(r) for r in recordings],
        total=total,
        page=skip // limit + 1 if limit > 0 else 1,
        per_page=limit
    )


@router.get("/{recording_id}", response_model=RecordingResponse)
async def get_recording(
    recording_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific recording.
    
    Args:
        recording_id: Recording ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Recording details
    """
    recording = (
        db.query(Recording)
        .filter(Recording.id == recording_id, Recording.user_id == current_user.id)
        .first()
    )
    
    if not recording:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recording not found"
        )
    
    return RecordingResponse.model_validate(recording)


@router.delete("/{recording_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recording(
    recording_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a recording.
    
    Args:
        recording_id: Recording ID
        current_user: Current authenticated user
        db: Database session
    """
    recording = (
        db.query(Recording)
        .filter(Recording.id == recording_id, Recording.user_id == current_user.id)
        .first()
    )
    
    if not recording:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recording not found"
        )
    
    # Delete file from disk
    try:
        file_path = Path(recording.audio_file_path)
        if file_path.exists():
            file_path.unlink()
            logger.info(f"Deleted file: {file_path}")
    except Exception as e:
        logger.error(f"Failed to delete file: {e}")
    
    # Delete from database
    db.delete(recording)
    db.commit()
    
    logger.info(f"Recording deleted: {recording_id}")
    
    return None
