# 📁 Structure du Projet - LLM + Power BI + KPI API

```
Projet LLM/
│
├── 📄 README.md                    ← Lire en premier!
├── 📄 QUICKSTART.md                ← Démarrage rapide (5 min)
├── 📄 POWERBI_GUIDE.md             ← Configuration Power BI
│
├── 🐍 SCRIPTS PRINCIPAUX
│   ├── start.py                    ← Menu de démarrage
│   ├── setup.py                    ← Configuration initiale
│   ├── check_project.py            ← Vérifier le projet
│   ├── test_api.py                 ← Tests de l'API
│   └── examples_integration.py      ← Exemples d'utilisation
│
├── ⚙️ CONFIGURATION
│   ├── config.py                   ← Configuration du projet
│   ├── .env.example                ← Variables d'environnement
│   ├── requirements.txt            ← Dépendances Python
│   └── __init__.py                 ← Package principal
│
├── 📡 API FASTAPI
│   └── api/
│       ├── main.py                 ← Application FastAPI principale
│       └── __init__.py
│
├── 🎯 MODÈLES & SCHÉMAS
│   └── models/
│       ├── schemas.py              ← Modèles Pydantic
│       └── __init__.py
│
├── 🛠️ UTILITAIRES
│   └── utils/
│       ├── llm_handler.py          ← Intégration LLM (OpenAI/Simulation)
│       ├── powerbi_handler.py      ← Intégration Power BI
│       └── __init__.py
│
└── 📊 DONNÉES D'EXEMPLE
    └── data/
        ├── sample_data.py          ← Données d'exemple Python
        └── sample_data.json        ← Données d'exemple JSON
```

## 📋 Fichiers principaux

### 🚀 Points d'entrée
- **`start.py`** - Menu interactif pour démarrer le projet
- **`setup.py`** - Installation des dépendances et configuration
- **`check_project.py`** - Vérification de la structure et des dépendances

### 📚 Documentation
- **`README.md`** - Documentation complète (lire en premier!)
- **`QUICKSTART.md`** - Guide 5 minutes pour démarrer
- **`POWERBI_GUIDE.md`** - Configuration Power BI étape par étape

### 🐍 Code Principal
- **`api/main.py`** - API FastAPI avec tous les endpoints
- **`utils/llm_handler.py`** - Gestion du LLM (OpenAI ou simulation)
- **`utils/powerbi_handler.py`** - Intégration Push API Power BI
- **`models/schemas.py`** - Modèles de données Pydantic

### 🧪 Tests & Exemples
- **`test_api.py`** - Tests des endpoints
- **`examples_integration.py`** - Exemples d'utilisation complète

### ⚙️ Configuration
- **`config.py`** - Centralisation de la configuration
- **`.env.example`** - Variables d'environnement
- **`requirements.txt`** - Dépendances Python

## 🚀 Démarrage rapide

### 1. Installation (Windows PowerShell)
```powershell
# Aller au projet
cd "c:\Users\adss4\OneDrive - Association Cesi Viacesi mail\Documents\Projet LLM"

# Créer environnement virtuel
python -m venv venv
venv\Scripts\activate

# Installer dépendances
pip install -r requirements.txt
```

### 2. Lancer l'API
```powershell
python api/main.py
```
→ L'API est accessible sur `http://127.0.0.1:8000`

### 3. Tester (dans une autre terminal)
```powershell
# Ouvrir une nouvelle PowerShell et activer venv
venv\Scripts\activate

# Tester
python test_api.py
```

### 4. Voir la documentation
- **Swagger UI**: https://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 📚 Description des modules

### `api/main.py` - Application FastAPI
```
Endpoints principaux:
├── GET /health                  - Vérifier l'état
├── GET /kpi                     - Récupérer les KPI
├── POST /ask                    - Poser une question (LLM)
├── POST /powerbi/push           - Envoyer à Power BI
└── ... (15+ endpoints)
```

