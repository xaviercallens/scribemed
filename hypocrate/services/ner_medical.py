"""
Service d'extraction d'entités médicales (NER) pour Hypocrate
Utilise scispaCy pour la détection d'entités biomédicales
"""
import spacy
import re
import logging
from typing import Dict, List, Set
from collections import defaultdict

logger = logging.getLogger(__name__)


class MedicalNERService:
    """Service d'extraction d'entités médicales"""
    
    def __init__(self, language: str = "fr"):
        """
        Initialise le service NER
        
        Args:
            language: Langue du modèle (fr ou en)
        """
        self.language = language
        self.nlp_fr = None
        self.nlp_en = None
        self.nlp_sci = None
        
        logger.info(f"Initialisation NER médical (langue: {language})")
    
    def _load_models(self):
        """Charge les modèles spaCy (lazy loading)"""
        try:
            if self.nlp_fr is None and self.language == "fr":
                logger.info("Chargement modèle spaCy français...")
                self.nlp_fr = spacy.load("fr_core_news_md")
            
            if self.nlp_en is None:
                logger.info("Chargement modèle spaCy anglais...")
                self.nlp_en = spacy.load("en_core_web_sm")
            
            if self.nlp_sci is None:
                logger.info("Chargement modèle scispaCy médical...")
                self.nlp_sci = spacy.load("en_ner_bc5cdr_md")
            
            logger.info("Modèles NER chargés avec succès")
            
        except Exception as e:
            logger.error(f"Erreur chargement modèles NER: {e}")
            logger.warning("Certaines fonctionnalités NER seront limitées")
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extrait toutes les entités médicales d'un texte
        
        Args:
            text: Texte de la consultation
            
        Returns:
            Dict avec les entités par catégorie
        """
        self._load_models()
        
        entities = {
            "symptoms": [],
            "diagnoses": [],
            "medications": [],
            "allergies": [],
            "medical_history": [],
            "examinations": [],
            "vital_signs": {}
        }
        
        # Extraction avec règles
        entities["allergies"] = self._extract_allergies(text)
        entities["vital_signs"] = self._extract_vital_signs(text)
        entities["medications"] = self._extract_medications(text)
        
        # Extraction avec scispaCy (maladies et substances chimiques)
        if self.nlp_sci:
            sci_entities = self._extract_with_scispacy(text)
            entities["diagnoses"].extend(sci_entities.get("diseases", []))
            entities["medications"].extend(sci_entities.get("chemicals", []))
        
        # Extraction avec spaCy standard
        if self.language == "fr" and self.nlp_fr:
            fr_entities = self._extract_with_spacy(text, self.nlp_fr)
            entities["symptoms"].extend(fr_entities.get("symptoms", []))
        
        # Déduplique et nettoie
        for key in entities:
            if isinstance(entities[key], list):
                entities[key] = list(set([e.strip() for e in entities[key] if e.strip()]))
        
        logger.info(f"Entités extraites: {sum(len(v) if isinstance(v, list) else len(v) for v in entities.values())} au total")
        
        return entities
    
    def _extract_allergies(self, text: str) -> List[str]:
        """Extrait les allergies avec des règles"""
        allergies = []
        
        # Patterns pour détecter les allergies
        patterns = [
            r"allergi(?:que|e)?\s+(?:à|au|aux)\s+([a-zéèêàâôù\s-]+)",
            r"allergi(?:que|e)?\s*:\s*([a-zéèêàâôù\s,-]+)",
            r"ne\s+(?:peut|doit)\s+pas\s+prendre\s+(?:de|d')?\s*([a-zéèêàâôù\s-]+)",
            r"intoléran(?:ce|t)\s+(?:à|au|aux)\s+([a-zéèêàâôù\s-]+)",
        ]
        
        text_lower = text.lower()
        
        for pattern in patterns:
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                allergy = match.group(1).strip()
                # Nettoie et capitalise
                allergy = allergy.split(',')[0].split('et')[0].strip()
                if len(allergy) > 2:
                    allergies.append(allergy.capitalize())
        
        return allergies
    
    def _extract_vital_signs(self, text: str) -> Dict[str, str]:
        """Extrait les constantes vitales"""
        vital_signs = {}
        
        # Température
        temp_pattern = r"(?:température|temp|T°?)\s*:?\s*(\d+(?:[.,]\d+)?)\s*°?C?"
        temp_match = re.search(temp_pattern, text, re.IGNORECASE)
        if temp_match:
            vital_signs["temperature"] = f"{temp_match.group(1)}°C"
        
        # Tension artérielle
        bp_pattern = r"(?:tension|TA|PA)\s*:?\s*(\d+)\s*/\s*(\d+)"
        bp_match = re.search(bp_pattern, text, re.IGNORECASE)
        if bp_match:
            vital_signs["blood_pressure"] = f"{bp_match.group(1)}/{bp_match.group(2)} mmHg"
        
        # Fréquence cardiaque
        hr_pattern = r"(?:fréquence cardiaque|FC|pouls)\s*:?\s*(\d+)"
        hr_match = re.search(hr_pattern, text, re.IGNORECASE)
        if hr_match:
            vital_signs["heart_rate"] = f"{hr_match.group(1)} bpm"
        
        # Saturation O2
        spo2_pattern = r"(?:saturation|SpO2|SaO2)\s*:?\s*(\d+)\s*%?"
        spo2_match = re.search(spo2_pattern, text, re.IGNORECASE)
        if spo2_match:
            vital_signs["oxygen_saturation"] = f"{spo2_match.group(1)}%"
        
        return vital_signs
    
    def _extract_medications(self, text: str) -> List[str]:
        """Extrait les médicaments mentionnés"""
        medications = []
        
        # Liste de médicaments courants (à étendre)
        common_meds = [
            "paracétamol", "ibuprofène", "aspirine", "doliprane",
            "amoxicilline", "pénicilline", "antibiotique",
            "anti-inflammatoire", "antalgique", "corticoïde"
        ]
        
        text_lower = text.lower()
        
        for med in common_meds:
            if med in text_lower:
                medications.append(med.capitalize())
        
        # Pattern pour médicaments avec posologie
        med_pattern = r"(?:prendre|prescrire|donner)\s+(?:de|du|des)?\s*([A-ZÉÈa-zéèêàâôù]+(?:\s+\d+(?:mg|g|ml)?)?)"
        matches = re.finditer(med_pattern, text, re.IGNORECASE)
        
        for match in matches:
            med = match.group(1).strip()
            if len(med) > 3 and not med.lower() in ["fois", "jour", "soir", "matin"]:
                medications.append(med.capitalize())
        
        return medications
    
    def _extract_with_scispacy(self, text: str) -> Dict[str, List[str]]:
        """Extrait entités avec scispaCy (maladies et substances)"""
        entities = defaultdict(list)
        
        if not self.nlp_sci:
            return entities
        
        try:
            doc = self.nlp_sci(text)
            
            for ent in doc.ents:
                if ent.label_ == "DISEASE":
                    entities["diseases"].append(ent.text)
                elif ent.label_ == "CHEMICAL":
                    entities["chemicals"].append(ent.text)
            
        except Exception as e:
            logger.error(f"Erreur scispaCy: {e}")
        
        return dict(entities)
    
    def _extract_with_spacy(self, text: str, nlp) -> Dict[str, List[str]]:
        """Extrait entités avec spaCy standard"""
        entities = defaultdict(list)
        
        try:
            doc = nlp(text)
            
            # Mots-clés symptômes
            symptom_keywords = [
                "douleur", "mal", "fièvre", "toux", "fatigue",
                "nausée", "vomissement", "diarrhée", "constipation",
                "vertige", "maux de tête", "migraine"
            ]
            
            for token in doc:
                if token.lemma_ in symptom_keywords:
                    # Capture le contexte (2 mots avant et après)
                    start = max(0, token.i - 2)
                    end = min(len(doc), token.i + 3)
                    symptom = doc[start:end].text
                    entities["symptoms"].append(symptom)
            
        except Exception as e:
            logger.error(f"Erreur spaCy: {e}")
        
        return dict(entities)
    
    def format_entities_display(self, entities: Dict) -> str:
        """Formate les entités pour affichage"""
        lines = []
        
        emoji_map = {
            "symptoms": "🤒",
            "diagnoses": "🏷️",
            "medications": "💊",
            "allergies": "⚠️",
            "examinations": "🔬",
            "vital_signs": "📏"
        }
        
        for category, items in entities.items():
            if category == "vital_signs":
                if items:
                    lines.append(f"\n{emoji_map.get(category, '•')} **Constantes vitales:**")
                    for key, value in items.items():
                        lines.append(f"  - {key.replace('_', ' ').title()}: {value}")
            elif items:
                emoji = emoji_map.get(category, '•')
                category_name = category.replace('_', ' ').title()
                lines.append(f"\n{emoji} **{category_name}:**")
                for item in items:
                    lines.append(f"  - {item}")
        
        return "\n".join(lines) if lines else "Aucune entité médicale détectée"


# Instance singleton
_ner_service: Optional[MedicalNERService] = None


def get_medical_ner_service(language: str = "fr") -> MedicalNERService:
    """
    Obtient l'instance du service NER
    
    Args:
        language: Langue du service
        
    Returns:
        Instance du service
    """
    global _ner_service
    
    if _ner_service is None or _ner_service.language != language:
        _ner_service = MedicalNERService(language=language)
    
    return _ner_service
