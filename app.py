import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Hotel Manager Pro", layout="wide")

# --- 1. DATABASE COMPLETO ---
HOTELS_DB = [
    {"nome": "Hotel De Prati", "cat": "3 stelle_Centro", "singole": 3, "doppie": 4, "triple": 0, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Touring", "cat": "3 stelle superior_Centro", "singole": 14, "doppie": 24, "triple": 5, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Carlton", "cat": "3 stelle superior_Centro", "singole": 19, "doppie": 10, "triple": 5, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Astra", "cat": "4 stelle_Centro", "singole": 36, "doppie": 12, "triple": 10, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Europa", "cat": "3 stelle superior_Centro", "singole": 11, "doppie": 13, "triple": 0, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Duchessa Isabella", "cat": "4 stelle_Centro", "singole": 5, "doppie": 13, "triple": 3, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Maxxim", "cat": "4 stelle_Centro", "singole": 7, "doppie": 12, "triple": 0, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Princess Art", "cat": "4 stelle_Centro", "singole": 5, "doppie": 4, "triple": 0, "quadruple": 0, "sestuple": 0},
    {"nome": "Locanda Borgonuovo", "cat": "3 stelle_Centro", "singole": 2, "doppie": 2, "triple": 0, "quadruple": 0, "sestuple": 0},
    {"nome": "Egò Residence", "cat": "3 stelle_Centro", "singole": 10, "doppie": 8, "triple": 7, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Nazionale", "cat": "3 stelle_Centro", "singole": 5, "doppie": 3, "triple": 0, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Ferrara", "cat": "4 stelle_Centro", "singole": 28, "doppie": 10, "triple": 0, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel The Dome", "cat": "3 stelle_Centro", "singole": 5, "doppie": 4, "triple": 0, "quadruple": 0, "sestuple": 0},
    {"nome": "Depandance Annunziata", "cat": "4 stelle_Centro", "singole": 3, "doppie": 2, "triple": 0, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Lucrezia Borgia", "cat": "3 stelle_Fuori", "singole": 11, "doppie": 11, "triple": 10, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Radisson", "cat": "4 stelle_Fuori", "singole": 31, "doppie": 22, "triple": 0, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel B&B", "cat": "3 stelle_Fuori", "singole": 8, "doppie": 8, "triple": 0, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Palace INN", "cat": "3 stelle_Fuori", "singole": 38, "doppie": 15, "triple": 0, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Duca D'Este", "cat": "4 stelle_Fuori", "singole": 7, "doppie": 10, "triple": 0, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Orologio", "cat": "4 stelle_Fuori", "singole": 8, "doppie": 4, "triple": 12, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Principessa Pio", "cat": "3 stelle_Fuori", "singole": 2, "doppie": 2, "triple": 2, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Boutique", "cat": "3 stelle_Fuori", "singole": 5, "doppie": 6, "triple": 0, "quadruple": 0, "sestuple": 0},
    {"nome": "Ostello Comune", "cat": "Ostello", "singole": 0, "doppie": 2, "triple": 1, "quadruple": 2, "sestuple": 2},
]

CATEGORIE = sorted(list(set([h['cat'] for h in HOTELS_DB])))

if 'ospiti' not in st.session_state:
    st.session_state.ospiti = pd.DataFrame(columns=[
        "Codice Scuola", "Nome", "Cognome", "Genere", "Ruolo", "Pacchetto", "Tipo Camera", "VIP", "Hotel Assegnato"
    ])

# --- SIDEBAR ---
page = st.sidebar.radio("Navigazione:", ["➕ Inserimento", "🗂️ Database", "🚀 Ottimizzazione"])

# --- PAGINA INSERIMENTO (CORRETTA) ---
if page == "➕ Inserimento":
    st.header("Registrazione Nuovo Ospite")
    
    # Usiamo colonne per il form
    c1, c2 = st.columns(2)
    
    with c1:
        scuola = st.text_input("Codice Scuola")
        nome = st.text_input("Nome")
        cognome = st.text_input("Cognome")
        genere = st.selectbox("Genere", ["M", "F"])
        
    with c2:
        ruolo = st.selectbox("Ruolo", ["Studente", "Docente"])
        # Pacchetto selezionato
        pacc_scelto = st.selectbox("Pacchetto (Categoria)", CATEGORIE, key="pacc_selector")
        
        # LOGICA CAMERE - CAMBIA ISTANTANEAMENTE
        if pacc_scelto == "Ostello":
            lista_camere = ["doppie", "triple", "quadruple", "sestuple"]
        else:
            lista_camere = ["singole", "doppie", "triple"]
            
        tipo_cam = st.selectbox("Tipo Camera", lista_camere, key="cam_selector")
        vip = st.checkbox("Segna come VIP")
        
        hotel_disp = [h['nome'] for h in HOTELS_DB if h['cat'] == pacc_scelto]
        hotel_fisso = st.selectbox("Hotel per VIP (opzionale)", ["-"] + hotel_disp)

    if st.button("➕ Salva in Database"):
        nuovo = pd.DataFrame([[scuola, nome, cognome, genere, ruolo, pacc_scelto, tipo_cam, vip, hotel_fisso if vip else "NON ASSEGNATO"]], 
                             columns=st.session_state.ospiti.columns)
        st.session_state.ospiti = pd.concat([st.session_state.ospiti, nuovo], ignore_index=True)
        st.success(f"Ospite {cognome} aggiunto!")
        st.rerun() # Forza l'aggiornamento per pulire i campi

# --- PAGINA DATABASE ---
elif page == "🗂️ Database":
    st.header("Gestione Dati")
    df_modificabile = st.data_editor(st.session_state.ospiti, num_rows="dynamic", use_container_width=True)
    if st.button("Salva modifiche"):
        st.session_state.ospiti = df_modificabile
        st.success("Dati aggiornati!")

# --- PAGINA OTTIMIZZAZIONE ---
elif page == "🚀 Ottimizzazione":
    st.header("Esegui Allocazione")
    if st.button("Avvia Algoritmo"):
        # (Qui inseriremo la logica dei posti letto che abbiamo discusso)
        st.info("Algoritmo in esecuzione... (sviluppo logica posti letto)")
    st.dataframe(st.session_state.ospiti)