import streamlit as st
from utils import save_current_state
from bonsai_app import bonsai_page
from fuzzy_app import fuzzy_page
import time
from datetime import datetime
from config.initSupabase import init_supabase
from supabase.client import create_client
from services.state_manager import StateManager
from services.db_service import DatabaseService
from services.auth_service import AuthService
from styles.custom_css import get_custom_css

# Initialize Supabase client with auth
@st.cache_resource
def get_supabase_client():
    """Cache Supabase client initialization"""
    try:
        supabase_url = st.secrets["supabase_url"]
        supabase_key = st.secrets["supabase_key"]
        service_role_key = st.secrets.get("service_role_key")
        
        client = create_client(supabase_url, supabase_key)
        admin_client = create_client(supabase_url, service_role_key) if service_role_key else None
        
        return client, admin_client
        
    except Exception as e:
        st.error(f"Error initializing Supabase: {str(e)}")
        st.stop()

# Initialize both clients
supabase, admin_supabase = get_supabase_client()

def init_auth():
    """Initialize authentication state"""
    # Initialize Supabase client if not already done
    if 'supabase' not in st.session_state:
        st.session_state.supabase = supabase
        st.session_state.admin_supabase = admin_supabase
    
    # Initialize authentication-related variables only
    auth_values = {
        'authentication_status': None,
        'username': None,
        'user_id': None,
        'selected_app': None,
    }
    
    # Initialize only auth variables if they don't exist
    for key, default_value in auth_values.items():
        if key not in st.session_state:
            st.session_state[key] = default_value
    
    # Load user state if authenticated
    if AuthService.is_authenticated():
        StateManager.load_last_state()

def login_page():
    """Display the login page"""
    st.title("Willkommen bei BonsAI")
    
    tab1, tab2 = st.tabs(["Anmelden", "Registrieren"])
    
    with tab1:
        email = st.text_input("E-Mail", key="login_email")
        password = st.text_input("Passwort", type="password", key="login_password")
        
        if st.button("Anmelden"):
            if AuthService.handle_login(email, password):
                if StateManager.load_last_state():
                    st.success("Erfolgreich angemeldet! Deine letzte Sitzung wurde wiederhergestellt.")
                else:
                    st.success("Erfolgreich angemeldet!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Ungültige Anmeldedaten oder E-Mail nicht verifiziert")
    
    with tab2:
        handle_registration()

def handle_registration():
    """Handle user registration"""
    reg_email = st.text_input("E-Mail", key="reg_email")
    reg_password = st.text_input("Passwort (mind. 6 Zeichen)", type="password", key="reg_pass")
    reg_password_confirm = st.text_input("Passwort bestätigen", type="password")
    full_name = st.text_input("Vollständiger Name")
    organization = st.text_input("Organisation (optional)")
    
    if st.button("Registrieren"):
        if len(reg_password) < 6:
            st.error("Das Passwort muss mindestens 6 Zeichen lang sein")
            return
            
        if reg_password != reg_password_confirm:
            st.error("Die Passwörter stimmen nicht überein")
            return
            
        try:
            if AuthService.handle_registration(reg_email, reg_password, full_name, organization):
                st.success("""
                    Registrierung erfolgreich! 
                    Bitte melde dich mit deinen Zugangsdaten an.
                """)
                time.sleep(1)
                st.rerun()
        except Exception as e:
            if "User already registered" in str(e):
                st.error("Diese E-Mail ist bereits registriert. Bitte versuche dich anzumelden.")
            else:
                st.error(f"Registrierung fehlgeschlagen: {str(e)}")

