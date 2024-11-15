import streamlit as st
from datetime import datetime
import pandas as pd

class DatabaseService:
    @staticmethod
    def save_session_state(state_data: dict):
        """Save session state to database"""
        try:
            st.session_state.supabase.table('session_states')\
                .upsert(state_data, on_conflict='user_id')\
                .execute()
        except Exception as e:
            print(f"Error saving session state: {str(e)}")
            raise

    @staticmethod
    def load_session_state(user_id: str) -> dict:
        """Load session state from database"""
        try:
            response = st.session_state.supabase.table('session_states')\
                .select('*')\
                .eq('user_id', user_id)\
                .order('created_at', desc=True)\
                .limit(1)\
                .execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error loading session state: {str(e)}")
            raise

    @staticmethod
    def log_ai_interaction(interaction_data: dict):
        """Log AI interaction to database"""
        try:
            st.session_state.supabase.table('ai_interactions')\
                .insert(interaction_data)\
                .execute()
        except Exception as e:
            print(f"Error logging AI interaction: {str(e)}")
            raise

    @staticmethod
    def save_codeplan(codeplan_data: dict):
        """Save codeplan to database"""
        try:
            response = st.session_state.supabase.table('saved_codeplans')\
                .insert(codeplan_data)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error saving codeplan: {str(e)}")
            raise

    @staticmethod
    def load_codeplans(user_id: str, include_public: bool = True):
        """Load codeplans from database"""
        try:
            query = st.session_state.supabase.table('saved_codeplans')\
                .select('*')
            
            if include_public:
                query = query.or_(f"user_id.eq.{user_id},is_public.eq.true")
            else:
                query = query.eq('user_id', user_id)
            
            response = query.order('created_at', desc=True).execute()
            return response.data
        except Exception as e:
            print(f"Error loading codeplans: {str(e)}")
            raise

    @staticmethod
    def save_study_context(context_data: dict):
        """Save study context to database"""
        try:
            response = st.session_state.supabase.table('study_contexts')\
                .insert(context_data)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error saving study context: {str(e)}")
            raise

    @staticmethod
    def load_study_contexts(user_id: str, include_public: bool = True):
        """Load study contexts from database"""
        try:
            query = st.session_state.supabase.table('study_contexts')\
                .select('*')
            
            if include_public:
                query = query.or_(f"user_id.eq.{user_id},is_public.eq.true")
            else:
                query = query.eq('user_id', user_id)
            
            response = query.order('created_at', desc=True).execute()
            return response.data
        except Exception as e:
            print(f"Error loading study contexts: {str(e)}")
            raise

    @staticmethod
    def save_example_set(example_data: dict):
        """Save example set to database"""
        try:
            response = st.session_state.supabase.table('example_sets')\
                .insert(example_data)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error saving example set: {str(e)}")
            raise

    @staticmethod
    def load_example_sets(user_id: str, include_public: bool = True):
        """Load example sets from database"""
        try:
            query = st.session_state.supabase.table('example_sets')\
                .select('*')
            
            if include_public:
                query = query.or_(f"user_id.eq.{user_id},is_public.eq.true")
            else:
                query = query.eq('user_id', user_id)
            
            response = query.order('created_at', desc=True).execute()
            return response.data
        except Exception as e:
            print(f"Error loading example sets: {str(e)}")
            raise

    @staticmethod
    def save_coding_instruction(instruction_data: dict):
        """Save coding instruction to database"""
        try:
            response = st.session_state.supabase.table('system_prompts')\
                .insert(instruction_data)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error saving coding instruction: {str(e)}")
            raise

    @staticmethod
    def load_coding_instructions(user_id: str, include_public: bool = True):
        """Load coding instructions from database"""
        try:
            query = st.session_state.supabase.table('system_prompts')\
                .select('*')
            
            if include_public:
                query = query.or_(f"user_id.eq.{user_id},is_public.eq.true")
            else:
                query = query.eq('user_id', user_id)
            
            response = query.order('created_at', desc=True).execute()
            return response.data
        except Exception as e:
            print(f"Error loading coding instructions: {str(e)}")
            raise

    @staticmethod
    def create_user_profile(profile_data: dict):
        """Create a new user profile"""
        try:
            response = st.session_state.supabase.table('user_profiles')\
                .insert(profile_data)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating user profile: {str(e)}")
            raise

    @staticmethod
    def get_recent_coding_history(user_id: str, limit: int = 5):
        """Get recent coding history for a user"""
        try:
            response = st.session_state.supabase.table('coding_history')\
                .select('*')\
                .eq('user_id', user_id)\
                .order('created_at', desc=True)\
                .limit(limit)\
                .execute()
            return response.data
        except Exception as e:
            print(f"Error getting coding history: {str(e)}")
            raise

    @staticmethod
    def log_coding_history(log_data: dict):
        """Log coding history to database"""
        try:
            response = st.session_state.supabase.table('coding_history')\
                .insert(log_data)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error logging coding history: {str(e)}")
            raise