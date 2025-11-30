"""
Configuration Hypocrate
"""

from .prompts import (
    MEDICAL_SCRIBE_SYSTEM_PROMPT,
    SOAP_GENERATION_PROMPT,
    LETTER_GENERATION_PROMPT,
    build_soap_prompt,
    build_letter_prompt,
    get_specialty_context
)

__all__ = [
    'MEDICAL_SCRIBE_SYSTEM_PROMPT',
    'SOAP_GENERATION_PROMPT',
    'LETTER_GENERATION_PROMPT',
    'build_soap_prompt',
    'build_letter_prompt',
    'get_specialty_context',
]
