"""
Script simple pour poser des questions à l'IA
"""

import requests

BASE_URL = "http://127.0.0.1:8000"

def ask_ia(question):
    """Poser une question à l'IA"""
    
    payload = {
        "question": question,
        "kpi_data": None  # Utilise les KPI actuels
    }
    
    response = requests.post(f"{BASE_URL}/ask", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            print(f"\n✅ Réponse:\n{result['answer']}")
            print(f"\n📊 Modèle utilisé: {result.get('model')}")
            print(f"📡 Source: {result.get('source')}\n")
        else:
            print(f"❌ Erreur: {result.get('error')}")
    else:
        print(f"❌ Erreur API: {response.status_code}")


# Questions d'exemple à tester
questions = [
    "Quelles sont nos ventes totales?",
    "Combien de clients avons-nous?",
    "Quel est notre taux de conversion?",
    "Comment évoluons-nous ce mois-ci?",
    "Quelle est la satisfaction client?",
    "Quel est le coût d'acquisition?",
]

if __name__ == "__main__":
    print("🤖 ASSISTANT IA - Questions sur les KPI\n")
    print("=" * 60)
    
    while True:
        print("\nOptions:")
        print("1️⃣  Poser une question")
        print("2️⃣  Voir les questions d'exemple")
        print("3️⃣  Quitter\n")
        
        choice = input("> Choisissez (1-3): ").strip()
        
        if choice == "1":
            question = input("\n❓ Votre question: ").strip()
            if question:
                ask_ia(question)
        
        elif choice == "2":
            print("\n📝 Questions d'exemple:\n")
            for i, q in enumerate(questions, 1):
                print(f"{i}. {q}")
            
            try:
                q_choice = int(input("\n> Choisissez une question (1-" + str(len(questions)) + "): "))
                if 1 <= q_choice <= len(questions):
                    ask_ia(questions[q_choice - 1])
            except ValueError:
                print("❌ Entrée invalide")
        
        elif choice == "3":
            print("\n👋 Au revoir!")
            break
        
        else:
            print("❌ Option invalide")
