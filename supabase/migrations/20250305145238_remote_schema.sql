

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;


CREATE EXTENSION IF NOT EXISTS "pgsodium" WITH SCHEMA "pgsodium";






COMMENT ON SCHEMA "public" IS 'standard public schema';



CREATE EXTENSION IF NOT EXISTS "pg_graphql" WITH SCHEMA "graphql";






CREATE EXTENSION IF NOT EXISTS "pg_stat_statements" WITH SCHEMA "extensions";






CREATE EXTENSION IF NOT EXISTS "pgcrypto" WITH SCHEMA "extensions";






CREATE EXTENSION IF NOT EXISTS "pgjwt" WITH SCHEMA "extensions";






CREATE EXTENSION IF NOT EXISTS "supabase_vault" WITH SCHEMA "vault";






CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA "extensions";






CREATE TYPE "public"."coding_method" AS ENUM (
    'single_label',
    'multi_label'
);


ALTER TYPE "public"."coding_method" OWNER TO "postgres";


CREATE TYPE "public"."prompt_type" AS ENUM (
    'system',
    'task',
    'custom'
);


ALTER TYPE "public"."prompt_type" OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."handle_updated_at"() RETURNS "trigger"
    LANGUAGE "plpgsql"
    AS $$
begin
    new.updated_at = timezone('utc'::text, now());
    return new;
end;
$$;


ALTER FUNCTION "public"."handle_updated_at"() OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."update_updated_at_column"() RETURNS "trigger"
    LANGUAGE "plpgsql"
    AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;


ALTER FUNCTION "public"."update_updated_at_column"() OWNER TO "postgres";

SET default_tablespace = '';

SET default_table_access_method = "heap";


CREATE TABLE IF NOT EXISTS "public"."ai_interactions" (
    "id" "uuid" DEFAULT "extensions"."uuid_generate_v4"() NOT NULL,
    "user_id" "uuid" NOT NULL,
    "input_text" "text" NOT NULL,
    "output_text" "text" NOT NULL,
    "model_used" character varying NOT NULL,
    "created_at" timestamp with time zone DEFAULT "timezone"('utc'::"text", "now"()) NOT NULL
);


ALTER TABLE "public"."ai_interactions" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."coding_history" (
    "id" "uuid" DEFAULT "extensions"."uuid_generate_v4"() NOT NULL,
    "user_id" "uuid" NOT NULL,
    "coding_method" character varying NOT NULL,
    "input_text" "text" NOT NULL,
    "assigned_codes" "jsonb" NOT NULL,
    "model_used" character varying,
    "processing_time" double precision,
    "created_at" timestamp with time zone DEFAULT "timezone"('utc'::"text", "now"()) NOT NULL
);


ALTER TABLE "public"."coding_history" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."coding_sessions" (
    "id" "uuid" DEFAULT "extensions"."uuid_generate_v4"() NOT NULL,
    "user_id" "uuid",
    "model_used" character varying,
    "created_at" timestamp with time zone DEFAULT "now"(),
    "total_items" integer,
    "input_data" "jsonb",
    "output_data" "jsonb",
    "metadata" "jsonb"
);


ALTER TABLE "public"."coding_sessions" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."example_sets" (
    "id" "uuid" DEFAULT "extensions"."uuid_generate_v4"() NOT NULL,
    "user_id" "uuid" NOT NULL,
    "name" character varying NOT NULL,
    "examples" "text"[] NOT NULL,
    "description" "text",
    "category" character varying,
    "is_public" boolean DEFAULT false,
    "created_at" timestamp with time zone DEFAULT "timezone"('utc'::"text", "now"()) NOT NULL
);


ALTER TABLE "public"."example_sets" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."saved_codeplans" (
    "id" "uuid" DEFAULT "extensions"."uuid_generate_v4"() NOT NULL,
    "user_id" "uuid" NOT NULL,
    "name" character varying NOT NULL,
    "codes" "text"[] NOT NULL,
    "categories" "text"[] NOT NULL,
    "description" "text",
    "is_public" boolean DEFAULT false,
    "created_at" timestamp with time zone DEFAULT "timezone"('utc'::"text", "now"()) NOT NULL
);


ALTER TABLE "public"."saved_codeplans" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."session_states" (
    "id" "uuid" DEFAULT "extensions"."uuid_generate_v4"() NOT NULL,
    "user_id" "uuid" NOT NULL,
    "codes_input" "text",
    "categories_input" "text",
    "search_words_input" "text",
    "study_context_input" "text",
    "beispiele_input" "text",
    "selected_task_template" character varying,
    "instructions_read" boolean DEFAULT false,
    "system_message" "text",
    "question_template" "text",
    "codeplan_expander_open" boolean DEFAULT false,
    "results_df" "jsonb",
    "created_at" timestamp with time zone DEFAULT "timezone"('utc'::"text", "now"()) NOT NULL,
    "updated_at" timestamp with time zone DEFAULT "timezone"('utc'::"text", "now"()) NOT NULL
);


