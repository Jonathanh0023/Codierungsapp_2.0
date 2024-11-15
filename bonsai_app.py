import streamlit as st
from components.codeplan import render_codeplan_section
from components.study_context import render_study_context_section
from components.examples import render_examples_section
from components.settings import render_settings_section
from components.sidebar import setup_sidebar
from components.processing import handle_processing
from components.manual_input import render_manual_input
from components.codierung_method import render_codierung_method_section
from components.start_button import render_start_button
from services.state_manager import StateManager
from services.auth_service import AuthService
from services.db_service import DatabaseService
from styles.custom_css import get_custom_css
from config.settings import ERROR_MESSAGES, SUCCESS_MESSAGES

def bonsai_page():
    """Main function for the BonsAI App"""
    # Check authentication
    if not AuthService.is_authenticated():
        st.error(ERROR_MESSAGES["AUTH_REQUIRED"])
        st.session_state.selected_app = None
        st.rerun()
    
    # Apply custom CSS
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    # Initialize state and setup sidebar
    StateManager.initialize_session_state()
    setup_sidebar()
    
    # Create a layout with a "Back to Home" button in the top right
    col1, col2 = st.columns([8, 2])
    with col1:
        st.title("BonsAI Codierungstool")
    with col2:
        if st.button("🏠", key="bonsai_back", use_container_width=True):
            # Save state before navigating back
            StateManager.save_current_state()
            st.session_state.selected_app = None
            st.rerun()
    
    # Check processing state at the start
    if st.session_state.get('processing', False):
        handle_processing()
        return  # Skip rendering the rest of the page while processing
    
    # Regular page content (only shown when not processing)
    render_page_content()

def render_page_content():
    """Render the main page content"""
    try:
        # Load any saved state if available
        current_user = AuthService.get_current_user()
        if current_user:
            saved_state = DatabaseService.load_session_state(current_user['user_id'])
            if saved_state:
                StateManager.update_from_saved_state(saved_state)
        
        # Render all sections
        render_codeplan_section()
        render_manual_input()
        render_study_context_section()
        render_examples_section()
        render_codierung_method_section()
        render_settings_section()
        render_start_button()
        
    except Exception as e:
        st.error(f"Fehler beim Laden der Seite: {str(e)}")
        print(f"Error in render_page_content: {str(e)}")

def handle_error(error: Exception, message: str = ERROR_MESSAGES["PROCESSING_ERROR"]):
    """Handle errors consistently"""
    error_msg = message.format(str(error))
    st.error(error_msg)
    print(f"Error: {str(error)}")  # For logging

if __name__ == "__main__":
    try:
        bonsai_page()
    except Exception as e:
        handle_error(e, "Kritischer Fehler in der Anwendung")
