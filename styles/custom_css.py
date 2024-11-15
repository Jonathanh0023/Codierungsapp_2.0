def get_custom_css():
    """Return the custom CSS for the application"""
    return """
        <style>
        /* Grundlegende Styles */
        * {
            font-family: sans-serif !important;
        }
        
        /* Haupthintergrund */
        .stApp {
            background: #f8f9fa !important;
        }
        
        /* Willkommensnachricht */
        .user-welcome {
            text-align: right;
            padding: 1rem;
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 2rem;
        }
        
        /* Haupttitel */
        .centered-title {
            text-align: center;
            font-size: 3.5rem !important;
            font-weight: bold !important;
            background: linear-gradient(45deg, #e5007f, #ff4081) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            margin: 2rem 0 3rem 0 !important;
            padding: 0 !important;
        }
        
        /* App Cards */
        .app-card {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1.5rem;
            transition: all 0.3s ease;
            height: 100%;
            border: 1px solid #e0e0e0;
        }
        
        .app-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(229, 0, 127, 0.2);
            border-color: #e5007f;
        }
        
        .app-title {
            font-size: 1.5rem;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 1.5rem;
        }
        
        .app-description {
            color: #666;
            font-size: 1rem;
            line-height: 1.6;
        }
        
        .app-description ul {
            padding-left: 1.5rem;
            margin: 1rem 0;
        }
        
        .app-description li {
            margin-bottom: 0.5rem;
            color: #4a5568;
        }
        
        /* Letzte Aktivitäten */
        .stExpander {
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            margin-top: 0.5rem;
        }
        
        /* Buttons */
        .stButton button {
            background: linear-gradient(45deg, #e5007f, #ff4081) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.75rem 1.5rem !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
        }
        
        .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(229, 0, 127, 0.3) !important;
            opacity: 0.95 !important;
        }
        
        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: white !important;
            border-right: 1px solid #e0e0e0;
            padding: 2rem 1rem !important;
        }
        
        /* Sidebar Eingabefelder */
        section[data-testid="stSidebar"] input[type="text"],
        section[data-testid="stSidebar"] input[type="password"],
        section[data-testid="stSidebar"] .stSelectbox > div[data-baseweb="select"] {
            background-color: white !important;
            border: 1px solid #e0e0e0 !important;
            border-radius: 10px !important;
        }

        /* Hover-Effekt für Sidebar-Eingabefelder */
        section[data-testid="stSidebar"] input[type="text"]:hover,
        section[data-testid="stSidebar"] input[type="password"]:hover,
        section[data-testid="stSidebar"] .stSelectbox > div[data-baseweb="select"]:hover {
            border-color: #e5007f !important;
            box-shadow: 0 2px 4px rgba(229, 0, 127, 0.1) !important;
        }
        
        /* Fokus-Effekt für Sidebar-Eingabefelder */
        section[data-testid="stSidebar"] input[type="text"]:focus,
        section[data-testid="stSidebar"] input[type="password"]:focus,
        section[data-testid="stSidebar"] .stSelectbox > div[data-baseweb="select"]:focus-within {
            border-color: #e5007f !important;
            box-shadow: 0 0 0 2px rgba(229, 0, 127, 0.2) !important;
            outline: none !important;
        }
        
        /* Sidebar Überschriften */
        section[data-testid="stSidebar"] .stMarkdown h3 {
            color: #2c3e50 !important;
            font-size: 1.2rem !important;
            margin-top: 2rem !important;
            margin-bottom: 1rem !important;
            padding-bottom: 0.5rem !important;
            border-bottom: 2px solid #e5007f !important;
        }
        
        /* Sidebar Help-Text */
        section[data-testid="stSidebar"] .stMarkdown small {
            color: #666 !important;
            font-size: 0.9rem !important;
            line-height: 1.4 !important;
        }
        
        /* Container */
        .main .block-container {
            padding: 2rem 5rem !important;
            max-width: 1400px !important;
        }
        
        /* Toolbar verstecken */
        [data-testid="stToolbar"] {
            display: none;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 2rem;
            color: #666;
            font-size: 0.9rem;
            margin-top: 3rem;
            border-top: 1px solid #e0e0e0;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .main .block-container {
                padding: 1rem !important;
            }
            
            .app-card {
                padding: 1.5rem;
            }
            
            .centered-title {
                font-size: 2.5rem !important;
            }
        }
        
        /* Letzte Aktivitäten Sektion */
        [data-testid="stHeader"] {
            background-color: transparent !important;
        }
        
        .recent-activity {
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid #e0e0e0;
        }
        
        .recent-activity h3 {
            color: #2c3e50;
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }
        </style>
    """ 