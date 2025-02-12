import streamlit as st
import pandas as pd
from datetime import datetime
import time
import base64
from io import BytesIO
from utils import save_current_state
from services.ai_service import process_with_ai

def handle_processing():
    """Handle the processing of words and display progress"""
    try:
        # Get total number of words
        total_words = len(st.session_state.words_to_process)
        
        # Create/Update DataFrame if not exists
        if 'results_df' not in st.session_state:
            st.session_state.results_df = pd.DataFrame(columns=['Nennung', 'Code', 'Zeitstempel'])
        
        # Display Codeplan for reference
        with st.sidebar:
            st.markdown("### 📋 Codeplan")
            codes = st.session_state.get('codes_input', '').strip().split('\n')
            categories = st.session_state.get('categories_input', '').strip().split('\n')
            
            # Create and display codeplan table
            if codes and categories:
                codeplan_df = pd.DataFrame({
                    'Code': codes,
                    'Kategorie': categories
                })
                st.dataframe(codeplan_df, use_container_width=True)
        
        # Create a container at the bottom of the page
        with st.container():
            # Create placeholders for dynamic content
            progress_placeholder = st.empty()
            status_placeholder = st.empty()
            results_placeholder = st.empty()
            
            # Process all remaining words
            while st.session_state.current_word_index < total_words:
                # Get current word
                current_word = st.session_state.words_to_process[st.session_state.current_word_index]
                
                # Update progress
                progress = (st.session_state.current_word_index + 1) / total_words
                progress_placeholder.progress(progress)
                status_placeholder.write(f"Verarbeite {st.session_state.current_word_index + 1} von {total_words} Nennungen")
                
                try:
                    # Process current word with AI
                    ai_result = process_with_ai(current_word)
                    
                    # Add result to DataFrame
                    new_row = pd.DataFrame([{
                        'Nennung': current_word,
                        'Code': ai_result,
                        'Zeitstempel': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }])
                    
                    st.session_state.results_df = pd.concat([st.session_state.results_df, new_row], ignore_index=True)
                    
                    # Display updated results
                    results_placeholder.dataframe(
                        st.session_state.results_df,
                        use_container_width=True,
                        height=400  # Reduzierte Höhe für bessere Integration
                    )
                    
                    # Move to next word
                    st.session_state.current_word_index += 1
                    
                    # Small delay to prevent rate limiting
                    time.sleep(0.1)
                    
                except Exception as e:
                    st.error(f"Fehler bei der Verarbeitung von '{current_word}': {str(e)}")
                    continue
            
            # Processing complete
            handle_completion()
            
    except Exception as e:
        st.error(f"Fehler bei der Verarbeitung: {str(e)}")
        st.session_state.processing = False
        st.rerun()

def handle_completion():
    """Handle completion of processing"""
    st.session_state.processing = False
    st.success("✅ Verarbeitung abgeschlossen!")
    
    # Create Excel download button
    excel_data = convert_df_to_excel()
    b64 = base64.b64encode(excel_data).decode()
    
    # HTML Download Button
    download_filename = f'codierungen_{datetime.now().strftime("%Y%m%d_%H%M")}.xlsx'
    html_button = f'''
        <a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" 
           download="{download_filename}"
           style="text-decoration: none; width: 100%;">
            <button style="
                background-color: #FF4B4B;
                color: white;
                padding: 0.5rem 1rem;
                border: none;
                border-radius: 0.5rem;
                cursor: pointer;
                width: 100%;
                font-size: 1rem;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;">
                <span>📥</span>
                <span>Als Excel-Datei herunterladen</span>
            </button>
        </a>
    '''
    st.markdown(html_button, unsafe_allow_html=True)

def convert_df_to_excel():
    """Convert DataFrame to Excel bytes"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        st.session_state.results_df.to_excel(writer, sheet_name='Codierungen', index=False)
    return output.getvalue()

def cancel_processing():
    """Cancel the current processing"""
    st.session_state.processing = False
    st.session_state.current_word_index = 0
    st.session_state.words_to_process = []
    if 'results_df' in st.session_state:
        del st.session_state.results_df
    st.rerun()

def handle_back_to_input():
    """Handle going back to input screen"""
    # Save current state to DB before going back
    try:
        save_current_state()
    except Exception as e:
        print(f"Error saving state: {str(e)}")
    
    # Reset processing state but keep inputs
    st.session_state.processing = False
    if 'results_df' in st.session_state:
        del st.session_state.results_df
    st.rerun() 