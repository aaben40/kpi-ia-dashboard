# � KPI IA Dashboard

Un dashboard interactif pour analyser les KPI d'une entreprise avec l'intelligence artificielle (Google Gemini). 

Interface Streamlit + API FastAPI + LLM multilingue pour répondre aux questions business en temps réel.

## 📋 Vue d'ensemble

Ce projet démontre comment:
1. **Créer un dashboard interactif** avec Streamlit
2. **Construire une API REST robuste** avec FastAPI
3. **Intégrer un LLM** (Google Gemini) pour analyser les KPI
4. **Gérer une architecture multi-couches** scalable
5. **Envoyer les données à Power BI** (infrastructure prête)

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Streamlit Dashboard (Frontend)             │
│  ┌─────────────────────────────────────────────────────────┤
│  │ • 🏠 Accueil (infos API)                               │
│  │ • 🤖 Questions IA (chatbot + historique)               │
│  │ • 📊 Données KPI (métriques temps réel)               │
│  │ • 💾 Power BI (intégration)                           │
│  │ • ❓ Aide (documentation)                              │
│  └─────────────────────────────────────────────────────────┘
                            │ HTTP Requests
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  FastAPI (Backend REST)                     │
│  ┌────────────────────────────────────────────────────────┤
│  │ • GET /health          (Health check)                  │
│  │ • GET /kpi             (Récupère les KPI)             │
│  │ • POST /ask            (Question → IA)                │
│  │ • GET /info            (Metadata API)                 │
│  │ • GET /templates/questions                            │
│  │ • POST /powerbi/...    (Intégration Power BI)        │
│  └────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                 LLM Handler (Multi-Provider)               │
│  ┌────────────────────────────────────────────────────────┤
│  │ Provider Primary: Google Gemini 2.5 Flash             │
│  │ Fallback Chain: OpenAI → Ollama → Simulation         │
│  └────────────────────────────────────────────────────────┘
```

## 🛠️ Installation

### Prérequis
- **Python 3.12+** (obligatoire pour google-generativeai)
- pip
- Git
- Une clé API Google Gemini (gratuite)

### Étapes d'installation

1. **Naviguer au projet**
```bash
cd votre pattern
```

2. **Créer un environnement virtuel**
```bash
python -m venv .venv

# Sur Windows:
.venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**
```bash
# Les variables essentielles dans .env:
LLM_PROVIDER=gemini
GEMINI_API_KEY=votre_clé_api_gemini
API_HOST=127.0.0.1
API_PORT=8000
DEBUG=True
```

## 🚀 Démarrage rapide

### 1️⃣ Terminal 1 - Lancer l'API
```bash
.venv\Scripts\activate
python api/main.py
```

Vous verrez:
```
✅ LLM Provider: Gemini
✅ Model: gemini-2.5-flash
Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

**Documentation API interactive**: 
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### 2️⃣ Terminal 2 - Lancer le Dashboard Streamlit
```bash
.venv\Scripts\activate
streamlit run app.py
```

Streamlit ouvrira automatiquement le navigateur sur `http://localhost:8501`

### 3️⃣ Utiliser l'application
- **Page Accueil** 🏠: Informations générales et status de l'API
- **Page Questions IA** 🤖: Poser des questions sur les KPI (ex: "Quelles sont nos ventes?")
- **Page Données KPI** 📊: Visualiser tous les KPI en temps réel
- **Page Power BI** 💾: Envoyer les données vers Power BI
- **Page Aide** ❓: Documentation et troubleshooting

## 📚 Endpoints principaux

### 1️⃣ Health Check
```http
GET /health
```
```json
{
  "status": "healthy",
  "llm_available": true,
  "llm_provider": "gemini"
}
```

### 2️⃣ Récupérer les KPI
```http
GET /kpi
```

**Response:**
```json
{
  "data": {
    "ventes_totales": 150000,
    "nombre_clients": 1250,
    "taux_conversion": 3.5,
    "revenu_moyen_client": 120,
    "satisfaction_client": 4.8,
    "croissance_mensuelle": 12.5,
    "cout_acquisition": 50
  },
  "last_updated": "2024-03-30T14:22:45.123456"
}
```

### 3️⃣ Poser une question à l'IA
```http
POST /ask
```

**Request Body:**
```json
{
  "question": "Quelles sont nos ventes totales?",
  "kpi_data": null
}
```

**Response:**
```json
{
  "success": true,
  "answer": "Vos ventes totales sont de 150 000 €, représentant une croissance de 12.5% ce mois. C'est un excellent résultat...",
  "question": "Quelles sont nos ventes totales?",
  "source": "gemini",
  "model": "gemini-2.5-flash"
}
```

