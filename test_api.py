"""
Script de test pour la API
"""

import requests
from config import SAMPLE_KPIS

BASE_URL = "http://127.0.0.1:8000"


def test_health():
    """Tester le health check"""
    print("\n=== Test Health Check ===")
    response = requests.get(f"{BASE_URL}/health")
    print(response.json())


def test_get_kpi():
    """Tester la récupération des KPI"""
    print("\n=== Test GET KPI ===")
    response = requests.get(f"{BASE_URL}/kpi")
    print(response.json())


def test_ask_question():
    """Tester une question LLM"""
    print("\n=== Test Ask Question ===")
    payload = {
        "question": "Quelles sont nos ventes totales?",
        "kpi_data": SAMPLE_KPIS
    }
    response = requests.post(f"{BASE_URL}/ask", json=payload)
    print(response.json())


def test_ask_simple():
    """Tester une question simple"""
    print("\n=== Test Ask Simple ===")
    params = {"question": "Combien de clients avons-nous?"}
    response = requests.get(f"{BASE_URL}/ask/simple", params=params)
    print(response.json())


def test_powerbi_push():
    """Tester l'envoi à Power BI"""
    print("\n=== Test Power BI Push ===")
    payload = {
        "table_name": "KPI_Data",
        "rows": [
            {
                "date": "2024-03-30",
                "ventes_totales": 150000,
                "nombre_clients": 1250
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/powerbi/push", json=payload)
    print(response.json())


def test_templates():
    """Obtenir les questions templates"""
    print("\n=== Questions Templates ===")
    response = requests.get(f"{BASE_URL}/templates/questions")
    print(response.json())


if __name__ == "__main__":
    print("🧪 Tests de l'API LLM + Power BI")
    print("Assurez-vous que l'API est en cours d'exécution: python api/main.py")
    
    try:
        test_health()
        test_get_kpi()
        test_templates()
        test_ask_simple()
        test_ask_question()
        test_powerbi_push()
        
        print("\n✅ Tous les tests sont terminés!")
    except requests.exceptions.ConnectionError:
        print("\n❌ Erreur: Impossible de se connecter à l'API")
        print("Assurez-vous que l'API est en cours d'exécution sur", BASE_URL)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
