import streamlit as st
import pandas as pd

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Gestore Hotel Evento Novembre", layout="wide")

# --- DATABASE HOTEL (Dati forniti da te) ---
HOTELS_DATA = {
    "3 stelle_Centro": [
        {"nome": "Hotel De Prati", "singole": 3, "doppie": 4, "triple": 0},
        {"nome": "Locanda Borgonuovo", "singole": 2, "doppie": 2, "triple": 0},
        {"nome": "Hotel Nazionale", "singole": 5, "doppie": 3, "triple": 0},
        {"nome": "Hotel The Dome", "singole": 5, "doppie": 4, "triple": 0},
        {"nome": "Egò Residence", "singole": 10, "doppie": 8, "triple": 7},
    ],
    "3 stelle superior_Centro": [
        {"nome": "Hotel Touring", "singole": 14, "doppie": 24, "triple": 5},
        {"nome": "Hotel Carlton", "singole": 19, "doppie": 10, "triple": 5},
        {"nome": "Hotel Europa", "singole": 11, "doppie": 13, "triple": 0},
    ],
    "4 stelle_Centro": [
        {"nome": "Hotel Astra", "singole": 36, "doppie": 12, "triple": 10},
        {"nome": "Hotel Duchessa Isabella", "singole": 5, "doppie": 13, "triple": 3},
        {"nome": "Hotel Maxxim", "singole": 7, "doppie": 12, "triple": 0},
        {"nome": "Hotel Princess Art", "singole": 5, "doppie": 4, "triple": 0},
        {"nome": "Hotel Ferrara", "singole": 28, "doppie": 10, "triple": 0},
        {"nome": "Depandance Annunziata", "singole": 3, "doppie": 2, "triple": 0},
    ],
    "3 stelle_Fuori": [
        {"nome": "Hotel Lucrezia Borgia", "singole": 11, "doppie": 11, "triple": 10},
        {"nome": "Hotel B&B", "singole": 8, "doppie": 8, "triple": 0},
        {"nome": "Hotel Palace INN", "singole": 38, "doppie": 15, "triple": 0},
        {"nome": "Hotel Principessa Pio", "singole": 2, "doppie": 2, "triple": 2},
        {"nome": "Hotel Boutique", "singole": 5, "doppie": 6, "triple": 0},
    ],
    "4 stelle_Fuori": [
        {"nome": "Hotel Radisson", "singole": 31, "doppie": 22, "triple": 0},
        {"nome": "Hotel Duca D'Este", "singole": 7, "doppie": 10, "triple": 0},
        {"nome": "Hotel Orologio", "singole": 8, "doppie": 4, "triple": 12},
    ],
    "Ostello_Fuori": [
        {"nome": "Ostello Comune", "doppie": 2, "triple": 1, "quadruple": 2, "sestuple": 2}
    ]
}

# --- INIZIALIZZAZIONE SESSIONE ---
if 'ospiti' not in st.session_state:
    st.session_state.ospiti = pd.DataFrame(columns=[
        "Codice Scuola", "Nome", "Cognome", "Genere", "Ruolo", "Pacchetto", "Tipo Camera", "VIP", "Hotel Assegnato"
    ])

st.title("🏨 Ottimizzatore Rooming List")

# --- SEZIONE 1: INSERIMENTO E MODIFICA ---
st.header("1. Gestione Ospiti")
col_form, col_stats = st.columns([1, 2])

with col_form:
    with st.expander("➕ Aggiungi Nuovo Ospite"):
        with st.form("nuovo_ospite"):
            scuola = st.text_input("Codice Scuola")
            nome = st.text_input("Nome")
            cognome = st.text_input("Cognome")
            genere = st.selectbox("Genere", ["M", "F"])
            ruolo = st.selectbox("Ruolo", ["Studente", "Docente"])
            pacchetto = st.selectbox("Categoria Hotel", list(HOTELS_DATA.keys()))
            camera = st.selectbox("Tipo Camera", ["singole", "doppie", "triple"])
            vip = st.checkbox("VIP (Blocca in un hotel)")
            hotel_pref = st.selectbox("Hotel (solo se VIP)", ["Nessuno"] + [h['nome'] for cat in HOTELS_DATA.values() for h in cat])
            
            if st.form_submit_button("Salva"):
                nuovo = pd.DataFrame([[scuola, nome, cognome, genere, ruolo, pacchetto, camera, vip, hotel_pref if vip else ""]], 
                                     columns=st.session_state.ospiti.columns)
                st.session_state.ospiti = pd.concat([st.session_state.ospiti, nuovo], ignore_index=True)
                st.rerun()

# Tabella interattiva per modifiche rapide
st.subheader("Modifica Dati")
edited_df = st.data_editor(st.session_state.ospiti, num_rows="dynamic", use_container_width=True)
if st.button("Aggiorna Database"):
    st.session_state.ospiti = edited_df
    st.success("Dati salvati!")

# --- SEZIONE 2: ALGORITMO DI ALLOCAZIONE ---
st.header("2. Algoritmo di Allocazione")

if st.button("🚀 Esegui Ottimizzazione"):
    df = st.session_state.ospiti.copy()
    
    # 1. Reset assegnazioni non-VIP
    df.loc[df['VIP'] == False, 'Hotel Assegnato'] = ""
    
    # 2. Creiamo inventario temporaneo basato sui VIP
    inventario_temp = {cat: [h.copy() for h in lista] for cat, lista in HOTELS_DATA.items()}
    
    # Sottraiamo i VIP dall'inventario
    for idx, vip in df[df['VIP'] == True].iterrows():
        for cat in inventario_temp.values():
            for h in cat:
                if h['nome'] == vip['Hotel Assegnato']:
                    h[vip['Tipo Camera']] -= 1

    # 3. Allocazione Scuole (Priorità dimensione scuola)
    scuole = df[df['VIP'] == False].groupby(['Codice Scuola', 'Pacchetto', 'Genere', 'Ruolo', 'Tipo Camera'])
    
    for (cod_scuola, pacchetto, genere, ruolo, tipo_cam), gruppo in scuole:
        numero_persone = len(gruppo)
        # Cerchiamo hotel con posti
        assegnato = False
        for hotel in inventario_temp.get(pacchetto, []):
            posti_disponibili = hotel[tipo_cam]
            # Nota: qui semplifichiamo 1 camera = 1 unità di tipo scelto
            # In un secondo step affineremo il riempimento dei singoli letti
            if posti_disponibili >= numero_persone:
                df.loc[gruppo.index, 'Hotel Assegnato'] = hotel['nome']
                hotel[tipo_cam] -= numero_persone
                assegnato = True
                break
        
        if not assegnato:
            st.error(f"Impossibile trovare posto unito per {cod_scuola} ({pacchetto})")

    st.session_state.ospiti = df
    st.success("Ottimizzazione Completata!")

# --- SEZIONE 3: RISULTATI ---
st.header("3. Risultati e Saturazione")
if not st.session_state.ospiti.empty:
    st.dataframe(st.session_state.ospiti.sort_values(by="Hotel Assegnato"))