# 🔐 Security Policy - Medical Scribe AI

## 📋 Supported Versions

Nous supportons activement les versions suivantes avec des mises à jour de sécurité:

| Version | Supported          | End of Support |
| ------- | ------------------ | -------------- |
| 1.0.x   | ✅ Yes             | TBD            |
| < 1.0   | ❌ No              | -              |

---

## 🚨 Reporting a Vulnerability

### ⚠️ IMPORTANT: Ne PAS créer d'issue publique

Si vous découvrez une vulnérabilité de sécurité, **NE créez PAS d'issue publique**.

### 📧 Contact Sécurité

**Email:** security@scribemed.com (à configurer)

**GitHub Security Advisory:**
1. Aller sur https://github.com/xaviercallens/scribemed/security/advisories
2. Cliquer "Report a vulnerability"
3. Remplir le formulaire

### 📝 Informations à Fournir

Veuillez inclure:

1. **Description** de la vulnérabilité
2. **Étapes de reproduction** détaillées
3. **Impact potentiel**
4. **Version affectée**
5. **Environnement** (OS, Python version, etc.)
6. **Preuve de concept** (si disponible)
7. **Suggestions de correction** (si vous en avez)

### ⏱️ Délai de Réponse

- **Accusé de réception:** 48 heures
- **Évaluation initiale:** 5 jours ouvrables
- **Mise à jour régulière:** Toutes les semaines
- **Correction:** Selon la sévérité (voir ci-dessous)

### 🎯 Sévérité et Délais de Correction

| Sévérité | Délai de Correction | Priorité |
|----------|---------------------|----------|
| **Critical** | 24-48 heures | P0 |
| **High** | 7 jours | P1 |
| **Medium** | 30 jours | P2 |
| **Low** | 90 jours | P3 |

---

## 🔒 Mesures de Sécurité Implémentées

### 1. Architecture Sécurisée

#### 🏠 Traitement 100% Local
- ✅ Aucune donnée envoyée à des serveurs externes
- ✅ Pas d'appels API tiers
- ✅ Pas de télémétrie
- ✅ Contrôle total de l'utilisateur

#### 🔐 Authentification (Medical Scribe API)
- ✅ JWT (JSON Web Tokens)
- ✅ Tokens avec expiration
- ✅ Refresh tokens
- ✅ Validation stricte

#### 🔑 Gestion des Mots de Passe
- ✅ Hashing bcrypt (cost factor 12)
- ✅ Jamais stockés en clair
- ✅ Validation force du mot de passe
- ✅ Protection contre brute force

### 2. Sécurité des Données

#### 💾 Base de Données
- ✅ SQLite locale (pas de réseau)
- ✅ Isolation par utilisateur
- ✅ Validation des entrées
- ✅ Prepared statements (protection SQL injection)

#### 📁 Fichiers Uploadés
- ✅ Validation type MIME
- ✅ Limitation taille (100MB)
- ✅ Stockage sécurisé
- ✅ Noms de fichiers sanitizés
- ✅ Isolation par utilisateur

#### 🔒 Données Sensibles
- ✅ Pas de logs de données médicales
- ✅ Variables d'environnement pour secrets
- ✅ .env exclu de Git
- ✅ Pas de hardcoded credentials

### 3. Sécurité API

#### 🛡️ Protection CORS
- ✅ CORS configuré
- ✅ Origins whitelist
- ✅ Credentials handling

#### ✅ Validation des Entrées
- ✅ Pydantic schemas
- ✅ Type checking
- ✅ Sanitization
- ✅ Limite de taille

#### 🚫 Protection Attaques
- ✅ Rate limiting (à implémenter)
- ✅ Input validation
- ✅ Error handling sécurisé
- ✅ Pas d'exposition de stack traces

### 4. Sécurité Code

#### 📝 Bonnes Pratiques
- ✅ Code review obligatoire
- ✅ Linting (flake8, pylint)
- ✅ Type hints
- ✅ Tests automatisés

#### 🔍 Analyse Sécurité
- ✅ Bandit (security linter)
- ✅ Dependabot alerts
- ✅ Dependency scanning
- ✅ Code scanning (GitHub)

---

## 🛡️ Recommandations de Sécurité

### Pour les Utilisateurs

#### 🔐 Configuration Sécurisée

**1. Variables d'Environnement:**
```bash
# .env
SECRET_KEY=generate-a-strong-random-key-here  # 32+ caractères
DATABASE_URL=sqlite:///./medical_scribe.db
ALLOWED_ORIGINS=http://localhost:3000
```

**Générer une clé sécurisée:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**2. Permissions Fichiers:**
```bash
# Protéger .env
chmod 600 .env

# Protéger base de données
chmod 600 medical_scribe.db

# Protéger uploads
chmod 700 uploads/
```

**3. Firewall:**
```bash
# Bloquer accès externe (local seulement)
# API écoute sur 127.0.0.1:8001
# Hypocrate écoute sur 127.0.0.1:8501
```

