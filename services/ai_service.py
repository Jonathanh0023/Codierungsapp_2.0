import openai
import streamlit as st
from datetime import datetime
from config.settings import AI_SETTINGS, ERROR_MESSAGES

def prepare_prompt(word: str) -> str:
    """Prepare the prompt for AI processing"""
    # Get template based on selected method
    template = st.session_state.question_template
    
    # Prepare context variables
    codes_and_categories = []
    codes = st.session_state.codes_input.strip().split('\n')
    categories = st.session_state.categories_input.strip().split('\n')
    
    for code, category in zip(codes, categories):
        codes_and_categories.append(f"{code}: {category}")
    
    codes_and_categories_text = "\n".join(codes_and_categories)
    
    # Get examples if available
    examples = st.session_state.beispiele_input.strip()
    if not examples:
        examples = "Keine Beispiele verfügbar"
    
    # Get study context if available
    context_section = st.session_state.study_context_input.strip()
    if not context_section:
        context_section = "Kein Studienkontext verfügbar"
    
    # Get first two categories for multi-label template
    first_category = categories[0] if categories else ""
    second_category = categories[1] if len(categories) > 1 else ""
    
    # Format the template with all variables
    return template.format(
        CODES_AND_CATEGORIES=codes_and_categories_text,
        word=word,
        examples=examples,
        context_section=context_section,
        first_category=first_category,
        second_category=second_category
    )

def process_with_ai(word: str) -> str:
    """Process a word with AI and return the code"""
    try:
        # Set API key
        openai.api_key = st.session_state.api_key
        
        # Prepare messages
        messages = [
            {"role": "system", "content": st.session_state.system_message},
            {"role": "user", "content": prepare_prompt(word)}
        ]
        
        # Get current model
        current_model = st.session_state.get('selected_model', AI_SETTINGS["DEFAULT_MODEL"])
        
        # Prepare base API parameters
        api_params = {
            "model": current_model,
            "messages": messages
        }
        
        # Add model-specific settings if they exist
        model_settings = AI_SETTINGS["MODEL_SETTINGS"].get(current_model, {})
        if model_settings:
            api_params.update(model_settings)
        
        # Make API call
        response = openai.chat.completions.create(**api_params)
        
        # Log the interaction
        log_ai_interaction(word, response.choices[0].message.content)
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Error in AI processing: {str(e)}")
        raise Exception(ERROR_MESSAGES["AI_ERROR"].format(str(e)))



def log_ai_interaction(input_text: str, output: str):
    """Log AI interaction to database"""
    try:
        # Truncate input text according to validation settings
        from config.settings import VALIDATION
        truncated_input = input_text[:VALIDATION["MAX_TEXT_LENGTH"]]
        
        log_data = {
            "user_id": st.session_state.user_id,
            "input_text": truncated_input,
            "output_text": output,
            "model_used": st.session_state.get('selected_model', AI_SETTINGS["DEFAULT_MODEL"]),
            "created_at": datetime.now().isoformat()
        }
        
        st.session_state.supabase.table('ai_interactions').insert(log_data).execute()
    except Exception as e:
        print(f"Error logging AI interaction: {str(e)}") 