import streamlit as st
from utils import save_current_state, get_session_value, update_session_state
from config.settings import UI_SETTINGS, DEFAULT_SYSTEM_MESSAGE, DEFAULT_TASK_TEMPLATES
from services.db_service import DatabaseService
import time
from datetime import datetime

def save_coding_instruction():
    """Save the coding instruction"""
    try:
        name = st.text_input("Name der Codierungsanweisung:", key="save_instruction_name")
        description = st.text_area("Beschreibung (optional):", key="save_instruction_description")
        is_public = st.checkbox("Öffentlich verfügbar machen?", key="save_instruction_public")
        
        if st.button("Codierungsanweisung speichern", key="save_instruction_button"):
            current_template = get_session_value('question_template')
            if not current_template.strip():
                st.error("Bitte gib eine Codierungsanweisung ein.")
                return
            
            if not name:
                st.error("Bitte gib einen Namen ein.")
                return
            
            instruction_data = {
                "user_id": st.session_state.user_id,
                "name": name,
                "prompt": current_template,
                "description": description,
                "is_public": is_public,
                "created_at": datetime.now().isoformat()
            }
            
            # Use database service to save instruction
            saved_instruction = DatabaseService.save_coding_instruction(instruction_data)
            if saved_instruction:
                st.success("✅ Codierungsanweisung erfolgreich gespeichert!")
                time.sleep(0.5)
                st.rerun()
    except Exception as e:
        st.error(f"Fehler beim Speichern: {str(e)}")

def load_coding_instruction():
    """Load a saved coding instruction"""
    try:
        # Use database service to load instructions
        instructions = DatabaseService.load_coding_instructions(st.session_state.user_id)
            
        if instructions:
            instruction_options = {f"{p['name']} ({p['created_at'][:10]})": p for p in instructions}
            selected_instruction = st.selectbox(
                "Wähle eine Codierungsanweisung:",
                list(instruction_options.keys()),
                key="load_instruction_select"
            )
            
            if instruction_options[selected_instruction]['description']:
                st.info(instruction_options[selected_instruction]['description'])
            
            if st.button("Codierungsanweisung laden", key="load_instruction_button"):
                instruction = instruction_options[selected_instruction]
                st.session_state.question_template = instruction['prompt']
                st.session_state.question_template_text = instruction['prompt']
                st.success("✅ Codierungsanweisung erfolgreich geladen!")
                save_current_state()
                time.sleep(0.5)
                st.rerun()
        else:
            st.info("Keine gespeicherten Codierungsanweisungen gefunden.")
    except Exception as e:
        st.error(f"Fehler beim Laden: {str(e)}")

def render_settings_section():
    """Render the settings section"""
    with st.expander("⚙️ Erweiterte Einstellungen", expanded=False):
        tab1, tab2 = st.tabs(["🎯 Codierungsanweisungen", "📝 System Message"])
        
        with tab1:
            st.markdown("### 🎯 Codierungsanweisungen anpassen")
            st.info("""
            Hier kannst du die Anweisungen für die KI anpassen. 
            Verfügbare Variablen:
            - `{CODES_AND_CATEGORIES}`: Deine definierten Codes und Kategorien
            - `{word}`: Die aktuelle Nennung
            - `{examples}`: Deine Beispiele
            - `{context_section}`: Dein Studienkontext
            - `{first_category}`: Die erste Kategorie
            - `{second_category}`: Die zweite Kategorie
            """)
            
            current_template = get_session_value('question_template', DEFAULT_TASK_TEMPLATES["single_label"])
            
            st.text_area(
                "Aktuelle Codierungsanweisung:",
                value=current_template,
                height=300,
                key="question_template_area",
                help="Hier kannst du die Anweisungen für die KI direkt bearbeiten",
                on_change=update_session_state,
                args=('question_template',)
            )
            
            save_load_tabs = st.tabs(["💾 Speichern", "📂 Laden"])
            
            with save_load_tabs[0]:
                save_coding_instruction()
                
            with save_load_tabs[1]:
                load_coding_instruction()
            
        with tab2:
            st.markdown("### ⚠️ System Message (Fortgeschrittene)")
            st.warning("""
            Die System Message definiert die grundlegende Rolle der KI. 
            Änderungen sollten nur von erfahrenen Nutzern vorgenommen werden, 
            da sie großen Einfluss auf die Codierungsqualität haben können.
            """)
            
            current_message = get_session_value('system_message', DEFAULT_SYSTEM_MESSAGE)
            
            st.text_area(
                "Systemnachricht für die KI:",
                value=current_message,
                height=100,
                key="system_message_area",
                on_change=update_session_state,
                args=('system_message',)
            )