import streamlit as st
import time
import openai
from datetime import datetime
from utils import save_current_state
from services.db_service import DatabaseService

def update_session_state(key: str):
    """Update session state from widget value"""
    if f"{key}_area" in st.session_state:
        st.session_state[key] = st.session_state[f"{key}_area"]
        save_current_state()

def save_codeplan():
    """Speichert den aktuellen Codeplan"""
    try:
        name = st.text_input("Name des Codeplans:", key="save_codeplan_name")
        description = st.text_area("Beschreibung (optional):", key="save_codeplan_description")
        is_public = st.checkbox("Öffentlich verfügbar machen?", key="save_codeplan_public")
        
        if st.button("Codeplan speichern", key="save_codeplan_button"):
            # Get values from session state using the correct keys
            codes = st.session_state.get('codes_input', '').strip()
            categories = st.session_state.get('categories_input', '').strip()
            
            if not codes or not categories:
                st.error("Bitte gib sowohl Codes als auch Kategorien ein.")
                return
            
            if not name:
                st.error("Bitte gib einen Namen ein.")
                return
            
            codeplan_data = {
                "user_id": st.session_state.user_id,
                "name": name,
                "codes": codes.split('\n'),
                "categories": categories.split('\n'),
                "description": description,
                "is_public": is_public,
                "created_at": datetime.now().isoformat()
            }
            
            # Use database service to save codeplan
            saved_codeplan = DatabaseService.save_codeplan(codeplan_data)
            if saved_codeplan:
                st.success("✅ Codeplan erfolgreich gespeichert!")
                time.sleep(0.5)
                st.rerun()
    except Exception as e:
        st.error(f"Fehler beim Speichern: {str(e)}")

def load_codeplan():
    """Lädt einen gespeicherten Codeplan"""
    try:
        # Use database service to load codeplans
        codeplans = DatabaseService.load_codeplans(st.session_state.user_id)
            
        if codeplans:
            codeplan_options = {f"{plan['name']} ({plan['created_at'][:10]})": plan for plan in codeplans}
            selected_plan = st.selectbox(
                "Wähle einen Codeplan:",
                list(codeplan_options.keys()),
                key="load_codeplan_select"
            )
            
            if codeplan_options[selected_plan]['description']:
                st.info(codeplan_options[selected_plan]['description'])
            
            if st.button("Codeplan laden", key="load_codeplan_button"):
                plan = codeplan_options[selected_plan]
                # Update both versions of the state
                st.session_state.codes_input = '\n'.join(plan['codes'])
                st.session_state.codes_input_area = '\n'.join(plan['codes'])
                st.session_state.categories_input = '\n'.join(plan['categories'])
                st.session_state.categories_input_area = '\n'.join(plan['categories'])
                st.success("✅ Codeplan erfolgreich geladen!")
                save_current_state()
                time.sleep(0.5)
                st.rerun()
        else:
            st.info("Keine gespeicherten Codepläne gefunden.")
    except Exception as e:
        st.error(f"Fehler beim Laden: {str(e)}")

