# 🤖 Workflow Automatique SUMY - Transcription → Résumé → Lettre

**Status :** ✅ DÉJÀ IMPLÉMENTÉ ET FONCTIONNEL

---

## 📋 Workflow Complet (4 Étapes Automatiques)

Quand vous uploadez un fichier audio, SUMY effectue automatiquement :

### 1️⃣ Transcription Audio (Whisper)
```
🎤 Audio → Texte
- Modèle : Whisper (base/small/medium)
- Device : CPU (stable)
- Détection de langue : Français/Anglais
- Timestamps : Oui
```

### 2️⃣ Extraction Entités Médicales (spaCy)
```
🔍 Texte → Entités
- Allergies ⚠️
- Médicaments 💊
- Symptômes 🤒
- Diagnostics 🏷️
- Constantes vitales 📏
```

### 3️⃣ Génération Compte-Rendu SOAP (Llama2 via Ollama)
```
📝 Transcription + Entités → SOAP
- S (Subjectif) : Plaintes du patient
- O (Objectif) : Observations cliniques
- A (Assessment) : Évaluation/Diagnostic
- P (Plan) : Plan de traitement

Modèle : llama2:latest (local)
```

### 4️⃣ Génération Lettre d'Adressage (Llama2 via Ollama)
```
📧 SOAP → Lettre spécialiste
- Destinataire : ORL, Cardiologue, etc.
- Contexte patient
- Raison de l'adressage
- Examens demandés

Modèle : llama2:latest (local)
```

---

## 🎯 Configuration dans la Sidebar

### Paramètres Patient
```
👤 Patient
- Nom : [Nom du patient]
- Âge : [Âge]
- Sexe : [Homme/Femme/Non spécifié]
```

### Paramètres Consultation
```
🏥 Consultation
- Spécialité : [Médecine générale/ORL/Cardiologie/...]
- Langue : [Français/Anglais]
```

### Paramètres Médecin
```
👨‍⚕️ Médecin
- Nom : [Dr. Nom]
```

### Paramètres Techniques
```
⚙️ Technique
- Modèle Whisper : [base/small/medium]
- Modèle Ollama : [llama2:latest]
```

---

## 🚀 Utilisation Pratique

### Étape 1 : Configurer
1. Ouvrez la sidebar (←)
2. Remplissez les informations patient
3. Sélectionnez la spécialité (ex: ORL)

### Étape 2 : Uploader l'audio
1. Glissez-déposez le fichier audio
2. Ou cliquez pour sélectionner
3. Formats : WAV, MP3, M4A, OGG, FLAC

### Étape 3 : Traitement automatique
L'application fait tout automatiquement :
```
🎤 Transcription...        ✅ 6.5s
🔍 Extraction entités...   ✅ 1.2s
📝 Génération SOAP...      ✅ 8.3s
📧 Génération lettre...    ✅ 5.1s
```

### Étape 4 : Résultats
Vous obtenez :
- ✅ Transcription complète
- ✅ Entités médicales extraites
- ✅ Compte-rendu SOAP structuré
- ✅ Lettre d'adressage au spécialiste

---

## 📄 Exemple de Résultat

### Transcription
```
Médecin : Bonjour, qu'est-ce qui vous amène aujourd'hui ?
Patient : J'ai des douleurs à l'oreille droite depuis 3 jours...
```

### Entités Extraites
```
⚠️ Allergies : Pénicilline
💊 Médicaments : Paracétamol 1g
🤒 Symptômes : Douleur oreille, Fièvre
📏 Constantes : Température 38.5°C
```

### Compte-Rendu SOAP
```
S - SUBJECTIF
Patient se plaint de douleurs à l'oreille droite depuis 3 jours...

O - OBJECTIF
Examen clinique : Tympan rouge et bombé...

A - ASSESSMENT
Otite moyenne aiguë droite

P - PLAN
- Prescription : Amoxicilline 1g x3/j pendant 7 jours
- Contrôle dans 48h si pas d'amélioration
- Adressage ORL si persistance
```

### Lettre d'Adressage ORL
```
Cher Confrère,

Je vous adresse Monsieur [Nom], 45 ans, pour avis spécialisé
concernant une otite moyenne aiguë droite ne répondant pas
au traitement antibiotique initial.

Antécédents : Allergie à la pénicilline
Traitement en cours : Amoxicilline 1g x3/j

Je vous remercie de bien vouloir prendre en charge ce patient
et reste à votre disposition pour tout complément d'information.

Cordialement,
Dr. [Nom]
```

---