### 4️⃣ Questions suggérées
```http
GET /templates/questions
```

```json
{
  "templates": [
    "Quelles sont nos ventes totales?",
    "Quel est notre taux de conversion?",
    "Combien de clients avons-nous?",
    "Quel est notre coût d'acquisition client?",
    "Quelle est notre satisfaction client?"
  ]
}
```

### 5️⃣ Métadonnées API
```http
GET /info
```

```json
{
  "version": "1.0.0",
  "config": {
    "llm_provider": "gemini",
    "llm_model": "gemini-2.5-flash",
    "debug": true
  }
}
```

## 🔐 Configuration Google Gemini

### Étapes pour obtenir une clé API gratuite

1. **Aller sur Google AI Studio**
   - Visitez https://ai.google.dev/

2. **Créer une clé API**
   - Cliquez "Get API Key"
   - Créez un nouveau projet ou sélectionnez un existant
   - Copiez votre clé API

3. **Ajouter à .env**
```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=votre_clé_api_ici
```

4. **Relancer l'API**
```bash
python api/main.py
```

**Quota gratuit Gemini:**
- 15 requêtes par minute
- 1,000,000 tokens/jour pour gemini-2.5-flash
- Gratuit à 100% pour les tests

### Modèles disponibles

Nous utilisons **`gemini-2.5-flash`** car:
- ✅ Rapide (latence faible)
- ✅ Quota gratuit élevé
- ✅ Bon pour l'analyse de texte
- ✅ Efficace pour KPI analysis

Autres modèles disponibles:
- `gemini-2.5-pro` - Plus puissant (quota réduit)
- `gemini-2.0-flash` - Version précédente
- `gemini-pro-latest` - Dernière version

## 📊 Exemple d'utilisation

### Cas d'usage: Analyser les KPI en temps réel

**Via l'interface Streamlit:**

1. Ouvrir http://localhost:8501
2. Aller à "Questions IA"
3. Taper une question: "Quel est notre taux de conversion?"
4. L'IA répond instantanément avec analyse

**Via l'API directement:**

```python
import requests

# Poser une question
response = requests.post(
    "http://127.0.0.1:8000/ask",
    json={
        "question": "Y a-t-il une relation entre le coût d'acquisition et la satisfaction client?"
    }
)

print(response.json())
# {
#   "success": true,
#   "answer": "Le coût d'acquisition de 50€ par client combiné à une satisfaction de 4.8/5...",
#   "source": "gemini",
#   "model": "gemini-2.5-flash"
# }
```

### Intégration Power BI (Infrastructure prête)

L'API a les endpoints Power BI prêts:
- `GET /powerbi/status` - Status de connexion
- `POST /powerbi/push-kpi` - Envoyer les KPI actuels

Pour configurer:
1. Créer un App Registration dans Azure
2. Ajouter les credentials dans .env
3. Relancer l'API

## 📁 Structure du projet

```
Projet LLM/
├── api/
│   ├── __init__.py
│   └── main.py                 # API FastAPI avec 15+ endpoints
├── models/
│   ├── __init__.py
│   └── schemas.py              # Modèles Pydantic v2
├── utils/
│   ├── __init__.py
│   ├── llm_handler.py          # Multi-provider LLM (Gemini, OpenAI, Ollama, Simulation)
│   └── powerbi_handler.py      # Intégration Power BI (optionnel)
├── data/
│   ├── sample_data.py
│   └── sample_kpi.json
├── app.py                       # Dashboard Streamlit avec 5 pages
├── config.py                    # Configuration centralisée
├── .env                         # Variables d'environnement (GEMINI_API_KEY, etc.)
├── requirements.txt             # Dépendances Python
└── README.md                    # Ce fichier
```

### Fichiers clés

**app.py** - Interface Streamlit
- 5 pages navigables (Accueil, Questions IA, Données KPI, Power BI, Aide)
- Historique chat persistant
- Affichage temps réel des KPI

**api/main.py** - Backend FastAPI
- 15+ endpoints RESTful
- Gestion multi-provider LLM
- Documentation Swagger auto-généré

**utils/llm_handler.py** - Intégration IA
- Provider selectable: Gemini, OpenAI, Ollama, Simulation
- Auto-fallback si un provider échoue
- Debug logging activé

## 🎯 Prochaines étapes

### MVP actuellement fonctionnel ✅
- Dashboard Streamlit complet
- API FastAPI robuste
- LLM Gemini intégré
- Historique des conversations
- Architecture extensible

