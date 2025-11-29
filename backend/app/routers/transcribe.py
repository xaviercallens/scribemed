"""Transcription router for processing recordings."""
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
import logging
from pathlib import Path

from ..database import get_db
from ..models.user import User
from ..models.recording import Recording
from ..models.medical_note import MedicalNote
from ..schemas.recording import RecordingResponse
from ..schemas.medical_note import MedicalNoteResponse
from ..utils.auth import get_current_user
from ..services.transcription import get_transcription_service
from ..services.medical_notes import get_medical_note_service

logger = logging.getLogger(__name__)

router = APIRouter()


def process_recording_background(recording_id: int, db_session):
    """Background task to process recording.
    
    Args:
        recording_id: Recording ID to process
        db_session: Database session
    """
    try:
        # Get recording
        recording = db_session.query(Recording).filter(Recording.id == recording_id).first()
        if not recording:
            logger.error(f"Recording {recording_id} not found")
            return
        
        # Update status
        recording.status = "transcribing"
        db_session.commit()
        
        # Transcribe audio
        logger.info(f"Transcribing recording {recording_id}")
        transcription_service = get_transcription_service()
        
        result = transcription_service.transcribe_audio(
            recording.audio_file_path,
            language="en"
        )
        
        # Update recording with transcript
        recording.transcript = result['text']
        recording.transcript_language = result['language']
        recording.duration_seconds = result.get('duration', 0)
        recording.status = "transcribed"
        db_session.commit()
        
        logger.info(f"Transcription completed for recording {recording_id}")
        
        # Generate medical note
        logger.info(f"Generating medical note for recording {recording_id}")
        recording.status = "processing"
        db_session.commit()
        
        medical_service = get_medical_note_service()
        note_result = medical_service.generate_soap_note(result['text'])
        
        # Create medical note
        medical_note = MedicalNote(
            recording_id=recording.id,
            soap_note=note_result['soap_note'],
            chief_complaint=note_result['soap_note'].get('chief_complaint', ''),
            allergies=note_result['soap_note'].get('allergies', []),
            medications=note_result['soap_note'].get('medications', []),
            model_used=note_result['model_used'],
            tokens_used=note_result.get('prompt_tokens', 0) + note_result.get('completion_tokens', 0),
            generation_time_seconds=note_result['generation_time_seconds']
        )
        
        db_session.add(medical_note)
        recording.status = "completed"
        db_session.commit()
        
        logger.info(f"Medical note generated for recording {recording_id}")
        
    except Exception as e:
        logger.error(f"Processing failed for recording {recording_id}: {e}")
        if recording:
            recording.status = "failed"
            recording.error_message = str(e)
            db_session.commit()


@router.post("/{recording_id}/transcribe", response_model=RecordingResponse)
async def transcribe_recording(
    recording_id: int,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start transcription for a recording.
    
    Args:
        recording_id: Recording ID
        background_tasks: FastAPI background tasks
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Updated recording
    """
    # Get recording
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
    
    # Check if already processed
    if recording.status in ["transcribing", "processing", "completed"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Recording is already {recording.status}"
        )
    
    # Check if file exists
    if not Path(recording.audio_file_path).exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audio file not found"
        )
    
    # Add background task
    background_tasks.add_task(process_recording_background, recording_id, db)
    
    # Update status immediately
    recording.status = "transcribing"
    db.commit()
    db.refresh(recording)
    
    logger.info(f"Transcription queued for recording {recording_id}")
    
    return RecordingResponse.model_validate(recording)


@router.get("/{recording_id}/note", response_model=MedicalNoteResponse)
async def get_medical_note(
    recording_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get medical note for a recording.
    
    Args:
        recording_id: Recording ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Medical note
    """
    # Get recording
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
    
    # Get medical note
    medical_note = (
        db.query(MedicalNote)
        .filter(MedicalNote.recording_id == recording_id)
        .first()
    )
    
    if not medical_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical note not found. Recording may not be processed yet."
        )
    
    return MedicalNoteResponse.model_validate(medical_note)


@router.post("/{recording_id}/regenerate-note", response_model=MedicalNoteResponse)
async def regenerate_medical_note(
    recording_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Regenerate medical note for a recording.
    
    Args:
        recording_id: Recording ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Updated medical note
    """
    # Get recording
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
    
    if not recording.transcript:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Recording must be transcribed first"
        )
    
    # Generate new medical note
    logger.info(f"Regenerating medical note for recording {recording_id}")
    
    medical_service = get_medical_note_service()
    note_result = medical_service.generate_soap_note(recording.transcript)
    
    # Get or create medical note
    medical_note = (
        db.query(MedicalNote)
        .filter(MedicalNote.recording_id == recording_id)
        .first()
    )
    
    if medical_note:
        # Update existing
        medical_note.soap_note = note_result['soap_note']
        medical_note.chief_complaint = note_result['soap_note'].get('chief_complaint', '')
        medical_note.allergies = note_result['soap_note'].get('allergies', [])
        medical_note.medications = note_result['soap_note'].get('medications', [])
        medical_note.model_used = note_result['model_used']
        medical_note.tokens_used = note_result.get('prompt_tokens', 0) + note_result.get('completion_tokens', 0)
        medical_note.generation_time_seconds = note_result['generation_time_seconds']
    else:
        # Create new
        medical_note = MedicalNote(
            recording_id=recording.id,
            soap_note=note_result['soap_note'],
            chief_complaint=note_result['soap_note'].get('chief_complaint', ''),
            allergies=note_result['soap_note'].get('allergies', []),
            medications=note_result['soap_note'].get('medications', []),
            model_used=note_result['model_used'],
            tokens_used=note_result.get('prompt_tokens', 0) + note_result.get('completion_tokens', 0),
            generation_time_seconds=note_result['generation_time_seconds']
        )
        db.add(medical_note)
    
    db.commit()
    db.refresh(medical_note)
    
    logger.info(f"Medical note regenerated for recording {recording_id}")
    
    return MedicalNoteResponse.model_validate(medical_note)
