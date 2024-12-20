import streamlit as st
import pandas as pd
from fuzzywuzzy import fuzz, process
from io import BytesIO
from utils import save_current_state
from services.db_service import DatabaseService
from datetime import datetime
from styles.custom_css import get_custom_css

def fuzzy_page():
    """Main function for the FuzzyWuzzy app"""
    # Apply custom CSS
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    # Create a layout with a "Back to Home" button in the top right
    col1, col2 = st.columns([8, 2])  # Adjusted column width for a wider button
    with col2:
        if st.button("🏠", key="fuzzy_back"):
            # Don't save state when navigating back
            st.session_state.selected_app = None
            st.rerun()

    # App layout
    st.title("FuzzyWuzzy Markencodierung")
    
    # Load saved codeplans if available
    saved_codeplan = None
    try:
        codeplans = DatabaseService.load_codeplans(st.session_state.user_id)
        if codeplans:
            st.subheader("Gespeicherte Codepläne")
            codeplan_options = {f"{plan['name']} ({plan['created_at'][:10]})": plan for plan in codeplans}
            selected_plan = st.selectbox(
                "Wähle einen Codeplan:",
                list(codeplan_options.keys()),
                key="fuzzy_codeplan_select"
            )
            
            if st.button("Codeplan laden"):
                saved_codeplan = codeplan_options[selected_plan]
                st.success("✅ Codeplan geladen!")
    except Exception as e:
        st.error(f"Fehler beim Laden der Codepläne: {str(e)}")

    # Settings for input processing
    with st.expander("⚙️ Erweiterte Einstellungen", expanded=False):
        col_settings1, col_settings2 = st.columns([1, 1])
        
        with col_settings1:
            use_spaces = st.checkbox(
                "Auch nach Leerzeichen trennen",
                help="Aktivieren Sie diese Option, wenn die Eingaben auch nach Leerzeichen getrennt werden sollen"
            )
        
        if use_spaces:
            with col_settings2:
                exceptions = st.text_area(
                    "Ausnahmen für Leerzeichen-Trennung (eine pro Zeile)",
                    help="Markennamen, die Leerzeichen enthalten und zusammen bleiben sollen",
                    placeholder="New Balance\nCoca Cola\nDr Pepper",
                    key="exceptions"
                )
                exception_set = {exc.strip().lower() for exc in exceptions.split('\n') if exc.strip()}
        else:
            exception_set = set()

    # Manual input section
    st.subheader("1️⃣ Codeplan")
    brands_and_codes = st.text_area(
        "Fügen Sie den Codeplan ein (aus Excel kopiert oder mit Tab getrennt)",
        value='\n'.join([f"{code}\t{cat}" for code, cat in zip(saved_codeplan['codes'], saved_codeplan['categories'])]) if saved_codeplan else "",
        key="code_plan",
        height=150
    )

    # Process input text and save to dictionary
    brand_codes = {}
    if brands_and_codes:
        for line in brands_and_codes.split("\n"):
            parts = line.split("\t")  # Assumes tab-separated data
            if len(parts) >= 2:
                code, brands = parts[0].strip(), parts[1].strip()
                # Add each brand to the dictionary, considering multiple names
                for brand in brands.split(','):
                    clean_brand = brand.strip()
                    if clean_brand:  # Ensure no empty strings
                        # Consider brands with multiple possible names
                        for name in clean_brand.split('/'):
                            brand_codes[name.strip().lower()] = code

    # Text area for survey data with improved UI
    st.subheader("2️⃣ Offene Nennungen")
    col_input1, col_input2 = st.columns([2, 1])
    
    with col_input1:
        survey_input = st.text_area(
            "Fügen Sie hier die zu codierenden Nennungen ein:",
            key="survey_input",
            height=150
        )
    
    with col_input2:
        st.markdown("##### 📝 Eingabeformat")
        st.markdown("""
        - Trennung durch Komma: `Nike, Adidas, Puma`
        """)
        
        if use_spaces:
            st.markdown("""
            - Zusätzlich durch Leerzeichen: `Nike Adidas Puma`
            - Mit Ausnahmen: `New Balance Nike Coca Cola`
            """)

    # Process button with loading state
    if st.button("🎯 Jetzt codieren", type="primary", use_container_width=True):
        with st.spinner("Verarbeite Eingaben..."):
            process_survey_data(survey_input, brand_codes, use_spaces, exception_set)

def process_survey_data(survey_input: str, brand_codes: dict, use_spaces: bool, exceptions: set):
    """Process survey data and display results"""
    if survey_input:
        try:
            all_matches = []
            start_time = datetime.now()
            
            # Process each input line
            for line in survey_input.split("\n"):
                line = line.strip()
                if line:  # Ensure input line is not empty
                    matched_line = match_organizations(line, brand_codes, use_spaces, exceptions)
                    all_matches.append(matched_line)
            
            # Convert matches to dataframe
            df_matches = pd.DataFrame(all_matches)
            
            # Display results in an expandable section
            with st.expander("📊 Ergebnisse anzeigen", expanded=True):
                st.dataframe(
                    df_matches,
                    use_container_width=True,
                    hide_index=True
                )
            
            # Create download button
            excel_data = create_excel_download(df_matches)
            st.download_button(
                label="📥 Download als Excel",
                data=excel_data,
                file_name=f'fuzzy_matches_{datetime.now().strftime("%Y%m%d_%H%M")}.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
            # Log the processing
            processing_time = (datetime.now() - start_time).total_seconds()
            log_fuzzy_processing(survey_input, df_matches, processing_time)
            
        except Exception as e:
            st.error(f"Fehler bei der Verarbeitung: {str(e)}")

def match_organizations(input_text: str, brand_codes: dict, use_spaces: bool, exceptions: set) -> list:
    """Match input text against brand codes using fuzzy matching"""
    # First split by comma
    comma_parts = [part.strip() for part in input_text.split(',')]
    organizations = []
    
    for part in comma_parts:
        if not part:  # Skip empty parts
            continue
            
        if use_spaces:
            # Protect exceptions by replacing spaces with temporary marker
            working_text = part.lower()
            temp_marker = "§§§"
            
            # Replace spaces in exceptions with marker
            for exception in exceptions:
                if exception in working_text:
                    working_text = working_text.replace(exception, exception.replace(" ", temp_marker))
            
            # Split by spaces and restore markers
            space_parts = [org.strip().replace(temp_marker, " ") for org in working_text.split()]
            organizations.extend(space_parts)
        else:
            organizations.append(part)
    
    matches = []
    for org in organizations:
        if org:  # Skip empty strings
            matched_code = process.extractOne(
                org.lower(),
                brand_codes.keys(),
                scorer=fuzz.partial_ratio,
                score_cutoff=75
            )
            if matched_code:
                matches.append(brand_codes[matched_code[0]])
            else:
                matches.append("Kein passender Code gefunden")
    
    return [input_text] + matches

def create_excel_download(df: pd.DataFrame) -> bytes:
    """Create Excel file from DataFrame"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

def log_fuzzy_processing(input_text: str, results_df: pd.DataFrame, processing_time: float):
    """Log the fuzzy processing to database"""
    try:
        log_data = {
            "user_id": st.session_state.user_id,
            "coding_method": "FuzzyWuzzy",
            "input_text": input_text[:500],  # Limit text length
            "assigned_codes": results_df.to_dict(),
            "processing_time": processing_time,
            "created_at": datetime.now().isoformat()
        }
        
        DatabaseService.log_coding_history(log_data)
    except Exception as e:
        print(f"Error logging fuzzy processing: {str(e)}")

if __name__ == "__main__":
    fuzzy_page()
