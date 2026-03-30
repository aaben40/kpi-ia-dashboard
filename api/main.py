"""
API FastAPI pour l'intégration LLM + Power BI + KPI
Cette API permet de:
1. Poser des questions sur les KPI et obtenir des réponses via un LLM
2. Envoyer des données à Power BI
3. Gérer les données KPI
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config import Config, SAMPLE_KPIS, DATA_CONTEXT
from models.schemas import (
    QuestionRequest,
    LLMResponse,
    PowerBIPushRequest,
    PowerBIResponse,
    KPIData
)
from utils.llm_handler import LLMHandler
from utils.powerbi_handler import PowerBIHandler
from datetime import datetime
from typing import Dict, Any
import json

# Initialiser l'application FastAPI
app = FastAPI(
    title="LLM + Power BI KPI API",
    description="API pour analyser les KPI avec l'IA et envoyer les données à Power BI",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialiser les gestionnaires
llm_handler = LLMHandler()
powerbi_handler = PowerBIHandler()

# Stockage des données KPI en mémoire (en production, utiliser une DB)
kpi_store: Dict[str, Any] = {
    "current": SAMPLE_KPIS.copy(),
    "last_updated": datetime.now().isoformat()
}


@app.get("/", tags=["Health"])
async def root():
    """Endpoint racine pour vérifier que l'API est active"""
    return {
        "message": "✨ Bienvenue dans l'API LLM + Power BI KPI!",
        "status": "active",
        "endpoints": {
            "kpi": "/docs",
            "ask_kpi": "POST /ask",
            "get_kpi": "GET /kpi",
            "send_to_powerbi": "POST /powerbi/push"
        }
    }


@app.get("/health", tags=["Health"])
async def health():
    """Endpoint de santé pour vérifier l'état de l'API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "api_version": "1.0.0",
        "llm_available": llm_handler.client is not None,
        "models": ["gpt-3.5-turbo", "Simulated"]
    }


@app.get("/info", tags=["Health"])
async def info():
    """Endpoint pour obtenir les informations de l'API et la configuration"""
    return {
        "version": "1.0.0",
        "name": "LLM + Power BI KPI API",
        "status": "active",
        "timestamp": datetime.now().isoformat(),
        "config": {
            "llm_provider": Config.LLM_PROVIDER,
            "llm_model": Config.GEMINI_MODEL if Config.LLM_PROVIDER == "gemini" else Config.OPENAI_MODEL,
            "debug": Config.DEBUG,
            "api_port": Config.API_PORT,
            "api_host": Config.API_HOST
        },
        "llm": {
            "provider": llm_handler.available_provider,
            "model": llm_handler.model.__class__.__name__ if llm_handler.model else "None"
        }
    }


# ============ ENDPOINTS KPI ============

@app.get("/kpi", tags=["KPI"])
async def get_kpi():
    """Récupérer tous les KPI actuels"""
    return {
        "success": True,
        "data": kpi_store["current"],
        "last_updated": kpi_store["last_updated"]
    }


@app.get("/kpi/{kpi_name}", tags=["KPI"])
async def get_kpi_value(kpi_name: str):
    """Récupérer la valeur d'un KPI spécifique"""
    if kpi_name not in kpi_store["current"]:
        raise HTTPException(
            status_code=404,
            detail=f"KPI '{kpi_name}' non trouvé. KPI disponibles: {list(kpi_store['current'].keys())}"
        )
    
    return {
        "success": True,
        "kpi": kpi_name,
        "value": kpi_store["current"][kpi_name],
        "last_updated": kpi_store["last_updated"]
    }


