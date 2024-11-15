import streamlit as st
from services.state_manager import StateManager
from services.db_service import DatabaseService
from config.settings import ERROR_MESSAGES

def save_current_state():
    """Save current state using StateManager"""
    try:
        StateManager.save_current_state()
    except Exception as e:
        print(f"Error saving state: {str(e)}")

def get_session_value(key: str, default_value: str = '') -> str:
    """Get value from session state with fallback to default"""
    # Remove '_area' suffix if present for checking the text version
    base_key = key.replace('_area', '')
    text_key = f"{base_key}_text"
    
    # First check if we have a value in session state
    if text_key in st.session_state:
        return st.session_state[text_key]
    elif key in st.session_state:
        return st.session_state[key]
    else:
        return default_value

def update_session_state(key: str):
    """Update session state from widget value"""
    try:
        # Remove '_area' suffix if present
        base_key = key.replace('_area', '')
        area_key = f"{base_key}_area"
        
        # Only update if the area value exists and has changed
        if area_key in st.session_state:
            value = st.session_state[area_key]
            
            # Update both versions
            st.session_state[base_key] = value
            st.session_state[area_key] = value
            
            # Save to database
            save_current_state()
            
    except Exception as e:
        print(f"Error updating session state: {str(e)}")

def handle_error(error: Exception, message: str = ERROR_MESSAGES["PROCESSING_ERROR"]):
    """Handle errors consistently"""
    error_msg = message.format(str(error))
    st.error(error_msg)
    print(f"Error: {str(error)}")  # For logging