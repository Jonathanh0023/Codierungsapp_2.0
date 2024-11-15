-- Users Profile Table
CREATE TABLE user_profiles (
    id UUID REFERENCES auth.users(id) PRIMARY KEY,
    email VARCHAR NOT NULL,
    full_name VARCHAR,
    organization VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Session States Table
CREATE TABLE session_states (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) NOT NULL,
    codes_input TEXT,
    categories_input TEXT,
    search_words_input TEXT,
    study_context_input TEXT,
    beispiele_input TEXT,
    selected_task_template VARCHAR,
    instructions_read BOOLEAN DEFAULT false,
    system_message TEXT,
    question_template TEXT,
    codeplan_expander_open BOOLEAN DEFAULT false,
    results_df JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    UNIQUE(user_id)
);

-- Saved Codeplans Table
CREATE TABLE saved_codeplans (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) NOT NULL,
    name VARCHAR NOT NULL,
    codes TEXT[] NOT NULL,
    categories TEXT[] NOT NULL,
    description TEXT,
    is_public BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Study Contexts Table
CREATE TABLE study_contexts (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) NOT NULL,
    name VARCHAR NOT NULL,
    context TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Example Sets Table
CREATE TABLE example_sets (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) NOT NULL,
    name VARCHAR NOT NULL,
    examples TEXT[] NOT NULL,
    description TEXT,
    category VARCHAR,
    is_public BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- System Prompts Table
CREATE TABLE system_prompts (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) NOT NULL,
    name VARCHAR NOT NULL,
    prompt TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Coding History Table
CREATE TABLE coding_history (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) NOT NULL,
    coding_method VARCHAR NOT NULL,
    input_text TEXT NOT NULL,
    assigned_codes JSONB NOT NULL,
    model_used VARCHAR,
    processing_time FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- AI Interactions Log Table
CREATE TABLE ai_interactions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) NOT NULL,
    input_text TEXT NOT NULL,
    output_text TEXT NOT NULL,
    model_used VARCHAR NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Row Level Security Policies
-- User Profiles
CREATE POLICY "Users can view their own profile"
    ON user_profiles FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can update their own profile"
    ON user_profiles FOR UPDATE
    USING (auth.uid() = id);

-- Session States
CREATE POLICY "Users can view their own sessions"
    ON session_states FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can update their own sessions"
    ON session_states FOR ALL
    USING (auth.uid() = user_id);

-- Saved Codeplans
CREATE POLICY "Users can view their own and public codeplans"
    ON saved_codeplans FOR SELECT
    USING (auth.uid() = user_id OR is_public = true);

CREATE POLICY "Users can manage their own codeplans"
    ON saved_codeplans FOR ALL
    USING (auth.uid() = user_id);

-- Study Contexts
CREATE POLICY "Users can view their own and public contexts"
    ON study_contexts FOR SELECT
    USING (auth.uid() = user_id OR is_public = true);

CREATE POLICY "Users can manage their own contexts"
    ON study_contexts FOR ALL
    USING (auth.uid() = user_id);

-- Example Sets
CREATE POLICY "Users can view their own and public examples"
    ON example_sets FOR SELECT
    USING (auth.uid() = user_id OR is_public = true);

CREATE POLICY "Users can manage their own examples"
    ON example_sets FOR ALL
    USING (auth.uid() = user_id);

-- System Prompts
CREATE POLICY "Users can view their own and public prompts"
    ON system_prompts FOR SELECT
    USING (auth.uid() = user_id OR is_public = true);

CREATE POLICY "Users can manage their own prompts"
    ON system_prompts FOR ALL
    USING (auth.uid() = user_id);

-- Coding History
CREATE POLICY "Users can view their own coding history"
    ON coding_history FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can manage their own coding history"
    ON coding_history FOR ALL
    USING (auth.uid() = user_id);

-- AI Interactions
CREATE POLICY "Users can view their own AI interactions"
    ON ai_interactions FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can manage their own AI interactions"
    ON ai_interactions FOR ALL
    USING (auth.uid() = user_id);

-- Enable RLS on all tables
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE session_states ENABLE ROW LEVEL SECURITY;
ALTER TABLE saved_codeplans ENABLE ROW LEVEL SECURITY;
ALTER TABLE study_contexts ENABLE ROW LEVEL SECURITY;
ALTER TABLE example_sets ENABLE ROW LEVEL SECURITY;
ALTER TABLE system_prompts ENABLE ROW LEVEL SECURITY;
ALTER TABLE coding_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_interactions ENABLE ROW LEVEL SECURITY;

-- Create indexes for better performance
CREATE INDEX idx_session_states_user_id ON session_states(user_id);
CREATE INDEX idx_saved_codeplans_user_id ON saved_codeplans(user_id);
CREATE INDEX idx_study_contexts_user_id ON study_contexts(user_id);
CREATE INDEX idx_example_sets_user_id ON example_sets(user_id);
CREATE INDEX idx_system_prompts_user_id ON system_prompts(user_id);
CREATE INDEX idx_coding_history_user_id ON coding_history(user_id);
CREATE INDEX idx_ai_interactions_user_id ON ai_interactions(user_id); 