# Setting up Supabase Credentials

1. Local Development:
   - Create a `.streamlit` folder in your project root
   - Create `secrets.toml` inside `.streamlit`
   - Add your credentials:
     ```toml
     supabase_url = "your-project-url"
     supabase_key = "your-anon-key"
     ```

2. Getting Supabase Credentials:
   - Go to https://app.supabase.io
   - Open your project
   - Go to Settings > API
   - Copy "Project URL" and "anon/public" key

3. Streamlit Cloud Deployment:
   - Go to your app on https://share.streamlit.io
   - Click on "Manage app" > "Secrets"
   - Add the same credentials as in your local secrets.toml

4. Security Notes:
   - Never commit secrets.toml to version control
   - Add .streamlit/secrets.toml to .gitignore
   - Use environment variables for additional security 