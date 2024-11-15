import streamlit as st
from utils import save_current_state, get_session_value, update_session_state
from config.settings import UI_SETTINGS
from services.db_service import DatabaseService
from datetime import datetime

def update_session_state(key: str):
    """Update session state from widget value"""
    if f"{key}_area" in st.session_state:
        st.session_state[key] = st.session_state[f"{key}_area"]
        save_current_state()

def save_example_set():
    """Save the current example set"""
    try:
        name = st.text_input("Name der Beispielsammlung:", key="save_examples_name")
        description = st.text_area("Beschreibung (optional):", key="save_examples_description")
        category = st.text_input("Kategorie (optional):", key="save_examples_category")
        is_public = st.checkbox("Öffentlich verfügbar machen?", key="save_examples_public")
        
        if st.button("Beispiele speichern", key="save_examples_button"):
            if not st.session_state.beispiele_input.strip():
                st.error("Bitte gib mindestens ein Beispiel ein.")
                return
            
            if not name:
                st.error("Bitte gib einen Namen ein.")
                return
            
            examples_data = {
                "user_id": st.session_state.user_id,
                "name": name,
                "examples": st.session_state.beispiele_input.splitlines(),
                "description": description,
                "category": category,
                "is_public": is_public,
                "created_at": datetime.now().isoformat()
            }
            
            # Use database service to save examples
            saved_examples = DatabaseService.save_example_set(examples_data)
            if saved_examples:
                st.success("✅ Beispiele erfolgreich gespeichert!")
                st.rerun()
    except Exception as e:
        st.error(f"Fehler beim Speichern: {str(e)}")

def load_example_set():
    """Load a saved example set"""
    try:
        # Use database service to load examples
        examples = DatabaseService.load_example_sets(st.session_state.user_id)
            
        if examples:
            example_options = {f"{ex['name']} ({ex['created_at'][:10]})": ex for ex in examples}
            selected_examples = st.selectbox(
                "Wähle eine Beispielsammlung:",
                list(example_options.keys()),
                key="load_examples_select"
            )
            
            if example_options[selected_examples]['description']:
                st.info(example_options[selected_examples]['description'])
            
            if st.button("Beispiele laden", key="load_examples_button"):
                example_set = example_options[selected_examples]
                st.session_state.beispiele_input = '\n'.join(example_set['examples'])
                st.success("✅ Beispiele erfolgreich geladen!")
                save_current_state()
                st.rerun()
        else:
            st.info("Keine gespeicherten Beispielsammlungen gefunden.")
    except Exception as e:
        st.error(f"Fehler beim Laden: {str(e)}")

def render_examples_section():
    """Render the examples section"""
    st.markdown("""### 🎯 Beispiele
    Gib hier typische Beispiele für die Codierung ein. Dies hilft der KI, die Codierung besser zu verstehen.
    """)
    
    # Main input field for examples
    st.text_area(
        "Beispiele für die Codierung:",
        value=st.session_state.beispiele_input,
        placeholder="Gib hier Beispiele ein...\nEin Beispiel pro Zeile",
        height=UI_SETTINGS["TEXT_AREA_HEIGHT"],
        key="beispiele_input_area",
        on_change=update_session_state,
        args=('beispiele_input',)
    )
    
    # Expander for save/load functionality
    with st.expander("💾 Beispiele verwalten", expanded=False):
        tab1, tab2 = st.tabs(["💾 Speichern", "📂 Laden"])
        
        with tab1:
            save_example_set()
            
        with tab2:
            load_example_set()