### Pour approfondir:

1. **Base de données persistante** 🗄️
   - Remplacer stockage mémoire par PostgreSQL/SQLite
   - Persister les conversations et KPI

2. **Authentification utilisateur** 🔐
   - JWT tokens
   - OAuth2 avec Google/Microsoft
   - Gestion des rôles

3. **Power BI integration** 📈
   - Configurer les credentials Azure
   - Créer un push automatique des KPI
   - Dashboards Power BI liés

4. **Monitoring & Analytics** 📊
   - Logs centralisés (ELK, Datadog)
   - Métriques de performance
   - Alertes

5. **Déploiement** 🚀
   - Docker (conteneurisation)
   - Kubernetes (orchestration)
   - Azure App Service, Heroku, AWS

6. **Features avancées** ⭐
   - Vraie analyse ML des trends KPI
   - Prédictions avec Prophet/LSTM
   - Multi-langue support
   - Export PDF/Excel des rapports

## 💡 Concepts clés

### Qu'est-ce qu'un LLM?
Un Large Language Model est un modèle d'IA entraîné sur des milliards de textes. Il peut:
- Comprendre des questions naturelles (NLP)
- Analyser du contexte (les KPI)
- Générer des réponses intelligentes et pertinentes

### Architecture du projet

**3 couches:** 
```
Streamlit (UI) → FastAPI (API) → Gemini (IA)
```

1. **Frontend (Streamlit)**: Interface utilisateur interactive
2. **Backend (FastAPI)**: Couche métier et orchestration
3. **LLM (Gemini)**: Moteur d'analyse IA

### Comment fonctionne une question IA?

```
1. Utilisateur tape: "Quelles sont nos ventes?"
                            ↓
2. Streamlit envoie: POST /ask
                            ↓
3. FastAPI récupère les KPI
                            ↓
4. FastAPI forge un prompt: "Voici les KPI: ... Question: ..."
                            ↓
5. Gemini API traite le prompt
                            ↓
6. Gemini retourne la réponse: "Vos ventes totales sont..."
                            ↓
7. FastAPI retourne le JSON
                            ↓
8. Streamlit affiche la réponse
```

### Multi-Provider Fallback

Si Gemini est indisponible, l'API bascule automatiquement:
```
Gemini ❌ → OpenAI ❌ → Ollama ❌ → Simulation ✅
```

Cela assure une continuité de service.

## 📖 Ressources utiles

### Documentation officielle
- [FastAPI Documentation](https://fastapi.tiangolo.com/) - Backend framework
- [Streamlit Documentation](https://docs.streamlit.io/) - Frontend framework
- [Google Gemini API](https://ai.google.dev/) - LLM API
- [Pydantic Documentation](https://docs.pydantic.dev/) - Data validation

### Tutoriels & Guides
- [FastAPI + Streamlit Integration](https://docs.streamlit.io/knowledge-base/tutorials)
- [Python async/await](https://docs.python.org/3/library/asyncio.html)
- [REST API Best Practices](https://restfulapi.net/)

### Outils utiles
- [Swagger Editor](https://editor.swagger.io/) - Valider les specs REST
- [Postman](https://www.postman.com/) - Tester les APIs
- [Visual Studio Code](https://code.visualstudio.com/) - IDE Python

## ⚠️ Limitations et notes

### Actuellement
- **Stockage KPI**: En mémoire (reset au redémarrage de l'API)
- **Historique chat**: Stocké en session Streamlit (reste 30 min)
- **Authentification**: Aucune (local/preuve de concept)
- **Power BI**: Infrastructure prête, credentials requis pour intégration

### À améliorer
- Ajouter une vraie base de données (PostgreSQL)
- Implémenter authentification JWT
- Caching des réponses LLM
- Rate limiting pour éviter quota exhaustion
- Logging structuré (ELK, Datadog)

### Quota Gemini
- 15 req/min (free tier)
- 1M tokens/jour pour gemini-2.5-flash
- Si quota épuisé: l'API bascule en mode Simulation

### Performance
- Latence moyenne: 1-3 secondes par question
- API réactif en async/await
- Streamlit rechargement rapide

## 🤝 Contribution & Feedback

Suggestions d'améliorations:
- 🔐 Ajouter authentification utilisateur
- 🗄️ Intégrer une base de données
- 🎨 Améliorer le design Streamlit
- 📊 Créer des graphiques de tendances
- 🌐 Support multi-langue
- 🧪 Ajouter des tests unitaires

## 📝 Licence

MIT License - Utilisez librement pour apprendre et développer

Dernier update: Décembre 2025
