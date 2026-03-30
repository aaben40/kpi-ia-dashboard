"""Gestionnaire du modèle LLM avec support multi-provider"""
import json
from typing import Dict, Any, Optional
from config import Config

# Support Gemini (Google)
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Gemini not available: {e}")
    GEMINI_AVAILABLE = False

# Support OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  OpenAI not available: {e}")
    OPENAI_AVAILABLE = False

# Support Ollama
try:
    import requests
    OLLAMA_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Ollama not available: {e}")
    OLLAMA_AVAILABLE = False


class LLMHandler:
    """Gestionnaire pour intégrer un LLM avec support multi-provider"""
    
    def __init__(self):
        """Initialiser le gestionnaire LLM"""
        self.provider = Config.LLM_PROVIDER
        self.client = None
        self.model = None
        self.available_provider = None
        
        print(f"\n{'='*60}")
        print("🔧 Initialisation LLM")
        print(f"{'='*60}")
        print(f"Provider configuré: {self.provider}")
        print(f"Gemini disponible: {GEMINI_AVAILABLE}")
        print(f"Gemini API Key présente: {bool(Config.GEMINI_API_KEY)}")
        if Config.GEMINI_API_KEY:
            print(f"Gemini API Key value: {Config.GEMINI_API_KEY[:10]}...{Config.GEMINI_API_KEY[-5:]}")
        
        # Initialiser selon le provider choisi
        if self.provider == "gemini":
            print("\n🎯 Tentative d'initialisation Gemini...")
            if not GEMINI_AVAILABLE:
                print("❌ Gemini pas disponible (import échoué)")
            elif not Config.GEMINI_API_KEY:
                print("❌ GEMINI_API_KEY non configurée dans .env")
            else:
                try:
                    print(f"   - Configuration avec clé: {Config.GEMINI_API_KEY[:15]}...")
                    genai.configure(api_key=Config.GEMINI_API_KEY)
                    print(f"   - Création du modèle: {Config.GEMINI_MODEL}")
                    self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
                    self.available_provider = "Gemini"
                    print(f"✅ LLM Provider: Gemini ({Config.GEMINI_MODEL})")
                    print(f"{'='*60}\n")
                    return
                except Exception as e:
                    print(f"❌ Gemini initialization failed: {type(e).__name__}: {e}")
                    self._try_next_provider()
        
        elif self.provider == "openai":
            print("\n🎯 Tentative d'initialisation OpenAI...")
            if not OPENAI_AVAILABLE:
                print("❌ OpenAI pas disponible")
            elif not Config.OPENAI_API_KEY:
                print("❌ OPENAI_API_KEY non configurée")
            else:
                try:
                    self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
                    self.model = Config.OPENAI_MODEL
                    self.available_provider = "OpenAI"
                    print(f"✅ LLM Provider: OpenAI ({self.model})")
                    print(f"{'='*60}\n")
                    return
                except Exception as e:
                    print(f"❌ OpenAI initialization failed: {e}")
                    self._try_next_provider()
        
        elif self.provider == "ollama":
            print("\n🎯 Tentative d'initialisation Ollama...")
            try:
                response = requests.get(f"{Config.OLLAMA_URL}/api/tags")
                if response.status_code == 200:
                    self.available_provider = "Ollama"
                    self.model = Config.OLLAMA_MODEL
                    print(f"✅ LLM Provider: Ollama ({self.model})")
                    print(f"{'='*60}\n")
                    return
                else:
                    print(f"❌ Ollama non accessible")
            except Exception as e:
                print(f"❌ Ollama initialization failed: {e}")
            self._try_next_provider()
        
        # Fallback: Simulation
        if self.available_provider is None:
            self.available_provider = "Simulation"
            print(f"\n⚠️  Aucun LLM externe disponible. Mode SIMULATION activé.")
            print(f"{'='*60}\n")
    
    def _try_next_provider(self):
        """Essayer le prochain provider disponible"""
        providers = ["gemini", "openai", "ollama"]
        current_idx = providers.index(self.provider) if self.provider in providers else -1
        
        for i in range(current_idx + 1, len(providers)):
            provider = providers[i]
            if provider == "gemini" and GEMINI_AVAILABLE and Config.GEMINI_API_KEY:
                try:
                    genai.configure(api_key=Config.GEMINI_API_KEY)
                    self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
                    self.available_provider = "Gemini"
                    self.provider = "gemini"
                    print(f"✅ Fallback: Using Gemini")
                    return
                except:
                    continue
            
            elif provider == "openai" and OPENAI_AVAILABLE and Config.OPENAI_API_KEY:
                try:
                    self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
                    self.model = Config.OPENAI_MODEL
                    self.available_provider = "OpenAI"
                    self.provider = "openai"
                    print(f"✅ Fallback: Using OpenAI")
                    return
                except:
                    continue
    
    def prepare_context(self, kpi_data: Dict[str, Any]) -> str:
        """
        Préparer le contexte avec les données KPI pour le LLM
        Supporte le contexte simple (KPI basiques) et enrichi (avec historique, régions, produits, etc.)
        
        Args:
            kpi_data: Dictionnaire avec les données KPI (simple ou enrichi)
            
        Returns:
            String contenant le contexte formaté
        """
        context = "="*80 + "\n"
        context += "CONTEXTE COMPLET DONNÉES MÉTIER POUR ANALYSE KPI\n"
        context += "="*80 + "\n\n"
        
        # Déterminer le type de contexte
        has_rich_context = "current_kpi" in kpi_data or "sales_by_region" in kpi_data
        
        if has_rich_context:
            # ============ KPI ACTUELS ============
            context += "📊 KPI ACTUELS (MARS 2026):\n"
            context += "-"*80 + "\n"
            current = kpi_data.get("current_kpi", {})
            for key, value in current.items():
                formatted_key = key.replace("_", " ").title()
                if isinstance(value, float):
                    context += f"  • {formatted_key}: {value:.2f}\n"
                else:
                    context += f"  • {formatted_key}: {value:,}\n"
            context += "\n"
            
            # ============ HISTORIQUE KPI 12 MOIS ============
            if "kpi_history" in kpi_data:
                context += "📈 HISTORIQUE COMPLET KPI (12 DERNIERS MOIS):\n"
                context += "-"*80 + "\n"
                history = kpi_data["kpi_history"]
                
                # Format tableau pour meilleure lisibilité
                context += f"{'Date':<12} | {'Ventes':<12} | {'Clients':<8} | {'Conv%':<6} | {'Satisfaction':<13}\n"
                context += "-"*80 + "\n"
                
                for record in history:
                    date = record['date']
                    ventes = record['ventes_totales']
                    clients = record['nombre_clients']
                    conv = record['taux_conversion']
                    satis = record['satisfaction_client']
                    context += f"{date:<12} | €{ventes:>10,} | {clients:>7} | {conv:>5.1f}% | {satis:>11.2f}/5\n"
                
                context += "\n"
            
            # ============ VENTES PAR RÉGION ============
            if "sales_by_region" in kpi_data:
                context += "🌍 VENTES PAR RÉGION (ACTUELLES):\n"
                context += "-"*80 + "\n"
                regions = kpi_data["sales_by_region"]
                
                context += f"{'Région':<20} | {'Ventes':<15} | {'Clients':<10} | {'Conv%':<8} | {'Satisf':<8}\n"
                context += "-"*80 + "\n"
                
                for region, data in regions.items():
                    context += f"{region:<20} | €{data['ventes']:>13,} | {data['clients']:>9} | {data['taux_conversion']:>6.1f}% | {data['satisfaction']:>7.2f}\n"
                context += "\n"
            
            # ============ VENTES PAR PRODUIT ============
            if "sales_by_product" in kpi_data:
                context += "📦 VENTES PAR PRODUIT/CATÉGORIE:\n"
                context += "-"*80 + "\n"
                products = kpi_data["sales_by_product"]
                
                context += f"{'Produit':<20} | {'Ventes':<15} | {'Units':<10} | {'Prix Unit':<12} | {'Marge%':<8}\n"
                context += "-"*80 + "\n"
                
                for product, data in products.items():
                    context += f"{product:<20} | €{data['ventes']:>13,} | {data['units']:>9} | €{data['prix_unitaire']:>10.2f} | {data['margin']:>6.1f}%\n"
                context += "\n"
            
            # ============ VENTES PAR CANAL ============
            if "sales_by_channel" in kpi_data:
                context += "📢 VENTES PAR CANAL DE DISTRIBUTION:\n"
                context += "-"*80 + "\n"
                channels = kpi_data["sales_by_channel"]
                
                context += f"{'Canal':<20} | {'Ventes':<15} | {'Transactions':<15} | {'Panier Moyen':<15} | {'Conv%':<8}\n"
                context += "-"*80 + "\n"
                
                for channel, data in channels.items():
                    context += f"{channel:<20} | €{data['ventes']:>13,} | {data['nb_transactions']:>14} | €{data['panier_moyen']:>13.2f} | {data['taux_conversion']:>6.1f}%\n"
                context += "\n"
            
            # ============ DÉMOGRAPHIE CLIENTS ============
            if "customer_demographics" in kpi_data:
                context += "👥 DONNÉES CLIENTS - DÉMOGRAPHIE:\n"
                context += "-"*80 + "\n"
                demo = kpi_data["customer_demographics"]
                
                context += f"Âge moyen: {demo['age_moyen']} ans\n\n"
                context += "Par groupe d'âge:\n"
                for age_group, data in demo['segmentation'].items():
                    context += f"  • {age_group}: {data['clients']} clients (LTV: €{data['lifetime_value']})\n"
                
                context += "\nPar type de client:\n"
                for client_type, data in demo['type_client'].items():
                    context += f"  • {client_type}: {data['clients']} clients, €{data['ventes']:,} ventes, LTV: €{data['lifetime_value']}\n"
                
                context += "\nStatut client:\n"
                context += f"  • Nouveaux: {demo['statut']['nouveau']}\n"
                context += f"  • Actifs: {demo['statut']['actif']}\n"
                context += f"  • Churn: {demo['statut']['churn']}\n"
                context += f"  • Taux de churn: {demo['statut']['taux_churn']:.1f}%\n"
                context += "\n"
            
            # ============ DONNÉES FINANCIÈRES ============
            if "financial_data" in kpi_data:
                context += "💰 DONNEES FINANCIÈRES DÉTAILLÉES:\n"
                context += "-"*80 + "\n"
                fin = kpi_data["financial_data"]
                
                context += f"Chiffre d'affaires: €{fin['chiffre_affaires']:,}\n"
                context += f"Coût des marchandises (COGS): €{fin['cout_cogs']:,}\n"
                context += f"Marge brute: €{fin['marge_brute']:,} ({fin['marge_brute_pct']:.1f}%)\n"
                context += f"Profit net: €{fin['profit_net']:,}\n\n"
                
                context += "Dépenses:\n"
                context += f"  • Marketing: €{fin['depenses_marketing']:,}\n"
                context += f"  • Personnel: €{fin['depenses_personnel']:,}\n\n"
                
                context += "Métriques clés:\n"
                context += f"  • CAC (Customer Acquisition Cost): €{fin['cac']}\n"
                context += f"  • LTV (Lifetime Value): €{fin['ltv']}\n"
                context += f"  • LTV/CAC Ratio: {fin['ltv_cac_ratio']:.1f}x\n"
                context += f"  • ROI Marketing: {fin['roi_marketing']:.2f}x\n"
                context += "\n"
            
            # ============ PERFORMANCE ÉQUIPE SALES ============
            if "sales_team_performance" in kpi_data:
                context += "👔 PERFORMANCE ÉQUIPE SALES:\n"
                context += "-"*80 + "\n"
                sales = kpi_data["sales_team_performance"]
                
                context += f"Total agents: {sales['total_agents']}\n"
                context += f"Moyenne ventes par agent par mois: €{sales['moyenne_ventes_agent']:,}\n"
                context += f"Productivité moyenne: €{sales['productivite']:.2f}K par agent\n\n"
                
                context += "Par région:\n"
                context += f"{'Région':<15} | {'Agents':<8} | {'Ventes':<15} | {'Ventes/Agent':<15} | {'%Objectif':<10}\n"
                context += "-"*80 + "\n"
                
                for region, team in sales['equipes'].items():
                    context += f"{region:<15} | {team['agents']:>7} | €{team['ventes']:>13,} | €{team['ventes_par_agent']:>13,} | {team['taux_objectif']:>8}%\n"
                context += "\n"
            
            # ============ INDICATEURS AVANCÉS ============
            if "advanced_metrics" in kpi_data:
                context += "⭐ INDICATEURS AVANCÉS DE PERFORMANCE:\n"
                context += "-"*80 + "\n"
                metrics = kpi_data["advanced_metrics"]
                
                context += "Satisfaction et fidélité:\n"
                context += f"  • NPS (Net Promoter Score): {metrics['nps']}\n"
                context += f"  • CSAT (Customer Satisfaction): {metrics['csat']:.2f}/5\n"
                context += f"  • CES (Customer Effort Score): {metrics['ces']:.1f}\n"
                context += f"  • Taux de rétention: {metrics['retention_rate']:.1f}%\n"
                context += f"  • Taux de churn: {metrics['churn_rate']:.1f}%\n"
                context += f"  • Taux de repeat: {metrics['repeat_rate']:.1f}%\n\n"
                
                context += "Croissance:\n"
                context += f"  • Taux d'upsell: {metrics['upsell_rate']:.1f}%\n"
                context += f"  • Taux de cross-sell: {metrics['cross_sell_rate']:.1f}%\n\n"
                
                context += "Efficacité vente:\n"
                context += f"  • Vélocité de vente: {metrics['sales_velocity']:.2f} jours du lead au client\n"
                context += f"  • Cycle de vente: {metrics['sales_cycle_days']} jours\n"
                context += f"  • Score qualité lead: {metrics['lead_quality_score']:.1f}/10\n"
                context += "\n"
        
        else:
            # Contexte simple (KPI basiques seulement)
            context += "KPI ACTUELS:\n\n"
            for key, value in kpi_data.items():
                formatted_key = key.replace("_", " ").title()
                if isinstance(value, float):
                    context += f"  • {formatted_key}: {value:.2f}\n"
                else:
                    context += f"  • {formatted_key}: {value:,}\n"
        
        context += "\n" + "="*80 + "\n"
        context += "INSTRUCTIONS POUR L'IA:\n"
        context += "- Analysez les données fournies avec précision\n"
        context += "- Utilisez les chiffres exacts pour justifier votre analyse\n"
        context += "- Identifiez les tendances et patterns dans les données\n"
        context += "- Donnez des insights actionnables basés sur les métriques\n"
        context += "="*80 + "\n\n"
        
        return context
    
    def ask_llm(self, question: str, kpi_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Poser une question à l'IA sur les KPI
        
        Args:
            question: Question posée par l'utilisateur
            kpi_data: Données KPI actuelles
            
        Returns:
            Dictionnaire avec la réponse et métadonnées
        """
        
        if self.available_provider == "Simulation":
            return self._simulate_response(question, kpi_data)
        
        try:
            context = self.prepare_context(kpi_data)
            full_prompt = f"{context}\n\nQuestion: {question}"
            
            # Gemini
            if self.provider == "gemini" and self.model:
                try:
                    response = self.model.generate_content(full_prompt)
                    answer = response.text
                    
                    return {
                        "success": True,
                        "answer": answer,
                        "question": question,
                        "model": Config.GEMINI_MODEL,
                        "source": "Gemini"
                    }
                except Exception as e:
                    return {
                        "success": False,
                        "error": str(e),
                        "question": question,
                        "source": "Gemini"
                    }
            
            # OpenAI
            elif self.provider == "openai" and self.client:
                try:
                    messages = [
                        {
                            "role": "system",
                            "content": "Tu es un analyste de données expert spécialisé dans l'analyse KPI. "
                                      "Réponds toujours de manière claire et structurée."
                        },
                        {
                            "role": "user",
                            "content": full_prompt
                        }
                    ]
                    
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        temperature=0.7,
                        max_tokens=500
                    )
                    
                    answer = response.choices[0].message.content
                    
                    return {
                        "success": True,
                        "answer": answer,
                        "question": question,
                        "model": self.model,
                        "source": "OpenAI"
                    }
                except Exception as e:
                    return {
                        "success": False,
                        "error": str(e),
                        "question": question,
                        "source": "OpenAI"
                    }
            
            # Ollama
            elif self.provider == "ollama":
                try:
                    response = requests.post(
                        f"{Config.OLLAMA_URL}/api/generate",
                        json={
                            "model": self.model,
                            "prompt": full_prompt,
                            "stream": False
                        }
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        answer = result.get("response", "")
                        
                        return {
                            "success": True,
                            "answer": answer,
                            "question": question,
                            "model": self.model,
                            "source": "Ollama"
                        }
                    else:
                        return {
                            "success": False,
                            "error": f"Ollama error: {response.status_code}",
                            "question": question,
                            "source": "Ollama"
                        }
                except Exception as e:
                    return {
                        "success": False,
                        "error": str(e),
                        "question": question,
                        "source": "Ollama"
                    }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "question": question,
                "source": self.available_provider
            }
    
    def _simulate_response(self, question: str, kpi_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simule une réponse LLM (sans API OpenAI)
        
        Args:
            question: Question posée
            kpi_data: Données KPI
            
        Returns:
            Dictionnaire avec réponse simulée
        """
        
        # Réponses simulées basées sur des mots-clés
        lower_question = question.lower()
        
        if "vente" in lower_question:
            answer = f"Les ventes totales sont de {kpi_data.get('ventes_totales', 'N/A')} €. " \
                    f"Avec {kpi_data.get('nombre_clients', 'N/A')} clients, " \
                    f"la moyenne par client est de {kpi_data.get('revenu_moyen_client', 'N/A')} €."
        
        elif "client" in lower_question:
            answer = f"Vous avez {kpi_data.get('nombre_clients', 'N/A')} clients actuellement. " \
                    f"La satisfaction est de {kpi_data.get('satisfaction_client', 'N/A')}/5. " \
                    f"Le coût d'acquisition moyen est de {kpi_data.get('cout_acquisition', 'N/A')} €."
        
        elif "conversion" in lower_question:
            answer = f"Le taux de conversion actuel est de {kpi_data.get('taux_conversion', 'N/A')}%. " \
                    f"C'est un bon indicateur pour votre activité."
        
        elif "croissance" in lower_question:
            answer = f"La croissance mensuelle est de {kpi_data.get('croissance_mensuelle', 'N/A')}%. " \
                    f"Continuez dans cette direction!"
        
        else:
            answer = f"Basé sur vos KPI: ventes totales ({kpi_data.get('ventes_totales', 'N/A')} €), " \
                    f"clients ({kpi_data.get('nombre_clients', 'N/A')}), " \
                    f"et croissance ({kpi_data.get('croissance_mensuelle', 'N/A')}%), " \
                    f"votre activité fonctionne bien."
        
        return {
            "success": True,
            "answer": answer,
            "question": question,
            "model": "Simulated",
            "source": "LocalSimulation"
        }
