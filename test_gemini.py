"""
Script de diagnostic pour vérifier Gemini et l'API
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "http://127.0.0.1:8000"
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

print("=" * 60)
print("🔍 DIAGNOSTIC GEMINI + API")
print("=" * 60)

# 1. Vérifier la clé Gemini
print("\n1️⃣  CLÉ GEMINI")
if GEMINI_KEY:
    print(f"✅ Clé trouvée: {GEMINI_KEY[:10]}...{GEMINI_KEY[-5:]}")
else:
    print("❌ Clé Gemini non configurée dans .env")

# 2. Tester la connexion API
print("\n2️⃣  CONNEXION API")
try:
    response = requests.get(f"{API_URL}/health")
    print(f"✅ API répond (Status: {response.status_code})")
    print(f"   Réponse: {response.json()}")
except Exception as e:
    print(f"❌ Impossible de se connecter à l'API: {e}")
    print("   Assurez-vous que l'API est lancée avec: python api/main.py")

# 3. Tester la récupération des KPI
print("\n3️⃣  KPI ENDPOINT")
try:
    response = requests.get(f"{API_URL}/kpi")
    if response.status_code == 200:
        kpi = response.json()
        print(f"✅ KPI récupérés:")
        print(f"   Ventes: €{kpi['data']['ventes_totales']:,.0f}")
        print(f"   Clients: {kpi['data']['nombre_clients']}")
    else:
        print(f"❌ Erreur {response.status_code}")
except Exception as e:
    print(f"❌ Erreur: {e}")

# 4. Tester une question simple
print("\n4️⃣  TEST LLM (Gemini)")
try:
    response = requests.post(
        f"{API_URL}/ask",
        json={"question": "Quel est mon montant de ventes totales?"}
    )
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Réponse reçue:")
        print(f"   Modèle: {result.get('model')}")
        print(f"   Source: {result.get('source')}")
        print(f"   Réponse: {result.get('answer')}")
        
        # Vérifier si c'est vraiment Gemini ou simulation
        if "simulation" in str(result.get('source')).lower():
            print("\n⚠️  ATTENTION: Le LLM utilise le mode SIMULATION!")
            print("   Cela signifie que Gemini n'initialise pas correctement.")
        elif "gemini" in str(result.get('model')).lower():
            print("\n✅ GEMINI FONCTIONNE CORRECTEMENT!")
    else:
        print(f"❌ Erreur {response.status_code}: {response.text}")
except Exception as e:
    print(f"❌ Erreur: {e}")

print("\n" + "=" * 60)
print("📋 RÉSUMÉ")
print("=" * 60)
print("✅ Si tous les tests passent, tout fonctionne correctement!")
print("❌ Si des tests échouent, vérifiez les messages d'erreur ci-dessus.")
print("=" * 60)
