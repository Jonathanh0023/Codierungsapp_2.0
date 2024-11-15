import streamlit as st
from datetime import datetime
from services.db_service import DatabaseService
import time

class AuthService:
    @staticmethod
    def handle_login(email: str, password: str) -> bool:
        """Handle user login"""
        try:
            res = st.session_state.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            st.session_state.authentication_status = True
            st.session_state.user_id = res.user.id
            st.session_state.username = email
            
            return True
            
        except Exception as e:
            print(f"Login error: {str(e)}")
            return False
    
    @staticmethod
    def handle_registration(email: str, password: str, full_name: str, organization: str = None) -> bool:
        """Handle user registration"""
        try:
            if not st.session_state.admin_supabase:
                raise Exception("Service-Role-Key not configured")
                
            # Create user with admin client
            user_response = st.session_state.admin_supabase.auth.admin.create_user({
                "email": email,
                "password": password,
                "email_confirm": True  # Auto-confirm email
            })
            
            if user_response.user:
                # Create user profile
                profile_data = {
                    'id': user_response.user.id,
                    'email': email,
                    'full_name': full_name,
                    'organization': organization,
                    'created_at': datetime.now().isoformat()
                }
                
                DatabaseService.create_user_profile(profile_data)
                return True
                
            return False
            
        except Exception as e:
            print(f"Registration error: {str(e)}")
            if "User already registered" in str(e):
                raise Exception("User already registered")
            raise
    
    @staticmethod
    def handle_logout():
        """Handle user logout"""
        try:
            st.session_state.supabase.auth.sign_out()
            for key in list(st.session_state.keys()):
                del st.session_state[key]
        except Exception as e:
            print(f"Logout error: {str(e)}")
            raise
    
    @staticmethod
    def is_authenticated() -> bool:
        """Check if user is authenticated"""
        return bool(st.session_state.get('authentication_status', False))
    
    @staticmethod
    def get_current_user() -> dict:
        """Get current user information"""
        if not AuthService.is_authenticated():
            return None
            
        return {
            'user_id': st.session_state.user_id,
            'username': st.session_state.username
        } 