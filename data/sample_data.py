"""
Données d'exemple enrichies pour le projet LLM + Power BI
Contient: KPI mensuels, données géographiques, par produit, par canal, et données détaillées
"""

# ============ KPI GLOBALS ACTUELS ============
sample_kpi = {
    "ventes_totales": 452500,
    "nombre_clients": 3847,
    "taux_conversion": 3.8,
    "revenu_moyen_client": 117.6,
    "satisfaction_client": 4.72,
    "croissance_mensuelle": 15.2,
    "cout_acquisition": 42.5,
    "taux_retention": 87.3,
    "nb_transactions": 12450,
    "panier_moyen": 36.35,
    "nb_employes_sales": 28
}

# ============ HISTORIQUE KPI - 12 MOIS ============
kpi_history = [
    {"date": "2025-04-30", "ventes_totales": 128000, "nombre_clients": 950, "taux_conversion": 2.8, "revenu_moyen_client": 134.7, "satisfaction_client": 4.5, "croissance_mensuelle": 5.2, "cout_acquisition": 55, "taux_retention": 82.1},
    {"date": "2025-05-31", "ventes_totales": 142000, "nombre_clients": 1050, "taux_conversion": 3.0, "revenu_moyen_client": 135.2, "satisfaction_client": 4.55, "croissance_mensuelle": 10.9, "cout_acquisition": 52, "taux_retention": 83.5},
    {"date": "2025-06-30", "ventes_totales": 156000, "nombre_clients": 1150, "taux_conversion": 3.1, "revenu_moyen_client": 135.7, "satisfaction_client": 4.58, "croissance_mensuelle": 9.9, "cout_acquisition": 50, "taux_retention": 84.2},
    {"date": "2025-07-31", "ventes_totales": 198000, "nombre_clients": 1420, "taux_conversion": 3.4, "revenu_moyen_client": 139.4, "satisfaction_client": 4.62, "croissance_mensuelle": 26.9, "cout_acquisition": 47, "taux_retention": 84.8},
    {"date": "2025-08-31", "ventes_totales": 215000, "nombre_clients": 1550, "taux_conversion": 3.5, "revenu_moyen_client": 138.7, "satisfaction_client": 4.65, "croissance_mensuelle": 8.6, "cout_acquisition": 45, "taux_retention": 85.3},
    {"date": "2025-09-30", "ventes_totales": 238000, "nombre_clients": 1720, "taux_conversion": 3.6, "revenu_moyen_client": 138.4, "satisfaction_client": 4.68, "croissance_mensuelle": 10.7, "cout_acquisition": 44, "taux_retention": 85.9},
    {"date": "2025-10-31", "ventes_totales": 285000, "nombre_clients": 2050, "taux_conversion": 3.7, "revenu_moyen_client": 138.9, "satisfaction_client": 4.69, "croissance_mensuelle": 19.7, "cout_acquisition": 43, "taux_retention": 86.4},
    {"date": "2025-11-30", "ventes_totales": 325000, "nombre_clients": 2380, "taux_conversion": 3.75, "revenu_moyen_client": 136.6, "satisfaction_client": 4.70, "croissance_mensuelle": 14.0, "cout_acquisition": 42, "taux_retention": 86.8},
    {"date": "2025-12-31", "ventes_totales": 392000, "nombre_clients": 2850, "taux_conversion": 3.8, "revenu_moyen_client": 137.5, "satisfaction_client": 4.71, "croissance_mensuelle": 20.5, "cout_acquisition": 41, "taux_retention": 87.0},
    {"date": "2026-01-31", "ventes_totales": 415000, "nombre_clients": 3100, "taux_conversion": 3.8, "revenu_moyen_client": 133.9, "satisfaction_client": 4.71, "croissance_mensuelle": 5.9, "cout_acquisition": 42, "taux_retention": 87.1},
    {"date": "2026-02-28", "ventes_totales": 435000, "nombre_clients": 3500, "taux_conversion": 3.8, "revenu_moyen_client": 124.3, "satisfaction_client": 4.71, "croissance_mensuelle": 4.8, "cout_acquisition": 42.2, "taux_retention": 87.2},
    {"date": "2026-03-30", "ventes_totales": 452500, "nombre_clients": 3847, "taux_conversion": 3.8, "revenu_moyen_client": 117.6, "satisfaction_client": 4.72, "croissance_mensuelle": 4.0, "cout_acquisition": 42.5, "taux_retention": 87.3},
]

# ============ DONNÉES PAR RÉGION ============
sales_by_region = {
    "France": {
        "ventes": 195000,
        "clients": 1650,
        "taux_conversion": 3.9,
        "satisfaction": 4.75
    },
    "Europe": {
        "ventes": 140000,
        "clients": 1200,
        "taux_conversion": 3.6,
        "satisfaction": 4.68
    },
    "Monde": {
        "ventes": 117500,
        "clients": 997,
        "taux_conversion": 3.4,
        "satisfaction": 4.65
    }
}

# ============ DONNÉES PAR PRODUIT/CATÉGORIE ============
sales_by_product = {
    "Premium": {
        "ventes": 180000,
        "units": 2800,
        "prix_unitaire": 64.3,
        "margin": 38.5,
        "top_region": "France"
    },
    "Standard": {
        "ventes": 210000,
        "units": 7200,
        "prix_unitaire": 29.2,
        "margin": 28.0,
        "top_region": "Europe"
    },
    "Economique": {
        "ventes": 62500,
        "units": 3400,
        "prix_unitaire": 18.4,
        "margin": 18.0,
        "top_region": "Monde"
    }
}

