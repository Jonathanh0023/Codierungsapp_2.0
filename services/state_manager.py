import streamlit as st
from datetime import datetime
import pandas as pd

class StateManager:
    @staticmethod
    def initialize_session_state():
        """Initialize all required session state variables"""
        default_values = {
            'api_key': '',
            'processing': False,
            'current_word_index': 0,
            'words_to_process': [],
            'results': [],
            'codes_input': '',
            'codes_input_area': '',
            'categories_input': '',
            'categories_input_area': '',
            'search_words_input': '',
            'search_words_input_area': '',
            'selected_model': 'gpt-4o-mini',
            'study_context_input': '',
            'study_context_input_area': '',
            'beispiele_input': '',
            'beispiele_input_area': '',
            'selected_task_template': None,
            'instructions_read': False,
            'system_message': '',
            'question_template': '',
            'codeplan_expander_open': False
        }
        
        # Initialize with defaults only if not already set
        for key, default_value in default_values.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
        
        # Try to load last state from DB
        StateManager.load_last_state()
    
    @staticmethod
    def load_last_state():
        """Load the last state from the database"""
        try:
            if not hasattr(st.session_state, 'user_id'):
                return False
                
            response = st.session_state.supabase.table('session_states')\
                .select('*')\
                .eq('user_id', st.session_state.user_id)\
                .order('updated_at', desc=True)\
                .limit(1)\
                .execute()
            
            if response.data:
                last_state = response.data[0]
                StateManager.update_from_saved_state(last_state)
                return True
                
            return False
            
        except Exception as e:
            print(f"Error loading last state: {str(e)}")
            return False
    
    @staticmethod
    def update_from_saved_state(saved_state: dict):
        """Update session state from saved state"""
        # Map of database fields to session state variables
        field_mapping = {
            'codes_input': ['codes_input', 'codes_input_area'],
            'categories_input': ['categories_input', 'categories_input_area'],
            'search_words_input': ['search_words_input', 'search_words_input_area'],
            'study_context_input': ['study_context_input', 'study_context_input_area'],
            'beispiele_input': ['beispiele_input', 'beispiele_input_area'],
            'selected_task_template': ['selected_task_template'],
            'instructions_read': ['instructions_read'],
            'system_message': ['system_message'],
            'question_template': ['question_template'],
            'codeplan_expander_open': ['codeplan_expander_open']
        }
        
        # Update session state
        for db_field, session_keys in field_mapping.items():
            if db_field in saved_state and saved_state[db_field] is not None:
                for session_key in session_keys:
                    st.session_state[session_key] = saved_state[db_field]
        
        # Restore results_df if it exists
        if saved_state.get('results_df'):
            try:
                st.session_state.results_df = pd.DataFrame.from_dict(saved_state['results_df'])
            except Exception as e:
                print(f"Error restoring results_df: {str(e)}")
    
    @staticmethod
    def save_current_state():
        """Save current state to database"""
        try:
            if not hasattr(st.session_state, 'user_id'):
                return
            
            # Prepare state data for saving
            current_state = {
                'user_id': st.session_state.user_id,
                'codes_input': st.session_state.get('codes_input', ''),
                'categories_input': st.session_state.get('categories_input', ''),
                'search_words_input': st.session_state.get('search_words_input', ''),
                'study_context_input': st.session_state.get('study_context_input', ''),
                'beispiele_input': st.session_state.get('beispiele_input', ''),
                'selected_task_template': st.session_state.get('selected_task_template'),
                'instructions_read': st.session_state.get('instructions_read', False),
                'system_message': st.session_state.get('system_message', ''),
                'question_template': st.session_state.get('question_template', ''),
                'codeplan_expander_open': st.session_state.get('codeplan_expander_open', False),
                'results_df': st.session_state.results_df.to_dict() if 'results_df' in st.session_state else None,
                'updated_at': datetime.now().isoformat()
            }
            
            # Save to database
            st.session_state.supabase.table('session_states')\
                .upsert(current_state, on_conflict='user_id')\
                .execute()
                
        except Exception as e:
            print(f"Error saving state: {str(e)}")