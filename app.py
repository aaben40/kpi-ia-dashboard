"""
Interface Streamlit pour le projet LLM + Power BI + KPI
Application interactive pour analyser les KPI avec l'IA
"""

import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import json

# Configuration Streamlit
st.set_page_config(
    page_title="KPI IA Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styles CSS personnalisés
st.markdown("""
<style>
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    .metric-value {
        font-size: 32px;
        font-weight: bold;
    }
    .metric-label {
        font-size: 14px;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# Configuration API
API_BASE_URL = "http://127.0.0.1:8000"

# Session state pour historique
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ============ HEADER ============

st.title("📊 KPI Assistant IA")
st.markdown("**Analysez vos KPI avec l'intelligence artificielle**")

# ============ SIDEBAR ============

with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Status
    try:
        health_response = requests.get(f"{API_BASE_URL}/health")
        if health_response.status_code == 200:
            health = health_response.json()
            col1, col2 = st.columns(2)
            with col1:
                st.metric("API Status", "✅ Active")
            with col2:
                st.metric("LLM", "🤖 " + ("GPT-3.5" if health.get("llm_available") else "Simulation"))
        else:
            st.error("❌ API non accessible")
    except:
        st.error("❌ Erreur de connexion à l'API")
    
    st.divider()
    
    # Navigation
    st.subheader("📍 Navigation")
    page = st.radio(
        "Choisissez une page:",
        ["🏠 Accueil", "🤖 Questions IA", "📊 Données KPI", "💾 Power BI", "❓ Aide"],
        label_visibility="collapsed"
    )

# ============ PAGE: ACCUEIL ============

if page == "🏠 Accueil":
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Bienvenue!")
        st.write("""
        Cette application vous permet de:
        
        ✅ **Visualiser** vos KPI en temps réel
        
        🤖 **Poser des questions** à l'IA sur vos données
        
        📊 **Envoyer** les données vers Power BI
        
        📈 **Analyser** les tendances
        """)
    
    with col2:
        st.subheader("📚 Fonctionnalités")
        
        # Récupérer les infos API
        try:
            info = requests.get(f"{API_BASE_URL}/info").json()
            st.write(f"**Version API:** {info['version']}")
            st.write(f"**Modèle:** {info['config']['llm_model']}")
            st.write(f"**Debug:** {'Activé' if info['config']['debug'] else 'Désactivé'}")
        except:
            st.warning("Impossible de récupérer les infos API")

# ============ PAGE: QUESTIONS IA ============

elif page == "🤖 Questions IA":
    st.subheader("💬 Posez une question à l'IA")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        question = st.text_input(
            "Votre question:",
            placeholder="Ex: Quelles sont nos ventes totales?",
            label_visibility="collapsed"
        )
    
    with col2:
        submit = st.button("🚀 Envoyer", use_container_width=True)
    
    # Envoyer la question
    if submit and question:
        with st.spinner("⏳ Analyse en cours..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/ask",
                    json={"question": question, "kpi_data": None}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if result.get("success"):
                        # Afficher la réponse
                        st.success("✅ Réponse reçue!")
                        st.markdown(f"""
                        ### 💭 Réponse:
                        {result['answer']}
                        
                        ---
                        **Source:** {result.get('source')} | **Modèle:** {result.get('model')}
                        """)
                        
                        # Ajouter à l'historique
                        st.session_state.chat_history.append({
                            "question": question,
                            "answer": result['answer'],
                            "timestamp": datetime.now().strftime("%H:%M:%S"),
                            "source": result.get('source'),
                            "model": result.get('model')
                        })
                    else:
                        st.error(f"❌ Erreur: {result.get('error')}")
                else:
                    st.error("❌ Erreur API")
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")
    
    # Questions templates
    st.divider()
    st.subheader("💡 Questions suggérées:")
    
    try:
        templates = requests.get(f"{API_BASE_URL}/templates/questions").json()
        
        for i, template in enumerate(templates.get("templates", []), 1):
            if st.button(f"{i}. {template}", key=f"template_{i}"):
                st.session_state.question = template
                st.rerun()
    except:
        st.warning("Impossible de charger les questions suggérées")
    
    # Historique des questions
    st.divider()
    if st.session_state.chat_history:
        st.subheader("📝 Historique")
        
        for i, item in enumerate(reversed(st.session_state.chat_history[-5:]), 1):
            with st.expander(f"**Q{i}:** {item['question'][:50]}... ({item['timestamp']})"):
                st.write(f"**Question:** {item['question']}")
                st.write(f"**Réponse:** {item['answer']}")
                st.caption(f"Source: {item['source']} | Modèle: {item['model']}")

# ============ PAGE: DONNÉES KPI ============

elif page == "📊 Données KPI":
    st.subheader("📈 KPI actuels")
    
    try:
        response = requests.get(f"{API_BASE_URL}/kpi")
        if response.status_code == 200:
            data = response.json()
            kpi_data = data["data"]
            
            # Afficher en grille
            cols = st.columns(3)
            metrics = [
                ("Ventes totales", f"€{kpi_data['ventes_totales']:,.0f}"),
                ("Clients", f"{kpi_data['nombre_clients']:,}"),
                ("Conversion", f"{kpi_data['taux_conversion']:.2f}%"),
                ("Revenu/Client", f"€{kpi_data['revenu_moyen_client']:.0f}"),
                ("Satisfaction", f"{kpi_data['satisfaction_client']:.1f}/5"),
                ("Croissance", f"{kpi_data['croissance_mensuelle']:.1f}%"),
                ("Coût acquisition", f"€{kpi_data['cout_acquisition']:.0f}"),
            ]
            
            for i, (label, value) in enumerate(metrics):
                with cols[i % 3]:
                    st.metric(label, value)
            
            # Tableau détaillé
            st.divider()
            st.subheader("📋 Détails complets")
            
            df = pd.DataFrame([kpi_data]).T
            df.columns = ["Valeur"]
            st.dataframe(df, use_container_width=True)
            
            st.caption(f"Dernière mise à jour: {data['last_updated']}")
        else:
            st.error("Impossible de récupérer les KPI")
    except Exception as e:
        st.error(f"Erreur: {str(e)}")
    
    # Mettre à jour les KPI
    st.divider()
    st.subheader("✏️ Mettre à jour un KPI")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("(Fonctionnalité optionnelle)")

# ============ PAGE: POWER BI ============

elif page == "💾 Power BI":
    st.subheader("📤 Intégration Power BI")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Envoyez vos données KPI vers Power BI")
        if st.button("📤 Envoyer les KPI actuels à Power BI", use_container_width=True):
            with st.spinner("Envoi en cours..."):
                try:
                    response = requests.post(f"{API_BASE_URL}/powerbi/push-kpi")
                    if response.status_code == 200:
                        result = response.json()
                        if result.get("success"):
                            st.success(f"✅ {result['message']}")
                            st.info(f"**Lignes envoyées:** {result.get('rows_count')}")
                        else:
                            st.error(f"❌ {result.get('error')}")
                    else:
                        st.error("Erreur API")
                except Exception as e:
                    st.error(f"Erreur: {str(e)}")
    
    with col2:
        st.write("Statut de la connexion:")
        try:
            status = requests.get(f"{API_BASE_URL}/powerbi/status").json()
            st.write(f"**Mode:** {status.get('mode')}")
            st.write(f"**Configuré:** {'✅ Oui' if status.get('configured') else '❌ Non'}")
        except:
            st.warning("Impossible de vérifier le statut")
    
    st.divider()
    st.subheader("📚 Guide Power BI")
    
    with st.expander("Comment configurer Power BI?"):
        st.markdown("""
        ### Étapes:
        
        1. **Créer un App Registration** dans Azure AD
        2. **Récupérer les credentials**
        3. **Remplir le fichier .env**
        4. **Relancer l'API**
        
        Pour plus de détails, consultez `POWERBI_GUIDE.md`
        """)

# ============ PAGE: AIDE ============

elif page == "❓ Aide":
    st.subheader("📖 Aide et Documentation")
    
    tabs = st.tabs(["Démarrage", "Questions fréquentes", "Troubleshooting"])
    
    with tabs[0]:
        st.markdown("""
        ### 🚀 Démarrage rapide
        
        1. **L'API doit être lancée:**
           ```powershell
           python api/main.py
           ```
        
        2. **Puis lancez cette application:**
           ```powershell
           streamlit run app.py
           ```
        
        3. **Commencez à poser des questions!**
        """)
    
    with tabs[1]:
        st.markdown("""
        ### ❓ FAQ
        
        **Q: Comment poser une question?**
        A: Allez à "Questions IA" et tapez votre question.
        
        **Q: Pourquoi je reçois une erreur 429?**
        A: Votre quota OpenAI est épuisé. Passez en mode simulation.
        
        **Q: Peut-on envoyer à Power BI?**
        A: Oui! Configurez vos credentials dans .env
        
        **Q: Comment fonctionne l'IA?**
        A: OpenAI GPT-3.5-turbo (ou simulation) analyse vos KPI.
        """)
    
    with tabs[2]:
        st.markdown("""
        ### 🔧 Troubleshooting
        
        **Problème: "API non accessible"**
        - Vérifiez que `python api/main.py` tourne
        - Vérifiez le port 8000
        
        **Problème: Pas de réponse de l'IA**
        - Vérifiez votre clé OpenAI
        - Ou passez en mode simulation
        
        **Problème: Streamlit ne lance pas**
        - `pip install streamlit==1.28.1`
        - `streamlit run app.py --logger.level=debug`
        """)

# ============ FOOTER ============

st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
    🚀 KPI IA Dashboard | Créé avec Streamlit | Powered by OpenAI
</div>
""", unsafe_allow_html=True)
