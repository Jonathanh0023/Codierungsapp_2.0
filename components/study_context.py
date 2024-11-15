# Funktionen für Studienkontext-Management
import streamlit as st
from utils import save_current_state, get_session_value, update_session_state
from config.settings import UI_SETTINGS
from services.db_service import DatabaseService
from datetime import datetime

def save_study_context():
    """Save the current study context"""
    try:
        name = st.text_input("Name des Studienkontexts:", key="save_context_name")
        description = st.text_area("Beschreibung (optional):", key="save_context_description")
        is_public = st.checkbox("Öffentlich verfügbar machen?", key="save_context_public")
        
        if st.button("Studienkontext speichern", key="save_context_button"):
            if not st.session_state.study_context_input.strip():
                st.error("Bitte gib einen Studienkontext ein.")
                return
            
            if not name:
                st.error("Bitte gib einen Namen ein.")
                return
            
            context_data = {
                "user_id": st.session_state.user_id,
                "name": name,
                "context": st.session_state.study_context_input,
                "description": description,
                "is_public": is_public,
                "created_at": datetime.now().isoformat()
            }
            
            # Use database service to save context
            saved_context = DatabaseService.save_study_context(context_data)
            if saved_context:
                st.success("✅ Studienkontext erfolgreich gespeichert!")
                st.rerun()
    except Exception as e:
        st.error(f"Fehler beim Speichern: {str(e)}")

def load_study_context():
    """Load a saved study context"""
    try:
        # Use database service to load contexts
        contexts = DatabaseService.load_study_contexts(st.session_state.user_id)
            
        if contexts:
            context_options = {f"{ctx['name']} ({ctx['created_at'][:10]})": ctx for ctx in contexts}
            selected_context = st.selectbox(
                "Wähle einen Studienkontext:",
                list(context_options.keys()),
                key="load_context_select"
            )
            
            if context_options[selected_context]['description']:
                st.info(context_options[selected_context]['description'])
            
            if st.button("Studienkontext laden", key="load_context_button"):
                context = context_options[selected_context]
                st.session_state.study_context_input = context['context']
                st.success("✅ Studienkontext erfolgreich geladen!")
                save_current_state()
                st.rerun()
        else:
            st.info("Keine gespeicherten Studienkontexte gefunden.")
    except Exception as e:
        st.error(f"Fehler beim Laden: {str(e)}")

def render_study_context_section():
    """Render the study context section"""
    st.markdown("""### 📚 Studienkontext
    Beschreibe hier den Kontext der Studie, um bessere Codierungen zu erhalten.
    """)
    
    # Main input field for study context
    st.text_area(
        "Studienkontext:",
        value=st.session_state.study_context_input,
        placeholder="Beschreibe hier den Kontext der Studie...",
        height=UI_SETTINGS["TEXT_AREA_HEIGHT"],
        key="study_context_input_area",
        on_change=update_session_state,
        args=('study_context_input',)
    )
    
    # Expander for save/load functionality
    with st.expander("💾 Studienkontext verwalten", expanded=False):
        tab1, tab2 = st.tabs(["💾 Speichern", "📂 Laden"])
        
        with tab1:
            save_study_context()
            
        with tab2:
            load_study_context()