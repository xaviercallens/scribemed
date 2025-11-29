"""
Générateur de lettres d'adressage médical
"""
import ollama
import logging
import time
from typing import Dict, Optional
from datetime import datetime

from ..config.prompts import build_letter_prompt, MEDICAL_SCRIBE_SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class LetterGenerator:
    """Générateur de lettres d'adressage professionnelles"""
    
    def __init__(self, model: str = "llama2:latest"):
        """
        Initialise le générateur de lettres
        
        Args:
            model: Modèle Ollama à utiliser
        """
        self.model = model
        logger.info(f"Initialisation générateur de lettres avec {model}")
    
    def generate_referral_letter(
        self,
        soap_note: Dict,
        specialty: str = "Spécialiste",
        patient_name: str = "Patient",
        doctor_name: str = "Dr. Médecin Traitant",
        letter_type: str = "adressage"
    ) -> Dict:
        """
        Génère une lettre d'adressage
        
        Args:
            soap_note: Compte-rendu SOAP
            specialty: Spécialité du destinataire
            patient_name: Nom du patient
            doctor_name: Nom du médecin
            letter_type: Type de lettre
            
        Returns:
            Dict avec la lettre et métadonnées
        """
        try:
            start_time = time.time()
            
            # Info patient
            patient_info = f"Patient: {patient_name}"
            if soap_note.get("chief_complaint"):
                patient_info += f"\nMotif: {soap_note['chief_complaint']}"
            
            # Construction du prompt
            prompt = build_letter_prompt(
                soap_note=soap_note,
                specialty=specialty,
                patient_info=patient_info,
                letter_type=letter_type
            )
            
            logger.info(f"Génération lettre d'adressage pour {specialty}...")
            
            # Génération avec Ollama
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Tu es un assistant médical expert en rédaction de correspondance médicale professionnelle."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                options={
                    "temperature": 0.4,
                    "num_predict": 1500,
                }
            )
            
            generation_time = time.time() - start_time
            
            # Formate la lettre
            letter_text = response['message']['content'].strip()
            
            # Ajoute signature si absente
            if not any(sig in letter_text.lower() for sig in ["cordialement", "salutations", "bien à vous"]):
                letter_text += f"\n\nBien cordialement,\n{doctor_name}"
            
            # Ajoute date si absente
            if "date" not in letter_text.lower()[:100]:
                date_str = datetime.now().strftime("%d/%m/%Y")
                letter_text = f"Le {date_str}\n\n{letter_text}"
            
            result = {
                "letter": letter_text,
                "specialty": specialty,
                "patient_name": patient_name,
                "doctor_name": doctor_name,
                "generation_time_seconds": generation_time,
                "model_used": self.model
            }
            
            logger.info(f"Lettre générée en {generation_time:.2f}s")
            
            return result
            
        except Exception as e:
            logger.error(f"Erreur génération lettre: {e}")
            raise
    
    def format_letter_display(self, letter: str) -> str:
        """Formate la lettre pour affichage"""
        # Ajoute un cadre visuel
        lines = letter.split('\n')
        formatted_lines = []
        
        for line in lines:
            # Met en évidence les formules de politesse
            if any(word in line.lower() for word in ["madame", "monsieur", "cher", "chère"]):
                formatted_lines.append(f"**{line}**")
            elif any(word in line.lower() for word in ["cordialement", "salutations", "bien à vous"]):
                formatted_lines.append(f"\n*{line}*")
            else:
                formatted_lines.append(line)
        
        return "\n".join(formatted_lines)


# Instance singleton
_letter_generator: Optional[LetterGenerator] = None


def get_letter_generator(model: str = "llama2:latest") -> LetterGenerator:
    """
    Obtient l'instance du générateur de lettres
    
    Args:
        model: Modèle Ollama à utiliser
        
    Returns:
        Instance du générateur
    """
    global _letter_generator
    
    if _letter_generator is None or _letter_generator.model != model:
        _letter_generator = LetterGenerator(model=model)
    
    return _letter_generator
