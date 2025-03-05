Übersicht der Codierungsapp 3.0
Allgemeine Struktur
Die Anwendung ist eine Streamlit-basierte Webanwendung mit dem Namen "BonsAI", die zwei Hauptfunktionalitäten bietet:
BonsAI Codierungstool: Ein KI-gestütztes Tool zur Codierung von offenen Nennungen
FuzzyWuzzy Markencodierung: Ein Tool zur Markencodierung mittels Fuzzy-String-Matching
Technologiestack
Frontend: Streamlit (Python-basiertes Web-Framework)
Backend: Python
Datenbank: Supabase (PostgreSQL)
Authentifizierung: Supabase Auth
KI-Integration: OpenAI API
Weitere Bibliotheken: Pandas, FuzzyWuzzy, XlsxWriter, etc.
Hauptkomponenten
1. Authentifizierung und Benutzerverwaltung
Benutzerregistrierung und -anmeldung
Profilmanagement
Sitzungsverwaltung
2. BonsAI Codierungstool
KI-gestützte Codierung von offenen Nennungen
Unterstützung für Single- und Multi-Label-Codierung
Codeplan-Management
Beispiel- und Kontextmanagement
Excel-Import/Export
3. FuzzyWuzzy Markencodierung
Ähnlichkeitsbasierte Zuordnung von Marken
Automatische Markenerkennung
Batch-Verarbeitung
Exportfunktion
Verzeichnisstruktur
components/: UI-Komponenten für die verschiedenen Teile der Anwendung
codeplan.py: Verwaltung von Codeplänen
codierung_method.py: Auswahl der Codierungsmethode
examples.py: Beispielverwaltung
manual_input.py: Manuelle Eingabe von Daten
processing.py: Verarbeitung der Daten
settings.py: Einstellungen der Anwendung
sidebar.py: Seitenleiste der Anwendung
start_button.py: Start-Button für die Verarbeitung
study_context.py: Verwaltung des Studienkontexts
config/: Konfigurationsdateien
database_schema.sql: SQL-Schema für die Datenbank
initSupabase.py: Initialisierung der Supabase-Verbindung
settings.py: Allgemeine Einstellungen der Anwendung
services/: Geschäftslogik
ai_service.py: Integration mit OpenAI API
auth_service.py: Authentifizierungsdienste
db_service.py: Datenbankdienste
state_manager.py: Verwaltung des Anwendungszustands
styles/: CSS-Stile für die Anwendung
utils/: Hilfsfunktionen
Hauptdateien:
main.py: Haupteinstiegspunkt der Anwendung
bonsai_app.py: BonsAI Codierungstool
fuzzy_app.py: FuzzyWuzzy Markencodierung
requirements.txt: Abhängigkeiten der Anwendung
Datenmodell
Die Anwendung verwendet eine Supabase-Datenbank mit folgenden Haupttabellen:
user_profiles: Benutzerprofile
session_states: Sitzungszustände
saved_codeplans: Gespeicherte Codepläne
study_contexts: Studienkontexte
example_sets: Beispielsets
system_prompts: Systemprompts
coding_history: Codierungshistorie
ai_interactions: KI-Interaktionen
Funktionsweise
Benutzerauthentifizierung:
Benutzer registrieren sich oder melden sich an
Benutzerprofile werden in der Datenbank gespeichert
Anwendungsauswahl:
Nach der Anmeldung wählt der Benutzer zwischen BonsAI Codierungstool und FuzzyWuzzy Markencodierung
BonsAI Codierungstool:
Benutzer erstellt oder lädt einen Codeplan
Benutzer gibt Studienkontexte und Beispiele ein
Benutzer wählt die Codierungsmethode (Single- oder Multi-Label)
Benutzer startet die Verarbeitung
KI codiert die Eingaben basierend auf dem Codeplan
Ergebnisse werden angezeigt und können exportiert werden
FuzzyWuzzy Markencodierung:
Benutzer lädt Daten hoch
Benutzer konfiguriert die Ähnlichkeitseinstellungen
Anwendung führt Fuzzy-Matching durch
Ergebnisse werden angezeigt und können exportiert werden
Datenspeicherung:
Sitzungszustände werden gespeichert
Codierungshistorie wird protokolliert
KI-Interaktionen werden aufgezeichnet
Zusammenfassung
Die Codierungsapp 3.0 ist eine umfassende Webanwendung zur KI-gestützten Codierung von offenen Nennungen und Marken. Sie bietet eine benutzerfreundliche Oberfläche, Authentifizierung, Datenspeicherung und verschiedene Codierungsmethoden. Die Anwendung ist modular aufgebaut und verwendet moderne Technologien wie Streamlit, Supabase und OpenAI