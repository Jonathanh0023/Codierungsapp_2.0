import streamlit as st
import pandas as pd
from utils import save_current_state

def render_start_button():
    """Render the start button and handle processing initiation"""
    # Check if we have all required inputs
    has_codes = bool(st.session_state.get('codes_input_area', '').strip())
    has_categories = bool(st.session_state.get('categories_input_area', '').strip())
    has_words = bool(st.session_state.get('search_words_input_area', '').strip())
    has_api_key = bool(st.session_state.get('api_key', ''))
    
    # Determine if button should be enabled
    start_disabled = not (has_codes and has_categories and has_words and has_api_key)
    
    # Show helpful message if button is disabled
    if start_disabled:
        missing_items = []
        if not has_codes:
            missing_items.append("Codes")
        if not has_categories:
            missing_items.append("Kategorien")
        if not has_words:
            missing_items.append("Offene Nennungen")
        if not has_api_key:
            missing_items.append("API-Schlüssel")
            
        if missing_items:
            st.warning(f"Bitte fülle noch folgende Felder aus: {', '.join(missing_items)}")

    # Los gehts button
    if st.button("Los gehts", disabled=start_disabled, use_container_width=True):
        with st.spinner("Starte Verarbeitung..."):
            try:
                # Prepare data - use _area version for most recent value
                words = st.session_state.get('search_words_input_area', '').strip().split('\n')
                
                # Start processing
                st.session_state.processing = True
                st.session_state.current_word_index = 0
                st.session_state.words_to_process = words
                
                # Initialize DataFrame
                st.session_state.results_df = pd.DataFrame(columns=['Nennung', 'Code', 'Zeitstempel'])
                
                # Save state before starting
                save_current_state()
                
                # Show success message before rerun
                st.success("✅ Verarbeitung wird gestartet!")
                st.markdown("### 🔄 Wechsle zur Verarbeitungsansicht...")
                
                # Force a small delay to show the transition
                import time
                time.sleep(0.5)
                
                # Rerun to start processing
                st.rerun()
                
            except Exception as e:
                st.error(f"Fehler beim Starten der Codierung: {str(e)}") 