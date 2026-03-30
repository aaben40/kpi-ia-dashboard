"""
LLM + Power BI + KPI API Project
Mini projet pour compendre comment intégrer l'IA avec une API Python et Power BI
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__description__ = "Integration of LLM with Power BI for KPI Analysis"

from config import Config
from utils import LLMHandler, PowerBIHandler

__all__ = ["Config", "LLMHandler", "PowerBIHandler"]