## 🔧 Configuration Ollama

### Vérifier qu'Ollama est lancé
```bash
# Vérifier le service
ollama list

# Devrait afficher :
# llama2:latest    3.8 GB    ...
```

### Si Ollama n'est pas lancé
```bash
# Démarrer Ollama
ollama serve

# Dans un autre terminal
ollama pull llama2
```

### Modèles disponibles
- **llama2:latest** (3.8 GB) - Recommandé ✅
- **mistral:7b** (4.4 GB) - Alternative
- **codellama:7b** (3.8 GB) - Pour code

---

## ⚙️ Personnalisation

### Changer le modèle Ollama
Dans `hypocrate_app.py` :
```python
# Ligne ~140
ollama_model = st.selectbox(
    "Modèle Ollama",
    ["llama2:latest", "mistral:7b", "codellama:7b"],
    index=0
)
```

### Changer la spécialité
Dans la sidebar :
```python
specialty = st.selectbox(
    "Spécialité",
    [
        "Médecine générale",
        "ORL",
        "Cardiologie",
        "Dermatologie",
        "Pneumologie",
        # Ajoutez d'autres spécialités
    ]
)
```

### Personnaliser les prompts
Fichier `config/prompts.py` :
- `MEDICAL_SCRIBE_SYSTEM_PROMPT` - Prompt système
- `build_soap_prompt()` - Prompt SOAP
- `build_letter_prompt()` - Prompt lettre

---

## 📊 Performance

### Temps de traitement typique
Pour un audio de 5 minutes :
```
🎤 Transcription :     ~30-60s (CPU)
🔍 Extraction :        ~2-5s
📝 SOAP :              ~10-20s (Llama2)
📧 Lettre :            ~8-15s (Llama2)
───────────────────────────────
Total :                ~50-100s
```

### Optimisations possibles
1. **GPU** : Utiliser CUDA si disponible (5x plus rapide)
2. **Faster-Whisper** : 4x plus rapide que Whisper standard
3. **Mistral** : Modèle plus rapide que Llama2
4. **Quantization** : Modèles 4-bit (2x plus rapide)

---

## 🎯 Cas d'Usage

### 1. Consultation ORL
```
Spécialité : ORL
→ Lettre d'adressage vers ORL
→ Examens : Audiométrie, Tympanométrie
```

### 2. Consultation Cardiologie
```
Spécialité : Cardiologie
→ Lettre d'adressage vers Cardiologue
→ Examens : ECG, Échographie cardiaque
```

### 3. Médecine Générale
```
Spécialité : Médecine générale
→ Compte-rendu SOAP complet
→ Pas de lettre d'adressage (sauf si nécessaire)
```

---

## ✅ Checklist de Fonctionnement

- [x] Ollama installé et lancé
- [x] Modèle llama2:latest téléchargé
- [x] Whisper installé (openai-whisper)
- [x] spaCy installé avec modèles français
- [x] Application Streamlit lancée
- [x] Workflow automatique configuré

---

## 🐛 Dépannage

### Erreur "Ollama n'est pas accessible"
```bash
# Vérifier qu'Ollama tourne
ps aux | grep ollama

# Relancer si nécessaire
ollama serve
```

### Génération SOAP/Lettre lente
```bash
# Vérifier la charge CPU
top

# Utiliser un modèle plus léger
# Dans la sidebar : Changer pour mistral:7b
```

### Erreur de mémoire
```bash
# Vérifier la RAM disponible
vm_stat

# Fermer d'autres applications
# Ou utiliser un modèle quantizé (4-bit)
```

---

## 📚 Documentation Technique

### Services utilisés
1. **TranscriptionService** (`services/transcription_hypocrate.py`)
2. **MedicalNERService** (`services/ner_medical.py`)
3. **SOAPGenerator** (`services/soap_generator.py`)
4. **LetterGenerator** (`services/letter_generator.py`)

### Fichiers de configuration
- `config/prompts.py` - Prompts Llama2
- `config/medical_terms.py` - Termes médicaux
- `.streamlit/config.toml` - Config Streamlit

---

## 🎉 Résumé

**Le workflow est 100% automatique et fonctionnel !**

1. ✅ Upload audio
2. ✅ Transcription automatique
3. ✅ Extraction entités automatique
4. ✅ Génération SOAP automatique (Ollama)
5. ✅ Génération lettre automatique (Ollama)

**Tout se fait en un clic !**

---

**🚀 Testez maintenant : http://localhost:8501**

**Uploadez un fichier audio et laissez SUMY faire le reste !**
