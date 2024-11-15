import streamlit as st
from config.settings import DEFAULT_TASK_TEMPLATES

def render_codierung_method_section():
    """Render the section for codierung method selection"""
    st.markdown("""
    ### 🤖 Vorlage für die KI-Aufgabe
    Wie soll die KI die Codierung durchführen?
    """)
    
    # Create a mapping for display names
    method_display_names = {
        "single_label": "Single Label",
        "multi_label": "Multi Label"
    }
    
    # Use templates from settings with display names
    selected_template = st.radio(
        "Wähle eine Codierungsmethode:",
        options=list(DEFAULT_TASK_TEMPLATES.keys()),
        format_func=lambda x: method_display_names.get(x, x),
        index=0
    )
    
    st.session_state.selected_task_template = selected_template
    st.session_state.question_template = DEFAULT_TASK_TEMPLATES[selected_template] 