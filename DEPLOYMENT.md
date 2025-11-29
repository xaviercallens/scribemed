# 🚀 Guide de Déploiement - Medical Scribe AI

Ce guide couvre le déploiement de Medical Scribe AI dans différents environnements.

---

## 📋 Table des Matières

- [Prérequis](#prérequis)
- [Déploiement Local](#déploiement-local)
- [Déploiement Docker](#déploiement-docker)
- [Déploiement Production](#déploiement-production)
- [Configuration](#configuration)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

---

## 🔧 Prérequis

### Matériel Recommandé

**Minimum:**
- CPU: 4 cores
- RAM: 8GB
- Stockage: 20GB
- OS: macOS, Linux, Windows

**Recommandé:**
- CPU: 8+ cores
- RAM: 16GB+
- GPU: NVIDIA (CUDA) ou Apple Silicon (MPS)
- Stockage: 50GB SSD
- OS: Ubuntu 22.04 LTS ou macOS

### Logiciels Requis

```bash
# Python 3.10+
python3 --version

# Ollama
ollama --version

# Git
git --version

# (Optionnel) Docker
docker --version
```

---

## 💻 Déploiement Local

### 1. Clone du Repository

```bash
git clone https://github.com/xaviercallens/scribemed.git
cd scribemed
```

### 2. Medical Scribe API

```bash
cd medical-scribe

# Créer environnement virtuel
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# ou
venv\Scripts\activate  # Windows

# Installer dépendances
pip install -r requirements.txt

# Configuration
./setup_env.sh

# Éditer .env si nécessaire
nano .env

# Lancer serveur
./start_server.sh
```

**Accès:** http://localhost:8001/docs

### 3. Hypocrate

```bash
cd hypocrate

# Utiliser le même venv ou créer un nouveau
source ../medical-scribe/venv/bin/activate

# Installer dépendances
pip install -r requirements_hypocrate.txt

# Télécharger modèles spaCy
python -m spacy download fr_core_news_md
python -m spacy download en_core_web_sm

# Installer scispaCy
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.0/en_ner_bc5cdr_md-0.5.0.tar.gz

# Lancer application
./start_hypocrate.sh
```

**Accès:** http://localhost:8501

---

## 🐳 Déploiement Docker

### Dockerfile - Medical Scribe API

Créer `medical-scribe/Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Installer dépendances système
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier application
COPY backend/ ./backend/
COPY uploads/ ./uploads/

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL=sqlite:///./medical_scribe.db

EXPOSE 8001

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

### Docker Compose

Créer `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build:
      context: ./medical-scribe
      dockerfile: Dockerfile
    ports:
      - "8001:8001"
    volumes:
      - ./medical-scribe/uploads:/app/uploads
      - ./medical-scribe/medical_scribe.db:/app/medical_scribe.db
    environment:
      - DATABASE_URL=sqlite:///./medical_scribe.db
      - OLLAMA_BASE_URL=http://ollama:11434
      - USE_LOCAL_WHISPER=true
    depends_on:
      - ollama
    networks:
      - scribemed

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    networks:
      - scribemed

  hypocrate:
    build:
      context: ./hypocrate
      dockerfile: Dockerfile
    ports:
      - "8501:8501"
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
    depends_on:
      - ollama
    networks:
      - scribemed

volumes:
  ollama_data:

networks:
  scribemed:
    driver: bridge
```

### Lancement Docker

```bash
# Build et démarrage
docker-compose up -d

# Télécharger Llama2 dans le container Ollama
docker-compose exec ollama ollama pull llama2

# Vérifier les logs
docker-compose logs -f

# Arrêt
docker-compose down
```

---

## 🌐 Déploiement Production

### Architecture Production

```
┌─────────────────────────────────────────┐
│         Load Balancer (Nginx)           │
│         SSL/TLS Termination             │
└────────────┬────────────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
┌───▼────┐      ┌────▼────┐
│  API   │      │ Hypocrate│
│ Server │      │  Server  │
└───┬────┘      └─────────┘
    │
┌───▼────────┐
│  Ollama    │
│  Server    │
└────────────┘
```

### 1. Configuration Nginx

```nginx
# /etc/nginx/sites-available/scribemed

upstream api_backend {
    server 127.0.0.1:8001;
}

upstream hypocrate_backend {
    server 127.0.0.1:8501;
}

server {
    listen 80;
    server_name api.scribemed.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.scribemed.com;

    ssl_certificate /etc/letsencrypt/live/api.scribemed.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.scribemed.com/privkey.pem;

    client_max_body_size 100M;

    location / {
        proxy_pass http://api_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 443 ssl http2;
    server_name hypocrate.scribemed.com;

    ssl_certificate /etc/letsencrypt/live/hypocrate.scribemed.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/hypocrate.scribemed.com/privkey.pem;

    location / {
        proxy_pass http://hypocrate_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 2. Systemd Services

**API Service** - `/etc/systemd/system/scribemed-api.service`:

```ini
[Unit]
Description=Medical Scribe API
After=network.target

[Service]
Type=simple
User=scribemed
WorkingDirectory=/opt/scribemed/medical-scribe
Environment="PATH=/opt/scribemed/venv/bin"
ExecStart=/opt/scribemed/venv/bin/uvicorn backend.app.main:app --host 0.0.0.0 --port 8001
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Hypocrate Service** - `/etc/systemd/system/hypocrate.service`:

```ini
[Unit]
Description=Hypocrate Medical Assistant
After=network.target

[Service]
Type=simple
User=scribemed
WorkingDirectory=/opt/scribemed/hypocrate
Environment="PATH=/opt/scribemed/venv/bin"
ExecStart=/opt/scribemed/venv/bin/streamlit run hypocrate_app.py --server.port 8501
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Ollama Service** - `/etc/systemd/system/ollama.service`:

```ini
[Unit]
Description=Ollama Service
After=network.target

[Service]
Type=simple
User=scribemed
ExecStart=/usr/local/bin/ollama serve
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 3. Activation Services

```bash
# Recharger systemd
sudo systemctl daemon-reload

# Activer services
sudo systemctl enable scribemed-api
sudo systemctl enable hypocrate
sudo systemctl enable ollama

# Démarrer services
sudo systemctl start ollama
sleep 10
sudo systemctl start scribemed-api
sudo systemctl start hypocrate

# Vérifier status
sudo systemctl status scribemed-api
sudo systemctl status hypocrate
sudo systemctl status ollama
```

### 4. SSL/TLS avec Let's Encrypt

```bash
# Installer certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtenir certificats
sudo certbot --nginx -d api.scribemed.com
sudo certbot --nginx -d hypocrate.scribemed.com

# Auto-renouvellement
sudo certbot renew --dry-run
```

---

## ⚙️ Configuration

### Variables d'Environnement Production

**Medical Scribe API** - `.env`:

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost/scribemed

# Security
SECRET_KEY=your-super-secret-key-change-this
ALLOWED_ORIGINS=https://api.scribemed.com,https://hypocrate.scribemed.com

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2:latest

# Whisper
USE_LOCAL_WHISPER=true
WHISPER_MODEL=base

# Upload
MAX_UPLOAD_SIZE=104857600
UPLOAD_DIR=/var/scribemed/uploads

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/scribemed/api.log
```

### PostgreSQL (Optionnel)

```bash
# Installer PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Créer base de données
sudo -u postgres psql
CREATE DATABASE scribemed;
CREATE USER scribemed_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE scribemed TO scribemed_user;
\q

# Mettre à jour DATABASE_URL
DATABASE_URL=postgresql://scribemed_user:secure_password@localhost/scribemed
```

---

## 📊 Monitoring

### 1. Logs

```bash
# Logs API
sudo journalctl -u scribemed-api -f

# Logs Hypocrate
sudo journalctl -u hypocrate -f

# Logs Ollama
sudo journalctl -u ollama -f

# Logs Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 2. Monitoring avec Prometheus (Optionnel)

Ajouter à `requirements.txt`:
```
prometheus-client==0.19.0
```

Dans `main.py`:
```python
from prometheus_client import Counter, Histogram, generate_latest

# Métriques
transcription_counter = Counter('transcriptions_total', 'Total transcriptions')
transcription_duration = Histogram('transcription_duration_seconds', 'Transcription duration')

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

### 3. Health Checks

```bash
# API Health
curl https://api.scribemed.com/health

# Hypocrate Health
curl https://hypocrate.scribemed.com/_stcore/health
```

---

## 🔧 Troubleshooting

### Problèmes Courants

**1. Ollama ne démarre pas**

```bash
# Vérifier status
sudo systemctl status ollama

# Vérifier logs
sudo journalctl -u ollama -n 50

# Redémarrer
sudo systemctl restart ollama
```

**2. API ne répond pas**

```bash
# Vérifier port
sudo lsof -i :8001

# Vérifier logs
sudo journalctl -u scribemed-api -n 50

# Tester localement
curl http://localhost:8001/health
```

**3. Problèmes de permissions**

```bash
# Corriger ownership
sudo chown -R scribemed:scribemed /opt/scribemed
sudo chown -R scribemed:scribemed /var/scribemed

# Corriger permissions uploads
sudo chmod 755 /var/scribemed/uploads
```

**4. Mémoire insuffisante**

```bash
# Vérifier utilisation
free -h
htop

# Ajuster swap si nécessaire
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## 🔐 Sécurité Production

### Checklist Sécurité

- [ ] SSL/TLS activé (HTTPS)
- [ ] Firewall configuré (UFW)
- [ ] Fail2ban installé
- [ ] Mots de passe forts
- [ ] SECRET_KEY unique
- [ ] Backups automatiques
- [ ] Logs monitoring
- [ ] Updates régulières

### Configuration Firewall

```bash
# UFW
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

### Backups

```bash
# Script backup
#!/bin/bash
BACKUP_DIR=/var/backups/scribemed
DATE=$(date +%Y%m%d_%H%M%S)

# Backup database
pg_dump scribemed > $BACKUP_DIR/db_$DATE.sql

# Backup uploads
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz /var/scribemed/uploads

# Nettoyer anciens backups (>30 jours)
find $BACKUP_DIR -mtime +30 -delete
```

---

## 📞 Support

Pour toute question sur le déploiement:
- Issues: https://github.com/xaviercallens/scribemed/issues
- Documentation: https://github.com/xaviercallens/scribemed

---

**Bon déploiement!** 🚀
