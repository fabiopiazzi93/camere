import streamlit as st
import pandas as pd

# Configurazione Pagina
st.set_page_config(page_title="Hotel Manager 850", layout="wide")

st.title("🏨 Gestore Allocazione Ospiti")

# --- DATABASE SIMULATO (In un'app reale useremo st.session_state o un file) ---
if 'ospiti' not in st.session_state:
    st.session_state.ospiti = pd.DataFrame(columns=[
        "Scuola", "Nome", "Cognome", "Genere", "Ruolo", "Pacchetto"
    ])

# --- SIDEBAR: INSERIMENTO DATI ---
with st.sidebar:
    st.header("➕ Nuovo Ospite")
    with st.form("form_inserimento"):
        scuola = st.text_input("Codice Scuola")
        nome = st.text_input("Nome")
        cognome = st.text_input("Cognome")
        genere = st.selectbox("Genere", ["M", "F"])
        ruolo = st.selectbox("Ruolo", ["Studente", "Docente"])
        pacchetto = st.selectbox("Pacchetto", [
            "4* Centro - Singola", 
            "3* Centro - Doppia", 
            "3* Sup Fuori - Tripla",
            "Ostello - Comune"
        ])
        
        if st.form_submit_button("Salva Ospite"):
            nuovo_ospite = pd.DataFrame([[scuola, nome, cognome, genere, ruolo, pacchetto]], 
                                        columns=st.session_state.ospiti.columns)
            st.session_state.ospiti = pd.concat([st.session_state.ospiti, nuovo_ospite], ignore_index=True)
            st.success("Ospite aggiunto!")

# --- MAIN: VISUALIZZAZIONE E LOGICA ---
tab1, tab2, tab3 = st.tabs(["📋 Elenco Ospiti", "⚙️ Logica Allocazione", "📊 Rooming List Finali"])

with tab1:
    st.subheader("Ospiti Inseriti")
    st.dataframe(st.session_state.ospiti, use_container_width=True)
    st.write(f"Totale iscritti: {len(st.session_state.ospiti)} / 850")

with tab2:
    st.subheader("Parametri Algoritmo")
    st.info("L'algoritmo raggrupperà per Genere e Pacchetto, mantenendo le scuole unite ove possibile.")
    # Qui inseriremo la funzione di "incastro" (Tetris) discussa prima

with tab3:
    st.subheader("Download Report per Hotel")
    st.button("Genera Rooming List Ottimizzata")
    # Qui l'app genererà i file Excel scaricabili