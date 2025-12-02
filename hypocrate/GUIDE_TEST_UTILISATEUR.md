# 🧪 Guide de Test Utilisateur - Hypocrate

## 📋 Objectif des Tests

Valider l'expérience utilisateur complète d'Hypocrate avec de vrais médecins/professionnels de santé pour :
- Tester l'interface et l'ergonomie
- Valider la qualité des transcriptions
- Évaluer la pertinence des comptes-rendus SOAP
- Identifier les améliorations nécessaires

---

## 🚀 Déploiement pour Tests

### Option 1 : Déploiement Local (Recommandé pour POC)

#### Prérequis
- MacBook ou PC avec Python 3.10+
- 8GB RAM minimum (16GB recommandé)
- Connexion internet pour téléchargement initial

#### Installation Rapide

```bash
# 1. Aller dans le dossier hypocrate
cd /Users/xcallens/CascadeProjects/windsurf-project/hypocrate

# 2. Lancer le script d'installation automatique
chmod +x start_hypocrate.sh
./start_hypocrate.sh
```

L'application sera accessible à : **http://localhost:8501**

#### Partage avec Testeurs Locaux

Si les testeurs sont sur le même réseau :

```bash
# Trouver votre IP locale
ipconfig getifaddr en0  # macOS
# ou
hostname -I  # Linux

# Lancer avec accès réseau
streamlit run hypocrate_app.py --server.address 0.0.0.0
```

Les testeurs accèdent via : **http://[VOTRE_IP]:8501**

---

### Option 2 : Déploiement Cloud (Pour Tests à Distance)

#### A. Streamlit Cloud (Gratuit, Recommandé)

**Avantages :**
- ✅ Gratuit
- ✅ Déploiement en 5 minutes
- ✅ URL publique partageable
- ✅ Mises à jour automatiques depuis GitHub

**Limitations :**
- ⚠️ Ressources limitées (1GB RAM)
- ⚠️ Peut être lent pour gros fichiers audio
- ⚠️ Nécessite modèles Whisper légers (tiny/base)

**Étapes :**

1. **Préparer le repository GitHub**
   ```bash
   # Déjà fait - votre repo est prêt !
   # https://github.com/xaviercallens/scribemed
   ```

2. **Créer fichier de configuration**
   ```bash
   # Créer .streamlit/config.toml
   mkdir -p .streamlit
   cat > .streamlit/config.toml << EOF
   [server]
   headless = true
   port = 8501
   
   [theme]
   primaryColor = "#4CAF50"
   backgroundColor = "#FFFFFF"
   secondaryBackgroundColor = "#F0F2F6"
   textColor = "#262730"
   EOF
   ```

3. **Se connecter à Streamlit Cloud**
   - Aller sur https://share.streamlit.io
   - Se connecter avec GitHub
   - Cliquer "New app"
   - Sélectionner : `xaviercallens/scribemed`
   - Branch : `main`
   - Main file : `hypocrate/hypocrate_app.py`
   - Cliquer "Deploy"

4. **URL de test générée**
   ```
   https://xaviercallens-scribemed-hypocrate-app.streamlit.app
   ```

**⚠️ Note Importante pour Streamlit Cloud :**
- Ollama ne fonctionnera PAS (nécessite serveur local)
- Solution : Utiliser API OpenAI ou Hugging Face à la place
- Modifier `hypocrate_app.py` pour utiliser API cloud

#### B. Heroku (Alternative)

**Avantages :**
- Plus de ressources que Streamlit Cloud
- Peut héberger Ollama (avec plan payant)

**Inconvénients :**
- Payant (~$7/mois minimum)
- Configuration plus complexe

#### C. AWS EC2 / Google Cloud (Pour Production)

**Avantages :**
- Contrôle total
- Performances optimales
- Peut héberger Ollama

**Inconvénients :**
- Coût plus élevé
- Configuration technique avancée
- Nécessite compétences DevOps

---

