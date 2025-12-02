# 🧪 Test du Workflow Complet SUMY

**Objectif :** Tester la génération automatique de compte-rendu SOAP et lettre d'adressage

---

## ✅ Prérequis Vérifiés

- [x] Ollama en cours d'exécution
- [x] Modèle llama2:latest disponible (3.8 GB)
- [x] Whisper installé (CPU mode)
- [x] spaCy installé avec modèles français
- [x] Application SUMY lancée sur http://localhost:8501

---

## 🎯 Scénario de Test : Consultation ORL

### Étape 1 : Configuration (Sidebar)

```
👤 PATIENT
- Nom : Jean Dupont
- Âge : 45
- Sexe : Homme

🏥 CONSULTATION
- Spécialité : ORL
- Langue : Français

👨‍⚕️ MÉDECIN
- Nom : Dr. Martin

⚙️ TECHNIQUE
- Modèle Whisper : base
- Modèle Ollama : llama2:latest
```

### Étape 2 : Upload Audio

**Fichier de test :** `Hypocrite 2.m4a` (33 secondes)

**Ou créez un audio de test avec :**
```
Médecin : Bonjour Monsieur Dupont, qu'est-ce qui vous amène ?

Patient : Bonjour docteur, j'ai mal à l'oreille droite depuis 3 jours.
C'est une douleur assez forte, et j'ai aussi un peu de fièvre.

Médecin : D'accord. Avez-vous des allergies connues ?

Patient : Oui, je suis allergique à la pénicilline.

Médecin : Très bien. Je vais examiner votre oreille...
Le tympan est rouge et bombé, c'est une otite moyenne aiguë.
Je vais vous prescrire de l'amoxicilline, mais vu votre allergie,
on va plutôt partir sur de l'azithromycine.

Patient : D'accord. Et si ça ne passe pas ?

Médecin : Si dans 48 heures il n'y a pas d'amélioration,
je vous adresserai à un confrère ORL pour un avis spécialisé.
```

### Étape 3 : Traitement Automatique

L'application va automatiquement :

```
⏳ Étape 1/4 : Transcription audio...
🎤 Whisper (base) sur CPU
⏱️ Durée estimée : ~6-10 secondes
✅ Transcription terminée

⏳ Étape 2/4 : Extraction entités médicales...
🔍 spaCy (fr_core_news_md)
⏱️ Durée estimée : ~1-2 secondes
✅ Entités extraites

⏳ Étape 3/4 : Génération compte-rendu SOAP...
📝 Llama2 via Ollama
⏱️ Durée estimée : ~10-20 secondes
✅ SOAP généré

⏳ Étape 4/4 : Génération lettre d'adressage...
📧 Llama2 via Ollama
⏱️ Durée estimée : ~8-15 secondes
✅ Lettre générée
```

**Temps total estimé : ~25-47 secondes**

---

## 📊 Résultats Attendus

### 1. Transcription
```
📄 TRANSCRIPTION

Médecin : Bonjour Monsieur Dupont, qu'est-ce qui vous amène ?
Patient : Bonjour docteur, j'ai mal à l'oreille droite depuis 3 jours...
[...]

Métadonnées :
- Durée traitement : 6.5s
- Modèle : base
- Device : cpu
```

### 2. Entités Médicales
```
🏷️ ENTITÉS MÉDICALES DÉTECTÉES

⚠️ Allergies
⚠️ Pénicilline

💊 Médicaments
💊 Amoxicilline
💊 Azithromycine

🤒 Symptômes
🤒 Douleur oreille droite
🤒 Fièvre

🏷️ Diagnostics
🏷️ Otite moyenne aiguë

📏 Constantes Vitales
Température : 38.5°C
```

### 3. Compte-Rendu SOAP
```
📋 COMPTE-RENDU SOAP

S - SUBJECTIF
Patient se présente avec une douleur à l'oreille droite évoluant
depuis 3 jours, accompagnée de fièvre. Allergie connue à la pénicilline.

O - OBJECTIF
Examen clinique :
- Tympan droit : rouge et bombé
- Température : 38.5°C
- État général : conservé

A - ASSESSMENT (ÉVALUATION)
Otite moyenne aiguë droite

P - PLAN
1. Traitement :
   - Azithromycine 500mg : 1cp/j pendant 3 jours
   - Paracétamol 1g : si douleur ou fièvre
   
2. Surveillance :
   - Contrôle dans 48h si pas d'amélioration
   - Adressage ORL si persistance des symptômes

3. Conseils :
   - Repos
   - Hydratation
   - Éviter l'eau dans l'oreille

Métadonnées :
- Temps de génération : 12.3s
- Modèle : llama2:latest
```

