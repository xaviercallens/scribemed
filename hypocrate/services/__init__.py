"""
Services Hypocrate - Assistant Médical IA
"""

from .transcription_hypocrate import get_hypocrate_transcription_service, HypocrateTranscriptionService
from .ner_medical import get_medical_ner_service, MedicalNERService
from .soap_generator import get_soap_generator, SOAPGenerator
from .letter_generator import get_letter_generator, LetterGenerator

__all__ = [
    'get_hypocrate_transcription_service',
    'HypocrateTranscriptionService',
    'get_medical_ner_service',
    'MedicalNERService',
    'get_soap_generator',
    'SOAPGenerator',
    'get_letter_generator',
    'LetterGenerator',
]
