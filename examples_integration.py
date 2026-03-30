"""
Exemples d'intégration avec Power BI
Montre comment connecter Power BI avec l'API LLM
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import json

BASE_API_URL = "http://127.0.0.1:8000"


class PowerBIIntegration:
    """Classe pour intégrer Power BI avec l'API"""
    
    def __init__(self, api_url=BASE_API_URL):
        self.api_url = api_url
    
    def get_current_kpi(self):
        """Récupérer les KPI actuels depuis l'API"""
        response = requests.get(f"{self.api_url}/kpi")
        if response.status_code == 200:
            return response.json()["data"]
        return None
    
    def ask_question(self, question):
        """Poser une question au LLM"""
        payload = {"question": question}
        response = requests.post(f"{self.api_url}/ask", json=payload)
        if response.status_code == 200:
            return response.json()
        return None
    
    def push_kpi_to_powerbi(self, kpi_data=None):
        """Envoyer les KPI à Power BI"""
        if kpi_data is None:
            kpi_data = self.get_current_kpi()
        
        kpi_data["date"] = datetime.now().isoformat()
        
        payload = {
            "table_name": "KPI_Data",
            "rows": [kpi_data]
        }
        
        response = requests.post(f"{self.api_url}/powerbi/push", json=payload)
        return response.json()
    
    def push_historical_data(self, days=30):
        """Envoyer les données historiques à Power BI"""
        historical_data = []
        
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            # Simuler une variation des KPI
            variation = i * 0.5
            
            data = {
                "date": date.strftime("%Y-%m-%d"),
                "ventes_totales": 150000 + (variation * 1000),
                "nombre_clients": 1250 + int(variation * 5),
                "taux_conversion": 3.5 + (variation * 0.1),
                "revenu_moyen_client": 120 + variation,
                "satisfaction_client": 4.8,
                "croissance_mensuelle": 12.5 + variation,
                "cout_acquisition": 45 - variation
            }
            historical_data.append(data)
        
        payload = {
            "table_name": "KPI_Historique",
            "rows": historical_data
        }
        
        response = requests.post(f"{self.api_url}/powerbi/push", json=payload)
        return response.json()


# ============ EXEMPLES D'UTILISATION ============

def example_1_get_current_kpi():
    """Exemple 1: Récupérer les KPI actuels"""
    print("\n📊 Exemple 1: Récupérer les KPI actuels")
    print("=" * 50)
    
    integration = PowerBIIntegration()
    kpi = integration.get_current_kpi()
    
    print("KPI Actuels:")
    for key, value in kpi.items():
        print(f"  • {key}: {value}")


def example_2_ask_questions():
    """Exemple 2: Poser des questions au LLM"""
    print("\n🤖 Exemple 2: Poser des questions au LLM")
    print("=" * 50)
    
    integration = PowerBIIntegration()
    
    questions = [
        "Quelles sont nos ventes totales?",
        "Combien de clients avons-nous?",
        "Quel est notre taux de conversion?",
        "Comment évoluons-nous ce mois?"
    ]
    
    for question in questions:
        print(f"\n❓ Question: {question}")
        response = integration.ask_question(question)
        
        if response and response.get("success"):
            print(f"✅ Réponse: {response['answer']}")
        else:
            print(f"❌ Erreur: {response.get('error')}")


def example_3_push_to_powerbi():
    """Exemple 3: Envoyer les données à Power BI"""
    print("\n📈 Exemple 3: Envoyer les données à Power BI")
    print("=" * 50)
    
    integration = PowerBIIntegration()
    
    # Envoyer les KPI actuels
    result = integration.push_kpi_to_powerbi()
    print(f"Résultat: {result['message']}")
    print(f"  • Table: {result.get('table')}")
    print(f"  • Lignes envoyées: {result.get('rows_count')}")
    print(f"  • Mode: {result.get('mode', 'production')}")


def example_4_push_historical_data():
    """Exemple 4: Envoyer les données historiques"""
    print("\n📅 Exemple 4: Envoyer les données historiques")
    print("=" * 50)
    
    integration = PowerBIIntegration()
    
    print("Envoi des données historiques (30 derniers jours)...")
    result = integration.push_historical_data(days=30)
    print(f"Résultat: {result['message']}")


