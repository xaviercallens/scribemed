"""
🏥 SUMY - Assistant Médical IA
Application Streamlit principale
"""
import streamlit as st
import logging
from pathlib import Path
import tempfile
import time

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration page
st.set_page_config(
    page_title="SUMY - Assistant Médical IA",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    .entity-tag {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        margin: 0.25rem;
        border-radius: 1rem;
        font-size: 0.9rem;
    }
    .allergy-tag {
        background-color: #ffebee;
        color: #c62828;
        border: 1px solid #ef5350;
    }
    .medication-tag {
        background-color: #e3f2fd;
        color: #1565c0;
        border: 1px solid #42a5f5;
    }
    .symptom-tag {
        background-color: #fff3e0;
        color: #e65100;
        border: 1px solid #ff9800;
    }
    .diagnosis-tag {
        background-color: #f3e5f5;
        color: #6a1b9a;
        border: 1px solid #ab47bc;
    }
    .warning-box {
        padding: 1rem;
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Import des services
from services.transcription_hypocrate import get_hypocrate_transcription_service
from services.ner_medical import get_medical_ner_service
from services.soap_generator import get_soap_generator
from services.letter_generator import get_letter_generator


def init_session_state():
    """Initialise l'état de session"""
    if 'transcript' not in st.session_state:
        st.session_state.transcript = None
    if 'entities' not in st.session_state:
        st.session_state.entities = None
    if 'soap_note' not in st.session_state:
        st.session_state.soap_note = None
    if 'letter' not in st.session_state:
        st.session_state.letter = None
    if 'processing' not in st.session_state:
        st.session_state.processing = False


def display_header():
    """Affiche l'en-tête de l'application"""
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.image("assets/sumy_logo.png", width=400)
    st.markdown('<div class="sub-header">Assistant Médical IA - 100% Local & Confidentiel</div>', unsafe_allow_html=True)
    
    # Badge de confidentialité
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("🔒 **Traitement 100% local** - Aucune donnée ne quitte votre machine")


def display_sidebar():
    """Affiche la barre latérale avec les paramètres"""
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Paramètres de transcription
        st.subheader("🎤 Transcription")
        whisper_model = st.selectbox(
            "Modèle Whisper",
            ["tiny", "base", "small", "medium", "large"],
            index=1,
            help="Base recommandé pour équilibre vitesse/qualité"
        )
        
        language = st.selectbox(
            "Langue",
            ["Français", "Anglais"],
            help="Langue de la consultation"
        )
        language_code = "fr" if language == "Français" else "en"
        
        # Paramètres médicaux
        st.subheader("🏥 Paramètres médicaux")
        specialty = st.selectbox(
            "Spécialité destinataire",
            ["Généraliste", "Cardiologie", "ORL", "Pédiatrie", "Dermatologie"],
            help="Pour la lettre d'adressage"
        )
        
        format_type = st.radio(
            "Format compte-rendu",
            ["SOAP structuré", "Texte libre"],
            help="Format du compte-rendu"
        )
        
        # Informations patient (optionnel)
        st.subheader("👤 Patient (optionnel)")
        patient_name = st.text_input("Nom du patient", "Patient")
        patient_age = st.number_input("Âge", min_value=0, max_value=120, value=35)
        patient_sex = st.selectbox("Sexe", ["Non spécifié", "Homme", "Femme"])
        
        # Informations médecin
        st.subheader("👨‍⚕️ Médecin")
        doctor_name = st.text_input("Nom du médecin", "Dr. Médecin Traitant")
        
        # À propos
        st.markdown("---")
        st.markdown("### 📚 À propos")
        st.markdown("""
        **SUMY** utilise:
        - 🎤 Whisper (transcription)
        - 🔍 scispaCy (NER médical)
        - 🤖 Llama2 (génération)
        - 🔒 100% local
        """)
        
        st.markdown("---")
        st.caption("v1.0.0 - PoC Démonstration")
    
    return {
        "whisper_model": whisper_model,
        "language": language_code,
        "specialty": specialty,
        "format_type": format_type,
        "patient_name": patient_name,
        "patient_age": patient_age,
        "patient_sex": patient_sex,
        "doctor_name": doctor_name
    }


def process_audio(audio_file, config):
    """Traite un fichier audio complet"""
    try:
        st.session_state.processing = True
        
        # Sauvegarde temporaire
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(audio_file.name).suffix) as tmp_file:
            tmp_file.write(audio_file.getvalue())
            tmp_path = tmp_file.name
        
        # Étape 1: Transcription
        with st.spinner("🎤 Transcription en cours..."):
            transcription_service = get_hypocrate_transcription_service(config["whisper_model"])
            
            # Estime le temps
            duration = transcription_service.get_audio_duration(tmp_path)
            estimated_time = transcription_service.estimate_processing_time(duration)
            
            st.info(f"⏱️ Durée audio: {duration:.1f}s - Temps estimé: {estimated_time:.1f}s")
            
            transcript_result = transcription_service.transcribe_audio(
                tmp_path,
                language=config["language"],
                with_timestamps=True
            )
            
            st.session_state.transcript = transcript_result
            st.success(f"✅ Transcription terminée en {transcript_result['duration_seconds']:.1f}s")
        
        # Étape 2: Extraction entités
        with st.spinner("🔍 Extraction des entités médicales..."):
            ner_service = get_medical_ner_service(config["language"])
            entities = ner_service.extract_entities(transcript_result['text'])
            st.session_state.entities = entities
            st.success("✅ Entités médicales extraites")
        
        # Étape 3: Génération SOAP
        with st.spinner("📝 Génération du compte-rendu SOAP..."):
            soap_generator = get_soap_generator()
            
            patient_context = f"Patient: {config['patient_name']}, {config['patient_age']} ans"
            if config['patient_sex'] != "Non spécifié":
                patient_context += f", {config['patient_sex']}"
            
            soap_result = soap_generator.generate_soap_note(
                transcript=transcript_result['text'],
                entities=entities,
                patient_context=patient_context,
                specialty=config['specialty']
            )
            
            st.session_state.soap_note = soap_result
            st.success(f"✅ SOAP généré en {soap_result['generation_time_seconds']:.1f}s")
        
        # Étape 4: Génération lettre
        with st.spinner("📧 Génération de la lettre d'adressage..."):
            letter_generator = get_letter_generator()
            
            letter_result = letter_generator.generate_referral_letter(
                soap_note=soap_result['soap_note'],
                specialty=config['specialty'],
                patient_name=config['patient_name'],
                doctor_name=config['doctor_name']
            )
            
            st.session_state.letter = letter_result
            st.success(f"✅ Lettre générée en {letter_result['generation_time_seconds']:.1f}s")
        
        # Nettoyage
        Path(tmp_path).unlink(missing_ok=True)
        
        st.session_state.processing = False
        return True
        
    except Exception as e:
        st.error(f"❌ Erreur lors du traitement: {str(e)}")
        logger.error(f"Erreur traitement: {e}", exc_info=True)
        st.session_state.processing = False
        return False


def display_results():
    """Affiche les résultats du traitement"""
    
    # Transcription
    if st.session_state.transcript:
        st.markdown('<div class="section-header">📄 Transcription</div>', unsafe_allow_html=True)
        
        with st.expander("Voir la transcription complète", expanded=False):
            transcript_data = st.session_state.transcript
            
            # Dialogue formaté
            if transcript_data.get('segments'):
                from services.transcription_hypocrate import get_hypocrate_transcription_service
                service = get_hypocrate_transcription_service()
                dialogue = service.format_dialogue(transcript_data['segments'], speaker_detection=True)
                st.markdown(dialogue)
            else:
                st.text(transcript_data['text'])
            
            # Métadonnées
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Durée traitement", f"{transcript_data['duration_seconds']:.1f}s")
            with col2:
                st.metric("Modèle", transcript_data['model'])
            with col3:
                st.metric("Device", transcript_data['device'])
    
    # Entités médicales
    if st.session_state.entities:
        st.markdown('<div class="section-header">🏷️ Entités Médicales Détectées</div>', unsafe_allow_html=True)
        
        entities = st.session_state.entities
        
        # Allergies (prioritaire)
        if entities.get('allergies'):
            st.markdown("### ⚠️ Allergies")
            for allergy in entities['allergies']:
                st.markdown(f'<span class="entity-tag allergy-tag">⚠️ {allergy}</span>', unsafe_allow_html=True)
        
        # Médicaments
        if entities.get('medications'):
            st.markdown("### 💊 Médicaments")
            for med in entities['medications']:
                st.markdown(f'<span class="entity-tag medication-tag">💊 {med}</span>', unsafe_allow_html=True)
        
        # Symptômes
        if entities.get('symptoms'):
            st.markdown("### 🤒 Symptômes")
            for symptom in entities['symptoms']:
                st.markdown(f'<span class="entity-tag symptom-tag">🤒 {symptom}</span>', unsafe_allow_html=True)
        
        # Diagnostics
        if entities.get('diagnoses'):
            st.markdown("### 🏷️ Diagnostics")
            for diag in entities['diagnoses']:
                st.markdown(f'<span class="entity-tag diagnosis-tag">🏷️ {diag}</span>', unsafe_allow_html=True)
        
        # Constantes vitales
        if entities.get('vital_signs'):
            st.markdown("### 📏 Constantes Vitales")
            vs_cols = st.columns(len(entities['vital_signs']))
            for i, (key, value) in enumerate(entities['vital_signs'].items()):
                with vs_cols[i]:
                    st.metric(key.replace('_', ' ').title(), value)
    
    # Compte-rendu SOAP
    if st.session_state.soap_note:
        st.markdown('<div class="section-header">📋 Compte-Rendu SOAP</div>', unsafe_allow_html=True)
        
        soap_data = st.session_state.soap_note
        soap_note = soap_data['soap_note']
        
        # Alertes de validation
        validation = soap_data.get('validation', {})
        if validation.get('warnings'):
            for warning in validation['warnings']:
                st.markdown(f'<div class="warning-box">⚠️ {warning}</div>', unsafe_allow_html=True)
        
        # Affichage SOAP
        from services.soap_generator import get_soap_generator
        generator = get_soap_generator()
        soap_formatted = generator.format_soap_display(soap_note)
        
        st.markdown(soap_formatted)
        
        # Bouton copie
        if st.button("📋 Copier le compte-rendu"):
            st.code(soap_formatted, language=None)
            st.success("✅ Compte-rendu prêt à copier")
        
        # Métadonnées
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Temps de génération", f"{soap_data['generation_time_seconds']:.1f}s")
        with col2:
            st.metric("Modèle", soap_data['model_used'])
    
    # Lettre d'adressage
    if st.session_state.letter:
        st.markdown('<div class="section-header">📧 Lettre d\'Adressage</div>', unsafe_allow_html=True)
        
        letter_data = st.session_state.letter
        
        from services.letter_generator import get_letter_generator
        generator = get_letter_generator()
        letter_formatted = generator.format_letter_display(letter_data['letter'])
        
        st.markdown(f'<div class="info-box">{letter_formatted}</div>', unsafe_allow_html=True)
        
        # Bouton copie
        if st.button("📧 Copier la lettre"):
            st.code(letter_data['letter'], language=None)
            st.success("✅ Lettre prête à copier")


def display_preparation_consultation():
    """Affiche le module de préparation de consultation"""
    st.markdown('<div class="section-header">📋 Préparation de Consultation</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🔍 Recherche Patient")
        search_term = st.text_input("Nom, Prénom ou N° Dossier", placeholder="Ex: Dupont Jean")
        
        if st.button("🔍 Rechercher", use_container_width=True):
            st.success("✅ Patient trouvé")
    
    with col2:
        st.subheader("📁 Dossier Patient (Démo)")
        
        # Informations patient
        st.markdown("**Informations générales**")
        info_col1, info_col2, info_col3 = st.columns(3)
        with info_col1:
            st.metric("Âge", "45 ans")
        with info_col2:
            st.metric("Groupe sanguin", "A+")
        with info_col3:
            st.metric("Dernière visite", "Il y a 3 mois")
        
        # Antécédents
        with st.expander("🏥 Antécédents médicaux", expanded=True):
            st.markdown("""
            - **Allergies:** Pénicilline
            - **Maladies chroniques:** Hypertension (depuis 2018)
            - **Chirurgies:** Appendicectomie (2010)
            - **Traitements en cours:** Amlodipine 5mg/jour
            """)
        
        # Dernières consultations
        with st.expander("📅 Historique consultations"):
            st.markdown("""
            | Date | Motif | Médecin |
            |------|-------|---------|
            | 15/09/2024 | Contrôle TA | Dr. Martin |
            | 12/06/2024 | Grippe | Dr. Dubois |
            | 20/03/2024 | Bilan annuel | Dr. Martin |
            """)


def display_sick_leave_generator():
    """Affiche le générateur d'arrêt maladie"""
    st.markdown('<div class="section-header">📄 Génération Arrêt Maladie</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Informations Arrêt")
        
        patient_name = st.text_input("Nom du patient", value="Dupont Jean")
        diagnosis = st.text_area("Diagnostic / Motif", 
                                 value="Syndrome grippal avec fièvre",
                                 height=100)
        
        start_date = st.date_input("Date de début")
        duration = st.number_input("Durée (jours)", min_value=1, max_value=365, value=3)
        
        work_accident = st.checkbox("Accident du travail")
        prolongation = st.checkbox("Prolongation d'arrêt")
        
        if st.button("📄 Générer l'arrêt maladie", type="primary", use_container_width=True):
            st.session_state.sick_leave_generated = True
    
    with col2:
        st.subheader("📋 Aperçu Arrêt Maladie")
        
        if st.session_state.get('sick_leave_generated'):
            st.markdown(f"""
            <div class="info-box">
            <h4>ARRÊT DE TRAVAIL</h4>
            <p><strong>Patient:</strong> {patient_name}</p>
            <p><strong>Diagnostic:</strong> {diagnosis}</p>
            <p><strong>Période:</strong> Du {start_date} ({duration} jours)</p>
            <p><strong>Type:</strong> {'Accident du travail' if work_accident else 'Maladie'}</p>
            <p><strong>Médecin prescripteur:</strong> Dr. Martin</p>
            <hr>
            <p style="font-size: 0.9rem; color: #666;">
            ⚠️ Document généré automatiquement - À valider par le médecin
            </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("📥 Télécharger PDF"):
                st.success("✅ PDF généré (fonctionnalité démo)")
        else:
            st.info("👈 Remplissez le formulaire et cliquez sur 'Générer'")


def display_patient_summary():
    """Affiche le générateur de compte-rendu patient"""
    st.markdown('<div class="section-header">📋 Compte-Rendu Patient</div>', unsafe_allow_html=True)
    
    st.info("💡 Génère un compte-rendu simplifié pour le patient à partir de la consultation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⚙️ Configuration")
        
        language_level = st.select_slider(
            "Niveau de langage",
            options=["Très simple", "Simple", "Standard", "Technique"],
            value="Simple"
        )
        
        include_sections = st.multiselect(
            "Sections à inclure",
            ["Diagnostic", "Examens réalisés", "Traitement prescrit", "Conseils", "Suivi"],
            default=["Diagnostic", "Traitement prescrit", "Conseils"]
        )
        
        if st.button("📝 Générer compte-rendu patient", type="primary", use_container_width=True):
            st.session_state.patient_summary_generated = True
    
    with col2:
        st.subheader("📄 Compte-Rendu Généré")
        
        if st.session_state.get('patient_summary_generated'):
            st.markdown("""
            <div class="success-box">
            <h4>Votre Consultation du 02/12/2024</h4>
            
            <h5>🔍 Ce qui a été constaté</h5>
            <p>Vous présentez une infection de l'oreille droite (otite moyenne aiguë). 
            C'est une inflammation causée par des microbes.</p>
            
            <h5>💊 Votre traitement</h5>
            <ul>
            <li><strong>Azithromycine 500mg:</strong> 1 comprimé par jour pendant 3 jours</li>
            <li><strong>Paracétamol 1g:</strong> Si douleur ou fièvre (max 3x/jour)</li>
            </ul>
            
            <h5>💡 Conseils importants</h5>
            <ul>
            <li>Reposez-vous et évitez l'eau dans l'oreille</li>
            <li>Prenez tous les médicaments même si vous vous sentez mieux</li>
            <li>Revenez si pas d'amélioration dans 48h</li>
            </ul>
            
            <h5>📅 Prochain rendez-vous</h5>
            <p>Contrôle dans 1 semaine si les symptômes persistent</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("📧 Envoyer par email"):
                st.success("✅ Email envoyé (fonctionnalité démo)")
        else:
            st.info("👈 Configurez et générez le compte-rendu")


def display_treatment_plan():
    """Affiche le planificateur de traitement"""
    st.markdown('<div class="section-header">💊 Plan de Traitement</div>', unsafe_allow_html=True)
    
    st.info("🎯 Génère un plan de traitement personnalisé avec suivi")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📋 Prescription")
        
        # Médicaments
        st.markdown("**Médicaments prescrits**")
        
        with st.expander("💊 Azithromycine 500mg", expanded=True):
            st.write("**Posologie:** 1 comprimé/jour")
            st.write("**Durée:** 3 jours")
            st.write("**Moment:** Pendant le repas")
            st.checkbox("Rappel automatique", key="med1")
        
        with st.expander("💊 Paracétamol 1g"):
            st.write("**Posologie:** 1 comprimé si besoin")
            st.write("**Max:** 3 fois par jour")
            st.write("**Moment:** Si douleur ou fièvre")
            st.checkbox("Rappel automatique", key="med2")
        
        # Examens de suivi
        st.markdown("**Examens de suivi**")
        exam_date = st.date_input("Date contrôle", key="exam_date")
        st.checkbox("Audiométrie si pas d'amélioration")
        st.checkbox("Consultation ORL si nécessaire")
    
    with col2:
        st.subheader("📅 Calendrier de Suivi")
        
        st.markdown("""
        <div class="info-box">
        <h5>Planning de traitement</h5>
        
        <p><strong>Jour 1-3:</strong> Azithromycine 500mg</p>
        <p style="padding-left: 20px;">✓ Matin avec petit-déjeuner</p>
        
        <p><strong>Si besoin:</strong> Paracétamol 1g</p>
        <p style="padding-left: 20px;">✓ Max 3x par jour</p>
        <p style="padding-left: 20px;">✓ Espacer de 6h minimum</p>
        
        <hr>
        
        <p><strong>📍 Jour 2:</strong> Point d'évaluation</p>
        <p style="padding-left: 20px;">→ Amélioration des symptômes?</p>
        
        <p><strong>📍 Jour 7:</strong> Contrôle médecin</p>
        <p style="padding-left: 20px;">→ Si symptômes persistent</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📲 Activer rappels SMS", use_container_width=True):
            st.success("✅ Rappels activés (fonctionnalité démo)")
        
        if st.button("📥 Télécharger planning", use_container_width=True):
            st.success("✅ Planning téléchargé (fonctionnalité démo)")


def display_accounting():
    """Affiche le module de comptabilité"""
    st.markdown('<div class="section-header">💰 Comptabilité Cabinet</div>', unsafe_allow_html=True)
    
    # Statistiques du jour
    st.subheader("📊 Aujourd'hui")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Consultations", "12", "+2")
    with col2:
        st.metric("Recettes", "720 €", "+120 €")
    with col3:
        st.metric("Moyenne/patient", "60 €")
    with col4:
        st.metric("Taux remplissage", "85%")
    
    # Détails
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 Consultations du jour")
        st.markdown("""
        | Heure | Patient | Type | Montant |
        |-------|---------|------|---------|
        | 09:00 | M. Dupont | Consultation | 25 € |
        | 09:30 | Mme Martin | Suivi | 25 € |
        | 10:00 | M. Bernard | Consultation | 25 € |
        | 10:30 | Mme Petit | Certificat | 20 € |
        | 11:00 | M. Durand | Consultation | 25 € |
        | ... | ... | ... | ... |
        """)
        
        if st.button("📥 Exporter journée", use_container_width=True):
            st.success("✅ Export Excel généré (démo)")
    
    with col2:
        st.subheader("📈 Statistiques Mois")
        
        # Graphique simple en texte
        st.markdown("""
        **Évolution recettes (30 derniers jours)**
        ```
        Semaine 1: ████████░░ 3,200 €
        Semaine 2: ██████████ 3,800 €
        Semaine 3: █████████░ 3,500 €
        Semaine 4: ████████░░ 3,100 €
        ```
        
        **Total mois:** 13,600 €  
        **Objectif:** 15,000 € (91%)
        """)
        
        st.markdown("**Répartition par type**")
        st.markdown("""
        - 🔵 Consultations: 65%
        - 🟢 Suivis: 20%
        - 🟡 Certificats: 10%
        - 🟠 Autres: 5%
        """)
        
        if st.button("📊 Rapport mensuel", use_container_width=True):
            st.success("✅ Rapport PDF généré (démo)")


def main():
    """Fonction principale"""
    init_session_state()
    display_header()
    config = display_sidebar()
    
    # Système d'onglets
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🎤 Consultation IA",
        "📋 Préparation",
        "📄 Arrêt Maladie",
        "📋 CR Patient",
        "💊 Plan Traitement",
        "💰 Comptabilité"
    ])
    
    with tab1:
        # Zone de contrôle
        st.markdown('<div class="section-header">🎤 Enregistrement / Upload Audio</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            audio_file = st.file_uploader(
                "Uploadez un fichier audio de consultation",
                type=["wav", "mp3", "m4a", "ogg", "flac"],
                help="Formats supportés: WAV, MP3, M4A, OGG, FLAC"
            )
        
        with col2:
            if audio_file:
                st.audio(audio_file)
        
        # Bouton traitement
        if audio_file and not st.session_state.processing:
            if st.button("🚀 Analyser la consultation", type="primary", use_container_width=True):
                success = process_audio(audio_file, config)
                if success:
                    st.balloons()
        
        # Affichage résultats
        if any([st.session_state.transcript, st.session_state.entities, 
                st.session_state.soap_note, st.session_state.letter]):
            st.markdown("---")
            display_results()
    
    with tab2:
        display_preparation_consultation()
    
    with tab3:
        display_sick_leave_generator()
    
    with tab4:
        display_patient_summary()
    
    with tab5:
        display_treatment_plan()
    
    with tab6:
        display_accounting()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        <p>🏥 <strong>SUMY</strong> - Assistant Médical IA | 
        Propulsé par Whisper • scispaCy • Llama2 | 
        🔒 100% Local & Confidentiel</p>
        <p style="font-size: 0.8rem;">
        ⚠️ Cet outil est une aide à la décision. Le médecin reste responsable de la validation finale.
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
