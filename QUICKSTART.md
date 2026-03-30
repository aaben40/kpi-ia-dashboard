# ⚡ Guide de Démarrage Rapide

Démarrez en 5 minutes!

## 1️⃣ Installation (2 min)

```bash
# Aller au projet
cd "c:\Users\adss4\OneDrive - Association Cesi Viacesi mail\Documents\Projet LLM"

# Créer l'environnement virtuel
python -m venv venv
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

## 2️⃣ Lancer l'API (1 min)

```bash
python api/main.py
```

Vous devriez voir:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

## 3️⃣ Test rapide (2 min)

Ouvrez http://127.0.0.1:8000/docs dans votre navigateur

### Tester un endpoint:

1. **Cliquez sur "GET /kpi"**
2. **Cliquez "Try it out"**
3. **Cliquez "Execute"**
4. Vous verrez les KPI actuels!

### Poser une question au LLM:

1. **Cliquez sur "POST /ask"**
2. **Cliquez "Try it out"**
3. **Changez le body en**:
```json
{
  "question": "Quelles sont nos ventes totales?"
}
```
4. **Cliquez "Execute"**
5. La réponse IA s'affiche!

### Envoyer à Power BI:

1. **Cliquez sur "POST /powerbi/push"**
2. **Cliquez "Try it out"**
3. **Gardez l'exemple du body**
4. **Cliquez "Execute"**
5. Données envoyées (en simulation)!

## 📚 Fichiers clés

| Fichier | Rôle |
|---------|------|
| `api/main.py` | L'API FastAPI |
| `config.py` | Configuration |
| `utils/llm_handler.py` | Intégration LLM |
| `utils/powerbi_handler.py` | Intégration Power BI |
| `models/schemas.py` | Modèles de données |

## 💡 Cas d'usage rapides

### Ex 1: Récupérer les KPI
```bash
curl "http://127.0.0.1:8000/kpi"
```

### Ex 2: Poser une question
```bash
curl -X POST "http://127.0.0.1:8000/ask/simple?question=Quelles%20sont%20nos%20ventes%20totales%3F"
```

### Ex 3: Envoyer à Power BI
```bash
curl -X POST "http://127.0.0.1:8000/powerbi/push" \
  -H "Content-Type: application/json" \
  -d '{
    "table_name": "KPI_Data",
    "rows": [{"date": "2024-03-30", "ventes": 150000}]
  }'
```

## 🔑 Configuration OpenAI (optionnel)

Si vous avez une clé OpenAI:

1. Modifiez `.env.example` en `.env`
2. Ajoutez votre clé:
   ```
   OPENAI_API_KEY=sk-...
   ```
3. Relancez l'API

Sans cette clé? Pas de problème! L'API fonctionne en mode simulation. 🎯

## 🧪 Tests automatiques

```bash
python test_api.py
```

## 🎓 Prochaines étapes

1. ✅ Lancer l'API
2. ✅ Tester les endpoints
3. 📖 Lire le [README complet](README.md)
4. 🔐 Configurer [Power BI](POWERBI_GUIDE.md)
5. 🤖 Ajouter votre clé OpenAI

---

**Besoin d'aide?** Consultez [README.md](README.md)
