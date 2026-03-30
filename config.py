"""Configuration du projet"""
import os
from dotenv import load_dotenv
from data.sample_data import sample_kpi, kpi_history, sales_by_region, sales_by_product, sales_by_channel, customer_demographics, financial_data, sales_team_performance, advanced_metrics

# Charger les variables d'environnement
load_dotenv()

class Config:
    """Configuration générale"""
    API_PORT = int(os.getenv("API_PORT", 8000))
    API_HOST = os.getenv("API_HOST", "127.0.0.1")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # LLM Selection
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")  # gemini, openai, ollama, simulation
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-3.5-turbo"
    
    # Gemini (Google)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = "gemini-2.5-flash"
    
    # Ollama (Local)
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
    
    # Power BI
    POWERBI_TENANT_ID = os.getenv("POWERBI_TENANT_ID")
    POWERBI_CLIENT_ID = os.getenv("POWERBI_CLIENT_ID")
    POWERBI_CLIENT_SECRET = os.getenv("POWERBI_CLIENT_SECRET")
    POWERBI_DATASET_ID = os.getenv("POWERBI_DATASET_ID")
    POWERBI_API_URL = "https://api.powerbi.com/v1.0/myorg"
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./kpi_data.db")

# KPI Actuels (depuis data/sample_data.py)
SAMPLE_KPIS = sample_kpi.copy()

# Ajouter les données enrichies dans la config pour l'LLM
DATA_CONTEXT = {
    "current_kpi": sample_kpi,
    "kpi_history": kpi_history,
    "sales_by_region": sales_by_region,
    "sales_by_product": sales_by_product,
    "sales_by_channel": sales_by_channel,
    "customer_demographics": customer_demographics,
    "financial_data": financial_data,
    "sales_team_performance": sales_team_performance,
    "advanced_metrics": advanced_metrics
}
