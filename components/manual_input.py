import streamlit as st
from utils import save_current_state, get_session_value, update_session_state
from config.settings import UI_SETTINGS

def render_codes_input():
    """Render the codes input area"""
    # Get current value from session state
    current_codes = st.session_state.get('codes_input_area', '')
    
    codes_input = st.text_area(
        "Codes", 
        key="codes_input_area", 
        value=current_codes,
        placeholder="1\n2\n3", 
        height=300,
        on_change=update_session_state,
        args=('codes_input',)
    )
    
    # Only update if changed
    if codes_input != current_codes:
        st.session_state['codes_input'] = codes_input
        st.session_state['codes_input_area'] = codes_input
        save_current_state()

def render_categories_input():
    """Render the categories input area"""
    # Get current value from session state
    current_categories = st.session_state.get('categories_input_area', '')
    
    categories = st.text_area(
        "Kategorien:", 
        key="categories_input_area",
        value=current_categories,
        placeholder='Kategorie für Code 1\nKategorie für Code 2\nKategorie für Code 3\n...', 
        height=300,
        on_change=update_session_state,
        args=('categories_input',)
    )
    
    # Only update if changed
    if categories != current_categories:
        st.session_state['categories_input'] = categories
        st.session_state['categories_input_area'] = categories
        save_current_state()

def render_words_input():
    """Render the words input area"""
    # Get current value from session state
    current_words = st.session_state.get('search_words_input_area', '')
    
    words = st.text_area(
        "Offene Nennungen:", 
        key="search_words_input_area",
        value=current_words,
        placeholder='Offene Nennungen untereinander einfügen', 
        height=300,
        on_change=update_session_state,
        args=('search_words_input',)
    )
    
    # Only update if changed
    if words != current_words:
        st.session_state['search_words_input'] = words
        st.session_state['search_words_input_area'] = words
        save_current_state()

def render_manual_input():
    """Render the complete manual input section with all three columns"""
    col1, col2, col3 = st.columns([0.6, 2, 2])
    with col1:
        render_codes_input()
    with col2:
        render_categories_input()
    with col3:
        render_words_input() 