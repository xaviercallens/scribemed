"""Transcription service using local Whisper."""
import whisper
import logging
from pathlib import Path
from typing import Dict, Optional
import time

from ..config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class TranscriptionService:
    """Service for audio transcription using local Whisper."""
    
    def __init__(self, model_size: Optional[str] = None):
        """Initialize transcription service.
        
        Args:
            model_size: Whisper model size (tiny, base, small, medium, large)
        """
        self.model_size = model_size or settings.whisper_model
        self.model = None
        logger.info(f"Initializing Whisper transcription service with model: {self.model_size}")
    
    def _load_model(self):
        """Load Whisper model lazily."""
        if self.model is None:
            logger.info(f"Loading Whisper model: {self.model_size}")
            start_time = time.time()
            self.model = whisper.load_model(self.model_size)
            load_time = time.time() - start_time
            logger.info(f"Whisper model loaded in {load_time:.2f}s")
    
    def transcribe_audio(
        self,
        audio_path: str,
        language: str = "en",
        task: str = "transcribe"
    ) -> Dict[str, any]:
        """Transcribe audio file using Whisper.
        
        Args:
            audio_path: Path to audio file
            language: Language code (e.g., 'en', 'es', 'fr')
            task: 'transcribe' or 'translate'
            
        Returns:
            Dict with transcription results
        """
        try:
            # Load model if not already loaded
            self._load_model()
            
            # Validate file exists
            if not Path(audio_path).exists():
                raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
            logger.info(f"Transcribing audio: {audio_path}")
            start_time = time.time()
            
            # Transcribe
            result = self.model.transcribe(
                audio_path,
                language=language,
                task=task,
                fp16=False  # Use FP32 for CPU compatibility
            )
            
            transcription_time = time.time() - start_time
            
            logger.info(f"Transcription completed in {transcription_time:.2f}s")
            
            return {
                "text": result["text"].strip(),
                "language": result.get("language", language),
                "segments": result.get("segments", []),
                "duration": transcription_time,
                "model": self.model_size
            }
            
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise Exception(f"Failed to transcribe audio: {str(e)}")
    
    def transcribe_with_timestamps(
        self,
        audio_path: str,
        language: str = "en"
    ) -> Dict[str, any]:
        """Transcribe with detailed timestamps.
        
        Args:
            audio_path: Path to audio file
            language: Language code
            
        Returns:
            Dict with transcription and segment timestamps
        """
        try:
            self._load_model()
            
            logger.info(f"Transcribing with timestamps: {audio_path}")
            
            result = self.model.transcribe(
                audio_path,
                language=language,
                word_timestamps=True,
                fp16=False
            )
            
            # Format segments with timestamps
            formatted_segments = []
            for segment in result.get("segments", []):
                formatted_segments.append({
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"].strip(),
                    "words": segment.get("words", [])
                })
            
            return {
                "text": result["text"].strip(),
                "language": result.get("language", language),
                "segments": formatted_segments,
                "model": self.model_size
            }
            
        except Exception as e:
            logger.error(f"Transcription with timestamps failed: {e}")
            raise Exception(f"Failed to transcribe with timestamps: {str(e)}")
    
    def get_audio_duration(self, audio_path: str) -> float:
        """Get audio file duration in seconds.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Duration in seconds
        """
        try:
            import librosa
            duration = librosa.get_duration(path=audio_path)
            return duration
        except ImportError:
            # Fallback: use pydub
            from pydub import AudioSegment
            audio = AudioSegment.from_file(audio_path)
            return len(audio) / 1000.0  # Convert ms to seconds
        except Exception as e:
            logger.error(f"Failed to get audio duration: {e}")
            return 0.0


# Singleton instance
_transcription_service: Optional[TranscriptionService] = None


def get_transcription_service() -> TranscriptionService:
    """Get or create transcription service instance.
    
    Returns:
        TranscriptionService instance
    """
    global _transcription_service
    if _transcription_service is None:
        _transcription_service = TranscriptionService()
    return _transcription_service
