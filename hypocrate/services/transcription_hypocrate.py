"""
Service de transcription audio avec Whisper local pour Hypocrate
"""
import whisper
import logging
from pathlib import Path
from typing import Dict, Optional, List
import time
import torch

logger = logging.getLogger(__name__)


class HypocrateTranscriptionService:
    """Service de transcription audio optimisé pour consultations médicales"""
    
    def __init__(self, model_size: str = "base", device: Optional[str] = None):
        """
        Initialise le service de transcription
        
        Args:
            model_size: Taille du modèle Whisper (tiny, base, small, medium, large)
            device: Device PyTorch (cuda, cpu, mps) - auto-détecté si None
        """
        self.model_size = model_size
        self.model = None
        self.device = device or self._detect_device()
        
        logger.info(f"Initialisation Whisper {model_size} sur {self.device}")
    
    def _detect_device(self) -> str:
        """Détecte le meilleur device disponible"""
        if torch.cuda.is_available():
            return "cuda"
        # MPS (Apple Silicon) a des problèmes de compatibilité avec Whisper
        # Utilisation forcée du CPU pour éviter les erreurs SparseMPS
        # elif torch.backends.mps.is_available():
        #     return "mps"
        return "cpu"
    
    def _load_model(self):
        """Charge le modèle Whisper (lazy loading)"""
        if self.model is None:
            logger.info(f"Chargement du modèle Whisper {self.model_size}...")
            start_time = time.time()
            
            self.model = whisper.load_model(self.model_size, device=self.device)
            
            load_time = time.time() - start_time
            logger.info(f"Modèle chargé en {load_time:.2f}s")
    
    def transcribe_audio(
        self,
        audio_path: str,
        language: str = "fr",
        task: str = "transcribe",
        with_timestamps: bool = True
    ) -> Dict:
        """
        Transcrit un fichier audio médical
        
        Args:
            audio_path: Chemin vers le fichier audio
            language: Langue de l'audio (fr, en, etc.)
            task: 'transcribe' ou 'translate'
            with_timestamps: Inclure les timestamps des segments
            
        Returns:
            Dict avec transcription et métadonnées
        """
        try:
            # Charge le modèle si nécessaire
            self._load_model()
            
            # Valide le fichier
            audio_file = Path(audio_path)
            if not audio_file.exists():
                raise FileNotFoundError(f"Fichier audio introuvable: {audio_path}")
            
            logger.info(f"Transcription de {audio_file.name} (langue: {language})")
            start_time = time.time()
            
            # Options de transcription optimisées pour médical
            options = {
                "language": language,
                "task": task,
                "fp16": self.device != "cpu",  # FP16 sur GPU/MPS
                "verbose": False,
                "word_timestamps": with_timestamps,
                # Paramètres pour améliorer la précision médicale
                "temperature": 0.0,  # Déterministe
                "compression_ratio_threshold": 2.4,
                "logprob_threshold": -1.0,
                "no_speech_threshold": 0.6,
            }
            
            # Transcription
            result = self.model.transcribe(str(audio_file), **options)
            
            transcription_time = time.time() - start_time
            
            # Formatage du résultat
            formatted_result = {
                "text": result["text"].strip(),
                "language": result.get("language", language),
                "segments": self._format_segments(result.get("segments", [])),
                "duration_seconds": transcription_time,
                "model": self.model_size,
                "device": self.device,
                "audio_file": audio_file.name
            }
            
            logger.info(f"Transcription terminée en {transcription_time:.2f}s")
            logger.info(f"Texte transcrit: {len(formatted_result['text'])} caractères")
            
            return formatted_result
            
        except Exception as e:
            logger.error(f"Erreur lors de la transcription: {e}")
            raise
    
    def _format_segments(self, segments: List[Dict]) -> List[Dict]:
        """Formate les segments avec timestamps"""
        formatted = []
        
        for segment in segments:
            formatted.append({
                "start": round(segment["start"], 2),
                "end": round(segment["end"], 2),
                "text": segment["text"].strip(),
                "confidence": segment.get("avg_logprob", 0.0)
            })
        
        return formatted
    
    def format_dialogue(self, segments: List[Dict], speaker_detection: bool = False) -> str:
        """
        Formate la transcription en dialogue médecin-patient
        
        Args:
            segments: Segments avec timestamps
            speaker_detection: Activer la détection de locuteurs (basique)
            
        Returns:
            Texte formaté en dialogue
        """
        if not segments:
            return ""
        
        dialogue_lines = []
        current_speaker = "Médecin"
        
        for i, segment in enumerate(segments):
            text = segment["text"].strip()
            
            if not text:
                continue
            
            # Détection basique de changement de locuteur (pause > 2s)
            if speaker_detection and i > 0:
                pause = segment["start"] - segments[i-1]["end"]
                if pause > 2.0:
                    # Change de locuteur
                    current_speaker = "Patient" if current_speaker == "Médecin" else "Médecin"
            
            # Formate la ligne
            timestamp = f"[{self._format_time(segment['start'])}]"
            dialogue_lines.append(f"{timestamp} **{current_speaker}**: {text}")
        
        return "\n\n".join(dialogue_lines)
    
    def _format_time(self, seconds: float) -> str:
        """Formate les secondes en MM:SS"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
    
    def get_audio_duration(self, audio_path: str) -> float:
        """
        Obtient la durée d'un fichier audio
        
        Args:
            audio_path: Chemin vers le fichier
            
        Returns:
            Durée en secondes
        """
        try:
            import librosa
            duration = librosa.get_duration(path=audio_path)
            return duration
        except ImportError:
            # Fallback avec pydub
            from pydub import AudioSegment
            audio = AudioSegment.from_file(audio_path)
            return len(audio) / 1000.0
        except Exception as e:
            logger.error(f"Erreur calcul durée audio: {e}")
            return 0.0
    
    def estimate_processing_time(self, audio_duration: float) -> float:
        """
        Estime le temps de traitement
        
        Args:
            audio_duration: Durée de l'audio en secondes
            
        Returns:
            Temps estimé en secondes
        """
        # Ratios approximatifs selon device et modèle
        ratios = {
            "cuda": {"tiny": 0.05, "base": 0.1, "small": 0.2, "medium": 0.4, "large": 0.8},
            "mps": {"tiny": 0.1, "base": 0.2, "small": 0.4, "medium": 0.8, "large": 1.5},
            "cpu": {"tiny": 0.3, "base": 0.5, "small": 1.0, "medium": 2.0, "large": 4.0}
        }
        
        ratio = ratios.get(self.device, ratios["cpu"]).get(self.model_size, 1.0)
        return audio_duration * ratio


# Instance singleton
_transcription_service: Optional[HypocrateTranscriptionService] = None


def get_hypocrate_transcription_service(model_size: str = "base") -> HypocrateTranscriptionService:
    """
    Obtient l'instance du service de transcription
    
    Args:
        model_size: Taille du modèle Whisper
        
    Returns:
        Instance du service
    """
    global _transcription_service
    
    if _transcription_service is None or _transcription_service.model_size != model_size:
        _transcription_service = HypocrateTranscriptionService(model_size=model_size)
    
    return _transcription_service
