# 🤖 SUMY - Workflow Automatique Complet

## 🎯 Résumé en 1 Phrase

**SUMY transcrit automatiquement vos consultations audio et génère un compte-rendu SOAP + une lettre d'adressage vers un spécialiste grâce à Ollama et Llama2.**

---

## 📊 Workflow Visuel

```
┌─────────────────────────────────────────────────────────────┐
│                     UPLOAD AUDIO                            │
│              (WAV, MP3, M4A, OGG, FLAC)                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  ÉTAPE 1 : TRANSCRIPTION (Whisper - CPU)                   │
│  🎤 Audio → Texte                                           │
│  ⏱️  ~6-10s pour 30s d'audio                                │
│                                                             │
│  Résultat :                                                 │
│  "Médecin : Bonjour, qu'est-ce qui vous amène ?            │
│   Patient : J'ai mal à l'oreille depuis 3 jours..."        │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  ÉTAPE 2 : EXTRACTION ENTITÉS (spaCy)                      │
│  🔍 Texte → Entités Médicales                               │
│  ⏱️  ~1-2s                                                   │
│                                                             │
│  Résultat :                                                 │
│  ⚠️  Allergies : Pénicilline                                │
│  💊 Médicaments : Amoxicilline, Azithromycine              │
│  🤒 Symptômes : Douleur oreille, Fièvre                    │
│  🏷️  Diagnostics : Otite moyenne aiguë                      │
│  📏 Constantes : Température 38.5°C                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  ÉTAPE 3 : GÉNÉRATION SOAP (Llama2 via Ollama)             │
│  📝 Transcription + Entités → Compte-Rendu Structuré        │
│  ⏱️  ~10-20s                                                 │
│                                                             │
│  Résultat :                                                 │
│  S - SUBJECTIF                                              │
│      Patient se plaint de douleur oreille droite...        │
│                                                             │
│  O - OBJECTIF                                               │
│      Tympan rouge et bombé, Température 38.5°C...          │
│                                                             │
│  A - ASSESSMENT                                             │
│      Otite moyenne aiguë droite                            │
│                                                             │
│  P - PLAN                                                   │
│      - Azithromycine 500mg x3/j                            │
│      - Contrôle 48h                                        │
│      - Adressage ORL si persistance                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  ÉTAPE 4 : GÉNÉRATION LETTRE (Llama2 via Ollama)           │
│  📧 SOAP → Lettre d'Adressage Spécialiste                   │
│  ⏱️  ~8-15s                                                  │
│                                                             │
│  Résultat :                                                 │
│  Cher Confrère,                                            │
│                                                             │
│  Je vous adresse M. Jean Dupont, 45 ans, pour avis         │
│  spécialisé en ORL concernant une otite moyenne aiguë...   │
│                                                             │
│  MOTIF : Absence d'amélioration après 48h de traitement    │
│  EXAMENS SUGGÉRÉS : Audiométrie, Tympanométrie             │
│                                                             │
│  Cordialement,                                             │
│  Dr. Martin                                                │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    RÉSULTATS FINAUX                         │
│                                                             │
│  ✅ Transcription complète                                  │
│  ✅ Entités médicales extraites                             │
│  ✅ Compte-rendu SOAP structuré                             │
│  ✅ Lettre d'adressage professionnelle                      │
│                                                             │
│  📋 Boutons : Copier SOAP | Copier Lettre                  │
│  💾 Export : TXT, PDF, DOCX (à venir)                      │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚡ Temps de Traitement

| Audio | Transcription | Entités | SOAP | Lettre | **Total** |
|-------|--------------|---------|------|--------|-----------|
| 30s   | ~6-10s       | ~1-2s   | ~10-20s | ~8-15s | **~25-47s** |
| 2min  | ~15-25s      | ~1-2s   | ~10-20s | ~8-15s | **~34-62s** |
| 5min  | ~35-60s      | ~2-5s   | ~10-20s | ~8-15s | **~55-100s** |

---

## 🎛️ Configuration Requise

### Sidebar (Interface)
```
👤 PATIENT
├─ Nom : Jean Dupont
├─ Âge : 45
└─ Sexe : Homme

🏥 CONSULTATION
├─ Spécialité : ORL / Cardiologie / Dermatologie / ...
└─ Langue : Français / Anglais

👨‍⚕️ MÉDECIN
└─ Nom : Dr. Martin

