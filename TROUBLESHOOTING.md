# 🔧 Troubleshooting & FAQ

## ❓ Questions fréquentes

### Q1: Comment démarrer le projet?

**R:** Trois méthodes:

**Méthode 1 (Interactive)**
```powershell
python start.py
```

**Méthode 2 (Direct API)**
```powershell
python api/main.py
```

**Méthode 3 (Command line)**
```powershell
python start.py api
```

### Q2: L'API ne démarre pas

**Vérifications:**
1. Python 3.9+ installé?
   ```powershell
   python --version
   ```

2. Dépendances installées?
   ```powershell
   pip install -r requirements.txt
   ```

3. Port 8000 libre?
   ```powershell
   netstat -ano | findstr :8000
   # Si occupé, changez dans config.py: API_PORT = 8001
   ```

4. Chemin du projet correct?
   ```powershell
   cd "c:\Users\adss4\OneDrive - Association Cesi Viacesi mail\Documents\Projet LLM"
   ```

### Q3: "ModuleNotFoundError: No module named 'fastapi'"

**Solutions:**
1. Vérifiez l'environnement virtuel:
   ```powershell
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

2. Installez les dépendances:
   ```powershell
   pip install -r requirements.txt
   ```

3. Vérifiez pip:
   ```powershell
   pip --version
   python -m pip install --upgrade pip
   ```

### Q4: Erreur "Address already in use"

**Solutions:**
1. L'API est déjà lancée dans une autre fenêtre?
   - Fermez l'autre process

2. Changez le port dans `config.py`:
   ```python
   API_PORT = 8001  # Au lieu de 8000
   ```

3. Tuez les processes Python:
   ```powershell
   taskkill /IM python.exe /F
   ```

### Q5: "ModuleNotFoundError" pour le projet lui-même

**Solutions:**
1. Assurez-vous d'être dans le bon répertoire:
   ```powershell
   cd "c:\Users\adss4\OneDrive - Association Cesi Viacesi mail\Documents\Projet LLM"
   pwd  # Vérifier le chemin
   ```

2. Vérifiez les imports dans le code:
   - Les chemins doivent être relatifs au dossier racine du projet

3. Lancez depuis la racine du projet:
   ```powershell
   python api/main.py  # Pas python api\main.py\
   ```

### Q6: OpenAI API key invalide

**Solutions:**
1. Vérifiez la clé dans `.env`:
   ```env
   OPENAI_API_KEY=sk-...
   ```

2. Régénérez une clé:
   - Allez sur https://platform.openai.com/account/api-keys
   - Créez une nouvelle clé
   - Collez-la dans `.env`

3. Testez sans clé (mode simulation):
   ```powershell
   # Supprimez ou commentez OPENAI_API_KEY dans .env
   python test_api.py
   ```

### Q7: Power BI: "Credentials manquantes"

**Solutions:**
1. C'est normal en mode développement
   - L'API fonctionne en mode simulation
   - Vous verrez: `[SIMULATION] X lignes envoyées`

2. Pour configurer Power BI:
   - Lisez [POWERBI_GUIDE.md](POWERBI_GUIDE.md)
   - Suivez les étapes pour Azure AD

### Q8: Impossible de se connecter à l'API depuis Power BI

**Solutions:**
1. Vérifiez que l'API est lancée:
   ```powershell
   curl http://127.0.0.1:8000/health
   ```

2. Utilisez l'URL complète dans Power BI:
   ```
   http://127.0.0.1:8000/kpi
   ```

3. Si sur un autre machine:
   ```
   http://votre_ip:8000/kpi
   ```

4. Vérifiez le firewall:
   - Autorisez le port 8000
   - Ou changez le port dans config.py

### Q9: Tests échouent

**Solutions:**
1. Vérifiez que l'API est lancée:
   ```powershell
   # Terminal 1
   python api/main.py
   
   # Terminal 2
   python test_api.py
   ```

2. Vérifiez la configuration:
   ```powershell
   python check_project.py
   ```

3. Lancez les tests avec debug:
   ```powershell
   python test_api.py --debug
   ```

### Q10: "PermissionError" sur les fichiers

**Solutions:**
1. VS Code bloque les fichiers:
   - Fermez les fichiers ouverts
   - Redémarrez VS Code

2. Windows Defender/Antivirus:
   - Ajoutez le dossier aux exceptions

3. Permissions fichier:
   ```powershell
   icacls "chemin\au\dossier" /grant:r "%USERNAME%:F" /t
   ```

---

## 🐛 Erreurs courantes

### Erreur 1: "json.decoder.JSONDecodeError"
**Cause:** API retourne du HTML au lieu du JSON
**Solution:** Vérifiez l'URL et les paramètres

### Erreur 2: "Connection refused"
**Cause:** L'API n'est pas lancée
**Solution:** `python api/main.py`

### Erreur 3: "401 Unauthorized"
**Cause:** Credentials Power BI invalides
**Solution:** Lisez POWERBI_GUIDE.md

### Erreur 4: "timeout"
**Cause:** L'API met trop de temps
**Solution:** 
- Vérifiez la performance
- Augmentez le timeout client
- Vérifiez les logs API

---

## 📊 Logs de débogage

### Activer le mode debug

Dans `.env`:
```env
DEBUG=True
```

Ou dans le code:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Voir les logs de l'API

```powershell
# Lancer avec logs
python api/main.py 2>&1 | Tee-Object -FilePath logs.txt
```

### Tester un endpoint spécifique

```powershell
# Avec curl
curl -X GET "http://127.0.0.1:8000/health"

# Avec Invoke-WebRequest (PowerShell)
Invoke-WebRequest -Uri "http://127.0.0.1:8000/health"

# Avec Python
python -c "import requests; print(requests.get('http://127.0.0.1:8000/health').json())"
```

---

## 🆘 Aide supplémentaire

### Vérifier la structure du projet
```powershell
python check_project.py
```

### Réinstaller les dépendances
```powershell
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Réinitialiser le projet
```powershell
# Supprimer l'environnement virtuel
rmdir /s venv

# Recréer
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Vérifier
python check_project.py
```

### Contacter du support
1. Lisez la documentation:
   - README.md
   - QUICKSTART.md
   - PROJECT_STRUCTURE.md

2. Vérifiez le code:
   - Commentaires dans les fichiers
   - Docstrings dans les fonctions

3. Testez manuellement:
   - http://127.0.0.1:8000/docs
   - Utilisez Swagger UI

---

## 💡 Conseils pratiques

### Performance
- Utilisez la mode simulation si vous n'avez pas de clé OpenAI
- Cachéz les réponses du LLM
- Utilisez un pool de connexions

### Sécurité
- Ne committez jamais votre .env
- Régénérez les tokens régulièrement
- Utilisez HTTPS en production

### Développement
- Utilisez le mode debug pendant le développement
- Testez avec curl ou Postman
- Logguez tout ce qui est important

---

## 📞 Résumé rapide des commandes

```powershell
# Installation
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Lancer l'API
python api/main.py

# Tester
python test_api.py

# Voir les exemples
python examples_integration.py

# Vérifier le projet
python check_project.py

# Menu interactif
python start.py
```

---

**Besoin d'aide?** Vérifiez les documentations dans l'ordre:
1. QUICKSTART.md (5 min)
2. README.md (complète)
3. POWERBI_GUIDE.md (Power BI)
4. Ce fichier (troubleshooting)
