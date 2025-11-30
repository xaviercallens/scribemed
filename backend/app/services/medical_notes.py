"""Medical note generation service using local Llama/Mistral."""
import json
import logging
import time
from typing import Dict, Optional, List

from .ollama_service import get_ollama_service

logger = logging.getLogger(__name__)


MEDICAL_SCRIBE_SYSTEM_PROMPT = """You are an expert medical scribe assistant. Your role is to convert doctor-patient conversations into structured, professional medical notes.

Guidelines:
1. Extract only information explicitly stated in the conversation
2. Use proper medical terminology
3. Be concise and accurate
4. Follow SOAP note format (Subjective, Objective, Assessment, Plan)
5. Flag any allergies or contraindications
6. Do not make assumptions or add information not in the conversation

Output Format: JSON with these fields:
- subjective: Patient's complaints and history
- objective: Observable findings and vital signs
- assessment: Diagnosis or clinical impression
- plan: Treatment plan and follow-up
- chief_complaint: Primary reason for visit
- allergies: List of allergies (empty list if none)
- medications: List of medications discussed (empty list if none)"""


class MedicalNoteService:
    """Service for generating medical notes from transcripts."""
    
    def __init__(self):
        """Initialize medical note service."""
        self.ollama = get_ollama_service()
        logger.info("Medical note service initialized")
    
    def generate_soap_note(
        self,
        transcript: str,
        patient_context: Optional[Dict] = None
    ) -> Dict[str, any]:
        """Generate SOAP note from transcript.
        
        Args:
            transcript: Transcribed conversation
            patient_context: Optional patient context (age, gender, etc.)
            
        Returns:
            Dict with SOAP note and metadata
        """
        try:
            start_time = time.time()
            
            # Build prompt
            prompt = self._build_soap_prompt(transcript, patient_context)
            
            logger.info("Generating SOAP note with Llama/Mistral")
            
            # Generate with Ollama
            response = self.ollama.generate(
                prompt=prompt,
                system_prompt=MEDICAL_SCRIBE_SYSTEM_PROMPT,
                temperature=0.3,  # Lower temperature for consistency
                max_tokens=1500
            )
            
            generation_time = time.time() - start_time
            
            # Parse response
            soap_note = self._parse_soap_response(response['response'])
            
            return {
                "soap_note": soap_note,
                "model_used": response['model'],
                "generation_time_seconds": generation_time,
                "prompt_tokens": response.get('prompt_eval_count', 0),
                "completion_tokens": response.get('eval_count', 0),
                "raw_response": response['response']
            }
            
        except Exception as e:
            logger.error(f"SOAP note generation failed: {e}")
            raise Exception(f"Failed to generate SOAP note: {str(e)}")
    
    def _build_soap_prompt(
        self,
        transcript: str,
        patient_context: Optional[Dict] = None
    ) -> str:
        """Build prompt for SOAP note generation.
        
        Args:
            transcript: Conversation transcript
            patient_context: Optional patient information
            
        Returns:
            Formatted prompt
        """
        prompt = "Convert the following doctor-patient conversation into a structured SOAP note.\n\n"
        
        if patient_context:
            prompt += "Patient Context:\n"
            for key, value in patient_context.items():
                prompt += f"- {key}: {value}\n"
            prompt += "\n"
        
        prompt += f"Conversation:\n{transcript}\n\n"
        prompt += "Generate a structured SOAP note in JSON format with the fields specified in the system prompt."
        
        return prompt
    
    def _parse_soap_response(self, response: str) -> Dict[str, any]:
        """Parse LLM response into structured SOAP note.
        
        Args:
            response: Raw LLM response
            
        Returns:
            Parsed SOAP note dict
        """
        try:
            # Try to extract JSON from response
            # Look for JSON block
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                soap_note = json.loads(json_str)
            else:
                # Fallback: parse as text
                soap_note = self._parse_text_soap(response)
            
            # Ensure required fields
            soap_note.setdefault('subjective', '')
            soap_note.setdefault('objective', '')
            soap_note.setdefault('assessment', '')
            soap_note.setdefault('plan', '')
            soap_note.setdefault('chief_complaint', '')
            soap_note.setdefault('allergies', [])
            soap_note.setdefault('medications', [])
            
            return soap_note
            
        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON, using text parsing")
            return self._parse_text_soap(response)
        except Exception as e:
            logger.error(f"Failed to parse SOAP response: {e}")
            return {
                "subjective": "",
                "objective": "",
                "assessment": "",
                "plan": "",
                "chief_complaint": "",
                "allergies": [],
                "medications": [],
                "raw_text": response
            }
    
    def _parse_text_soap(self, text: str) -> Dict[str, any]:
        """Parse SOAP note from plain text.
        
        Args:
            text: Plain text response
            
        Returns:
            Structured SOAP note
        """
        soap_note = {
            "subjective": "",
            "objective": "",
            "assessment": "",
            "plan": "",
            "chief_complaint": "",
            "allergies": [],
            "medications": []
        }
        
        # Simple text parsing
        lines = text.split('\n')
        current_section = None
        
        for line in lines:
            line_lower = line.lower().strip()
            
            if 'subjective' in line_lower:
                current_section = 'subjective'
            elif 'objective' in line_lower:
                current_section = 'objective'
            elif 'assessment' in line_lower:
                current_section = 'assessment'
            elif 'plan' in line_lower:
                current_section = 'plan'
            elif current_section and line.strip():
                soap_note[current_section] += line.strip() + " "
        
        # Clean up
        for key in ['subjective', 'objective', 'assessment', 'plan']:
            soap_note[key] = soap_note[key].strip()
        
        return soap_note
    
    def extract_medical_entities(self, transcript: str) -> Dict[str, List[str]]:
        """Extract medical entities from transcript.
        
        Args:
            transcript: Conversation transcript
            
        Returns:
            Dict with extracted entities (symptoms, medications, allergies)
        """
        try:
            prompt = f"""Extract medical entities from this conversation:

{transcript}

List:
1. Symptoms mentioned
2. Medications discussed
3. Allergies mentioned
4. Medical conditions

Format as JSON with keys: symptoms, medications, allergies, conditions"""
            
            response = self.ollama.generate(
                prompt=prompt,
                temperature=0.2,
                max_tokens=500
            )
            
            # Parse response
            entities = self._parse_entities_response(response['response'])
            return entities
            
        except Exception as e:
            logger.error(f"Entity extraction failed: {e}")
            return {
                "symptoms": [],
                "medications": [],
                "allergies": [],
                "conditions": []
            }
    
    def _parse_entities_response(self, response: str) -> Dict[str, List[str]]:
        """Parse entity extraction response.
        
        Args:
            response: Raw response
            
        Returns:
            Parsed entities
        """
        try:
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                entities = json.loads(json_str)
                return entities
        except:
            pass
        
        # Fallback
        return {
            "symptoms": [],
            "medications": [],
            "allergies": [],
            "conditions": []
        }


# Singleton instance
_medical_note_service: Optional[MedicalNoteService] = None


def get_medical_note_service() -> MedicalNoteService:
    """Get or create medical note service instance.
    
    Returns:
        MedicalNoteService instance
    """
    global _medical_note_service
    if _medical_note_service is None:
        _medical_note_service = MedicalNoteService()
    return _medical_note_service
