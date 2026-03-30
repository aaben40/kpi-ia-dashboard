"""
Script de vérification du projet - Lance une checklist complète
"""

import os
import sys
from pathlib import Path

# Couleurs pour le terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
CHECKMARK = '✅'
XMARK = '❌'
ARROW = '➜'


def print_header(text):
    """Afficher un header"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text:^60}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")


def check_file_exists(filepath):
    """Vérifier si un fichier existe"""
    return os.path.exists(filepath)


def check_project_structure():
    """Vérifier la structure du projet"""
    print_header("✓ STRUCTURE DU PROJET")
    
    base_path = Path(__file__).parent
    
    required_files = {
        "API": [
            "api/main.py",
            "api/__init__.py"
        ],
        "Models": [
            "models/schemas.py",
            "models/__init__.py"
        ],
        "Utils": [
            "utils/llm_handler.py",
            "utils/powerbi_handler.py",
            "utils/__init__.py"
        ],
        "Configuration": [
            "config.py",
            ".env.example",
            "requirements.txt"
        ],
        "Documentation": [
            "README.md",
            "QUICKSTART.md",
            "POWERBI_GUIDE.md"
        ],
        "Data": [
            "data/sample_data.py",
            "data/sample_data.json"
        ],
        "Tests": [
            "test_api.py",
            "examples_integration.py"
        ]
    }
    
    all_ok = True
    for category, files in required_files.items():
        print(f"\n{YELLOW}{category}{RESET}")
        for file in files:
            filepath = base_path / file
            exists = check_file_exists(filepath)
            status = f"{GREEN}{CHECKMARK}{RESET}" if exists else f"{RED}{XMARK}{RESET}"
            print(f"  {status} {file}")
            if not exists:
                all_ok = False
    
    return all_ok


def check_python_installation():
    """Vérifier Python"""
    print_header("✓ CONFIGURATION PYTHON")
    
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"\nVersion Python: {version}")
    
    if sys.version_info >= (3, 9):
        print(f"{GREEN}{CHECKMARK} Python 3.9+ installé{RESET}")
        return True
    else:
        print(f"{RED}{XMARK} Python 3.9+ requis{RESET}")
        return False


def check_dependencies():
    """Vérifier les dépendances"""
    print_header("✓ DÉPENDANCES")
    
    required_packages = {
        "fastapi": "FastAPI",
        "uvicorn": "Uvicorn",
        "pydantic": "Pydantic",
        "requests": "Requests",
        "python-dotenv": "python-dotenv"
    }
    
    print(f"\n{YELLOW}Dépendances requises:{RESET}")
    
    all_installed = True
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"  {GREEN}{CHECKMARK}{RESET} {name}")
        except ImportError:
            print(f"  {RED}{XMARK}{RESET} {name}")
            all_installed = False
    
    print(f"\n{YELLOW}Pour installer:{RESET}")
    print(f"  pip install -r requirements.txt")
    
    return all_installed


def print_quick_start():
    """Afficher le guide de démarrage rapide"""
    print_header("🚀 DÉMARRAGE RAPIDE")
    
    commands = [
        ("1. Installer les dépendances", "pip install -r requirements.txt"),
        ("2. Lancer l'API", "python api/main.py"),
        ("3. Accéder à l'API", "http://127.0.0.1:8000"),
        ("4. Accéder à Swagger UI", "http://127.0.0.1:8000/docs"),
        ("5. Tester l'API", "python test_api.py"),
        ("6. Voir les exemples", "python examples_integration.py"),
    ]
    
    for step, command in commands:
        print(f"\n{YELLOW}{step}{RESET}")
        print(f"  {BLUE}$ {command}{RESET}")


def print_features():
    """Afficher les features du projet"""
    print_header("✨ FEATURES DU PROJET")
    
    features = {
        "API FastAPI": [
            "Endpoints REST pour les KPI",
            "Intégration LLM (OpenAI compatible)",
            "Envoyer les données à Power BI",
            "Documentation Swagger automatique"
        ],
        "LLM Integration": [
            "Support OpenAI GPT-3.5",
            "Mode simulation pour tests",
            "Contexte KPI automatique",
            "Parsing intelligent des questions"
        ],
        "Power BI Integration": [
            "Envoi de données via Push API",
            "Support authentification Azure AD",
            "Mode simulation pour tests",
            "Gestion des tables dynamiques"
        ],
        "Utilitaires": [
            "Scripts de test automatiques",
            "Exemples d'intégration complets",
            "Configuration par fichier .env",
            "Gestion d'erreurs
"
        ]
    }
    
    for category, items in features.items():
        print(f"\n{YELLOW}{category}:{RESET}")
        for item in items:
            print(f"  {ARROW} {item}")


def print_config_guide():
    """Afficher le guide de configuration"""
    print_header("🔑 CONFIGURATION")
    
    print(f"\n{YELLOW}Variables d'environnement requises (.env):{RESET}")
    
    configs = {
        "API Configuration": [
            ("API_PORT", "8000", "Port de l'API"),
            ("API_HOST", "127.0.0.1", "Host de l'API"),
            ("DEBUG", "False", "Mode debug")
        ],
        "OpenAI Configuration": [
            ("OPENAI_API_KEY", "[optionnel]", "Clé API OpenAI")
        ],
        "Power BI Configuration": [
            ("POWERBI_TENANT_ID", "[optionnel]", "ID du tenant Azure AD"),
            ("POWERBI_CLIENT_ID", "[optionnel]", "ID de l'app registration"),
            ("POWERBI_CLIENT_SECRET", "[optionnel]", "Secret de l'app"),
            ("POWERBI_DATASET_ID", "[optionnel]", "ID du dataset Power BI")
        ]
    }
    
    for section, items in configs.items():
        print(f"\n  {BLUE}{section}{RESET}")
        for var, default, desc in items:
            print(f"    • {var}: {default}")
            print(f"      → {desc}")
        

def print_next_steps():
    """Afficher les prochaines étapes"""
    print_header("📚 PROCHAINES ÉTAPES")
    
    steps = [
        ("Lire la documentation", "QUICKSTART.md"),
        ("Configuration complète", "README.md"),
        ("Setup Power BI", "POWERBI_GUIDE.md"),
        ("Explorer l'API", "http://127.0.0.1:8000/docs"),
        ("Tester les exemples", "python examples_integration.py"),
        ("Configurer OpenAI", ".env (optionnel)"),
        ("Configurer Power BI", ".env (optionnel)")
    ]
    
    for step, reference in steps:
        print(f"\n{ARROW} {YELLOW}{step}{RESET}")
        print(f"   → {reference}")


def main():
    """Fonction principale"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{'🎓 PROJECT CHECKER - LLM + Power BI API':^60}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    
    # Vérifications
    structure_ok = check_project_structure()
    python_ok = check_python_installation()
    deps_ok = check_dependencies()
    
    # Afficher les informations
    print_features()
    print_quick_start()
    print_config_guide()
    print_next_steps()
    
    # Résumé
    print_header("📊 RÉSUMÉ")
    
    print(f"\n{YELLOW}État du projet:{RESET}")
    print(f"  {GREEN if structure_ok else RED}{'✓' if structure_ok else '✗'}{RESET} Structure: {'✅ OK' if structure_ok else '❌ Manque des fichiers'}")
    print(f"  {GREEN if python_ok else RED}{'✓' if python_ok else '✗'}{RESET} Python: {'✅ OK' if python_ok else '❌ Version insuffisante'}")
    print(f"  {GREEN if deps_ok else RED}{'✓' if deps_ok else '✗'}{RESET} Dépendances: {'✅ Installées' if deps_ok else '❌ Manquantes'}")
    
    print(f"\n{YELLOW}Prêt à démarrer?{RESET}")
    
    if not deps_ok:
        print(f"\n  {RED}1. Installez les dépendances:{RESET}")
        print(f"     pip install -r requirements.txt")
    
    print(f"\n  {GREEN}2. Lancez l'API:{RESET}")
    print(f"     python api/main.py")
    
    print(f"\n  {GREEN}3. Ouvrez:{RESET}")
    print(f"     http://127.0.0.1:8000/docs")
    
    print(f"\n{GREEN}Bon apprentissage! 🚀{RESET}\n")


if __name__ == "__main__":
    main()