@app.post("/kpi/update", tags=["KPI"])
async def update_kpi(updates: KPIData):
    """Mettre à jour tous les KPI"""
    try:
        kpi_store["current"] = updates.model_dump()
        kpi_store["last_updated"] = datetime.now().isoformat()
        
        return {
            "success": True,
            "message": "KPI mis à jour avec succès",
            "data": kpi_store["current"],
            "timestamp": kpi_store["last_updated"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============ ENDPOINTS LLM ============

@app.post("/ask", response_model=LLMResponse, tags=["LLM"])
async def ask_about_kpi(request: QuestionRequest):
    """
    Poser une question sur les KPI et obtenir une réponse via le LLM
    
    Contexte fourni: KPI actuels, historique 12 mois, données par région/produit/canal,
    démographie clients, financières, équipe sales, et indicateurs avancés.
    """
    try:
        # Utiliser les KPI fournis ou sinon les KPI actuels + contexte enrichi
        if request.kpi_data:
            kpi_data = request.kpi_data
        else:
            # Passer tout le contexte enrichi à l'LLM
            kpi_data = DATA_CONTEXT
        
        # Poser la question au LLM avec le contexte enrichi
        response = llm_handler.ask_llm(request.question, kpi_data)
        
        return LLMResponse(**response)
        
    except Exception as e:
        return LLMResponse(
            success=False,
            question=request.question,
            error=str(e),
            source="API"
        )


@app.post("/ask/simple", tags=["LLM"])
async def ask_simple(question: str = Query(..., description="Question sur les KPI")):
    """
    Poser une question simple sur les KPI (via Query parameter)
    
    Exemple: /ask/simple?question=Quelles%20sont%20nos%20ventes%20totales?
    """
    try:
        response = llm_handler.ask_llm(question, kpi_store["current"])
        return response
    except Exception as e:
        return {
            "success": False,
            "question": question,
            "error": str(e),
            "source": "API"
        }


@app.get("/templates/questions", tags=["LLM"])
async def template_questions():
    """Obtenir des questions templates avancées pour tester le LLM avec contexte enrichi"""
    from data.sample_data import example_questions
    return {
        "templates": example_questions,
        "categories": {
            "basiques": 3,
            "tendances": 3,
            "géographiques": 3,
            "produits": 3,
            "canaux": 3,
            "clients": 3,
            "financières": 3,
            "équipe": 3,
            "nps_satisfaction": 3,
            "avancées": 10
        },
        "total": len(example_questions)
    }


# ============ ENDPOINTS POWER BI ============

@app.post("/powerbi/push", response_model=PowerBIResponse, tags=["Power BI"])
async def push_to_powerbi(request: PowerBIPushRequest):
    """
    Envoyer des données à Power BI via l'API REST
    
    Table name: Doit correspondre à une table existante dans votre dataset Power BI
    Rows: Liste des lignes avec les colonnes correspondant au modèle de données
    """
    try:
        result = powerbi_handler.push_data_to_powerbi(request.table_name, request.rows)
        return PowerBIResponse(**result)
    except Exception as e:
        return PowerBIResponse(
            success=False,
            message="Erreur lors de l'envoi",
            error=str(e)
        )


@app.post("/powerbi/push-kpi", tags=["Power BI"])
async def push_kpi_to_powerbi():
    """
    Envoyer les KPI actuels à Power BI
    
    Crée une ligne avec tous les KPI actuels et la date actuelle
    """
    try:
        current_kpi = kpi_store["current"].copy()
        current_kpi["date"] = datetime.now().isoformat()
        
        result = powerbi_handler.push_data_to_powerbi("KPI_Data", [current_kpi])
        return PowerBIResponse(**result)
    except Exception as e:
        return PowerBIResponse(
            success=False,
            message="Erreur lors de l'envoi des KPI",
            error=str(e)
        )


@app.get("/powerbi/status", tags=["Power BI"])
async def powerbi_status():
    """Vérifier le statut de la connexion Power BI"""
    return {
        "configured": all([
            Config.POWERBI_TENANT_ID,
            Config.POWERBI_CLIENT_ID,
            Config.POWERBI_CLIENT_SECRET
        ]),
        "tenant_id": Config.POWERBI_TENANT_ID or "Non configuré",
        "dataset_id": Config.POWERBI_DATASET_ID or "Non configuré",
        "mode": "production" if Config.POWERBI_TENANT_ID else "simulation"
    }


@app.get("/powerbi/integration-guide", tags=["Power BI"])
async def powerbi_guide():
    """Guide pour intégrer Power BI avec l'API"""
    return {
        "title": "Guide d'intégration Power BI",
        "steps": [
            {
                "step": 1,
                "title": "Configurer les credentials Power BI",
                "description": "Remplissez les variables d'environnement dans .env",
                "variables": [
                    "POWERBI_TENANT_ID",
                    "POWERBI_CLIENT_ID",
                    "POWERBI_CLIENT_SECRET",
                    "POWERBI_DATASET_ID"
                ]
            },
            {
                "step": 2,
                "title": "Créer un app registration dans Azure AD",
                "url": "https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps"
            },
            {
                "step": 3,
                "title": "Obtenir les IDs et secrets",
                "fields": ["Client ID", "Client Secret"]
            },
            {
                "step": 4,
                "title": "Donner les permissions Power BI à l'app",
                "permission": "App owns data"
            }
        ],
        "example_request": {
            "table_name": "KPI_Ventes",
            "rows": [
                {"Date": "2024-03-30", "Ventes": 15000, "Clients": 125}
            ]
        }
    }


# ============ ENDPOINTS UTILITAIRES ============

@app.get("/info", tags=["Info"])
async def api_info():
    """Obtenir les informations de l'API"""
    return {
        "api": "LLM + Power BI + KPI Integration",
        "version": "1.0.0",
        "description": "API pour analyser les KPI avec l'IA et Power BI",
        "features": [
            "Poser des questions sur les KPI via LLM",
            "Envoyer les données à Power BI",
            "Gérer et mettre à jour les KPI",
            "Intégration avec OpenAI"
        ],
        "config": {
            "debug": Config.DEBUG,
            "llm_model": Config.MODEL_NAME,
            "llm_available": llm_handler.client is not None
        }
    }


@app.get("/docs-custom", tags=["Info"])
async def custom_docs():
    """Documentation personnalisée pour l'API"""
    return {
        "title": "LLM + Power BI KPI API",
        "description": "Une API pour comprendre comment intégrer l'IA avec Power BI",
        "quick_start": [
            {
                "name": "1. Vérifier la santé de l'API",
                "endpoint": "GET /health"
            },
            {
                "name": "2. Récupérer les KPI",
                "endpoint": "GET /kpi"
            },
            {
                "name": "3. Poser une question",
                "endpoint": "POST /ask",
                "example": {
                    "question": "Quelles sont nos ventes totales?",
                    "kpi_data": None
                }
            },
            {
                "name": "4. Envoyer des données à Power BI",
                "endpoint": "POST /powerbi/push",
                "example": {
                    "table_name": "KPI_Ventes",
                    "rows": [{"Date": "2024-03-30", "Ventes": 15000}]
                }
            }
        ]
    }


# ============ ERROR HANDLERS ============

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Gestionnaire d'exceptions HTTP personnalisé"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "success": False}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host=Config.API_HOST,
        port=Config.API_PORT,
        reload=Config.DEBUG
    )