def generate_codeplan():
    """KI-gestützte Generierung eines Codeplans"""
    # Initialize session state variables if they don't exist
    if 'codes_input_area' not in st.session_state:
        st.session_state.codes_input_area = ''
    if 'categories_input_area' not in st.session_state:
        st.session_state.categories_input_area = ''
    if 'search_words_input_area' not in st.session_state:
        st.session_state.search_words_input_area = ''
    
    num_categories = st.slider(
        "Anzahl der zu generierenden Kategorien:",
        min_value=2,
        max_value=20,
        value=5,
        help="Wähle, wie viele Kategorien die KI erstellen soll"
    )
    
    ai_context = st.text_area(
        "Studienkontext für die Kategorienbildung:",
        placeholder="Beschreibe hier den Kontext der Studie, um bessere Kategorien zu erhalten...",
        height=100
    )
    
    ai_nennungen = st.text_area(
        "Nennungen für die Kategorienbildung:",
        placeholder="Füge hier die Nennungen ein, die kategorisiert werden sollen...",
        height=200
    )
    
    # Erstelle einen Container für die Ergebnisse
    result_container = st.empty()
    
    # Überprüfe, ob der Button deaktiviert sein sollte
    is_disabled = not (ai_nennungen and st.session_state.get('api_key', ''))
    
    # Direkter Streamlit-Button für die Generierung
    if st.button("🤖 Codeplan generieren", key="generate_codeplan_button", disabled=is_disabled, type="primary"):
        with result_container:
            with st.spinner("Generiere Codeplan mit KI..."):
                try:
                    # Setze den API-Key
                    openai.api_key = st.session_state.api_key
                    
                    # Bereite den Prompt vor
                    prompt = f"""
                    Aufgabe: Erstelle einen Codeplan mit {num_categories} Kategorien basierend auf den folgenden Nennungen.
                    
                    Studienkontext: {ai_context if ai_context else 'Nicht angegeben'}
                    
                    Nennungen:
                    {ai_nennungen}
                    
                    Bitte erstelle einen Codeplan im folgenden Format:
                    | Code | Kategorie | Beschreibung |
                    |------|-----------|-------------|
                    | 1 | Kategorie 1 | Beschreibung für Kategorie 1 |
                    | 2 | Kategorie 2 | Beschreibung für Kategorie 2 |
                    ...
                    
                    Wichtig:
                    1. Erstelle genau {num_categories} Kategorien
                    2. Jede Kategorie sollte einen klaren, präzisen Namen haben
                    3. Die Beschreibung sollte erklären, welche Art von Nennungen in diese Kategorie fallen
                    4. Verwende als Codes einfache Zahlen (1, 2, 3, ...)
                    """
                    
                    # Hole das aktuelle Modell
                    current_model = st.session_state.get('selected_model', 'gpt-4o-mini')
                    
                    # Bereite die API-Parameter vor
                    api_params = {
                        "model": current_model,
                        "messages": [
                            {"role": "system", "content": "Du bist ein Experte für qualitative Inhaltsanalyse und Kategorienbildung."},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.7
                    }
                    
                    # Füge modellspezifische Einstellungen hinzu, wenn vorhanden
                    from config.settings import AI_SETTINGS
                    model_settings = AI_SETTINGS["MODEL_SETTINGS"].get(current_model, {})
                    if model_settings:
                        api_params.update(model_settings)
                    
                    # Mache den API-Aufruf
                    response = openai.chat.completions.create(**api_params)
                    result = response.choices[0].message.content.strip()
                    
                    # Verarbeite die Antwort
                    handle_ai_response(result, ai_nennungen)
                    
                except Exception as e:
                    st.error(f"Fehler bei der Generierung des Codeplans: {str(e)}")
                    import traceback
                    st.error(traceback.format_exc())

def handle_ai_response(result: str, ai_nennungen: str):
    """Handle the AI response and update the UI"""
    # Show the result
    st.markdown("### Generierter Codeplan")
    st.text(result)
    
    # Extract codes and categories
    lines = result.strip().split('\n')
    codes = []
    categories = []
    descriptions = []
    
    # Debug-Ausgabe
    st.write("Extrahiere Daten aus folgenden Zeilen:")
    
    for line in lines:
        if '|' in line:
            parts = [p.strip() for p in line.split('|')]
            # Debug-Ausgabe für jede Zeile
            st.write(f"Zeile: {line}")
            st.write(f"Teile: {parts}")
            
            # Überspringe Überschriften und Trennzeilen
            if not any(header in line.lower() for header in ['code', 'kategorie', 'beschreibung', '---']):
                try:
                    # In einer Markdown-Tabelle ist das erste Element leer
                    # Format: | Code | Kategorie | Beschreibung |
                    if len(parts) >= 4:  # Mindestens 4 Teile (leerer Teil + Code + Kategorie + Beschreibung)
                        code = parts[1].strip()  # Code ist in der zweiten Spalte (Index 1)
                        category = parts[2].strip()  # Kategorie ist in der dritten Spalte (Index 2)
                        description = parts[3].strip() if len(parts) > 3 else ""  # Beschreibung ist in der vierten Spalte (Index 3)
                        
                        if code and category:
                            codes.append(code)
                            categories.append(category)
                            descriptions.append(description)
                            st.write(f"Extrahiert: Code={code}, Kategorie={category}")
                except IndexError as e:
                    st.write(f"Fehler bei der Extraktion: {str(e)}")
                    continue
    
    if codes and categories:
        st.success(f"{len(codes)} Kategorien erfolgreich erstellt!")
        
        # Save generated codeplan
        codeplan_data = {
            "user_id": st.session_state.user_id,
            "name": f"KI-generierter Codeplan ({datetime.now().strftime('%Y-%m-%d %H:%M')})",
            "codes": codes,
            "categories": categories,
            "description": f"Automatisch generierter Codeplan basierend auf {len(ai_nennungen.splitlines())} Nennungen",
            "is_public": False
        }
        
        try:
            # Save using database service
            saved_plan = DatabaseService.save_codeplan(codeplan_data)
            if saved_plan:
                # Update session state - Korrigierte Variablennamen
                st.session_state.codes_input = '\n'.join(codes)
                st.session_state.codes_input_area = '\n'.join(codes)
                st.session_state.categories_input = '\n'.join(categories)
                st.session_state.categories_input_area = '\n'.join(categories)
                st.session_state.search_words_input = ai_nennungen
                st.session_state.search_words_input_area = ai_nennungen
                
                st.success("✅ KI-generierter Codeplan wurde in die Eingabefelder übernommen!")
                save_current_state()
                time.sleep(1.5)  # Längere Verzögerung für bessere Sichtbarkeit
                st.rerun()
        except Exception as e:
            st.error(f"Fehler beim Speichern des generierten Codeplans: {str(e)}")
            import traceback
            st.error(traceback.format_exc())
    else:
        st.error("Konnte keine gültigen Codes und Kategorien aus der KI-Antwort extrahieren.")
        st.write("Rohdaten der KI-Antwort:")
        st.code(result)

def render_codeplan_section():
    """Rendert den Codeplan-Bereich der UI"""
    st.markdown("""### 📋 Codeplan erstellen oder importieren
    Der Codeplan ist das Herzstück der Codierung. Du hast folgende Möglichkeiten:
     🤖 KI-Generierung: Lass die KI einen Codeplan aus deinen Nennungen erstellen
     💾 Speichern: Speichere deinen aktuellen Codeplan
     📂 Laden: Lade einen gespeicherten Codeplan
    """)
    
    with st.expander("🎯 Codeplan-Assistent", expanded=st.session_state.codeplan_expander_open):
        tab1, tab2, tab3 = st.tabs(["🤖 KI-Generierung", "💾 Speichern", "📂 Laden"])
        
        with tab1:
            generate_codeplan()
            
        with tab2:
            save_codeplan()
            
        with tab3:
            load_codeplan()