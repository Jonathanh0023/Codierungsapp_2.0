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
    
    generate_button = st.button(
        "🤖 Codeplan generieren", 
        disabled=not (ai_nennungen and st.session_state.api_key),
        key="generate_codeplan_button"
    )
    
    if generate_button:
        if not st.session_state.api_key:
            st.error("Bitte gib einen OpenAI API-Schlüssel ein.")
            return
            
        with st.spinner("KI generiert Codeplan..."):
            try:
                # Setze den API Key
                openai.api_key = st.session_state.api_key
                
                # Prompt für die KI
                prompt = f"""Analysiere die folgenden Nennungen und erstelle {num_categories} sinnvolle Kategorien zur Codierung.

Studienkontext:
{ai_context}

Nennungen:
{ai_nennungen}

Erstelle einen Codeplan mit folgenden Anforderungen:
1. Genau {num_categories} Kategorien
2. Jede Kategorie sollte prägnant und eindeutig sein
3. Die Kategorien sollten alle wichtigen Aspekte der Nennungen abdecken
4. Vergib für jede Kategorie einen numerischen Code (1, 2, 3, ...)

Antworte im Format:
Code | Kategorie | Beschreibung
1 | [Kategorie 1] | [Kurze Beschreibung]
2 | [Kategorie 2] | [Kurze Beschreibung]
...
"""
                # KI-Anfrage
                response = openai.chat.completions.create(
                    model=st.session_state.selected_model,
                    messages=[
                        {"role": "system", "content": "Du bist ein Experte für die Entwicklung von Kategoriensystemen und Codeplänen."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                
                # Log AI interaction
                DatabaseService.log_ai_interaction({
                    "user_id": st.session_state.user_id,
                    "input_text": prompt,
                    "output_text": response.choices[0].message.content,
                    "model_used": st.session_state.selected_model,
                    "created_at": datetime.now().isoformat()
                })
                
                # Process and display results
                handle_ai_response(response.choices[0].message.content, ai_nennungen)
                
            except Exception as e:
                st.error(f"Fehler bei der KI-Generierung: {str(e)}")

def handle_ai_response(result: str, ai_nennungen: str):
    """Handle the AI response and update the UI"""
    # Show the result
    st.markdown("### Generierter Codeplan")
    st.text(result)
    
    # Extract codes and categories
    lines = result.strip().split('\n')
    codes = []
    categories = []
    
    for line in lines:
        if '|' in line:
            parts = [p.strip() for p in line.split('|')]
            if not any(header in line.lower() for header in ['code', 'kategorie', 'beschreibung', '---']):
                try:
                    code = parts[0].strip()
                    category = parts[1].strip()
                    if code and category:
                        codes.append(code)
                        categories.append(category)
                except IndexError:
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
                # Update session state
                st.session_state.codes_input_text = '\n'.join(codes)
                st.session_state.codes_input_area = '\n'.join(codes)
                st.session_state.categories_input_text = '\n'.join(categories)
                st.session_state.categories_input_area = '\n'.join(categories)
                st.session_state.search_words_input = ai_nennungen
                st.session_state.search_words_input_area = ai_nennungen
                
                st.success("✅ KI-generierter Codeplan wurde in die Eingabefelder übernommen!")
                save_current_state()
                time.sleep(0.5)
                st.rerun()
        except Exception as e:
            st.error(f"Fehler beim Speichern des generierten Codeplans: {str(e)}")
    else:
        st.error("Konnte keine gültigen Codes und Kategorien aus der KI-Antwort extrahieren.")

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