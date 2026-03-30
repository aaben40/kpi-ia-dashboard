#!/usr/bin/env python
"""
Script de démarrage - Exécute le projet facilement
"""

import os
import sys
import subprocess
from pathlib import Path

print("""

╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║          🚀 LLM + Power BI + KPI API - Démarrage                  ║
║                                                                    ║
║  Mini projet pour apprendre l'intégration IA avec Power BI        ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝

""")

def run_check():
    """Vérifier le projet"""
    print("📋 Vérification du projet...")
    subprocess.run([sys.executable, "check_project.py"])


def run_api():
    """Lancer l'API"""
    print("\n▶️  Lancement de l'API...")
    print("   → Accédez à http://127.0.0.1:8000")
    print("   → Documentation: http://127.0.0.1:8000/docs\n")
    try:
        subprocess.run([sys.executable, "api/main.py"])
    except KeyboardInterrupt:
        print("\n\n⏹️  API arrêtée")


def run_tests():
    """Lancer les tests"""
    print("\n🧪 Lancement des tests...")
    subprocess.run([sys.executable, "test_api.py"])


def run_examples():
    """Exécuter les exemples"""
    print("\n📚 Exécution des exemples...")
    subprocess.run([sys.executable, "examples_integration.py"])


def main():
    """Menu principal"""
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "check":
            run_check()
        elif command == "api":
            run_api()
        elif command == "test":
            run_tests()
        elif command == "examples":
            run_examples()
        else:
            print(f"❌ Commande inconnue: {command}")
            print("\nCommandes disponibles:")
            print("  python start.py check     - Vérifier le projet")
            print("  python start.py api       - Lancer l'API")
            print("  python start.py test      - Tester l'API")
            print("  python start.py examples  - Voir les exemples")
    
    else:
        # Menu interactif
        print("\n📌 Que voulez-vous faire?\n")
        print("1️⃣  Vérifier le projet")
        print("2️⃣  Lancer l'API")
        print("3️⃣  Tester l'API")
        print("4️⃣  Voir les exemples")
        print("5️⃣  Quitter")
        
        choice = input("\n> Choisissez une option (1-5): ").strip()
        
        if choice == "1":
            run_check()
        elif choice == "2":
            run_api()
        elif choice == "3":
            run_tests()
        elif choice == "4":
            run_examples()
        elif choice == "5":
            print("\n👋 À bientôt!")
        else:
            print("\n❌ Option invalide")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Arrêt du programme")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        sys.exit(1)
