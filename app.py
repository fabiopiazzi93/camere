import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hotel Manager Pro", layout="wide")

# --- DATABASE HOTEL AGGIORNATO ---
HOTELS_DATA = {
    "3 stelle_Centro": ["Hotel De Prati", "Locanda Borgonuovo", "Hotel Nazionale", "Hotel The Dome", "Egò Residence"],
    "3 stelle superior_Centro": ["Hotel Touring", "Hotel Carlton", "Hotel Europa"],
    "4 stelle_Centro": ["Hotel Astra", "Hotel Duchessa Isabella", "Hotel Maxxim", "Hotel Princess Art", "Hotel Ferrara", "Depandance Annunziata"],
    "3 stelle_Fuori": ["Hotel Lucrezia Borgia", "Hotel B&B", "Hotel Palace INN", "Hotel Principessa Pio", "Hotel Boutique"],
    "4 stelle_Fuori": ["Hotel Radisson", "Hotel Duca D'Este", "Hotel Orologio"],
    "Ostello": ["Ostello Comune"]
}

# Inizializzazione database ospiti
if 'ospiti' not in st.session_state:
    st.session_state.ospiti = pd.DataFrame(columns=[
        "Codice Scuola", "Nome", "Cognome", "Genere", "Ruolo", "Pacchetto", "Tipo Camera", "VIP", "Hotel Assegnato"
    ])

# --- SIDEBAR ---
st.sidebar.title("Navigazione")
page = st.sidebar.radio("Vai a:", ["➕ Inserimento", "🗂️ Gestione Database", "⚙️ Elaborazione"])

# --- PAGINA 1: INSERIMENTO ---
if page == "➕ Inserimento":
    st.header("Nuovo Ospite")
    
    with st.form("form_nuovo"):
        c1, c2 = st.columns(2)
        with c1:
            scuola = st.text_input("Codice Scuola")
            nome = st.text_input("Nome")
            cognome = st.text_input("Cognome")
            genere = st.selectbox("Genere", ["M", "F"])
        with c2:
            ruolo = st.selectbox("Ruolo", ["Studente", "Docente"])
            # Menu Pacchetto
            pacchetto = st.selectbox("Categoria Hotel", list(HOTELS_DATA.keys()))
            
            # LOGICA DINAMICA CAMERE
            if pacchetto == "Ostello":
                opzioni_camera = ["doppie", "triple", "quadruple", "sestuple"]
            else:
                opzioni_camera = ["singole", "doppie", "triple"]
                
            camera = st.selectbox("Tipo Camera", opzioni_camera)
            vip = st.checkbox("VIP (Blocca posizione)")
            
            # Lista hotel filtrata per pacchetto scelto per selezione VIP
            hotel_per_vip = HOTELS_DATA[pacchetto]
            hotel_pref = st.selectbox("Assegna a Hotel (Solo se VIP)", ["-"] + hotel_per_vip)

        if st.form_submit_button("Aggiungi"):
            nuovo = pd.DataFrame([[scuola, nome, cognome, genere, ruolo, pacchetto, camera, vip, hotel_pref if vip else "NON ASSEGNATO"]], 
                                 columns=st.session_state.ospiti.columns)
            st.session_state.ospiti = pd.concat([st.session_state.ospiti, nuovo], ignore_index=True)
            st.success(f"Aggiunto {nome} {cognome}")