### 4. Lettre d'Adressage ORL
```
📧 LETTRE D'ADRESSAGE

Cher Confrère,

Je vous adresse Monsieur Jean Dupont, 45 ans, pour avis spécialisé
en ORL concernant une otite moyenne aiguë droite.

MOTIF DE CONSULTATION
Patient consultant pour douleur oreille droite depuis 3 jours avec fièvre.

ANTÉCÉDENTS
- Allergie : Pénicilline

EXAMEN CLINIQUE
- Tympan droit rouge et bombé
- Température : 38.5°C

DIAGNOSTIC RETENU
Otite moyenne aiguë droite

TRAITEMENT INITIÉ
- Azithromycine 500mg : 1cp/j pendant 3 jours
- Paracétamol 1g si besoin

RAISON DE L'ADRESSAGE
Absence d'amélioration après 48h de traitement antibiotique.
Avis spécialisé souhaité pour évaluation complémentaire et
prise en charge adaptée.

EXAMENS COMPLÉMENTAIRES SUGGÉRÉS
- Audiométrie
- Tympanométrie
- Otoscopie approfondie

Je vous remercie de bien vouloir prendre en charge ce patient
et reste à votre disposition pour tout complément d'information.

Cordialement,
Dr. Martin

Métadonnées :
- Temps de génération : 10.1s
- Modèle : llama2:latest
```

---

## 🎯 Points de Vérification

### ✅ Transcription
- [ ] Texte complet et lisible
- [ ] Dialogue médecin/patient identifié
- [ ] Timestamps présents
- [ ] Durée de traitement raisonnable (<15s)

### ✅ Entités Médicales
- [ ] Allergies détectées (Pénicilline)
- [ ] Médicaments identifiés (Azithromycine)
- [ ] Symptômes extraits (Douleur, Fièvre)
- [ ] Diagnostic présent (Otite)

### ✅ Compte-Rendu SOAP
- [ ] Structure SOAP respectée (S-O-A-P)
- [ ] Informations patient intégrées
- [ ] Diagnostic cohérent
- [ ] Plan de traitement détaillé
- [ ] Génération < 30s

### ✅ Lettre d'Adressage
- [ ] Destinataire ORL mentionné
- [ ] Contexte patient complet
- [ ] Raison d'adressage claire
- [ ] Examens suggérés pertinents
- [ ] Ton professionnel
- [ ] Génération < 20s

---

## 🐛 Problèmes Potentiels

### Problème 1 : Ollama ne répond pas
```bash
# Vérifier qu'Ollama tourne
ps aux | grep ollama

# Relancer si nécessaire
ollama serve

# Tester manuellement
ollama run llama2 "Bonjour"
```

### Problème 2 : Génération trop lente
```bash
# Vérifier la charge CPU
top

# Utiliser un modèle plus léger
# Dans la sidebar : mistral:7b au lieu de llama2
```

### Problème 3 : Erreur de transcription (MPS)
```
✅ DÉJÀ RÉSOLU
Le code force l'utilisation du CPU pour Whisper
```

### Problème 4 : Entités mal détectées
```
Cause : Modèle spaCy français
Solution : Vérifier que fr_core_news_md est installé
```

---

## 📈 Métriques de Performance

### Configuration Actuelle
- **CPU :** Apple Silicon (M1/M2/M3)
- **RAM :** 16 GB minimum recommandé
- **Whisper :** CPU mode (stable)
- **Ollama :** llama2:latest (3.8 GB)

### Temps Attendus
```
Audio 30s  → ~25-35s total
Audio 2min → ~40-60s total
Audio 5min → ~80-120s total
```

### Optimisations Futures
1. **GPU pour Whisper** : 3-5x plus rapide (si MPS fixé)
2. **Faster-Whisper** : 4x plus rapide
3. **Mistral 7B** : 1.5x plus rapide que Llama2
4. **Quantization 4-bit** : 2x plus rapide

---

## 🎉 Test Réussi Si...

- ✅ Transcription complète et correcte
- ✅ Entités médicales pertinentes extraites
- ✅ SOAP structuré et cohérent
- ✅ Lettre ORL professionnelle et complète
- ✅ Temps total < 60 secondes
- ✅ Aucune erreur dans les logs

---

## 🚀 Lancer le Test

```bash
# 1. Vérifier qu'Ollama tourne
ollama list

# 2. Ouvrir l'application
open http://localhost:8501

# 3. Configurer la sidebar (ORL)

# 4. Uploader l'audio de test

# 5. Attendre le traitement automatique

# 6. Vérifier les 4 résultats
```

---

**📝 Note :** Le workflow est 100% automatique. Vous n'avez qu'à :
1. Configurer les paramètres
2. Uploader l'audio
3. Attendre les résultats

**Tout le reste se fait automatiquement avec Ollama + Llama2 !**

---

**🎯 Prêt pour le test : http://localhost:8501**