# ============ DONNÉES PAR CANAL DE VENTE ============
sales_by_channel = {
    "Direct": {
        "ventes": 180000,
        "nb_transactions": 4200,
        "panier_moyen": 42.86,
        "taux_conversion": 5.5
    },
    "Web": {
        "ventes": 215000,
        "nb_transactions": 6800,
        "panier_moyen": 31.62,
        "taux_conversion": 2.8
    },
    "Partners": {
        "ventes": 57500,
        "nb_transactions": 1450,
        "panier_moyen": 39.66,
        "taux_conversion": 3.2
    }
}

# ============ DONNÉES CLIENTS ============
customer_demographics = {
    "age_moyen": 38,
    "segmentation": {
        "18-25": {"clients": 420, "lifetime_value": 450},
        "25-35": {"clients": 1150, "lifetime_value": 650},
        "35-50": {"clients": 1480, "lifetime_value": 880},
        "50+": {"clients": 797, "lifetime_value": 720}
    },
    "type_client": {
        "B2B": {"clients": 1200, "ventes": 285000, "lifetime_value": 2375},
        "B2C": {"clients": 2647, "ventes": 167500, "lifetime_value": 633}
    },
    "statut": {
        "nouveau": 420,
        "actif": 2950,
        "churn": 477,
        "taux_churn": 12.7
    }
}

# ============ DONNÉES FINANCIÈRES DÉTAILLÉES ============
financial_data = {
    "chiffre_affaires": 452500,
    "cout_cogs": 252500,  # Cost of Goods Sold
    "marge_brute": 200000,
    "marge_brute_pct": 44.2,
    "depenses_marketing": 45000,
    "depenses_personnel": 85000,
    "profit_net": 70000,
    "roi_marketing": 10.05,
    "cac": 42.5,  # Customer Acquisition Cost
    "ltv": 730,  # Lifetime Value
    "ltv_cac_ratio": 17.2
}

# ============ DONNÉES ÉQUIPE SALES ============
sales_team_performance = {
    "total_agents": 28,
    "equipes": {
        "France": {"agents": 12, "ventes": 195000, "ventes_par_agent": 16250, "taux_objectif": 95},
        "Europe": {"agents": 10, "ventes": 140000, "ventes_par_agent": 14000, "taux_objectif": 88},
        "Monde": {"agents": 6, "ventes": 117500, "ventes_par_agent": 19583, "taux_objectif": 92}
    },
    "moyenne_ventes_agent": 16160,
    "productivite": 16.16  # K€ par agent par mois
}

# ============ INDICATEURS DE PERFORMANCE AVANCÉS ============
advanced_metrics = {
    "nps": 72,  # Net Promoter Score
    "csat": 4.72,  # Customer Satisfaction
    "ces": 2.1,  # Customer Effort Score (lower is better)
    "churn_rate": 12.7,
    "retention_rate": 87.3,
    "repeat_rate": 64.5,
    "upsell_rate": 23.8,
    "cross_sell_rate": 18.5,
    "sales_velocity": 36.35,  # Days from lead to customer
    "sales_cycle_days": 28,
    "lead_quality_score": 7.8  # out of 10
}

# Exemple de requête Power BI
powerbi_request_example = {
    "table_name": "KPI_Mensuel_Complet",
    "rows": [
        {
            "Date": "2026-03-30",
            "Ventes_Totales": 452500,
            "Nombre_Clients": 3847,
            "Taux_Conversion": 3.8,
            "Satisfaction": 4.72,
            "Croissance": 4.0,
            "France_Ventes": 195000,
            "Europe_Ventes": 140000,
            "Monde_Ventes": 117500,
            "Premium_Ventes": 180000,
            "Standard_Ventes": 210000,
            "Economique_Ventes": 62500,
            "Direct_Ventes": 180000,
            "Web_Ventes": 215000,
            "Partners_Ventes": 57500
        }
    ]
}

# Questions d'exemple
example_questions = [
    # Questions KPI basiques
    "Quelles sont nos ventes totales?",
    "Combien de clients avons-nous?",
    "Quel est notre taux de conversion?",
    
    # Questions de tendances
    "Comment évoluons-nous ce mois-ci?",
    "Y a-t-il des tendances négatives?",
    "Quels KPI améliorer en priorité?",
    
    # Questions géographiques
    "Quelle région performe le mieux?",
    "Comparaison France vs Europe?",
    "Où avons-nous le plus gros potentiel de croissance?",
    
    # Questions produit
    "Quel produit génère le plus de profit?",
    "Quelle est la marge par catégorie?",
    "Le Premium se vend-il mieux que le Standard?",
    
    # Questions canal
    "Canal Direct vs Web: comparaison?",
    "Quel canal a le meilleur ROI?",
    "Les partenaires performent-ils bien?",
    
    # Questions clients
    "Quel est notre churn rate?",
    "Démographie de nos clients?",
    "Quelle est la valeur lifetime d'un client?",
    
    # Questions financières
    "Quel est notre profit net?",
    "Marge brute par canal?",
    "ROI du marketing?",
    
    # Questions équipe
    "Comment performe notre équipe sales?",
    "Ventes par agent par région?",
    "Qui sont les meilleurs performers?",
    
    # Questions NPS & satisfaction
    "Quelle est notre satisfaction client?",
    "Score NPS?",
    "Taux de churn?",
    
    # Questions avancées
    "Analysez la corrélation ventes et satisfaction?",
    "Quel est le coût d'acquisition optimal?",
    "Ratio LTV/CAC acceptable?",
    "Évolution du panier moyen?",
    "Analyse des segments clients?",
    "Prédiction chiffre affaires Q2?",
    "Comparaison B2B vs B2C?",
    "Tendances par catégorie d'âge?",
    "Vitesse de vente par région?",
    "Efficacité du upsell et cross-sell?"
]
