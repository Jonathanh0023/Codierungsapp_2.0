import streamlit as st
from config.settings import AI_SETTINGS

def setup_sidebar():
    """Setup the sidebar with all its components"""
    st.sidebar.title("")
    
    # API Key Input
    api_key = st.sidebar.text_input(
        "OpenAI API Key:",
        value=st.session_state.api_key,
        type="password",
        help="Dein OpenAI API Key wird benötigt, um die KI-Funktionen zu nutzen"
    )
    if api_key:
        st.session_state.api_key = api_key
    
    # Model Selection using settings
    st.session_state.selected_model = st.sidebar.selectbox(
        "Modell auswählen:",
        options=AI_SETTINGS["AVAILABLE_MODELS"],
        index=AI_SETTINGS["AVAILABLE_MODELS"].index(AI_SETTINGS["DEFAULT_MODEL"]),
        help="Wähle das zu verwendende KI-Modell"
    )
    
    # Instructions
    render_sidebar_instructions()

def render_sidebar_instructions():
    """Render the instructions in the sidebar"""
    st.sidebar.markdown("""
    ### 🚀 Schnellstart
    1. **🔑 API-Schlüssel** eingeben
    2. **🤖 Modell** wählen (gpt-4o-mini für einfache Codierungen)
    3. **📋 Codeplan erstellen**:
       - KI-Generierung aus Nennungen
       - Import aus Excel
       - Manuelle Eingabe
    4. **📚 Studienkontext** beschreiben
    5. **🎯 Beispiele** eingeben
    6. **✨ Codierungsmethode** wählen und starten
    
    ### 💰 Kosten sparen
    - Nutze **gpt-4o-mini** für einfache Codierungen
    - Teste erst mit wenigen Nennungen
    - Gute Beispiele = bessere Ergebnisse
    """) 