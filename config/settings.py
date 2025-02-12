# UI Settings
UI_SETTINGS = {
    "TEXT_AREA_HEIGHT": 200,
    "EXPANDER_DEFAULT_STATE": False,
    "PROGRESS_BAR_HEIGHT": 20,
    "BUTTON_HEIGHT": 40,
    "SIDEBAR_WIDTH": 300,
    "MAX_CONTENT_WIDTH": 1200
}

# Default system message for AI
DEFAULT_SYSTEM_MESSAGE = """Du bist ein präziser Codierer, der Texte anhand vorgegebener Kategorien einordnet. 
Antworte ausschließlich mit den passenden Codes. Deine Aufgabe ist es, die gegebenen Texte sorgfältig zu analysieren 
und die am besten passenden Kategorien zuzuweisen."""

# Task templates for different coding methods
DEFAULT_TASK_TEMPLATES = {
    "single_label": """{CODES_AND_CATEGORIES}

        {context_section}
        
        Zu kategorisierende Nennung: {word}
        
        1. Analysiere die Nennung im Kontext der Studie
        2. Wähle die EINE am besten passende Kategorie aus
        3. Berücksichtige nur direkte, eindeutige Übereinstimmungen
        4. Vergib genau einen Code
        
        Antworte ausschließlich mit einem einzigen Code.
        
        Beispiele zur Orientierung:
        {examples}""",

    "multi_label": """{CODES_AND_CATEGORIES}

        {context_section}
        
        Zu kategorisierende Nennung: {word}
        
        1. Lies die Nennung sorgfältig im Studienkontext
        2. Vergleiche sie mit jeder Kategorie:
           - Kategorie 1 '{first_category}'
           - Kategorie 2 '{second_category}'
           - ...
        3. Prüfe auf direkte und indirekte Übereinstimmungen
        4. Vergib alle zutreffenden Codes
        
        Antworte ausschließlich mit den Codes (durch Kommas getrennt).
        
        Beispiele zur Orientierung:
        {examples}"""
}

# AI Model settings
AI_SETTINGS = {
    "DEFAULT_MODEL": "gpt-4o-mini",
    "AVAILABLE_MODELS": ["gpt-4o-mini", "o3-mini"],
    "TEMPERATURE": 0.2,
    "FREQUENCY_PENALTY": 0.0,
    "PRESENCE_PENALTY": 0.0
}

# Database table names
DB_TABLES = {
    "SESSION_STATES": "session_states",
    "SAVED_CODEPLANS": "saved_codeplans",
    "STUDY_CONTEXTS": "study_contexts",
    "EXAMPLE_SETS": "example_sets",
    "SYSTEM_PROMPTS": "system_prompts",
    "USER_PROFILES": "user_profiles",
    "CODING_HISTORY": "coding_history",
    "AI_INTERACTIONS": "ai_interactions"
}

# Error messages
ERROR_MESSAGES = {
    "AUTH_REQUIRED": "Bitte melde dich an, um diese Seite zu nutzen.",
    "INVALID_CREDENTIALS": "Ungültige Anmeldedaten oder E-Mail nicht verifiziert",
    "USER_EXISTS": "Diese E-Mail ist bereits registriert. Bitte versuche dich anzumelden.",
    "MISSING_INPUT": "Bitte fülle alle erforderlichen Felder aus.",
    "SAVE_ERROR": "Fehler beim Speichern: {}",
    "LOAD_ERROR": "Fehler beim Laden: {}",
    "PROCESSING_ERROR": "Fehler bei der Verarbeitung: {}",
    "AI_ERROR": "Fehler bei der KI-Verarbeitung: {}"
}

# Success messages
SUCCESS_MESSAGES = {
    "LOGIN": "Erfolgreich angemeldet!",
    "LOGIN_WITH_STATE": "Erfolgreich angemeldet! Deine letzte Sitzung wurde wiederhergestellt.",
    "REGISTRATION": "Registrierung erfolgreich! Bitte melde dich mit deinen Zugangsdaten an.",
    "SAVE": "✅ {} erfolgreich gespeichert!",
    "LOAD": "✅ {} erfolgreich geladen!",
    "PROCESSING": "✅ Verarbeitung abgeschlossen!"
}

# Validation settings
VALIDATION = {
    "MIN_PASSWORD_LENGTH": 6,
    "MAX_TEXT_LENGTH": 500,
    "ALLOWED_FILE_TYPES": [".xlsx", ".xls", ".csv"],
    "MAX_FILE_SIZE": 5 * 1024 * 1024  # 5MB
} 