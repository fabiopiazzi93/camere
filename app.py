import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hotel Manager Pro", layout="wide")

# --- DATABASE HOTEL AGGIORNATO CON OSTELLO ---
HOTELS_DATA = {
    "3 stelle_Centro": [{"nome": n, "singole": s, "doppie": d, "triple": 0} for n, s, d in [
        ("Hotel De Prati", 3, 4), ("Locanda Borgonuovo", 2, 2), ("Hotel Nazionale", 5, 3), 
        ("Hotel The Dome", 5, 4), ("Egò Residence", 10, 8)]], # Egò ha anche triple, aggiungile se serve
    "4 stelle_Centro": [{"nome": "Hotel Astra", "singole": 36, "doppie": 12, "triple": 10}, 
                        {"nome": "Hotel Ferrara", "singole": 28, "doppie": 10, "triple": 0}],
    "Ostello_Fuori": [{"nome": "Ostello Comune", "doppie": 2, "triple": 1, "quadruple": 2, "sestuple": 2}]
}

# Inizializzazione database ospiti
if 'ospiti' not in st.session_state:
    st.session_state.ospiti = pd.DataFrame(columns=[
        "Codice Scuola", "Nome", "Cognome", "Genere", "Ruolo", "Pacchetto", "Tipo Camera", "VIP", "Hotel Assegnato"
    ])

# --- SIDEBAR DI NAVIGAZIONE ---
st.sidebar.title("Navegazione")
page = st.sidebar.radio("Vai a:", ["➕ Inserimento", "🗂️ Gestione Database", "⚙️ Elaborazione e Risultati"])

# --- PAGINA 1: INSERIMENTO ---
if page == "➕ Inserimento":
    st.header("Inserimento Nuovo Ospite")
    
    with st.form("form_nuovo"):
        col1, col2 = st.columns(2)
        with col1:
            scuola = st.text_input("Codice Scuola")
            nome = st.text_input("Nome")
            cognome = st.text_input("Cognome")
            genere = st.selectbox("Genere", ["M", "F"])
        with col2:
            ruolo = st.selectbox("Ruolo", ["Studente", "Docente"])
            pacchetto = st.selectbox("Categoria Hotel", list(HOTELS_DATA.keys()))
            
            # Logica Dinamica Camere
            opzioni_camera = ["singole", "doppie", "triple"]
            if "Ostello" in pacchetto:
                opzioni_camera = ["doppie", "triple", "quadruple", "sestuple"]
            
            camera = st.selectbox("Tipo Camera", opzioni_camera)
            vip = st.checkbox("Segna come VIP")
            hotel_pref = st.selectbox("Assegna a Hotel (Solo VIP)", ["-"] + [h['nome'] for cat in HOTELS_DATA.values() for h in cat])

        if st.form_submit_button("Aggiungi all'elenco"):
            nuovo = pd.DataFrame([[scuola, nome, cognome, genere, ruolo, pacchetto, camera, vip, hotel_pref if vip else ""]], 
                                 columns=st.session_state.ospiti.columns)
            st.session_state.ospiti = pd.concat([st.session_state.ospiti, nuovo], ignore_index=True)
            st.success(f"{nome} {cognome} aggiunto!")

# --- PAGINA 2: GESTIONE DATABASE ---
elif page == "🗂️ Gestione Database":
    st.header("Database Ospiti")
    st.write(f"Totale registrati: **{len(st.session_state.ospiti)}** / 850")
    
    # Filtro rapido per scuola
    search = st.text_input("Cerca per Scuola o Cognome")
    df_display = st.session_state.ospiti
    if search:
        df_display = df_display[df_display.apply(lambda row: search.lower() in str(row).lower(), axis=1)]

    edited_df = st.data_editor(df_display, num_rows="dynamic", use_container_width=True)
    
    if st.button("Salva Modifiche"):
        st.session_state.ospiti = edited_df
        st.rerun()

# --- PAGINA 3: ELABORAZIONE ---
elif page == "⚙️ Elaborazione e Risultati":
    st.header("Ottimizzazione Rooming List")
    
    if st.button("Far girare l'Algoritmo"):
        df = st.session_state.ospiti.copy()
        # Reset assegnazioni non bloccate
        df.loc[df['VIP'] == False, 'Hotel Assegnato'] = "NON ASSEGNATO"
        
        # --- LOGICA DI ASSEGNAZIONE (Aggiornata per Scuole) ---
        # Ordiniamo per scuola per tenerle unite
        scuole_unite = df[df['VIP'] == False].groupby(['Codice Scuola', 'Pacchetto', 'Genere', 'Tipo Camera'])
        
        for (scuola_id, pacchetto, gen, cam), gruppo in scuole_unite:
            # Qui l'algoritmo cerca l'hotel nel pacchetto scelto con abbastanza posti per il tipo cam
            for hotel in HOTELS_DATA.get(pacchetto, []):
                # Semplificazione: controllo posti liberi (qui andrebbe il conteggio reale)
                df.loc[gruppo.index, 'Hotel Assegnato'] = hotel['nome']
                break
        
        st.session_state.ospiti = df
        st.success("Allocazione completata!")

    # Visualizzazione Risultati per Hotel
    st.subheader("Risultati per Struttura")
    hotel_scelto = st.selectbox("Seleziona Hotel per vedere la lista:", ["Tutti"] + [h['nome'] for cat in HOTELS_DATA.values() for h in cat])
    
    res_df = st.session_state.ospiti
    if hotel_scelto != "Tutti":
        res_df = res_df[res_df['Hotel Assegnato'] == hotel_scelto]
    
    st.dataframe(res_df, use_container_width=True)