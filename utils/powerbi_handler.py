"""Gestionnaire pour l'intégration avec Power BI"""
import json
from typing import Dict, List, Any
import requests
from config import Config


class PowerBIHandler:
    """Gestionnaire pour envoyer des données à Power BI via l'API REST"""
    
    def __init__(self):
        """Initialiser le gestionnaire Power BI"""
        self.tenant_id = Config.POWERBI_TENANT_ID
        self.client_id = Config.POWERBI_CLIENT_ID
        self.client_secret = Config.POWERBI_CLIENT_SECRET
        self.dataset_id = Config.POWERBI_DATASET_ID
        self.access_token = None
    
    def get_access_token(self) -> bool:
        """
        Obtenir un token d'accès pour l'API Power BI
        
        Returns:
            True si succès, False sinon
        """
        
        if not all([self.tenant_id, self.client_id, self.client_secret]):
            print("⚠️  Credentials Power BI manquantes. Mode simulation activé.")
            return False
        
        try:
            url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
            
            data = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "scope": "https://analysis.windows.net/powerbi/api/.default"
            }
            
            response = requests.post(url, data=data)
            
            if response.status_code == 200:
                self.access_token = response.json()["access_token"]
                return True
            else:
                print(f"Erreur d'authentification Power BI: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"Erreur lors de l'authentification: {e}")
            return False
    
    def push_data_to_powerbi(self, table_name: str, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Envoyer des données à Power BI via Push API
        
        Args:
            table_name: Nom de la table dans Power BI
            rows: Liste des lignes de données
            
        Returns:
            Dictionnaire avec le statut
        """
        
        if not self.access_token and not self.get_access_token():
            return self._simulate_push(table_name, rows)
        
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            url = f"{Config.POWERBI_API_URL}/datasets/{self.dataset_id}/tables/{table_name}/rows"
            
            payload = {"rows": rows}
            
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "message": f"{len(rows)} lignes envoyées à Power BI",
                    "table": table_name,
                    "rows_count": len(rows)
                }
            else:
                return {
                    "success": False,
                    "error": f"Erreur Power BI: {response.status_code}",
                    "details": response.text
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _simulate_push(self, table_name: str, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Simuler un envoi de données (sans credentials Power BI)
        
        Args:
            table_name: Nom de la table
            rows: Données
            
        Returns:
            Dictionnaire avec le statut simulé
        """
        
        return {
            "success": True,
            "message": f"[SIMULATION] {len(rows)} lignes envoyées à Power BI - Table: {table_name}",
            "table": table_name,
            "rows_count": len(rows),
            "mode": "simulation",
            "details": "Credentials Power BI non configurées, mode simulation activé"
        }
    
    def get_dataset_refresh_info(self) -> Dict[str, Any]:
        """
        Obtenir les informations de rafraîchissement d'un dataset
        
        Returns:
            Dictionnaire avec les informations de rafraîchissement
        """
        
        if not self.access_token and not self.get_access_token():
            return {"error": "Impossible de s'authentifier", "type": "simulation"}
        
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
            
            url = f"{Config.POWERBI_API_URL}/datasets/{self.dataset_id}/refreshes"
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "refreshes": response.json().get("value", [])
                }
            else:
                return {
                    "success": False,
                    "error": f"Erreur: {response.status_code}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
