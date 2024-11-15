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
    def get_current_user():
        """Get current user information including profile data"""
        try:
            # Get basic auth data
            user = st.session_state.supabase.auth.get_user()
            user_id = user.user.id
            email = user.user.email

            # Fetch user profile data from user_profiles table
            profile_data = st.session_state.supabase.table('user_profiles') \
                .select('*') \
                .eq('id', user_id) \
                .single() \
                .execute()

            # Combine auth data with profile data
            return {
                'user_id': user_id,
                'username': email,
                'full_name': profile_data.data.get('full_name', email),
                'organization': profile_data.data.get('organization', '')
            }
        except Exception as e:
            print(f"Error fetching user data: {str(e)}")
            return {
                'user_id': None,
                'username': None,
                'full_name': None,
                'organization': None
            } 