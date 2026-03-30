"""
Configuration d'initialisation automatique pour le projet
Crée les fichiers .env et installe les dépendances
"""

import os
import sys
import subprocess
from pathlib import Path

def create_env_file():
    """Créer le fichier .env s'il n'existe pas"""
    env_path = Path(".env")
    example_path = Path(".env.example")
    
    if not env_path.exists() and example_path.exists():
        print("Création du fichier .env...")
        with open(example_path, 'r') as f:
            content = f.read()
        with open(env_path, 'w') as f:
            f.write(content)
        print("✅ .env créé (copie de .env.example)")
    elif env_path.exists():
        print("✅ .env exists")
    else:
        print("⚠️  .env.example non trouvé")


def install_dependencies():
    """Installer les dépendances"""
    print("\nInstallation des dépendances...")
    print("Note: Assurez-vous d'avoir Python 3.9+ et pip installés\n")
    
    try:
        # Vérifier Python
        if sys.version_info < (3, 9):
            print("❌ Python 3.9+ requis")
            return False
        
        # Installer les packages
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        
        print("\n✅ Dépendances installées avec succès")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erreur lors de l'installation: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        return False


def print_next_steps():
    """Afficher les prochaines étapes"""
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║               ✅ Installation complète!                           ║
║                                                                    ║
║  Prochaines étapes:                                              ║
║                                                                    ║
║  1️⃣  Lancez l'API:                                                ║
║     python api/main.py                                           ║
║                                                                    ║
║  2️⃣  Accédez à l'API:                                             ║
║     http://127.0.0.1:8000                                        ║
║                                                                    ║
║  3️⃣  Documentation interactive:                                   ║
║     http://127.0.0.1:8000/docs                                   ║
║                                                                    ║
║  4️⃣  Testez l'API:                                                ║
║     python test_api.py                                           ║
║                                                                    ║
║  📚 Documentation:                                                ║
║     - QUICKSTART.md        (Démarrage rapide)                    ║
║     - README.md            (Documentation complète)              ║
║     - POWERBI_GUIDE.md     (Configuration Power BI)              ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
""")


def main():
    """Fonction principale"""
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║     🎓 Initialisation - LLM + Power BI + KPI API                  ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
""")
    
    # Créer .env
    create_env_file()
    
    # Installer les dépendances
    install_dependencies()
    
    # Afficher les prochaines étapes
    print_next_steps()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Installation annulée")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        sys.exit(1)