ALTER TABLE "public"."session_states" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."study_contexts" (
    "id" "uuid" DEFAULT "extensions"."uuid_generate_v4"() NOT NULL,
    "user_id" "uuid" NOT NULL,
    "name" character varying NOT NULL,
    "context" "text" NOT NULL,
    "description" "text",
    "is_public" boolean DEFAULT false,
    "created_at" timestamp with time zone DEFAULT "timezone"('utc'::"text", "now"()) NOT NULL
);


ALTER TABLE "public"."study_contexts" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."system_prompts" (
    "id" "uuid" DEFAULT "extensions"."uuid_generate_v4"() NOT NULL,
    "user_id" "uuid" NOT NULL,
    "name" character varying NOT NULL,
    "prompt" "text" NOT NULL,
    "description" "text",
    "is_public" boolean DEFAULT false,
    "created_at" timestamp with time zone DEFAULT "timezone"('utc'::"text", "now"()) NOT NULL
);


ALTER TABLE "public"."system_prompts" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."user_profiles" (
    "id" "uuid" NOT NULL,
    "email" character varying NOT NULL,
    "full_name" character varying,
    "organization" character varying,
    "created_at" timestamp with time zone DEFAULT "timezone"('utc'::"text", "now"()) NOT NULL,
    "updated_at" timestamp with time zone DEFAULT "timezone"('utc'::"text", "now"()) NOT NULL
);


ALTER TABLE "public"."user_profiles" OWNER TO "postgres";


ALTER TABLE ONLY "public"."ai_interactions"
    ADD CONSTRAINT "ai_interactions_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."coding_history"
    ADD CONSTRAINT "coding_history_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."coding_sessions"
    ADD CONSTRAINT "coding_sessions_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."example_sets"
    ADD CONSTRAINT "example_sets_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."saved_codeplans"
    ADD CONSTRAINT "saved_codeplans_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."session_states"
    ADD CONSTRAINT "session_states_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."session_states"
    ADD CONSTRAINT "session_states_user_id_key" UNIQUE ("user_id");



ALTER TABLE ONLY "public"."study_contexts"
    ADD CONSTRAINT "study_contexts_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."system_prompts"
    ADD CONSTRAINT "system_prompts_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."user_profiles"
    ADD CONSTRAINT "user_profiles_pkey" PRIMARY KEY ("id");



CREATE INDEX "idx_ai_interactions_user_id" ON "public"."ai_interactions" USING "btree" ("user_id");



CREATE INDEX "idx_coding_history_user_id" ON "public"."coding_history" USING "btree" ("user_id");



CREATE INDEX "idx_example_sets_user_id" ON "public"."example_sets" USING "btree" ("user_id");



CREATE INDEX "idx_saved_codeplans_user_id" ON "public"."saved_codeplans" USING "btree" ("user_id");



CREATE INDEX "idx_session_states_user_id" ON "public"."session_states" USING "btree" ("user_id");



CREATE INDEX "idx_study_contexts_user_id" ON "public"."study_contexts" USING "btree" ("user_id");



CREATE INDEX "idx_system_prompts_user_id" ON "public"."system_prompts" USING "btree" ("user_id");



ALTER TABLE ONLY "public"."ai_interactions"
    ADD CONSTRAINT "ai_interactions_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id");



ALTER TABLE ONLY "public"."coding_history"
    ADD CONSTRAINT "coding_history_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id");



ALTER TABLE ONLY "public"."coding_sessions"
    ADD CONSTRAINT "coding_sessions_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id");



ALTER TABLE ONLY "public"."example_sets"
    ADD CONSTRAINT "example_sets_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id");



ALTER TABLE ONLY "public"."saved_codeplans"
    ADD CONSTRAINT "saved_codeplans_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id");



ALTER TABLE ONLY "public"."session_states"
    ADD CONSTRAINT "session_states_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id");



ALTER TABLE ONLY "public"."study_contexts"
    ADD CONSTRAINT "study_contexts_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id");



ALTER TABLE ONLY "public"."system_prompts"
    ADD CONSTRAINT "system_prompts_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id");



ALTER TABLE ONLY "public"."user_profiles"
    ADD CONSTRAINT "user_profiles_id_fkey" FOREIGN KEY ("id") REFERENCES "auth"."users"("id");



CREATE POLICY "Admins can manage all sessions" ON "public"."session_states" USING ((("auth"."role"() = 'admin'::"text") OR ("auth"."uid"() = "user_id")));



CREATE POLICY "Users can insert their own AI interactions" ON "public"."ai_interactions" FOR INSERT WITH CHECK (("auth"."uid"() = "user_id"));



CREATE POLICY "Users can insert their own codeplans" ON "public"."saved_codeplans" FOR INSERT WITH CHECK (("auth"."uid"() = "user_id"));



CREATE POLICY "Users can insert their own coding history" ON "public"."coding_history" FOR INSERT WITH CHECK (("auth"."uid"() = "user_id"));



CREATE POLICY "Users can insert their own contexts" ON "public"."study_contexts" FOR INSERT WITH CHECK (("auth"."uid"() = "user_id"));



CREATE POLICY "Users can insert their own examples" ON "public"."example_sets" FOR INSERT WITH CHECK (("auth"."uid"() = "user_id"));



