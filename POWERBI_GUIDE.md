# 📊 Guide d'Intégration Power BI

Ce guide explique comment intégrer Power BI avec l'API LLM.

## 1. Configuration basique (Mode Simulation)

### Démarrage rapide sans credentials

Si vous voulez juste tester l'API:

1. **Lancez l'API**
```bash
python api/main.py
```

2. **Power BI en simulation mode**
   - L'API créera des données fictives
   - Aucun credential n'est nécessaire
   - Parfait pour apprendre!

## 2. Configuration avec credentials Power BI réels

### Création du Service Principal

#### Étape 1: Créer l'App Registration

1. Allez sur [Azure Portal](https://portal.azure.com)
2. Recherchez **App registrations**
3. Cliquez **New registration**
4. Remplissez les informations:
   - **Name**: `LLM-PowerBI-API`
   - **Supported account types**: Accounts in this organizational directory only
5. Cliquez **Register**

#### Étape 2: Récupérer les credentials

Dans la page d'accueil de l'application:

1. **Copier Application (client) ID** → Utilisez pour `POWERBI_CLIENT_ID`
2. **Copier Directory (tenant) ID** → Utilisez pour `POWERBI_TENANT_ID`

Pour le secret:
1. Allez dans **Certificates & secrets**
2. Cliquez **New client secret**
3. Donnez-lui un nom et une durée
4. Cliquez **Add**
5. **Copier la valeur** → Utilisez pour `POWERBI_CLIENT_SECRET`

#### Étape 3: Configurer les permissions Power BI

1. Allez dans **API permissions**
2. Cliquez **Add a permission**
3. Recherchez **Power BI Service**
4. Sélectionnez **Delegated permissions**
5. Cochez les permissions:
   - `Content.Create`
   - `Workspace.ReadWrite.All`
   - `Report.ReadWrite.All`
   - `Dataset.ReadWrite.All`
6. Cliquez **Add permissions**
7. **Important**: Cliquez "Grant admin consent for..."

#### Étape 4: Configurer votre fichier .env

```env
POWERBI_TENANT_ID=your-directory-id
POWERBI_CLIENT_ID=your-application-id
POWERBI_CLIENT_SECRET=your-secret-value
POWERBI_DATASET_ID=your-dataset-id
```

## 3. Configuration Power BI Desktop

### Créer un Dataset Power BI

1. **Ouvrir Power BI Desktop**
2. **Créer une nouvelle requête**
   - Home → New Source → Web
   - URL: `http://127.0.0.1:8000/kpi`

3. **Configurer le refresh automatique**
   - File → Options → Power Query Editor
   - Configurer le refresh planifié

### Créer des visuels avec questions LLM

#### Option 1: Tableau blanc pour les questions

1. **Ajouter un new page**
2. **Insert → Text box**
3. **Dans la boîte de texte**, ajouter une question:
   ```
   Questions KPI :
   - Quelles sont nos ventes totales?
   - Quel est notre taux de conversion?
   - Comment évoluons-nous?
   ```

4. **Ajouter un bouton pour poster la question**
   - Insert → Buttons → Blank
   - Configurez une action Power Query pour appeler l'API

#### Option 2: Utiliser Power Query pour appeler l'API LLM

1. **Home → New Source → Web**
2. **URL**: `http://127.0.0.1:8000/ask`
3. **Headers**:
   ```
   Content-Type: application/json
   ```
4. **Body**:
   ```json
   {"question": "Quelles sont nos ventes totales?"}
   ```

## 4. Intégration API Power BI REST

### Endpoint pour Push des données

```
POST https://api.powerbi.com/v1.0/myorg/datasets/{datasetId}/tables/{tableName}/rows

Headers:
  Authorization: Bearer {accessToken}
  Content-Type: application/json

Body:
{
  "rows": [
    {
      "Date": "2024-03-30",
      "Ventes": 150000,
      "Clients": 1250
    }
  ]
}
```

### Via Python/API

```python
import requests

# Depuis votre application
payload = {
    "table_name": "KPI_Ventes",
    "rows": [
        {
            "Date": "2024-03-30",
            "Ventes": 150000,
            "Clients": 1250,
            "Croissance": 12.5
        }
    ]
}

response = requests.post(
    "http://127.0.0.1:8000/powerbi/push",
    json=payload
)

print(response.json())
```

## 5. Créer un Dashboard avec les Questions LLM

### Architecture recommandée

```
Power BI Dashboard
├── Visuels KPI (Cartes, jauges)
├── Graphiques (Ventes, Clients, Croissance)
├── Table de texte pour les questions
└── Boutons pour chaque question fréquente
    ├── "Ventes totales?" → POST /ask
    ├── "Taux conversion?" → POST /ask
    └── "Comment on évolue?" → POST /ask
```

### Exemple de Requête Power Query

```m
let
    Url = "http://127.0.0.1:8000/ask",
    Question = "Quelles sont nos ventes totales?",
    Headers = [#"Content-Type" = "application/json"],
    Body = Text.FromBinary(Json.FromValue([question = Question])),
    Response = Json.Document(
        Web.Contents(
            Url,
            [
                Headers = Headers,
                Content = Text.ToBinary(Body),
                ManualStatusHandling = {400, 404}
            ]
        )
    )
in
    Response[answer]
```

## 6. Refresh et Automation

### Configurer des refreshs automatiques

1. **Power BI Service**
2. **Datasets → Paramètres du dataset**
3. **Planification du refresh**
4. Configurez pour refresh quotidien

### Automation avec Python

```python
import schedule
import requests
import time

def update_powerbi():
    # Récupérer les KPI
    kpi_response = requests.get("http://localhost:8000/kpi")
    kpi_data = kpi_response.json()["data"]
    
    # Envoyer à Power BI
    payload = {
        "table_name": "KPI_Historique",
        "rows": [{
            "Date": "2024-03-30",
            **kpi_data
        }]
    }
    
    response = requests.post(
        "http://localhost:8000/powerbi/push",
        json=payload
    )
    
    print(f"✅ Power BI mis à jour: {response.json()}")

# Refresh tous les jours à 9:00
schedule.every().day.at("09:00").do(update_powerbi)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## 7. Troubleshooting

### Problème: "Erreur d'authentification Power BI"

**Solutions**:
1. Vérifiez les credentials .env
2. Assurez-vous que le secret n'a pas expiré
3. Régénérez le secret si nécessaire

### Problème: "Dataset not found"

**Solutions**:
1. Vérifiez le `POWERBI_DATASET_ID`
2. Le dataset doit être publié en Power BI Service
3. Vérifiez les permissions du service principal

### Problème: "Mode simulation activé"

**Raison**: Credentials Power BI manquantes
**Solution**: Remplissez .env ou utilisez en mode simulation

## 8. Cas d'usage avancés

### Créer un cockpit avec propositions IA

```
Dashboard Power BI
│
├─ Visuels KPI actuels
├─ Graphiques de tendance
└─ Widget IA
   ├ Question proposée: "Recommandations optimisation"
   ├ Réponse LLM: "D' après vos données..."
   └ Bouton "Exécuter Action"
```

### Intégration avec Power Automate

Créer un flow Power Automate:
1. Trigger: Lors d'un refresh Power BI
2. Action: Appeler l'API `/ask`
3. Stocker la réponse en Power BI

## 9. Performance et limitations

### Limitations Power BI
- **Max 10000 lignes par push** (limitez avec pagination)
- **Max 1GB de données** en direct
- **Max 8 requêtes parallèles**

### Optimisations
- Paginé les données
- Cache les réponses LLM
- Utiliser Row-Level Security (RLS)

---

📚 Pour plus d'info: [Microsoft Power BI Developer](https://learn.microsoft.com/en-us/power-bi/developer/)
