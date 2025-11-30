"""
Prompts pour la génération de contenu médical avec LLM
"""

MEDICAL_SCRIBE_SYSTEM_PROMPT = """Tu es Hypocrate, un assistant médical expert spécialisé dans la rédaction de documents cliniques.

RÈGLES IMPORTANTES:
1. Extrais UNIQUEMENT les informations explicitement mentionnées dans la conversation
2. Utilise une terminologie médicale appropriée et professionnelle
3. Sois concis, précis et factuel
4. Suis strictement le format SOAP (Subjectif, Objectif, Analyse, Plan)
5. Signale toute allergie ou contre-indication
6. Ne fais AUCUNE supposition ou ajout d'information non mentionnée
7. Réponds TOUJOURS en français médical professionnel

FORMAT DE SORTIE:
Génère un document JSON avec ces champs obligatoires:
{
  "subjectif": "Plaintes et historique du patient",
  "objectif": "Observations cliniques et examens",
  "analyse": "Diagnostic ou impression clinique",
  "plan": "Plan de traitement et suivi",
  "chief_complaint": "Motif principal de consultation",
  "allergies": ["liste des allergies"],
  "medications": ["liste des médicaments discutés"],
  "vital_signs": {
    "temperature": "valeur si mentionnée",
    "blood_pressure": "valeur si mentionnée",
    "heart_rate": "valeur si mentionnée"
  }
}
"""

SOAP_GENERATION_PROMPT = """Analyse la consultation médicale suivante et génère un compte-rendu SOAP structuré.

CONTEXTE PATIENT:
{patient_context}

TRANSCRIPTION DE LA CONSULTATION:
{transcript}

ENTITÉS MÉDICALES DÉTECTÉES:
{entities}

INSTRUCTIONS:
- Génère un compte-rendu SOAP complet et professionnel
- Intègre toutes les entités médicales détectées
- Respecte le format JSON spécifié
- Sois factuel et précis
- Signale toute information critique (allergies, contre-indications)

Génère maintenant le compte-rendu au format JSON:
"""

LETTER_GENERATION_PROMPT = """Rédige une lettre d'adressage médicale professionnelle basée sur ce compte-rendu SOAP.

COMPTE-RENDU SOAP:
{soap_note}

INFORMATIONS DESTINATAIRE:
Spécialité: {specialty}
Type de lettre: {letter_type}

PATIENT:
{patient_info}

INSTRUCTIONS:
- Rédige une lettre formelle et professionnelle
- Commence par "Madame, Monsieur," ou "Cher(e) Confrère/Consœur,"
- Résume le motif de consultation
- Mentionne les éléments cliniques pertinents
- Indique clairement la demande (avis, prise en charge, etc.)
- Termine par une formule de politesse appropriée
- Signe "Dr. [Nom du médecin traitant]"

Rédige maintenant la lettre:
"""

ENTITY_EXTRACTION_PROMPT = """Extrais les entités médicales de cette transcription.

TRANSCRIPTION:
{transcript}

Identifie et liste:
1. SYMPTÔMES: tous les symptômes mentionnés
2. DIAGNOSTICS: diagnostics évoqués ou confirmés
3. MÉDICAMENTS: tous les médicaments cités
4. ALLERGIES: toutes les allergies mentionnées
5. ANTÉCÉDENTS: antécédents médicaux pertinents
6. EXAMENS: examens cliniques ou paracliniques réalisés
7. CONSTANTES: température, tension, fréquence cardiaque, etc.

Format JSON:
{
  "symptoms": ["liste"],
  "diagnoses": ["liste"],
  "medications": ["liste"],
  "allergies": ["liste"],
  "medical_history": ["liste"],
  "examinations": ["liste"],
  "vital_signs": {
    "temperature": "valeur",
    "blood_pressure": "valeur",
    "heart_rate": "valeur"
  }
}
"""

VALIDATION_PROMPT = """Vérifie la cohérence et la sécurité de ce compte-rendu médical.

COMPTE-RENDU:
{soap_note}

ALLERGIES CONNUES:
{allergies}

MÉDICAMENTS PRESCRITS:
{medications}

VÉRIFICATIONS À EFFECTUER:
1. Cohérence entre allergies et médicaments prescrits
2. Présence de toutes les sections SOAP
3. Cohérence entre symptômes et diagnostic
4. Clarté du plan de traitement
5. Mentions de suivi appropriées

Retourne un JSON:
{
  "is_valid": true/false,
  "warnings": ["liste des avertissements"],
  "errors": ["liste des erreurs critiques"],
  "suggestions": ["liste de suggestions d'amélioration"]
}
"""

# Prompts spécifiques par spécialité
SPECIALTY_PROMPTS = {
    "Cardiologie": {
        "focus": "Concentre-toi sur les antécédents cardiovasculaires, facteurs de risque, symptômes cardiaques.",
        "vital_signs": ["tension artérielle", "fréquence cardiaque", "saturation O2"]
    },
    "ORL": {
        "focus": "Détaille l'examen ORL (gorge, oreilles, nez), symptômes respiratoires hauts.",
        "examinations": ["examen pharyngé", "otoscopie", "rhinoscopie"]
    },
    "Pédiatrie": {
        "focus": "Mentionne l'âge, le poids, la taille, le développement psychomoteur.",
        "vital_signs": ["température", "poids", "taille", "périmètre crânien"]
    },
    "Généraliste": {
        "focus": "Approche globale, tous systèmes, prévention.",
        "vital_signs": ["température", "tension", "poids"]
    }
}

def get_specialty_context(specialty: str) -> str:
    """Retourne le contexte spécifique à une spécialité"""
    context = SPECIALTY_PROMPTS.get(specialty, SPECIALTY_PROMPTS["Généraliste"])
    return f"\nCONTEXTE SPÉCIALITÉ: {context['focus']}\n"

def build_soap_prompt(transcript: str, entities: dict, patient_context: str = "", specialty: str = "Généraliste") -> str:
    """Construit le prompt complet pour génération SOAP"""
    specialty_ctx = get_specialty_context(specialty)
    
    entities_str = "\n".join([
        f"- Symptômes: {', '.join(entities.get('symptoms', []))}",
        f"- Diagnostics: {', '.join(entities.get('diagnoses', []))}",
        f"- Médicaments: {', '.join(entities.get('medications', []))}",
        f"- Allergies: {', '.join(entities.get('allergies', []))}",
    ])
    
    return SOAP_GENERATION_PROMPT.format(
        patient_context=patient_context + specialty_ctx,
        transcript=transcript,
        entities=entities_str
    )

def build_letter_prompt(soap_note: dict, specialty: str, patient_info: str, letter_type: str = "adressage") -> str:
    """Construit le prompt pour génération de lettre"""
    soap_str = f"""
SUBJECTIF: {soap_note.get('subjectif', '')}
OBJECTIF: {soap_note.get('objectif', '')}
ANALYSE: {soap_note.get('analyse', '')}
PLAN: {soap_note.get('plan', '')}
    """
    
    return LETTER_GENERATION_PROMPT.format(
        soap_note=soap_str,
        specialty=specialty,
        patient_info=patient_info,
        letter_type=letter_type
    )
