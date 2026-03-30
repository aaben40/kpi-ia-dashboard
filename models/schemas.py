"""Modèles de données Pydantic"""
from pydantic import BaseModel
from typing import Dict, Any, Optional, List


class KPIData(BaseModel):
    """Modèle pour les données KPI"""
    ventes_totales: float
    nombre_clients: int
    taux_conversion: float
    revenu_moyen_client: float
    satisfaction_client: float
    croissance_mensuelle: float
    cout_acquisition: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "ventes_totales": 150000,
                "nombre_clients": 1250,
                "taux_conversion": 3.5,
                "revenu_moyen_client": 120,
                "satisfaction_client": 4.8,
                "croissance_mensuelle": 12.5,
                "cout_acquisition": 45
            }
        }


class QuestionRequest(BaseModel):
    """Modèle pour une question KPI"""
    question: str
    kpi_data: Optional[Dict[str, Any]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "Quelles sont nos ventes totales?",
                "kpi_data": {
                    "ventes_totales": 150000,
                    "nombre_clients": 1250
                }
            }
        }


class LLMResponse(BaseModel):
    """Modèle pour la réponse LLM"""
    success: bool
    answer: Optional[str] = None
    question: str
    error: Optional[str] = None
    source: str
    model: Optional[str] = None


class PowerBIPushRequest(BaseModel):
    """Modèle pour pousser des données vers Power BI"""
    table_name: str
    rows: List[Dict[str, Any]]
    
    class Config:
        json_schema_extra = {
            "example": {
                "table_name": "KPI_Ventes",
                "rows": [
                    {
                        "Date": "2024-03-30",
                        "Ventes": 15000,
                        "Clients": 125,
                        "Region": "France"
                    }
                ]
            }
        }


class PowerBIResponse(BaseModel):
    """Modèle pour la réponse Power BI"""
    success: bool
    message: str
    table: Optional[str] = None
    rows_count: Optional[int] = None
    error: Optional[str] = None
    mode: Optional[str] = None