def example_5_advanced_workflow():
    """Exemple 5: Workflow complet"""
    print("\n🚀 Exemple 5: Workflow complet")
    print("=" * 50)
    
    integration = PowerBIIntegration()
    
    # Étape 1: Récupérer les KPI
    print("\n1️⃣  Récupération des KPI...")
    kpi = integration.get_current_kpi()
    print(f"   ✅ {len(kpi)} KPI récupérés")
    
    # Étape 2: Les envoyer à Power BI
    print("\n2️⃣  Envoi à Power BI...")
    result = integration.push_kpi_to_powerbi(kpi)
    print(f"   ✅ {result['rows_count']} ligne(s) envoyée(s)")
    
    # Étape 3: Poser des questions
    print("\n3️⃣  Analyse avec l'IA...")
    questions = [
        "Quelle est notre performance globale?",
        "Y a-t-il des domaines à améliorer?",
        "Quelles sont nos forces?"
    ]
    
    for question in questions:
        response = integration.ask_question(question)
        if response and response.get("success"):
            print(f"\n   Q: {question}")
            print(f"   R: {response['answer'][:100]}...")
    
    print("\n✅ Workflow terminé!")


def example_6_continuous_monitoring():
    """Exemple 6: Monitoring continu"""
    print("\n📊 Exemple 6: Monitoring continu (simulation)")
    print("=" * 50)
    
    integration = PowerBIIntegration()
    
    print("\nSimulation d'un monitoring continu:")
    print("  • Chaque heure: Récupérer les KPI")
    print("  • Chaque heure: Envoyer à Power BI")
    print("  • Chaque jour: Analyser avec l'IA")
    
    # Exemple pour une heure
    print("\n⏰ Simulation - 1ère heure:")
    
    # Récupérer
    kpi = integration.get_current_kpi()
    print(f"   ✓ KPI récupérés: {len(kpi)} métriques")
    
    # Envoyer
    result = integration.push_kpi_to_powerbi(kpi)
    print(f"   ✓ Données envoyées à Power BI")
    
    # Analyser
    response = integration.ask_question("Résuméz nos performances actuelles?")
    if response and response.get("success"):
        print(f"   ✓ Analyse IA: {response['answer'][:80]}...")


# ============ GUIDE POWER BI DESKTOP ============

def get_powerbi_desktop_guide():
    """Guide pour configurer Power BI Desktop"""
    guide = """
    📖 Guide Power BI Desktop Integration
    =====================================
    
    ÉTAPE 1: Créer une nouvelle requête
    ------------------------------------
    1. Ouvrir Power BI Desktop
    2. Données → Nouvelle source → Web
    3. URL: http://127.0.0.1:8000/kpi
    4. OK
    5. Power BI chargera les données KPI
    
    ÉTAPE 2: Créer des visuels
    ----------------------------
    1. Table de ventes, courbes de croissance, etc.
    2. Ajouter des filtres par date
    3. Configurer les mises en forme
    
    ÉTAPE 3: Ajouter une question AI
    --------------------------------
    1. Insert → Text Box
    2. Ajouter: "Posez une question sur les KPI"
    3. Insert → Button
    4. Configurer l'action pour appeler /ask
    
    ÉTAPE 4: Refresh automatique
    ----------------------------
    1. Accueil → Basculer vers mode édition
    2. Transformer les données → Paramètres
    3. Configurer refresh: Chaque heure
    
    DATABASE (Optionnel):
    --------------------
    Power BI Service → Datasets → Paramètres
    Planification du refresh: Quotidien 9:00
    """
    return guide


# ============ EXÉCUTION PRINCIPALE ============

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🎓 EXEMPLES D'INTÉGRATION POWER BI + LLM")
    print("=" * 70)
    
    try:
        # Vérifier que l'API est accessible
        response = requests.get(f"{BASE_API_URL}/health")
        if response.status_code != 200:
            print("❌ Erreur: L'API n'est pas accessible")
            print(f"   Assurez-vous que l'API est lancée: python api/main.py")
            exit(1)
        
        # Exécuter les exemples
        example_1_get_current_kpi()
        example_2_ask_questions()
        example_3_push_to_powerbi()
        example_4_push_historical_data()
        example_5_advanced_workflow()
        example_6_continuous_monitoring()
        
        # Afficher le guide
        print("\n" + "=" * 70)
        print(get_powerbi_desktop_guide())
        print("=" * 70)
        
        print("\n✅ Tous les exemples sont terminés!")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Erreur: Impossible de se connecter à l'API")
        print("   Assurez-vous que l'API est lancée: python api/main.py")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