## 👥 Protocole de Test Utilisateur

### Phase 1 : Tests Internes (1-2 jours)

**Objectif :** Valider le fonctionnement technique

**Testeurs :** Équipe projet (2-3 personnes)

**Scénarios :**
1. Upload fichier audio court (1-2 min)
2. Upload fichier audio moyen (3-5 min)
3. Test différentes qualités audio
4. Test différentes spécialités
5. Vérifier tous les exports

**Checklist :**
- [ ] Interface charge correctement
- [ ] Upload fonctionne (tous formats)
- [ ] Transcription s'affiche
- [ ] Entités médicales extraites
- [ ] Compte-rendu SOAP généré
- [ ] Lettre d'adressage créée
- [ ] Exports fonctionnent (TXT, PDF, DOCX)
- [ ] Pas d'erreurs dans les logs

---

### Phase 2 : Tests Utilisateurs Réels (1 semaine)

**Objectif :** Valider l'expérience utilisateur et la qualité médicale

**Testeurs :** 5-10 médecins/professionnels de santé

**Profils recherchés :**
- 2-3 médecins généralistes
- 1-2 spécialistes (cardio, dermato, etc.)
- 1-2 infirmiers/infirmières
- 1 secrétaire médicale

#### Matériel de Test Fourni

**1. Guide Utilisateur Simplifié**
```
📧 Email d'invitation :

Bonjour Dr [Nom],

Vous êtes invité(e) à tester Hypocrate, un assistant IA pour 
automatiser vos comptes-rendus médicaux.

🔗 Accès : http://[URL]
📖 Guide : [lien vers guide]
⏱️ Durée : 30-45 minutes

Merci de tester avec 2-3 consultations réelles (anonymisées).

Cordialement,
L'équipe Hypocrate
```

**2. Fichiers Audio de Test**

Fournir 3 exemples :
- ✅ `consultation_courte.wav` (1 min - pharyngite simple)
- ✅ `consultation_moyenne.wav` (3 min - suivi diabète)
- ✅ `consultation_complexe.wav` (5 min - multi-pathologies)

**3. Questionnaire de Feedback**

```markdown
# Questionnaire de Test - Hypocrate

## Informations
- Nom : _______________
- Spécialité : _______________
- Date : _______________

## 1. Facilité d'utilisation (1-5)
- Interface intuitive : ⭐⭐⭐⭐⭐
- Clarté des instructions : ⭐⭐⭐⭐⭐
- Fluidité du workflow : ⭐⭐⭐⭐⭐

## 2. Qualité de la Transcription (1-5)
- Précision globale : ⭐⭐⭐⭐⭐
- Reconnaissance termes médicaux : ⭐⭐⭐⭐⭐
- Gestion des accents/bruits : ⭐⭐⭐⭐⭐

## 3. Extraction d'Entités (1-5)
- Allergies correctement identifiées : ⭐⭐⭐⭐⭐
- Médicaments corrects : ⭐⭐⭐⭐⭐
- Symptômes pertinents : ⭐⭐⭐⭐⭐

## 4. Compte-Rendu SOAP (1-5)
- Structure claire : ⭐⭐⭐⭐⭐
- Contenu pertinent : ⭐⭐⭐⭐⭐
- Utilisable tel quel : ⭐⭐⭐⭐⭐

## 5. Lettre d'Adressage (1-5)
- Ton professionnel : ⭐⭐⭐⭐⭐
- Informations complètes : ⭐⭐⭐⭐⭐
- Prête à envoyer : ⭐⭐⭐⭐⭐

## 6. Performance
- Temps de traitement acceptable : ☐ Oui ☐ Non
- Temps moyen observé : _____ secondes

## 7. Questions Ouvertes

**Ce qui fonctionne bien :**
_________________________________________________
_________________________________________________

**Ce qui pourrait être amélioré :**
_________________________________________________
_________________________________________________

**Fonctionnalités manquantes :**
_________________________________________________
_________________________________________________

**Utiliseriez-vous cet outil en pratique ?**
☐ Oui, certainement
☐ Oui, avec améliorations
☐ Peut-être
☐ Non

**Seriez-vous prêt à payer pour cet outil ?**
☐ Oui (prix acceptable : _____ €/mois)
☐ Non

**Commentaires additionnels :**
_________________________________________________
_________________________________________________
```