#### 🔒 Bonnes Pratiques

- ✅ Utiliser des mots de passe forts (12+ caractères)
- ✅ Ne pas partager les tokens JWT
- ✅ Déconnecter après utilisation
- ✅ Mettre à jour régulièrement
- ✅ Sauvegarder les données chiffrées
- ✅ Utiliser HTTPS en production
- ✅ Activer le chiffrement disque

### Pour les Développeurs

#### 🔐 Développement Sécurisé

**1. Secrets:**
```python
# ❌ JAMAIS
SECRET_KEY = "hardcoded-secret"

# ✅ TOUJOURS
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    
    class Config:
        env_file = ".env"
```

**2. Validation:**
```python
# ✅ Toujours valider les entrées
from pydantic import BaseModel, validator

class AudioUpload(BaseModel):
    filename: str
    
    @validator('filename')
    def validate_filename(cls, v):
        # Sanitize filename
        return secure_filename(v)
```

**3. Logging:**
```python
# ❌ JAMAIS logger de données sensibles
logger.info(f"User password: {password}")

# ✅ Logger sans données sensibles
logger.info(f"User {user_id} authenticated")
```

#### 🧪 Tests de Sécurité

```bash
# Lancer Bandit
bandit -r backend/app

# Vérifier dépendances
pip-audit

# Scanner secrets
gitleaks detect
```

---

## 🚨 Vulnérabilités Connues

### Actuellement: Aucune

Nous maintenons une liste des vulnérabilités connues et leur statut.

---

## 📊 Historique des Mises à Jour Sécurité

### Version 1.0.0 (2025-01-01)

**Mesures de sécurité initiales:**
- JWT authentication
- Password hashing (bcrypt)
- Input validation
- CORS protection
- File upload security
- Local-only processing

---

## 🔍 Audit de Sécurité

### Dernier Audit: N/A

Nous encourageons les audits de sécurité indépendants.

### Demander un Audit

Pour demander un audit de sécurité ou partager les résultats:
- Email: security@scribemed.com
- GitHub Security Advisory

---

## 🏆 Reconnaissance

### Hall of Fame

Nous remercions les chercheurs en sécurité qui nous aident à améliorer la sécurité:

<!-- Liste des contributeurs sécurité -->
- *Aucun pour le moment*

### Récompenses

Nous ne proposons pas actuellement de bug bounty program, mais nous reconnaissons publiquement les contributions sécurité.

---

## 📚 Ressources

### Documentation Sécurité

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

### Outils Recommandés

- **Bandit** - Python security linter
- **pip-audit** - Dependency scanner
- **gitleaks** - Secret scanner
- **OWASP ZAP** - Web app scanner

---

## 🔐 Conformité

### RGPD (GDPR)

Medical Scribe AI est conçu pour être conforme RGPD:

- ✅ Traitement 100% local
- ✅ Pas de transfert de données
- ✅ Contrôle total utilisateur
- ✅ Droit à l'oubli facile
- ✅ Pas de profilage
- ✅ Transparence totale

### HIPAA (US)

Pour une conformité HIPAA complète:

- ⚠️ Chiffrement au repos requis
- ⚠️ Audit logs détaillés requis
- ⚠️ Contrôle d'accès renforcé requis
- ⚠️ Backup sécurisés requis

**Note:** La version actuelle est une base, des configurations additionnelles sont nécessaires pour HIPAA.

---

## 📞 Contact

### Équipe Sécurité

- **Email:** security@scribemed.com
- **GitHub:** https://github.com/xaviercallens/scribemed/security
- **PGP Key:** (à configurer)

### Temps de Réponse

- **Urgent (Critical):** 24h
- **Important (High):** 48h
- **Normal (Medium/Low):** 5 jours

---

## ✅ Checklist Sécurité Déploiement

Avant de déployer en production:

### Configuration
- [ ] SECRET_KEY unique et fort
- [ ] .env protégé (chmod 600)
- [ ] ALLOWED_ORIGINS configuré
- [ ] Database protégée
- [ ] Uploads directory protégé

### Réseau
- [ ] HTTPS activé (Let's Encrypt)
- [ ] Firewall configuré
- [ ] Ports non-essentiels fermés
- [ ] Rate limiting activé

### Système
- [ ] OS à jour
- [ ] Python à jour
- [ ] Dépendances à jour
- [ ] Logs configurés
- [ ] Backups automatiques

### Monitoring
- [ ] Logs monitoring
- [ ] Alertes configurées
- [ ] Health checks
- [ ] Métriques sécurité

---

<div align="center">

**🔒 La sécurité est notre priorité 🔒**

*Merci de nous aider à garder Medical Scribe AI sécurisé*

[Report Vulnerability](https://github.com/xaviercallens/scribemed/security/advisories/new) • [Security Updates](https://github.com/xaviercallens/scribemed/security)

</div>