### `utils/llm_handler.py` - Gestionnaire LLM
```
Fonctionnalités:
├── OpenAI GPT-3.5 intégration
├── Préparation du contexte KPI
├── Réponses simulées (sans API)
└── Gestion des erreurs
```

### `utils/powerbi_handler.py` - Gestionnaire Power BI
```
Fonctionnalités:
├── Authentification Azure AD
├── Push API pour envoyer les données
├── Gestion des tokens
└── Mode simulation
```

## 🔑 Variables d'environnement (.env)

```env
# API
API_PORT=8000
API_HOST=127.0.0.1
DEBUG=False

# OpenAI (optionnel)
OPENAI_API_KEY=sk-...

# Power BI (optionnel)
POWERBI_TENANT_ID=...
POWERBI_CLIENT_ID=...
POWERBI_CLIENT_SECRET=...
POWERBI_DATASET_ID=...
```

## 💡 Comment utiliser

### Cas 1: Récupérer les KPI
```python
import requests
response = requests.get("http://127.0.0.1:8000/kpi")
kpi = response.json()["data"]
```

### Cas 2: Poser une question
```python
import requests
response = requests.post("http://127.0.0.1:8000/ask", json={
    "question": "Quelles sont nos ventes totales?"
})
answer = response.json()["answer"]
```

### Cas 3: Envoyer à Power BI
```python
import requests
response = requests.post("http://127.0.0.1:8000/powerbi/push", json={
    "table_name": "KPI_Ventes",
    "rows": [{"Date": "2024-03-30", "Ventes": 150000}]
})
```

## 🎯 Architecture

```
┌─────────────────────────────────────────────────┐
│               Power BI Desktop                  │
│          (Visualisations + Questions)           │
└────────────────────┬────────────────────────────┘
                     │ Requêtes REST API
                     ▼
┌─────────────────────────────────────────────────┐
│              FastAPI (Port 8000)                │
│  ┌─────────────────────────────────────────────┤
│  │ • GET /kpi          - Récupérer les KPI    │
│  │ • POST /ask         - Question LLM         │
│  │ • POST /powerbi/push - Envoyer à Power BI  │
│  └─────────────────────────────────────────────┤
│               │              │                  │
│               ▼              ▼                  │
│         ┌─────────┐    ┌──────────────┐       │
│         │ LLM     │    │ Power BI     │       │
│         │ Handler │    │ Handler      │       │
│         └─────────┘    └──────────────┘       │
│               │              │                  │
└───────────────┼──────────────┼──────────────────┘
                │              │
                ▼              ▼
          ┌─────────┐    ┌──────────────┐
          │ OpenAI  │    │ Azure AD /   │
          │ API     │    │ Power BI API │
          └─────────┘    └──────────────┘
```

## 🔗 Ressources

- [FastAPI](https://fastapi.tiangolo.com/)
- [OpenAI API](https://platform.openai.com/docs/api-reference)
- [Power BI Developer](https://learn.microsoft.com/en-us/power-bi/developer/)
- [Pydantic](https://docs.pydantic.dev/)
- [Uvicorn](https://www.uvicorn.org/)

## ✨ Features

✅ API RESTful complète
✅ Intégration LLM (OpenAI + Simulation)
✅ Intégration Power BI (Push API)
✅ Documentation Swagger automatique
✅ Gestion d'erreurs robuste
✅ Modèles de données typés
✅ Configuration par .env
✅ Tests inclus
✅ Exemples complets
✅ Mode simulation (sans credentials)

## 🎓 Apprentissage

Ce projet enseigne:
- ✅ Comment créer une API Python avec FastAPI
- ✅ Comment intégrer un LLM à une application
- ✅ Comment envoyer des données à Power BI
- ✅ Comment gérer les configurations
- ✅ Comment tester une API REST
- ✅ Comment structurer un projet Python

---

**Créé pour apprendre l'intégration LLM + Power BI** 🎓

Pour démarrer: Lisez [README.md](README.md) ou [QUICKSTART.md](QUICKSTART.md)