---

## 📊 Collecte des Résultats

### Métriques à Suivre

**Quantitatives :**
- Taux de réussite upload : ____%
- Temps moyen de traitement : _____ sec
- Taux d'erreurs techniques : ____%
- Taux de complétion des tests : ____%

**Qualitatives :**
- Score moyen facilité d'utilisation : ___/5
- Score moyen qualité transcription : ___/5
- Score moyen pertinence SOAP : ___/5
- Taux d'adoption potentielle : ____%

### Analyse des Feedbacks

**Bugs Critiques :**
- [ ] Liste des bugs bloquants
- [ ] Priorité de correction

**Améliorations Prioritaires :**
1. _____________________________
2. _____________________________
3. _____________________________

**Fonctionnalités Demandées :**
1. _____________________________
2. _____________________________
3. _____________________________

---

## 🔧 Support Pendant les Tests

### Hotline Test
- **Email :** support-hypocrate@[votre-domaine]
- **Slack/Discord :** Canal #hypocrate-tests
- **Téléphone :** [Numéro] (9h-18h)

### FAQ Testeurs

**Q : L'upload ne fonctionne pas**
R : Vérifiez le format (WAV, MP3, M4A) et la taille (<100MB)

**Q : La transcription est vide**
R : Vérifiez que l'audio contient bien de la parole

**Q : Le traitement est très long**
R : Normal pour fichiers >3min. Patience !

**Q : Erreur "Ollama not found"**
R : Contactez le support (problème serveur)

---

## 📅 Planning de Test

### Semaine 1 : Préparation
- Jour 1-2 : Tests internes
- Jour 3 : Corrections bugs critiques
- Jour 4-5 : Préparation matériel testeurs

### Semaine 2 : Tests Utilisateurs
- Jour 1 : Envoi invitations + onboarding
- Jour 2-4 : Tests actifs + support
- Jour 5 : Collecte feedbacks

### Semaine 3 : Analyse
- Jour 1-2 : Analyse résultats
- Jour 3-4 : Priorisation améliorations
- Jour 5 : Rapport final

---

## ✅ Checklist Déploiement

### Avant les Tests
- [ ] Application déployée et accessible
- [ ] URL de test partagée
- [ ] Fichiers audio de test préparés
- [ ] Guide utilisateur finalisé
- [ ] Questionnaire de feedback créé
- [ ] Support disponible
- [ ] Logs et monitoring activés

### Pendant les Tests
- [ ] Monitoring actif (erreurs, performances)
- [ ] Support réactif (<2h réponse)
- [ ] Collecte feedbacks quotidienne
- [ ] Corrections bugs critiques en temps réel

### Après les Tests
- [ ] Tous les questionnaires collectés
- [ ] Analyse complète effectuée
- [ ] Rapport de test rédigé
- [ ] Roadmap améliorations définie
- [ ] Remerciements envoyés aux testeurs

---

## 🎯 Critères de Succès

**Le POC est validé si :**
- ✅ 80%+ des testeurs trouvent l'interface intuitive (≥4/5)
- ✅ 75%+ des transcriptions sont jugées précises (≥4/5)
- ✅ 70%+ des SOAP sont utilisables tel quel (≥4/5)
- ✅ 60%+ des testeurs utiliseraient l'outil en pratique
- ✅ Moins de 5% de bugs critiques

---

## 📞 Contact

**Chef de Projet :** Xavier Callens
**Email :** xavier@[domaine]
**GitHub :** https://github.com/xaviercallens/scribemed

---

**Bonne chance pour les tests ! 🚀**