CREATE POLICY "Users can insert their own prompts" ON "public"."system_prompts" FOR INSERT WITH CHECK (("auth"."uid"() = "user_id"));



CREATE POLICY "Users can insert their own sessions" ON "public"."session_states" FOR INSERT WITH CHECK (("auth"."uid"() = "user_id"));



CREATE POLICY "Users can update their own profile" ON "public"."user_profiles" FOR UPDATE USING (("auth"."uid"() = "id"));



CREATE POLICY "Users can update their own sessions" ON "public"."session_states" FOR UPDATE USING (("auth"."uid"() = "user_id"));



CREATE POLICY "Users can view their own AI interactions" ON "public"."ai_interactions" FOR SELECT USING (("auth"."uid"() = "user_id"));



CREATE POLICY "Users can view their own and public codeplans" ON "public"."saved_codeplans" FOR SELECT USING ((("auth"."uid"() = "user_id") OR ("is_public" = true)));



CREATE POLICY "Users can view their own and public contexts" ON "public"."study_contexts" FOR SELECT USING ((("auth"."uid"() = "user_id") OR ("is_public" = true)));



CREATE POLICY "Users can view their own and public examples" ON "public"."example_sets" FOR SELECT USING ((("auth"."uid"() = "user_id") OR ("is_public" = true)));



CREATE POLICY "Users can view their own and public prompts" ON "public"."system_prompts" FOR SELECT USING ((("auth"."uid"() = "user_id") OR ("is_public" = true)));



CREATE POLICY "Users can view their own coding history" ON "public"."coding_history" FOR SELECT USING (("auth"."uid"() = "user_id"));



CREATE POLICY "Users can view their own profile" ON "public"."user_profiles" FOR SELECT USING (("auth"."uid"() = "id"));



CREATE POLICY "Users can view their own sessions" ON "public"."session_states" FOR SELECT USING (("auth"."uid"() = "user_id"));





ALTER PUBLICATION "supabase_realtime" OWNER TO "postgres";


GRANT USAGE ON SCHEMA "public" TO "postgres";
GRANT USAGE ON SCHEMA "public" TO "anon";
GRANT USAGE ON SCHEMA "public" TO "authenticated";
GRANT USAGE ON SCHEMA "public" TO "service_role";




















































































































































































GRANT ALL ON FUNCTION "public"."handle_updated_at"() TO "anon";
GRANT ALL ON FUNCTION "public"."handle_updated_at"() TO "authenticated";
GRANT ALL ON FUNCTION "public"."handle_updated_at"() TO "service_role";



GRANT ALL ON FUNCTION "public"."update_updated_at_column"() TO "anon";
GRANT ALL ON FUNCTION "public"."update_updated_at_column"() TO "authenticated";
GRANT ALL ON FUNCTION "public"."update_updated_at_column"() TO "service_role";


















GRANT ALL ON TABLE "public"."ai_interactions" TO "anon";
GRANT ALL ON TABLE "public"."ai_interactions" TO "authenticated";
GRANT ALL ON TABLE "public"."ai_interactions" TO "service_role";



GRANT ALL ON TABLE "public"."coding_history" TO "anon";
GRANT ALL ON TABLE "public"."coding_history" TO "authenticated";
GRANT ALL ON TABLE "public"."coding_history" TO "service_role";



GRANT ALL ON TABLE "public"."coding_sessions" TO "anon";
GRANT ALL ON TABLE "public"."coding_sessions" TO "authenticated";
GRANT ALL ON TABLE "public"."coding_sessions" TO "service_role";



GRANT ALL ON TABLE "public"."example_sets" TO "anon";
GRANT ALL ON TABLE "public"."example_sets" TO "authenticated";
GRANT ALL ON TABLE "public"."example_sets" TO "service_role";



GRANT ALL ON TABLE "public"."saved_codeplans" TO "anon";
GRANT ALL ON TABLE "public"."saved_codeplans" TO "authenticated";
GRANT ALL ON TABLE "public"."saved_codeplans" TO "service_role";



GRANT ALL ON TABLE "public"."session_states" TO "anon";
GRANT ALL ON TABLE "public"."session_states" TO "authenticated";
GRANT ALL ON TABLE "public"."session_states" TO "service_role";



GRANT ALL ON TABLE "public"."study_contexts" TO "anon";
GRANT ALL ON TABLE "public"."study_contexts" TO "authenticated";
GRANT ALL ON TABLE "public"."study_contexts" TO "service_role";



GRANT ALL ON TABLE "public"."system_prompts" TO "anon";
GRANT ALL ON TABLE "public"."system_prompts" TO "authenticated";
GRANT ALL ON TABLE "public"."system_prompts" TO "service_role";



GRANT ALL ON TABLE "public"."user_profiles" TO "anon";
GRANT ALL ON TABLE "public"."user_profiles" TO "authenticated";
GRANT ALL ON TABLE "public"."user_profiles" TO "service_role";



ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES  TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES  TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES  TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES  TO "service_role";






ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS  TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS  TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS  TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS  TO "service_role";






ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES  TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES  TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES  TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES  TO "service_role";






























RESET ALL;
