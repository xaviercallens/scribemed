"""
Générateur de comptes-rendus SOAP avec Llama2 local via Ollama
"""
import ollama
import json
import logging
import time
import re
from typing import Dict, Optional

from ..config.prompts import (
    MEDICAL_SCRIBE_SYSTEM_PROMPT,
    build_soap_prompt,
    VALIDATION_PROMPT
)

logger = logging.getLogger(__name__)


class SOAPGenerator:
    """Générateur de comptes-rendus SOAP avec LLM local"""
    
    def __init__(self, model: str = "llama2:latest"):
        """
        Initialise le générateur SOAP
        
        Args:
            model: Modèle Ollama à utiliser
        """
        self.model = model
        logger.info(f"Initialisation générateur SOAP avec {model}")
        
        # Vérifie que le modèle est disponible
        self._check_model_availability()
    
    def _check_model_availability(self):
        """Vérifie que le modèle Ollama est disponible"""
        try:
            models_response = ollama.list()
            available_models = [m.model for m in models_response.models]
            
            if self.model not in available_models:
                logger.warning(f"Modèle {self.model} non trouvé. Modèles disponibles: {available_models}")
                logger.info(f"Tentative de pull du modèle {self.model}...")
                ollama.pull(self.model)
            else:
                logger.info(f"Modèle {self.model} disponible")
                
        except Exception as e:
            logger.error(f"Erreur vérification modèle: {e}")
            raise RuntimeError(f"Ollama n'est pas accessible. Assurez-vous qu'Ollama est lancé: ollama serve")
    
    def generate_soap_note(
        self,
        transcript: str,
        entities: Dict,
        patient_context: str = "",
        specialty: str = "Généraliste"
    ) -> Dict:
        """
        Génère un compte-rendu SOAP à partir d'une transcription
        
        Args:
            transcript: Transcription de la consultation
            entities: Entités médicales extraites
            patient_context: Contexte patient (âge, sexe, etc.)
            specialty: Spécialité médicale
            
        Returns:
            Dict avec le compte-rendu SOAP et métadonnées
        """
        try:
            start_time = time.time()
            
            # Construction du prompt
            prompt = build_soap_prompt(
                transcript=transcript,
                entities=entities,
                patient_context=patient_context,
                specialty=specialty
            )
            
            logger.info(f"Génération SOAP avec {self.model}...")
            
            # Génération avec Ollama
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": MEDICAL_SCRIBE_SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                options={
                    "temperature": 0.3,  # Faible pour cohérence
                    "num_predict": 2000,  # Max tokens
                    "top_p": 0.9,
                }
            )
            
            generation_time = time.time() - start_time
            
            # Parse la réponse
            soap_note = self._parse_soap_response(response['message']['content'])
            
            # Validation
            validation = self._validate_soap_note(soap_note, entities)
            
            result = {
                "soap_note": soap_note,
                "model_used": self.model,
                "generation_time_seconds": generation_time,
                "validation": validation,
                "raw_response": response['message']['content']
            }
            
            logger.info(f"SOAP généré en {generation_time:.2f}s")
            
            return result
            
        except Exception as e:
            logger.error(f"Erreur génération SOAP: {e}")
            raise
    
    def _parse_soap_response(self, response: str) -> Dict:
        """Parse la réponse LLM en structure SOAP"""
        try:
            # Essaie d'extraire le JSON
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            
            if json_match:
                soap_note = json.loads(json_match.group())
            else:
                # Fallback: parse texte
                soap_note = self._parse_text_soap(response)
            
            # Assure les champs obligatoires
            soap_note.setdefault('subjectif', '')
            soap_note.setdefault('objectif', '')
            soap_note.setdefault('analyse', '')
            soap_note.setdefault('plan', '')
            soap_note.setdefault('chief_complaint', '')
            soap_note.setdefault('allergies', [])
            soap_note.setdefault('medications', [])
            soap_note.setdefault('vital_signs', {})
            
            return soap_note
            
        except json.JSONDecodeError:
            logger.warning("Échec parse JSON, utilisation parse texte")
            return self._parse_text_soap(response)
        except Exception as e:
            logger.error(f"Erreur parse réponse: {e}")
            return {
                "subjectif": "",
                "objectif": "",
                "analyse": "",
                "plan": "",
                "chief_complaint": "",
                "allergies": [],
                "medications": [],
                "vital_signs": {},
                "raw_text": response
            }
    
    def _parse_text_soap(self, text: str) -> Dict:
        """Parse un SOAP en texte libre"""
        soap_note = {
            "subjectif": "",
            "objectif": "",
            "analyse": "",
            "plan": "",
            "chief_complaint": "",
            "allergies": [],
            "medications": [],
            "vital_signs": {}
        }
        
        # Patterns pour sections SOAP
        sections = {
            "subjectif": r"(?:SUBJECTIF|Subjectif|S:)(.*?)(?=OBJECTIF|Objectif|O:|ANALYSE|$)",
            "objectif": r"(?:OBJECTIF|Objectif|O:)(.*?)(?=ANALYSE|Analyse|A:|PLAN|$)",
            "analyse": r"(?:ANALYSE|Analyse|ASSESSMENT|A:)(.*?)(?=PLAN|Plan|P:|$)",
            "plan": r"(?:PLAN|Plan|P:)(.*?)$"
        }
        
        for section, pattern in sections.items():
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                soap_note[section] = match.group(1).strip()
        
        return soap_note
    
    def _validate_soap_note(self, soap_note: Dict, entities: Dict) -> Dict:
        """Valide la cohérence du SOAP"""
        validation = {
            "is_valid": True,
            "warnings": [],
            "errors": [],
            "suggestions": []
        }
        
        # Vérifie sections obligatoires
        required_sections = ["subjectif", "objectif", "analyse", "plan"]
        for section in required_sections:
            if not soap_note.get(section):
                validation["errors"].append(f"Section '{section}' manquante ou vide")
                validation["is_valid"] = False
        
        # Vérifie cohérence allergies
        soap_allergies = [a.lower() for a in soap_note.get("allergies", [])]
        soap_meds = [m.lower() for m in soap_note.get("medications", [])]
        
        # Détecte conflits allergie/médicament
        for allergy in soap_allergies:
            for med in soap_meds:
                if allergy in med or med in allergy:
                    validation["warnings"].append(
                        f"⚠️ ATTENTION: Allergie '{allergy}' et médicament '{med}' - Vérifier compatibilité"
                    )
        
        # Suggestions
        if len(soap_note.get("subjectif", "")) < 20:
            validation["suggestions"].append("Section Subjectif très courte - Vérifier complétude")
        
        if len(soap_note.get("plan", "")) < 20:
            validation["suggestions"].append("Plan de traitement court - Vérifier si complet")
        
        return validation
    
    def format_soap_display(self, soap_note: Dict) -> str:
        """Formate le SOAP pour affichage"""
        sections = []
        
        # Motif de consultation
        if soap_note.get("chief_complaint"):
            sections.append(f"**MOTIF DE CONSULTATION**\n{soap_note['chief_complaint']}\n")
        
        # Sections SOAP
        soap_sections = [
            ("SUBJECTIF", "subjectif"),
            ("OBJECTIF", "objectif"),
            ("ANALYSE", "analyse"),
            ("PLAN", "plan")
        ]
        
        for title, key in soap_sections:
            if soap_note.get(key):
                sections.append(f"**{title}**\n{soap_note[key]}\n")
        
        # Allergies
        if soap_note.get("allergies"):
            allergies_str = ", ".join(soap_note["allergies"])
            sections.append(f"**⚠️ ALLERGIES**\n{allergies_str}\n")
        
        # Constantes vitales
        if soap_note.get("vital_signs"):
            vs_lines = []
            for key, value in soap_note["vital_signs"].items():
                vs_lines.append(f"- {key.replace('_', ' ').title()}: {value}")
            if vs_lines:
                sections.append(f"**📏 CONSTANTES VITALES**\n" + "\n".join(vs_lines) + "\n")
        
        return "\n".join(sections)


# Instance singleton
_soap_generator: Optional[SOAPGenerator] = None


def get_soap_generator(model: str = "llama2:latest") -> SOAPGenerator:
    """
    Obtient l'instance du générateur SOAP
    
    Args:
        model: Modèle Ollama à utiliser
        
    Returns:
        Instance du générateur
    """
    global _soap_generator
    
    if _soap_generator is None or _soap_generator.model != model:
        _soap_generator = SOAPGenerator(model=model)
    
    return _soap_generator