⚙️ TECHNIQUE
├─ Modèle Whisper : base / small / medium
└─ Modèle Ollama : llama2:latest
```

### Services Requis
```
✅ Ollama : localhost:11434 (EN COURS)
✅ Llama2 : 3.8 GB (INSTALLÉ)
✅ Whisper : CPU mode (OPÉRATIONNEL)
✅ spaCy : fr_core_news_md (INSTALLÉ)
```

---

## 🚀 Utilisation en 3 Clics

### 1️⃣ Configurer
Ouvrez la sidebar et remplissez :
- Nom patient
- Spécialité (ex: ORL)
- Nom médecin

### 2️⃣ Uploader
Glissez-déposez votre fichier audio
ou cliquez pour sélectionner

### 3️⃣ Attendre
Le système fait tout automatiquement :
- ✅ Transcription
- ✅ Extraction entités
- ✅ Génération SOAP
- ✅ Génération lettre

**C'est tout ! 🎉**

---

## 📋 Exemple Concret : Consultation ORL

### Input
```
🎤 Audio : consultation_otite.m4a (33 secondes)

Configuration :
- Patient : Jean Dupont, 45 ans, Homme
- Spécialité : ORL
- Médecin : Dr. Martin
```

### Output (Automatique)
```
📄 TRANSCRIPTION (6.5s)
Médecin : Bonjour Monsieur Dupont...
Patient : J'ai mal à l'oreille droite depuis 3 jours...

🏷️ ENTITÉS MÉDICALES (1.2s)
⚠️  Pénicilline
💊 Amoxicilline, Azithromycine
🤒 Douleur oreille, Fièvre
🏷️  Otite moyenne aiguë

📋 COMPTE-RENDU SOAP (12.3s)
S - Patient se plaint de douleur oreille droite...
O - Tympan rouge et bombé, T° 38.5°C...
A - Otite moyenne aiguë droite
P - Azithromycine 500mg, Contrôle 48h, Adressage ORL

📧 LETTRE D'ADRESSAGE ORL (10.1s)
Cher Confrère,
Je vous adresse M. Jean Dupont, 45 ans...
Examens suggérés : Audiométrie, Tympanométrie...
```

**Temps total : 30.1 secondes**

---

## 🎯 Spécialités Supportées

Le système génère automatiquement des lettres adaptées pour :

- **ORL** → Audiométrie, Tympanométrie, Otoscopie
- **Cardiologie** → ECG, Échographie cardiaque, Holter
- **Dermatologie** → Biopsie, Dermoscopie
- **Pneumologie** → Spirométrie, Radiographie thorax
- **Gastro-entérologie** → Endoscopie, Échographie abdominale
- **Rhumatologie** → Radiographie, IRM, Bilan inflammatoire
- **Neurologie** → IRM cérébrale, EEG, Scanner
- **Ophtalmologie** → Fond d'œil, Tonométrie, OCT
- **Médecine générale** → Bilan sanguin, Examens standards

---

## 🔧 Technologies Utilisées

```
┌─────────────────────────────────────┐
│  FRONTEND                           │
│  Streamlit                          │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│  TRANSCRIPTION                      │
│  OpenAI Whisper (base)              │
│  CPU mode (stable)                  │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│  NER (Named Entity Recognition)    │
│  spaCy + scispaCy                   │
│  fr_core_news_md                    │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│  LLM (Large Language Model)         │
│  Llama2 7B via Ollama               │
│  localhost:11434                    │
└─────────────────────────────────────┘
```

---

## 🔒 Sécurité & Confidentialité

✅ **100% Local**
- Aucune donnée ne quitte votre machine
- Pas d'API externe
- Pas de cloud

✅ **RGPD Compliant**
- Données médicales confidentielles
- Traitement local uniquement
- Pas de stockage externe

✅ **Open Source**
- Code auditable
- Modèles open-source
- Transparence totale

---

## 📊 Performance

### Configuration Actuelle
- **CPU :** Apple Silicon (M1/M2/M3)
- **RAM :** 2-3 GB utilisés
- **Stockage :** ~8 GB (modèles)

### Optimisations Futures
- **GPU Whisper :** 3-5x plus rapide
- **Faster-Whisper :** 4x plus rapide
- **Mistral 7B :** 1.5x plus rapide
- **Quantization 4-bit :** 2x plus rapide

---

## 🎉 Avantages

✅ **Gain de temps**
- Transcription automatique
- Compte-rendu structuré
- Lettre professionnelle

✅ **Qualité**
- Structure SOAP médicale
- Entités extraites automatiquement
- Lettres adaptées par spécialité

✅ **Simplicité**
- 3 clics seulement
- Interface intuitive
- Workflow automatique

✅ **Confidentialité**
- 100% local
- RGPD compliant
- Données sécurisées

---

## 🚀 Commencer Maintenant

```bash
# 1. Vérifier qu'Ollama tourne
ollama list

# 2. Ouvrir l'application
open http://localhost:8501

# 3. Uploader un audio et c'est parti !
```

---

## 📚 Documentation

- **WORKFLOW_AUTOMATIQUE.md** - Explication détaillée
- **TEST_WORKFLOW_COMPLET.md** - Guide de test avec exemple
- **START_HERE.md** - Démarrage rapide
- **INDEX_DOCUMENTATION.md** - Navigation complète

---

**🎊 SUMY - L'assistant médical IA qui fait tout automatiquement !**

**→ http://localhost:8501**