def landing_page():
    """Display the landing page with app selection"""
    # Apply custom CSS
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    # Get current user info
    current_user = AuthService.get_current_user()
    
    # User welcome message
    st.markdown(f"""
        <div class='user-welcome'>
            Willkommen, {current_user['username']}! 👋
        </div>
    """, unsafe_allow_html=True)

    # Title with gradient
    st.markdown('<h1 class="centered-title">BonsAI Codierung</h1>', unsafe_allow_html=True)

    # Subtitle
    st.markdown("""
        <div class='subtitle' style='text-align: center;'>
            Wähle eine der folgenden Anwendungen:
        </div>
    """, unsafe_allow_html=True)

    # Create two columns for the app cards
    col1, col2 = st.columns(2)

    with col1:
        render_bonsai_card()
        if st.button("Starten", key="bonsai_button", use_container_width=True):
            handle_app_selection("BonsAI Codierungstool")

    with col2:
        render_fuzzy_card()
        if st.button("Starten", key="fuzzy_button", use_container_width=True):
            handle_app_selection("FuzzyWuzzy Markencodierung")

    render_recent_activity()
    render_footer()

    # Create four equal columns
    col1, col2= st.columns(2)

    # Use the fourth column for the logout button
    with col1:
        if st.button('Logout'):
            # Logic for logging out the user
            st.session_state.logged_in = False  # Example logic
            st.success("You have been logged out.")

def handle_app_selection(app_name: str):
    """Handle app selection and state loading"""
    # Load user state before changing the app
    if AuthService.is_authenticated():
        StateManager.load_last_state()
    st.session_state.selected_app = app_name
    st.rerun()

def render_bonsai_card():
    """Render the BonsAI app card"""
    st.markdown("""
        <div class='app-card'>
            <div class='app-title'>🤖 BonsAI Codierungstool</div>
            <div class='app-description'>
                KI-gestützte Codierung von offenen Nennungen mit folgenden Features:
                <ul>
                    <li>Automatische Kategorisierung</li>
                    <li>Single- und Multi-Label Codierung</li>
                    <li>Excel Import/Export</li>
                    <li>Interaktive Benutzeroberfläche</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_fuzzy_card():
    """Render the FuzzyWuzzy app card"""
    st.markdown("""
        <div class='app-card'>
            <div class='app-title'>🔍 FuzzyWuzzy Markencodierung</div>
            <div class='app-description'>
                Fuzzy-String-Matching für Markencodierung mit:
                <ul>
                    <li>Ähnlichkeitsbasierte Zuordnung</li>
                    <li>Automatische Markenerkennung</li>
                    <li>Batch-Verarbeitung</li>
                    <li>Exportfunktion</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_recent_activity():
    """Render the recent activity section"""
    st.markdown("### 📊 Letzte Aktivitäten")
    try:
        current_user = AuthService.get_current_user()
        recent_history = DatabaseService.get_recent_coding_history(current_user['user_id'], limit=5)

        if recent_history:
            for item in recent_history:
                with st.expander(f"Codierung vom {item['created_at'][:10]}"):
                    st.write(f"Methode: {item['coding_method']}")
                    st.write(f"Modell: {item['model_used']}")
                    st.write(f"Verarbeitungszeit: {item['processing_time']:.2f} Sekunden")
                    st.write(f"Eingabetext: {item['input_text']}")
                    st.write(f"Zugewiesene Codes: {item['assigned_codes']}")
        else:
            st.info("Noch keine Codierungen vorhanden. Starte eine Codierung, um deine Historie hier zu sehen!")
    except Exception as e:
        st.error(f"Fehler beim Laden der letzten Aktivitäten: {str(e)}")

def render_footer():
    """Render the footer"""
    st.markdown("""
        <div class='footer'>
            <p>Entwickelt von BonsAI ❤️</p>
        </div>
    """, unsafe_allow_html=True)

def main():
    """Main application function"""
    init_auth()
    
    if not AuthService.is_authenticated():
        login_page()
        return
        
    if st.session_state.selected_app is None:
        landing_page()
    elif st.session_state.selected_app == "BonsAI Codierungstool":
        bonsai_page()
    elif st.session_state.selected_app == "FuzzyWuzzy Markencodierung":
        fuzzy_page()
    

def handle_logout():
    """Handle user logout"""
    # Save current state before logout
    if AuthService.is_authenticated():
        try:
            StateManager.save_current_state()
        except Exception as e:
            print(f"Error saving state before logout: {str(e)}")
    
    AuthService.handle_logout()
    st.rerun()

if __name__ == "__main__":
    main()


