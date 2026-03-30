# 🎯 Configuration Gemini - Guide rapide

## 🚀 Étape 1: Obtenir une clé Gemini GRATUITE

1. Allez sur: **https://ai.google.dev/tutorials/setup**
2. Cliquez **"Get API Key"**
3. Acceptez les termes
4. Copiez votre clé (commence par `AIza...`)

## ✏️ Étape 2: Configurer votre .env

Ouvrez le fichier `.env` dans le projet:

```env
# LLM Provider Selection
LLM_PROVIDER=gemini

# Gemini Configuration
GEMINI_API_KEY=AIza_YOUR_KEY_HERE
```

Remplacez `AIza_YOUR_KEY_HERE` par votre vraie clé!

## ✅ Étape 3: Redémarrer l'API

```powershell
# Arrêtez l'API en cours (Ctrl+C)
# Puis relancez:
python api/main.py
```

Vous devriez voir:
```
✅ LLM Provider: Gemini (gemini-1.5-flash)
INFO:     Uvicorn running on http://127.0.0.1:8000
```

## 🎉 C'est tout!

Maintenant vous avez:
- ✅ **Gemini gratuit** (60 appels/minute inclus)
- ✅ **Pas de quota** (contrairement à OpenAI)
- ✅ **Modèle très puissant** (gemini-1.5-flash)
- ✅ **Entièrement gratuit**

## 📊 Limitations Gemini

- **60 requêtes/minute** (très généreux!)
- **Context window:** 128K tokens
- **Gratuit:** Oui, sans crédit

## 🔑 Où obtenir la clé

https://ai.google.dev/tutorials/setup

## 💡 Alternatives

Si Gemini ne fonctionne pas:
- Le code basculera automatiquement à OpenAI
- Puis à Ollama
- Puis au mode Simulation

Changez le LLM_PROVIDER dans .env si vous préférez!

---

**Besoin d'aide?** Consultez [README.md](README.md)
